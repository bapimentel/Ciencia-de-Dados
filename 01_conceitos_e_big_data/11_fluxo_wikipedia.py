# Velocidade de verdade: o fluxo continuo de edicoes da Wikipedia, processado com Spark Structured Streaming.
# requer: pyspark
# Fonte: Wikimedia EventStreams (https://stream.wikimedia.org/v2/stream/recentchange), um fluxo publico,
# ao vivo, com todas as alteracoes em todos os projetos da Wikimedia: dezenas de eventos por segundo,
# alguns milhoes por dia, sem fim. Sem internet (ou com --simulado), usamos um fluxo simulado no mesmo formato.
#
# Arquitetura de um sistema real, em miniatura:
#   produtor (uma thread) -> pasta de entrada (o papel do Kafka) -> Spark Structured Streaming -> resultados
# O produtor le o fluxo e grava, a cada 2 s, um arquivo JSON com os eventos que chegaram.
# O Spark trata a pasta como uma tabela sem fim: a cada 5 s processa SO os arquivos novos (um micro-lote)
# e atualiza os resumos guardados no "estado", sem reler o que ja processou.
# Guardamos so campos tecnicos: nada de nomes de usuarios, titulos de paginas ou comentarios.
#
# Uso: python 11_fluxo_wikipedia.py [--segundos 90] [--simulado]

import os
import json
import time
import random
import shutil
import argparse
import threading
import urllib.request
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import functions as F
from spark_ambiente import iniciar_spark, pasta_dados, coletar, ESTILO, PASTA_FIGURAS

URL = 'https://stream.wikimedia.org/v2/stream/recentchange'
argumentos = argparse.ArgumentParser()
argumentos.add_argument('--segundos', type=int, default=90, help='por quanto tempo ouvir o fluxo')
argumentos.add_argument('--simulado', action='store_true', help='usar o fluxo simulado mesmo com internet')
opcoes = argumentos.parse_args()
plt.style.use(ESTILO)

base = pasta_dados('wikipedia')
entrada = os.path.join(base, 'entrada')
shutil.rmtree(base, ignore_errors=True)            # cada execucao comeca de um fluxo vazio
os.makedirs(entrada)


def resumir(evento):
    tamanho = evento.get('length') or {}
    novo, antigo = tamanho.get('new'), tamanho.get('old')
    return {'momento': datetime.fromisoformat(evento['meta']['dt'].replace('Z', '+00:00')).timestamp(),
            'wiki': evento.get('wiki'), 'tipo': evento.get('type'), 'robo': bool(evento.get('bot')),
            'bytes': (novo or 0) - (antigo or 0) if novo is not None else None}


def gravar(lote, numero):
    # Grava com nome temporario (comecando com '.', que o Spark ignora) e so depois renomeia:
    # assim o Spark nunca le um arquivo pela metade.
    temporario = os.path.join(entrada, f'.lote_{numero:05d}.tmp')
    with open(temporario, 'w', encoding='utf-8') as arquivo:
        arquivo.writelines(json.dumps(e) + '\n' for e in lote)
    os.replace(temporario, os.path.join(entrada, f'lote_{numero:05d}.json'))


def eventos_reais():
    pedido = urllib.request.Request(URL, headers={'User-Agent': 'exemplo-didatico-ciencia-de-dados/1.0',
                                                  'Accept': 'text/event-stream'})
    with urllib.request.urlopen(pedido, timeout=30) as resposta:
        for linha in resposta:
            if linha.startswith(b'data:'):
                try:
                    yield resumir(json.loads(linha[5:]))
                except (ValueError, KeyError):
                    continue                                    # veracidade: linha malformada e descartada


def eventos_simulados():
    gerador = random.Random(11)
    wikis = ['commonswiki', 'wikidatawiki', 'enwiki', 'frwiki', 'dewiki', 'eswiki', 'ptwiki', 'jawiki', 'ruwiki']
    pesos = [30, 28, 14, 5, 5, 4, 3, 3, 3]
    while True:
        time.sleep(gerador.expovariate(40))                     # cerca de 40 eventos por segundo
        robo = gerador.random() < 0.45
        yield {'momento': time.time() - gerador.expovariate(1), 'wiki': gerador.choices(wikis, pesos)[0],
               'tipo': gerador.choices(['edit', 'categorize', 'log', 'new'], [45, 40, 10, 5])[0], 'robo': robo,
               'bytes': int(gerador.gauss(30 if robo else 150, 400))}


estatisticas = {'recebidos': 0, 'fonte': 'simulado' if opcoes.simulado else 'real'}
parar = threading.Event()


def produtor():
    fonte = eventos_simulados() if opcoes.simulado else eventos_reais()
    lote, numero, ultimo = [], 0, time.time()
    try:
        for evento in fonte:
            lote.append(evento)
            estatisticas['recebidos'] += 1
            if time.time() - ultimo >= 2:
                gravar(lote, numero)
                lote, numero, ultimo = [], numero + 1, time.time()
            if parar.is_set():
                break
    except OSError as erro:                                     # sem internet: troca para o simulado
        print(f'Fluxo real indisponivel ({erro}); usando o simulado.')
        opcoes.simulado, estatisticas['fonte'] = True, 'simulado'
        produtor()
        return
    if lote:
        gravar(lote, numero)


spark = iniciar_spark('fluxo_wikipedia', config={'spark.sql.shuffle.partitions': '4'})
esquema = 'momento DOUBLE, wiki STRING, tipo STRING, robo BOOLEAN, bytes LONG'
# readStream em vez de read: a mesma tabela, mas que nunca termina. Num sistema real, a unica linha que
# muda e esta: spark.readStream.format('kafka').option('subscribe', 'wikipedia')...
fluxo = (spark.readStream.schema(esquema).json(entrada)
         .withColumn('momento', F.timestamp_seconds('momento')))

# Consulta 1: edicoes por janela de 10 s (pelo horario do EVENTO), separando pessoas e robos.
# A marca d'agua (watermark) de 30 s diz ao Spark: "depois de 30 s, a janela esta fechada; pode esquecer".
por_janela = (fluxo.withWatermark('momento', '30 seconds')
              .groupBy(F.window('momento', '10 seconds'), 'robo')
              .agg(F.count('*').alias('eventos'), F.sum(F.abs('bytes')).alias('bytes')))
janelas = {}


def guardar_janelas(lote, numero_lote):
    # A cada micro-lote, o Spark entrega so as janelas que mudaram (modo update)
    for linha in lote.collect():
        janelas[(linha['window']['start'], linha['robo'])] = (linha['eventos'], linha['bytes'])


consulta_janelas = (por_janela.writeStream.outputMode('update').foreachBatch(guardar_janelas)
                    .option('checkpointLocation', os.path.join(base, 'checkpoints', 'janelas'))
                    .trigger(processingTime='5 seconds').start())
# Consulta 2: total acumulado por wiki desde o inicio (estado sem watermark: uma linha por wiki)
consulta_wikis = (fluxo.groupBy('wiki').count().writeStream.outputMode('complete').format('memory')
                  .queryName('por_wiki').option('checkpointLocation', os.path.join(base, 'checkpoints', 'wikis'))
                  .trigger(processingTime='5 seconds').start())

threading.Thread(target=produtor, daemon=True).start()
print(f'Ouvindo o fluxo {estatisticas["fonte"]} por {opcoes.segundos} s...')
for segundo in range(opcoes.segundos):
    time.sleep(1)
    if (segundo + 1) % 15 == 0:
        print(f'  {segundo + 1:>3} s: {estatisticas["recebidos"]:,} eventos recebidos, '
              f'{len(os.listdir(entrada))} arquivos na entrada')
parar.set()
time.sleep(2.5)
consulta_janelas.processAllAvailable()
consulta_wikis.processAllAvailable()


def progresso(p):
    return p if isinstance(p, dict) else json.loads(p.json)


progressos = [progresso(p) for p in consulta_janelas.recentProgress if progresso(p)['numInputRows'] > 0]
mais_editadas = coletar(spark.sql('SELECT wiki, count FROM por_wiki ORDER BY count DESC LIMIT 8'))
consulta_janelas.stop()
consulta_wikis.stop()
spark.stop()

total = sum(p['numInputRows'] for p in progressos)
duracoes = [p['durationMs']['triggerExecution'] for p in progressos]
estado = [p['stateOperators'][0]['numRowsTotal'] for p in progressos]
print(f'\nFonte: fluxo {estatisticas["fonte"]}. {total:,} eventos processados em {len(progressos)} micro-lotes '
      f'({total / opcoes.segundos:.0f} por segundo, cerca de {total / opcoes.segundos * 86400 / 1e6:.1f} milhoes por dia).')
demais = duracoes[1:]
print(f'O primeiro micro-lote, que ainda aquece o Java, levou {duracoes[0] / 1000:.2f} s. Os outros levaram em media '
      f'{sum(demais) / len(demais) / 1000:.2f} s (no maximo {max(demais) / 1000:.2f} s), menos que os 5 s entre lotes: '
      'o processamento acompanha o fluxo.')
print(f'Estado da consulta por janela: no maximo {max(estado)} linhas, mesmo com {total:,} eventos recebidos.')
print('\nWikis com mais eventos desde o inicio:')
print(mais_editadas.to_string(index=False))

serie = pd.DataFrame([(inicio, robo, ev) for (inicio, robo), (ev, _) in janelas.items()],
                     columns=['inicio', 'robo', 'eventos']).pivot_table(index='inicio', columns='robo', values='eventos').sort_index()
serie = serie.iloc[1:-1]                    # a primeira e a ultima janela estao incompletas
fracao_robos = serie.get(True, pd.Series(dtype=float)).sum() / serie.sum().sum()
print(f'Robos fizeram {100 * fracao_robos:.0f}% dos eventos nas janelas completas.')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12.5, 4.4))
relogio = (serie.index - serie.index[0]).total_seconds()
for robo, nome, cor, traco in [(False, 'pessoas', '#2F648F', '-'), (True, 'robôs', '#168A8A', '--')]:
    if robo in serie:
        esq.plot(relogio, serie[robo], color=cor, linestyle=traco)
        esq.text(relogio[-1] + 2, serie[robo].iloc[-1], nome, color=cor, va='center')
esq.set_ylim(0, serie.max().max() * 1.2)
esq.set_xlabel('Segundos desde o início da escuta')
esq.set_ylabel('Eventos por janela de 10 s')
esq.set_title(f'Fluxo {estatisticas["fonte"]} da Wikimedia: {total / opcoes.segundos:.0f} eventos por segundo')
acumulado = pd.Series([p['numInputRows'] for p in progressos]).cumsum()
lotes = range(1, len(progressos) + 1)
dir.plot(lotes, acumulado, color='#8794A3', marker='o', markersize=4)
dir.plot(lotes, estado, color='#2F648F', marker='D', markersize=4)
dir.text(len(progressos) + 0.3, acumulado.iloc[-1], 'eventos recebidos\n(acumulado)', color='#8794A3', va='center', fontsize=9)
dir.text(len(progressos) + 0.3, estado[-1], 'linhas no estado', color='#2F648F', va='center', fontsize=9)
dir.set_yscale('log')
dir.set_xlim(0.5, len(progressos) + 4)
dir.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
dir.set_xlabel('Micro-lote (a cada 5 s)')
dir.set_ylabel('Linhas (escala log)')
dir.set_title(f'O fluxo cresce; o estado fica em até {max(estado)} linhas')
plt.tight_layout()
plt.savefig(os.path.join(PASTA_FIGURAS, 'fluxo_wikipedia.png'))
plt.show()
shutil.rmtree(base, ignore_errors=True)
