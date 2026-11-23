# Tempo do evento, atrasos e falhas: o que torna o processamento em fluxo dificil, e como o Spark lida com isso.
# requer: pyspark
# Cenario simulado (semente fixa): 1.000 camaras frias de uma rede de supermercados enviam a temperatura a
# cada 10 s, durante 3 horas (1,08 milhao de leituras). Regra de negocio: alertar quando a media de um
# minuto de uma camara passa de 8 °C (acima disso carne e leite comecam a se perder).
# O que acontece no mundo real, e esta simulado aqui:
#   - 40 incidentes (porta esquecida aberta, compressor falhando): a temperatura sobe de 1 a 1,6 °C por minuto;
#   - 150 camaras ficam em lojas do interior ligadas por satelite: o equipamento da loja junta as leituras e
#     as envia de uma vez a cada 15 minutos. Metade dos incidentes acontece nessas lojas;
#   - 1% das demais leituras se atrasa de 1 a 20 minutos; 0,1% sao 999 (erro do sensor, como no script 07);
#   - o processamento pode cair no meio e precisa continuar de onde parou, sem perder nem repetir nada.
# As leituras sao gravadas em arquivos pela hora de CHEGADA (um arquivo a cada 5 minutos) e o Spark os
# consome um por vez, como se chegassem ao vivo: o resultado e reprodutivel e nao precisa esperar 3 horas.

import os
import json
import glob
import time
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import functions as F
from spark_ambiente import iniciar_spark, pasta_dados, coletar, ESTILO, PASTA_FIGURAS

plt.style.use(ESTILO)
gerador = np.random.default_rng(12)
base = pasta_dados('camaras_frias')
shutil.rmtree(base, ignore_errors=True)
INICIO = 1_768_456_800                      # 15/01/2026, 06:00 UTC
CAMARAS, PASSO, DURACAO = 1000, 10, 3 * 3600

# ---------------------------------------------------------------- 1. Gerar as leituras e seus atrasos
camara = np.repeat(np.arange(CAMARAS), DURACAO // PASSO)
segundo = np.tile(np.arange(0, DURACAO, PASSO), CAMARAS).astype(float)
temperatura = np.repeat(gerador.normal(3, 0.6, CAMARAS), DURACAO // PASSO) + gerador.normal(0, 0.3, camara.size)
atraso = gerador.exponential(2, camara.size)                                      # rede normal: ~2 s
tardias = gerador.random(camara.size) < 0.01
atraso[tardias] = gerador.uniform(60, 1200, tardias.sum())                         # 1%: 1 a 20 min
satelite = gerador.choice(CAMARAS, 150, replace=False)
via_satelite = np.isin(camara, satelite)
fase = gerador.uniform(0, 900, CAMARAS)[camara]                  # cada loja envia em seu proprio horario
proximo_envio = (np.floor((segundo + fase) / 900) + 1) * 900 - fase
atraso[via_satelite] = (proximo_envio - segundo)[via_satelite] + gerador.exponential(5, via_satelite.sum())
incidentes = []
normais = np.setdiff1d(np.arange(CAMARAS), satelite)
for tipo, candidatas in [('conexão normal', normais), ('via satélite', satelite)]:
    for c in gerador.choice(candidatas, 20, replace=False):
        comeco = gerador.uniform(600, DURACAO - 2400)                               # longe das bordas
        fim = comeco + gerador.uniform(300, 720)
        dentro = (camara == c) & (segundo >= comeco) & (segundo < fim)
        temperatura[dentro] += gerador.uniform(1.0, 1.6) * (segundo[dentro] - comeco) / 60   # °C por minuto
        incidentes.append({'tipo': tipo, 'camara': int(c), 'comeco': comeco, 'fim': fim})
temperatura[gerador.random(camara.size) < 0.001] = 999.0
leituras = pd.DataFrame({'camara': camara, 'momento': INICIO + segundo, 'temperatura': temperatura.round(2),
                         'chegada': INICIO + segundo + atraso})
incidentes = pd.DataFrame(incidentes)

# Um arquivo por intervalo de 5 minutos de CHEGADA; dentro de cada um, a ordem de chegada
leituras['arquivo'] = ((leituras['chegada'] - INICIO) // 300).astype(int)
pasta_lotes = os.path.join(base, 'lotes')
os.makedirs(pasta_lotes)
linhas_por_arquivo = {}
for numero, lote in leituras.sort_values('chegada').groupby('arquivo'):
    caminho = os.path.join(pasta_lotes, f'lote_{numero:03d}.json')
    lote[['camara', 'momento', 'temperatura']].to_json(caminho, orient='records', lines=True)
    linhas_por_arquivo[caminho] = int(lote['temperatura'].between(-30, 30).sum())    # validas: o 999 cai na leitura
arquivos = sorted(linhas_por_arquivo)
fora_de_ordem = (leituras.sort_values('chegada')['momento'].diff() < 0).mean()
print(f'{len(leituras):,} leituras em {len(arquivos)} arquivos de chegada; '
      f'{100 * fora_de_ordem:.1f}% chegam depois de uma leitura mais recente (fora de ordem)')

spark = iniciar_spark('camaras_frias', config={'spark.sql.shuffle.partitions': '4'})
esquema = 'camara INT, momento DOUBLE, temperatura DOUBLE'


def alertas_de(leituras_df):
    validas = (leituras_df.withColumn('momento', F.timestamp_seconds('momento'))
               .where(F.col('temperatura').between(-30, 30)))            # veracidade: descarta o 999
    return validas, (lambda df: df.groupBy(F.window('momento', '1 minute'), 'camara')
                     .agg(F.avg('temperatura').alias('media')).where('media > 8')
                     .select('camara', F.unix_seconds(F.col('window.start')).alias('minuto'), 'media'))


# ---------------------------------------------------------------- 2. A verdade: lote, com todos os dados ja chegados
validas, agregar = alertas_de(spark.read.schema(esquema).json(pasta_lotes))
verdade = coletar(agregar(validas))
print(f'Processando em lote, depois que tudo chegou: {len(verdade)} minutos-camara em alerta '
      f'({verdade["camara"].isin(satelite).sum()} em lojas via satelite)')


def encontrados(alertas):
    """Fracao dos minutos em alerta da referencia (lote) que o fluxo tambem encontrou, por tipo de conexao."""
    achados = set(zip(alertas['camara'], alertas['minuto']))
    ok = pd.Series([(c, m) in achados for c, m in zip(verdade['camara'], verdade['minuto'])])
    remota = verdade['camara'].isin(satelite).to_numpy()
    return ok[~remota].mean(), ok[remota].mean()


def rodar_fluxo(nome, marca_dagua, arquivos_entrada, entrada=None, modo='append'):
    """Consome os arquivos como um fluxo, um por micro-lote. Devolve os progressos de cada micro-lote."""
    entrada = entrada or os.path.join(base, nome, 'entrada')
    os.makedirs(entrada, exist_ok=True)
    for arquivo in arquivos_entrada:
        shutil.copy(arquivo, entrada)
    fluxo, agregar_fluxo = alertas_de(spark.readStream.schema(esquema).option('maxFilesPerTrigger', 1).json(entrada))
    if marca_dagua:
        fluxo = fluxo.withWatermark('momento', marca_dagua)
    escrita = agregar_fluxo(fluxo).writeStream.outputMode(modo) \
        .option('checkpointLocation', os.path.join(base, nome, 'checkpoint'))
    if modo == 'append':        # sink de arquivos: com o checkpoint, cada resultado e gravado exatamente uma vez
        escrita = escrita.format('parquet').option('path', os.path.join(base, nome, 'saida'))
    else:
        escrita = escrita.format('noop')
    consulta = escrita.trigger(availableNow=True).start()
    consulta.awaitTermination()
    return [p if isinstance(p, dict) else json.loads(p.json) for p in consulta.recentProgress]


def ler_saida(nome):
    pasta = os.path.join(base, nome, 'saida')
    return coletar(spark.read.parquet(pasta)) if glob.glob(os.path.join(pasta, '*.parquet')) else pd.DataFrame(
        columns=['camara', 'minuto', 'media'])


# ---------------------------------------------------------------- 3. O mesmo calculo em fluxo, com tres tolerancias
resultados = {}
for marca in ['1 minute', '5 minutes', '20 minutes']:
    inicio = time.perf_counter()
    progressos = rodar_fluxo(marca.replace(' ', '_'), marca, arquivos)
    alertas = ler_saida(marca.replace(' ', '_'))
    normal, remota = encontrados(alertas)
    resultados[marca] = {
        'estado': [p['stateOperators'][0]['numRowsTotal'] for p in progressos],
        'descartadas': sum(p['stateOperators'][0].get('numRowsDroppedByWatermark', 0) for p in progressos),
        'normal': normal, 'satelite': remota, 'alertas': alertas}
    r = resultados[marca]
    print(f'Marca d\'agua {marca:<10}: {len(alertas):>4} alertas | minutos em alerta encontrados: conexao normal '
          f'{100 * normal:3.0f}%, via satelite {100 * remota:3.0f}% | leituras atrasadas descartadas '
          f'{r["descartadas"]:>6,} | estado maximo {max(r["estado"]):>6,} linhas | {time.perf_counter() - inicio:.0f} s')

# Sem marca d'agua o Spark nunca sabe que uma janela terminou: o estado cresce para sempre.
sem_marca = [p['stateOperators'][0]['numRowsTotal'] for p in rodar_fluxo('sem_marca', None, arquivos, modo='update')]
print(f'Sem marca d\'agua: o estado termina com {sem_marca[-1]:,} linhas e continuaria crescendo.')

# ---------------------------------------------------------------- 4. Falha no meio do caminho
# Metade dos arquivos chega, a consulta para (a "queda"); depois chega o resto e ela e reiniciada com o mesmo
# checkpoint. O Spark retoma do ultimo micro-lote confirmado: nada e perdido nem processado duas vezes.
metade = len(arquivos) // 2
entrada_falha = os.path.join(base, 'falha', 'entrada')
rodar_fluxo('falha', '20 minutes', arquivos[:metade], entrada_falha)
antes = len(ler_saida('falha'))
retomada = rodar_fluxo('falha', '20 minutes', arquivos[metade:], entrada_falha)
depois = ler_saida('falha')
sem_falha = resultados['20 minutes']['alertas']
iguais = (depois.sort_values(['camara', 'minuto']).reset_index(drop=True).round(6)
          .equals(sem_falha.sort_values(['camara', 'minuto']).reset_index(drop=True).round(6)))
lidas_na_retomada = sum(p['numInputRows'] for p in retomada)
chegaram_depois = sum(linhas_por_arquivo[a] for a in arquivos[metade:])
print(f'\nFalha depois de {metade} arquivos: {antes} alertas ja gravados. A retomada leu {lidas_na_retomada:,} '
      f'leituras validas; chegaram {chegaram_depois:,} depois da falha. Total de {len(depois)} alertas. '
      f'Igual ao fluxo sem falha? {iguais}')
print(f'Recalcular tudo a cada lote, como fariamos com pandas, exigiria guardar as {len(leituras):,} leituras '
      f'(e mais 360 mil por hora, para sempre). Com marca d\'agua de 20 min, o Spark guardou no maximo '
      f'{max(resultados["20 minutes"]["estado"]):,} linhas.')
spark.stop()

fig, (a, b, c) = plt.subplots(1, 3, figsize=(16, 4.4))
atraso_min = ((leituras['chegada'] - leituras['momento']) / 60).to_numpy()
limites = np.logspace(-2, np.log10(25), 200)
for grupo, nome, cor, traco in [(~via_satelite, 'conexão normal', '#2F648F', '-'),
                                (via_satelite, 'via satélite (envio a cada 15 min)', '#BD5B58', '-')]:
    ordenado = np.sort(atraso_min[grupo])
    acima = 100 * (1 - np.searchsorted(ordenado, limites, side='right') / ordenado.size)
    a.plot(limites, acima, color=cor, linestyle=traco, label=nome)
a.set_xscale('log')
for minutos, rotulo in [(1, '1 min'), (5, '5 min'), (20, '20 min')]:
    a.axvline(minutos, color='#D69A35', linewidth=1)
    a.text(minutos * 1.08, 102, rotulo, color='#D69A35', fontsize=9)
a.set_ylim(0, 110)
a.set_xlabel('Atraso (minutos, escala log)')
a.set_ylabel('% das leituras com atraso maior')
a.set_title('Lojas via satélite chegam até 15 min atrasadas')
a.legend(loc='center left', fontsize=9)
marcas = list(resultados)
x = np.arange(len(marcas))
b.bar(x - 0.2, [100 * resultados[m]['normal'] for m in marcas], width=0.4, color='#2F648F', label='conexão normal')
b.bar(x + 0.2, [100 * resultados[m]['satelite'] for m in marcas], width=0.4, color='#BD5B58', label='via satélite')
for i, m in enumerate(marcas):
    b.text(i + 0.2, 100 * resultados[m]['satelite'] + 2, f'{100 * resultados[m]["satelite"]:.0f}%', ha='center',
           fontsize=9, color='#BD5B58')
b.set_xticks(x)
b.set_xticklabels(['1 min', '5 min', '20 min'])
b.set_xlabel("Marca d'água (quanto atraso o Spark espera)")
b.set_ylabel('Minutos em alerta encontrados (%)')
b.set_ylim(0, 115)
b.set_title('Esperar pouco perde alertas das lojas remotas')
b.legend(loc='upper left', fontsize=9)
for m, cor in zip(marcas, ['#7A9CC6', '#2F648F', '#20324A']):
    estado = resultados[m]['estado']
    c.plot(range(1, len(estado) + 1), estado, color=cor)
    c.text(len(estado) + 0.7, max(estado), m.replace('minutes', 'min').replace('minute', 'min'), color=cor,
           va='center', fontsize=9)
c.plot(range(1, len(sem_marca) + 1), sem_marca, color='#BD5B58', linestyle='--')
c.text(len(sem_marca) + 0.7, sem_marca[-1], "sem marca\nd'água", color='#BD5B58', va='center', fontsize=9)
c.set_yscale('log')
c.set_xlim(0, len(sem_marca) + 8)
c.set_xlabel('Micro-lote (5 minutos de chegada)')
c.set_ylabel('Linhas guardadas no estado (escala log)')
c.set_title('Sem marca d\'água, a memória não para de crescer')
plt.tight_layout()
plt.savefig(os.path.join(PASTA_FIGURAS, 'janelas_atrasos_e_falhas.png'))
plt.show()
shutil.rmtree(base, ignore_errors=True)
