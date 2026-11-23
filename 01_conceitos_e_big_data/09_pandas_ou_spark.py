# pandas ou Spark? Um experimento honesto com registros de navegacao (cliques) de uma loja on-line.
# requer: pyspark
# Pergunta de negocio: em que hora do dia cada categoria transforma mais visitas em compras?
# Os registros chegam como arquivos CSV, como os logs de um servidor: cada linha e um evento com
# momento, usuario, categoria, tipo (visualizacao, carrinho, compra) e preco.
# Dados sinteticos (semente fixa), com alguns padroes plantados de proposito; sao gerados pelo
# proprio Spark em ~/ciencia-de-dados-big-data/cliques e apagados no fim (use --manter-dados).
#
# A mesma conta, feita de tres jeitos, para 1, 4, 16 e 48 milhoes de linhas:
#   pandas inteiro  : le tudo para a memoria e agrupa (o jeito da unidade 03)
#   pandas em blocos: le um pedaco por vez e soma os resumos (o MapReduce do script 05, em um nucleo)
#   Spark           : le os arquivos em paralelo, com a memoria do Java limitada a 1 GB
# Cada medida roda em um processo separado, para que a memoria de uma nao contamine a outra.
#
# Uso: python 09_pandas_ou_spark.py [--tamanhos 1 4 16 48] [--manter-dados]

import os
import sys
import glob
import json
import time
import shutil
import argparse
import subprocess
from spark_ambiente import pasta_dados, memoria_pico_mb, memoria_total_mb, ESTILO, PASTA_FIGURAS

CATEGORIAS = ['eletronicos', 'moda', 'casa', 'beleza', 'esporte', 'livros',
              'brinquedos', 'mercado', 'pet', 'automotivo', 'jardim', 'games']
PRECO_BASE = [900, 120, 180, 60, 150, 45, 80, 35, 70, 200, 90, 250]
ESQUEMA = 'momento TIMESTAMP, usuario INT, categoria STRING, evento STRING, preco DOUBLE'
FORMATO_DATA = 'yyyy-MM-dd HH:mm:ss'


def pasta_tamanho(milhoes):
    return os.path.join(pasta_dados('cliques'), f'{milhoes}_milhoes')


def gerar_dados(spark, milhoes):
    """Grava milhoes x 1.000.000 eventos em arquivos CSV (pelo menos 8, de ate ~2 milhoes de linhas)."""
    from pyspark.sql import functions as F
    linhas = milhoes * 1_000_000
    arquivos = max(8, milhoes // 2)
    # Primeiro sorteamos todos os numeros aleatorios, cada um em sua coluna; so depois derivamos o resto.
    # (Cada F.rand tem seu proprio gerador: repetido dentro de um when, ele se dessincroniza.)
    sorteios = spark.range(linhas, numPartitions=arquivos).select(
        *[F.rand(semente).alias(f'u{semente}') for semente in range(10, 16)], F.randn(16).alias('z'),
        F.rand(17).alias('u17'))
    faixa = F.col('u10')
    hora = (F.when(faixa < 0.12, F.floor(F.col('u11') * 7))                 # madrugada: pouco trafego
             .when(faixa < 0.55, 7 + F.floor(F.col('u11') * 11))             # 7h-17h
             .otherwise(18 + F.floor(F.col('u11') * 6)))                     # 18h-23h: pico
    indice = (F.floor(F.col('u14') * len(CATEGORIAS)) + 1).cast('int')
    com_hora = sorteios.select('*', hora.cast('int').alias('hora'),
                               F.element_at(F.array(*[F.lit(c) for c in CATEGORIAS]), indice).alias('categoria'),
                               F.element_at(F.array(*[F.lit(p) for p in PRECO_BASE]), indice).alias('preco_base'))
    c, h = F.col('categoria'), F.col('hora')
    # Padroes plantados: cada categoria converte melhor em certos horarios
    p_compra = (F.lit(0.02)
                + F.when((c == 'mercado') & h.between(7, 10), 0.02).otherwise(0)
                + F.when((c == 'games') & (h >= 21), 0.025).otherwise(0)
                + F.when((c == 'eletronicos') & h.between(12, 13), 0.015).otherwise(0)
                + F.when((c == 'moda') & h.between(19, 22), 0.015).otherwise(0))
    evento = F.when(F.col('u15') < p_compra, 'compra').when(F.col('u15') < p_compra + 0.06, 'carrinho') \
        .otherwise('visualizacao')
    momento = F.timestamp_seconds(F.lit(1_772_323_200) + F.floor(F.col('u13') * 30) * 86400   # marco de 2026
                                  + h * 3600 + F.floor(F.col('u12') * 3600))
    tabela = com_hora.select(momento.alias('momento'), F.floor(F.col('u17') * 2_000_000).cast('int').alias('usuario'),
                             'categoria', evento.alias('evento'),
                             F.round(F.col('preco_base') * F.exp(F.col('z') * 0.5), 2).alias('preco'))
    tabela.write.mode('overwrite').option('header', True).option('timestampFormat', FORMATO_DATA) \
        .csv(pasta_tamanho(milhoes))


# ---------------------------------------------------------------- as tres formas de fazer a conta

def resumir_pandas(tabela):
    import pandas as pd
    tabela['hora'] = pd.to_datetime(tabela['momento'], format='%Y-%m-%d %H:%M:%S').dt.hour
    tabela['visualizacoes'] = tabela['evento'] == 'visualizacao'
    tabela['compras'] = tabela['evento'] == 'compra'
    tabela['receita'] = tabela['preco'].where(tabela['compras'], 0.0)
    return tabela.groupby(['categoria', 'hora'])[['visualizacoes', 'compras', 'receita']].sum()


def medir_pandas_inteiro(milhoes):
    import pandas as pd
    arquivos = sorted(glob.glob(os.path.join(pasta_tamanho(milhoes), '*.csv')))
    inicio = time.perf_counter()
    tabela = pd.concat([pd.read_csv(arquivo) for arquivo in arquivos], ignore_index=True)
    resumo = resumir_pandas(tabela)
    return time.perf_counter() - inicio, memoria_pico_mb(), resumo


def medir_pandas_blocos(milhoes):
    import pandas as pd
    arquivos = sorted(glob.glob(os.path.join(pasta_tamanho(milhoes), '*.csv')))
    inicio = time.perf_counter()
    parciais = [resumir_pandas(bloco) for arquivo in arquivos                       # MAP
                for bloco in pd.read_csv(arquivo, chunksize=1_000_000)]
    resumo = pd.concat(parciais).groupby(level=[0, 1]).sum()                        # REDUCE
    return time.perf_counter() - inicio, memoria_pico_mb(), resumo


def medir_spark(milhoes):
    from pyspark.sql import functions as F
    from spark_ambiente import iniciar_spark, memoria_jvm_pico_mb, coletar
    inicio_sessao = time.perf_counter()
    spark = iniciar_spark('pandas_ou_spark', memoria='1g')
    spark.range(1).collect()
    partida = time.perf_counter() - inicio_sessao
    inicio = time.perf_counter()
    eventos = spark.read.csv(pasta_tamanho(milhoes), header=True, schema=ESQUEMA, timestampFormat=FORMATO_DATA)
    e_compra = F.col('evento') == 'compra'
    resumo = coletar(eventos.groupBy('categoria', F.hour('momento').alias('hora')).agg(
        F.sum((F.col('evento') == 'visualizacao').cast('int')).alias('visualizacoes'),
        F.sum(e_compra.cast('int')).alias('compras'),
        F.sum(F.when(e_compra, F.col('preco')).otherwise(0.0)).alias('receita')))
    tempo = time.perf_counter() - inicio
    memoria = memoria_jvm_pico_mb(spark) + memoria_pico_mb()          # Java + Python
    spark.stop()
    return tempo, memoria, resumo.set_index(['categoria', 'hora']).sort_index(), partida


def medir(metodo, milhoes):
    """Roda uma medida em um processo novo e devolve o que ele imprimiu na ultima linha (JSON)."""
    processo = subprocess.run([sys.executable, '-X', 'utf8', os.path.abspath(__file__), '--medir', metodo, str(milhoes)],
                              capture_output=True, text=True, encoding='utf-8')
    linhas = [l for l in processo.stdout.splitlines() if l.startswith('RESULTADO ')]
    if processo.returncode != 0 or not linhas:
        print(processo.stderr[-2000:])
        raise SystemExit(f'A medida {metodo} com {milhoes} milhoes falhou.')
    return json.loads(linhas[-1][len('RESULTADO '):])


# ---------------------------------------------------------------- modos que rodam em processo separado
if '--gerar' in sys.argv:
    from spark_ambiente import iniciar_spark
    spark = iniciar_spark('gerar_cliques')
    gerar_dados(spark, int(sys.argv[sys.argv.index('--gerar') + 1]))
    spark.stop()
    sys.exit(0)

if '--medir' in sys.argv:
    metodo, milhoes = sys.argv[sys.argv.index('--medir') + 1], int(sys.argv[sys.argv.index('--medir') + 2])
    partida = 0.0
    if metodo == 'spark':
        tempo, memoria, resumo, partida = medir_spark(milhoes)
    else:
        tempo, memoria, resumo = (medir_pandas_inteiro if metodo == 'pandas' else medir_pandas_blocos)(milhoes)
    resumo = resumo.sort_index()
    print('RESULTADO ' + json.dumps({
        'tempo': tempo, 'memoria': memoria, 'partida': partida,
        'compras': int(resumo['compras'].sum()), 'receita': round(float(resumo['receita'].sum()), 2),
        'resumo': resumo.reset_index().astype({'hora': int, 'visualizacoes': int, 'compras': int}).to_dict('records')}))
    sys.exit(0)

# ---------------------------------------------------------------- experimento
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

argumentos = argparse.ArgumentParser()
argumentos.add_argument('--tamanhos', type=int, nargs='+', default=[1, 4, 16, 48], help='milhoes de linhas')
argumentos.add_argument('--manter-dados', action='store_true')
opcoes = argumentos.parse_args()
plt.style.use(ESTILO)
ram_total = memoria_total_mb()
print(f'Este computador tem {ram_total / 1000:.0f} GB de RAM e {os.cpu_count()} nucleos.')

for milhoes in opcoes.tamanhos:
    if glob.glob(os.path.join(pasta_tamanho(milhoes), '*.csv')):
        continue
    inicio = time.perf_counter()
    subprocess.run([sys.executable, '-X', 'utf8', os.path.abspath(__file__), '--gerar', str(milhoes)], check=True)
    tamanho = sum(os.path.getsize(a) for a in glob.glob(os.path.join(pasta_tamanho(milhoes), '*.csv')))
    print(f'Gerados {milhoes} milhoes de eventos: {tamanho / 1e9:.2f} GB de CSV em {time.perf_counter() - inicio:.0f} s',
          flush=True)

resultados = []
for milhoes in opcoes.tamanhos:
    for metodo, nome in [('pandas', 'pandas inteiro'), ('blocos', 'pandas em blocos'), ('spark', 'Spark')]:
        # Protecao: se a medida anterior do pandas inteiro indica que esta nao cabe na RAM, nao tentamos.
        anteriores = [r for r in resultados if r['metodo'] == 'pandas' and r['memoria'] is not None]
        if metodo == 'pandas' and anteriores:
            previsto = anteriores[-1]['memoria'] / anteriores[-1]['milhoes'] * milhoes
            if previsto > 0.7 * ram_total:
                print(f'{milhoes:>3} milhoes | {nome:<16} | PULADO: precisaria de ~{previsto / 1000:.1f} GB de RAM')
                resultados.append({'milhoes': milhoes, 'metodo': metodo, 'tempo': None, 'memoria': None,
                                   'previsto': previsto})
                continue
        medida = medir(metodo, milhoes)
        medida.update(milhoes=milhoes, metodo=metodo)
        resultados.append(medida)
        extra = f' (+{medida["partida"]:.0f} s para iniciar o Spark)' if metodo == 'spark' else ''
        print(f'{milhoes:>3} milhoes | {nome:<16} | {medida["tempo"]:6.1f} s{extra:<32} | '
              f'pico de memoria {medida["memoria"] / 1000:5.2f} GB | compras {medida["compras"]:,} | '
              f'receita {medida["receita"]:,.2f}', flush=True)

# Verificacao: os tres metodos precisam dar exatamente o mesmo resumo
maior = max(opcoes.tamanhos)
resumos = {r['metodo']: pd.DataFrame(r['resumo']).set_index(['categoria', 'hora']) for r in resultados
           if r['milhoes'] == maior and r.get('resumo')}
referencia = resumos['spark']
for metodo, resumo in resumos.items():
    if metodo != 'spark':
        iguais = (resumo[['visualizacoes', 'compras']].equals(referencia[['visualizacoes', 'compras']])
                  and np.allclose(resumo['receita'], referencia['receita']))
        print(f'Resumo do {metodo} igual ao do Spark? {iguais}')

# A resposta de negocio (com o maior volume): a hora de maior conversao de cada categoria.
# Os padroes plantados na geracao foram: mercado 7h-10h, eletronicos 12h-13h, moda 19h-22h, games 21h-23h.
referencia = referencia.assign(conversao=referencia['compras'] / referencia['visualizacoes'])
melhor = referencia.reset_index().sort_values('conversao').groupby('categoria').tail(1).sort_values('conversao')
print(f'\nHora de maior conversao por categoria ({maior} milhoes de eventos):')
print(melhor[['categoria', 'hora', 'conversao']].assign(conversao=lambda d: (100 * d['conversao']).round(2))
      .rename(columns={'conversao': 'conversao (%)'}).to_string(index=False))
print('Padroes plantados: mercado 7h-10h, eletronicos 12h-13h, moda 19h-22h, games 21h-23h; o resto converte ~2%.')

if not opcoes.manter_dados:
    shutil.rmtree(pasta_dados('cliques'), ignore_errors=True)

tabela = pd.DataFrame([{k: r.get(k) for k in ('milhoes', 'metodo', 'tempo', 'memoria', 'previsto')} for r in resultados])
estilos = {'pandas': ('pandas inteiro', '#8794A3', '-', 'o'), 'blocos': ('pandas em blocos (script 05)', '#168A8A', '--', 's'),
           'spark': ('Spark (1 GB de memória)', '#2F648F', '-', 'D')}
fig, (esq, dir) = plt.subplots(1, 2, figsize=(13.5, 4.6))
for metodo, (nome, cor, traco, marcador) in estilos.items():
    dados = tabela[(tabela['metodo'] == metodo) & tabela['tempo'].notna()]
    esq.plot(dados['milhoes'], dados['tempo'], color=cor, linestyle=traco, marker=marcador, label=nome)
    dir.plot(dados['milhoes'], dados['memoria'] / 1000, color=cor, linestyle=traco, marker=marcador, label=nome)
esq.set_xlabel('Milhões de eventos (CSV)')
esq.set_ylabel('Tempo da consulta (s)')
spark_maior = tabela[(tabela['metodo'] == 'spark') & (tabela['milhoes'] == maior)].iloc[0]
pandas_maior = tabela[(tabela['metodo'] == 'blocos') & (tabela['milhoes'] == maior)].iloc[0]
esq.set_title(f'Com {maior} milhões, o Spark é {pandas_maior["tempo"] / spark_maior["tempo"]:.1f}× mais rápido')
esq.legend()
partida = np.mean([r['partida'] for r in resultados if r['metodo'] == 'spark'])
esq.text(maior, 0, f'o Spark ainda leva ~{partida:.0f} s para iniciar\n(uma vez por sessão)', ha='right', va='bottom',
         fontsize=9, color='#2F648F')
# Memoria: o pandas inteiro cresce na proporcao das linhas; extrapolamos a reta medida
medidos = tabela[(tabela['metodo'] == 'pandas') & tabela['memoria'].notna()]
por_milhao = (medidos['memoria'] / medidos['milhoes']).iloc[-1] / 1000
limite_x = max(100, maior * 2)
dir.plot([medidos['milhoes'].iloc[-1], limite_x], [medidos['memoria'].iloc[-1] / 1000, por_milhao * limite_x],
         color='#8794A3', linestyle=':', linewidth=1.5)
pulados = tabela[tabela['previsto'].notna()]
dir.scatter(pulados['milhoes'], pulados['previsto'] / 1000, facecolor='white', edgecolor='#BD5B58', zorder=3,
            label='pandas inteiro: não coube (previsto)')
dir.axhline(8, color='#D69A35', linewidth=1)
dir.text(limite_x, 8.2, 'RAM de um notebook comum (8 GB)', color='#D69A35', ha='right', va='bottom', fontsize=9)
cruza = 8 / por_milhao
dir.set_xlim(0, limite_x)
dir.set_ylim(0, max(por_milhao * limite_x, 9) * 1.05)
dir.set_xlabel('Milhões de eventos (CSV)')
dir.set_ylabel('Pico de memória (GB)')
dir.set_title(f'O pandas inteiro passa de 8 GB perto de {cruza:.0f} milhões')
if len(pulados):
    dir.legend(loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(PASTA_FIGURAS, 'pandas_ou_spark.png'))
plt.show()
