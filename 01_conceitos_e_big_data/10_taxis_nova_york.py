# Um problema real de Big Data: um ano de corridas de taxi em Nova York (cerca de 40 milhoes de linhas).
# requer: pyspark
# Dados: registros oficiais da Taxi & Limousine Commission (TLC) de Nova York, publicados todo mes em
# Parquet (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page). Na primeira execucao o
# script baixa os 12 meses de 2024 (cerca de 650 MB) para ~/ciencia-de-dados-big-data/taxis.
#
# Perguntas de uma cooperativa de taxistas:
#   1) Em que dias e horas ha mais corridas (onde concentrar motoristas)?
#   2) Em que hora uma corrida rende mais por minuto ao volante?
#   3) Quanto da receita sai dos aeroportos?
# E a pergunta de veracidade que vem antes: quantos registros sao impossiveis?
#
# Uso: python 10_taxis_nova_york.py [--meses 12]

import io
import os
import re
import sys
import json
import glob
import time
import shutil
import argparse
import contextlib
import subprocess
import urllib.request
from spark_ambiente import pasta_dados, memoria_pico_mb, ESTILO, PASTA_FIGURAS

ANO = 2024
URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{ano}-{mes:02d}.parquet'
URL_ZONAS = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
COLUNAS = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance',
           'PULocationID', 'total_amount']

# ---------------------------------------------------------------- modo "medida do pandas" (processo separado)
if '--medir-pandas' in sys.argv:
    import pandas as pd
    arquivo, quais = sys.argv[sys.argv.index('--medir-pandas') + 1:][:2]
    inicio = time.perf_counter()
    tabela = pd.read_parquet(arquivo, columns=None if quais == 'todas' else COLUNAS)
    tabela.groupby(tabela['tpep_pickup_datetime'].dt.hour)['total_amount'].sum()
    print('RESULTADO ' + json.dumps({'tempo': time.perf_counter() - inicio, 'memoria': memoria_pico_mb(),
                                     'linhas': len(tabela), 'colunas': tabela.shape[1]}))
    sys.exit(0)

import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import functions as F
from spark_ambiente import iniciar_spark, coletar, memoria_jvm_pico_mb

argumentos = argparse.ArgumentParser()
argumentos.add_argument('--meses', type=int, default=12, help='quantos meses de 2024 usar (1 a 12)')
opcoes = argumentos.parse_args()
plt.style.use(ESTILO)


def baixar(url, destino):
    if os.path.exists(destino):
        return
    pedido = urllib.request.Request(url, headers={'User-Agent': 'exemplo-didatico-ciencia-de-dados/1.0'})
    with urllib.request.urlopen(pedido, timeout=300) as resposta, open(destino + '.parte', 'wb') as arquivo:
        shutil.copyfileobj(resposta, arquivo, 1 << 20)
    os.replace(destino + '.parte', destino)          # so vira arquivo "de verdade" quando terminou
    print(f'  baixado {os.path.basename(destino)} ({os.path.getsize(destino) / 1e6:.0f} MB)')


pasta_viagens = pasta_dados('taxis', 'viagens')
arquivos = [os.path.join(pasta_viagens, f'yellow_tripdata_{ANO}-{mes:02d}.parquet') for mes in range(1, opcoes.meses + 1)]
if not all(os.path.exists(a) for a in arquivos):
    print(f'Baixando {opcoes.meses} mes(es) de corridas da TLC (so na primeira vez)...')
for mes, arquivo in enumerate(arquivos, start=1):
    baixar(URL.format(ano=ANO, mes=mes), arquivo)
arquivo_zonas = os.path.join(pasta_dados('taxis'), 'taxi_zone_lookup.csv')
baixar(URL_ZONAS, arquivo_zonas)
tamanho_disco = sum(os.path.getsize(a) for a in arquivos)

spark = iniciar_spark('taxis', memoria='2g', config={'spark.sql.maxMetadataStringLength': '2000'})
inicio_total = time.perf_counter()

# ---------------------------------------------------------------- 1. Volume: quanto dado e este?
viagens = spark.read.parquet(*arquivos)
linhas = viagens.count()                # rapido: o Parquet guarda a contagem no rodape de cada arquivo
print(f'\n{len(arquivos)} arquivos Parquet, {tamanho_disco / 1e6:.0f} MB em disco: '
      f'{linhas:,} corridas x {len(viagens.columns)} colunas')

# ---------------------------------------------------------------- 2. Veracidade: registros impossiveis
inicio_c = F.col('tpep_pickup_datetime').cast('timestamp')
fim_c = F.col('tpep_dropoff_datetime').cast('timestamp')
minutos = (F.unix_seconds(fim_c) - F.unix_seconds(inicio_c)) / 60
milhas_por_hora = F.try_divide(F.col('trip_distance'), minutos / 60)
regras = {
    'data fora de 2024': F.year(inicio_c) != ANO,
    'duracao <= 0 ou > 5 h': (minutos <= 0) | (minutos > 300),
    'distancia zero': F.col('trip_distance') <= 0,
    'valor total <= 0': F.col('total_amount') <= 0,
    'velocidade > 80 mph': milhas_por_hora > 80,
}
contagens = viagens.agg(*[F.sum(F.coalesce(regra, F.lit(False)).cast('int')).alias(nome) for nome, regra in regras.items()],
                        F.sum(F.col('passenger_count').isNull().cast('int')).alias('passageiros ausentes'))
problemas = coletar(contagens).iloc[0].sort_values()
# Corrida valida = passa em TODAS as regras. Escrito assim (condicoes ligadas por E), o Spark consegue
# empurrar parte do filtro para dentro da leitura do Parquet.
valida = ((F.year(inicio_c) == ANO) & (minutos > 0) & (minutos <= 300) & (F.col('trip_distance') > 0)
          & (F.col('total_amount') > 0) & (milhas_por_hora <= 80))
validas = (viagens.where(valida)
           .select(inicio_c.alias('inicio'), minutos.alias('minutos'), 'trip_distance', 'PULocationID', 'total_amount'))
descartadas = linhas - validas.count()
print('\nRegistros com problema (uma corrida pode ter mais de um):')
for nome, quantidade in problemas.items():
    print(f'  {nome:<24} {quantidade:>10,}  ({100 * quantidade / linhas:.2f}%)')
print(f'Descartadas por serem impossiveis: {descartadas:,} ({100 * descartadas / linhas:.1f}%). '
      'Passageiros ausentes nao invalidam a corrida e ficam.')

# ---------------------------------------------------------------- 3. Pergunta 1: dias e horas de mais corridas
por_dia_hora = (validas.groupBy(F.to_date('inicio').alias('data'), F.dayofweek('inicio').alias('dia'),
                                F.hour('inicio').alias('hora')).count()
                .groupBy('dia', 'hora').agg(F.avg('count').alias('corridas')))
mapa = coletar(por_dia_hora).pivot(index='hora', columns='dia', values='corridas').sort_index()
mapa = mapa[[2, 3, 4, 5, 6, 7, 1]]          # dayofweek: 1 = domingo; reordenamos de segunda a domingo
mapa.columns = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
pico = mapa.stack().idxmax()
print(f'\nPico medio: {mapa.stack().max():,.0f} corridas por hora ({pico[1]}, {pico[0]}h); '
      f'vale: {mapa.stack().min():,.0f} ({mapa.stack().idxmin()[1]}, {mapa.stack().idxmin()[0]}h)')

# ---------------------------------------------------------------- 4. Pergunta 2: rendimento por minuto
rendimento = coletar(validas.groupBy(F.hour('inicio').alias('hora'))
                     .agg((F.sum('total_amount') / F.sum('minutos')).alias('dolares_por_minuto'),
                          F.avg(F.try_divide(F.col('trip_distance'), F.col('minutos') / 60)).alias('mph'))
                     .orderBy('hora')).set_index('hora')
melhor, pior = rendimento['dolares_por_minuto'].idxmax(), rendimento['dolares_por_minuto'].idxmin()
print(f'Receita por minuto com passageiro: {rendimento.loc[melhor, "dolares_por_minuto"]:.2f} US$/min as {melhor}h '
      f'(media de {rendimento.loc[melhor, "mph"]:.0f} mph) contra {rendimento.loc[pior, "dolares_por_minuto"]:.2f} '
      f'as {pior}h ({rendimento.loc[pior, "mph"]:.0f} mph): o transito decide o rendimento')

# ---------------------------------------------------------------- 5. Pergunta 3: aeroportos (variedade: Parquet + CSV)
zonas = spark.read.csv(arquivo_zonas, header=True, inferSchema=True)
por_zona = (validas.join(F.broadcast(zonas), validas['PULocationID'] == zonas['LocationID'])
            .groupBy('Zone', 'Borough').agg(F.count('*').alias('corridas'), F.sum('total_amount').alias('receita')))
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    por_zona.explain()
plano = saida.getvalue()
zonas_pd = coletar(por_zona).sort_values('receita', ascending=False)
aeroportos = zonas_pd['Zone'].str.contains('Airport', na=False)
print(f'\nAeroportos (JFK, LaGuardia, Newark): {100 * zonas_pd.loc[aeroportos, "corridas"].sum() / zonas_pd["corridas"].sum():.1f}% '
      f'das corridas e {100 * zonas_pd.loc[aeroportos, "receita"].sum() / zonas_pd["receita"].sum():.1f}% da receita')
print(zonas_pd.head(8).assign(receita=lambda d: (d['receita'] / 1e6).round(1))
      .rename(columns={'receita': 'receita (US$ mi)'}).to_string(index=False))

# O que o Spark fez sem pedirmos: leu so as colunas usadas, empurrou o filtro para a leitura do
# Parquet e enviou a tabela pequena de zonas inteira a cada trabalhador (broadcast) em vez de embaralhar.
lidas = re.search(r'FileScan parquet \[([^\]]*)\]', plano)
colunas_lidas = [c.split('#')[0] for c in lidas.group(1).split(',')] if lidas else []
print(f'\nColunas lidas do Parquet: {len(colunas_lidas)} de {len(viagens.columns)} ({", ".join(colunas_lidas)})')
filtros = re.search(r'PushedFilters: \[([^\]]*)\]', plano)
print('Filtros empurrados para a leitura:', filtros.group(1) if filtros else 'nenhum')
print('Juncao usada:', 'BroadcastHashJoin (a tabela de zonas vai inteira a cada nucleo; nada de shuffle)'
      if 'BroadcastHashJoin' in plano else 'outra')

# ---------------------------------------------------------------- 6. Gravar o resultado como um "data lake"
# Resumo por data e hora, particionado por mes: cada mes vira uma pasta, e quem le um mes so abre essa pasta.
destino = pasta_dados('taxis', 'resumo_por_hora')
(validas.groupBy(F.month('inicio').alias('mes'), F.to_date('inicio').alias('data'), F.hour('inicio').alias('hora'))
 .agg(F.count('*').alias('corridas'), F.sum('total_amount').alias('receita'), F.sum('minutos').alias('minutos'))
 .write.mode('overwrite').partitionBy('mes').parquet(destino))
tamanho_resumo = sum(os.path.getsize(a) for a in glob.glob(os.path.join(destino, '**', '*.parquet'), recursive=True))
julho = spark.read.parquet(destino).where('mes = 7')
print(f'\nResumo gravado em {len(glob.glob(os.path.join(destino, "mes=*")))} pastas (uma por mes), '
      f'{tamanho_resumo / 1e6:.1f} MB; julho tem {julho.count()} linhas (data x hora)')
tempo_spark = time.perf_counter() - inicio_total
memoria_spark = memoria_jvm_pico_mb(spark) + memoria_pico_mb()
spark.stop()

# ---------------------------------------------------------------- 7. E se fosse com pandas?
medidas = {}
for quais in ['todas', 'usadas']:
    processo = subprocess.run([sys.executable, '-X', 'utf8', os.path.abspath(__file__), '--medir-pandas', arquivos[0], quais],
                              capture_output=True, text=True, encoding='utf-8')
    medidas[quais] = json.loads([l for l in processo.stdout.splitlines() if l.startswith('RESULTADO ')][-1][10:])
fator = linhas / medidas['todas']['linhas']
print(f'\nSpark: todas as etapas acima, {linhas / 1e6:.0f} milhoes de corridas, em {tempo_spark:.0f} s, '
      f'com pico de {memoria_spark / 1000:.1f} GB no total (heap do Java limitado a 2 GB, mais a memoria fora '
      'do heap e o Python). O limite vem da configuracao, nao do tamanho dos dados.')
for quais, rotulo in [('todas', 'todas as 19 colunas'), ('usadas', f'so as {len(COLUNAS)} colunas usadas')]:
    m = medidas[quais]
    print(f'pandas, 1 mes ({m["linhas"] / 1e6:.1f} milhoes), {rotulo}: {m["tempo"]:.1f} s e {m["memoria"] / 1000:.1f} GB '
          f'-> o ano todo precisaria de ~{m["memoria"] * fator / 1000:.0f} GB de RAM')

fig, (a, b, c) = plt.subplots(1, 3, figsize=(16, 4.6), gridspec_kw={'width_ratios': [1.15, 1, 1]})
imagem = a.imshow(mapa.values, aspect='auto', cmap='Blues', origin='lower')
a.set_xticks(range(7))
a.set_xticklabels(mapa.columns)
a.set_yticks(range(0, 24, 3))
a.set_yticklabels([f'{h}h' for h in range(0, 24, 3)])
a.grid(False)
a.set_title(f'Pico: {pico[1]} às {pico[0]}h (média por hora)')
plt.colorbar(imagem, ax=a, label='corridas por hora (média)')
b.plot(rendimento.index, rendimento['dolares_por_minuto'], color='#2F648F', marker='o', markersize=4)
b.scatter([melhor], [rendimento.loc[melhor, 'dolares_por_minuto']], color='#D69A35', zorder=3, s=60)
b.annotate(f'{melhor}h: {rendimento.loc[melhor, "dolares_por_minuto"]:.2f} US$/min',
           (melhor, rendimento.loc[melhor, 'dolares_por_minuto']), textcoords='offset points', xytext=(8, 4), fontsize=9)
b.set_xticks(range(0, 24, 3))
b.set_xlabel('Hora do embarque')
b.set_ylabel('US$ por minuto com passageiro')
b.set_ylim(0, rendimento['dolares_por_minuto'].max() * 1.15)
b.set_title(f'Rende mais às {melhor}h, quando o trânsito flui')
rotulos = {'duracao <= 0 ou > 5 h': 'duração ≤ 0 ou > 5 h', 'distancia zero': 'distância zero',
           'valor total <= 0': 'valor total ≤ 0', 'passageiros ausentes': 'passageiros ausentes (mantidas)'}
c.barh(range(len(problemas)), problemas.values / 1000,
       color=['#8794A3' if nome == 'passageiros ausentes' else '#BD5B58' for nome in problemas.index])
c.set_yticks(range(len(problemas)))
c.set_yticklabels([rotulos.get(nome, nome) for nome in problemas.index])
c.set_xlabel('Milhares de registros')
c.grid(axis='x', color='#E6EBF0')
c.grid(axis='y', visible=False)
for i, valor in enumerate(problemas.values):
    c.text(valor / 1000, i, f' {100 * valor / linhas:.1f}%', va='center', fontsize=9)
c.set_xlim(0, problemas.max() / 1000 * 1.25)
c.set_title(f'{descartadas / 1e6:.1f} milhão de corridas impossíveis ({100 * descartadas / linhas:.1f}%)')
fig.suptitle(f'Táxis amarelos de Nova York, {ANO}: {linhas / 1e6:.1f} milhões de corridas processadas com Spark',
             x=0.01, ha='left', fontsize=12, color='#20324A')
plt.tight_layout()
plt.savefig(os.path.join(PASTA_FIGURAS, 'taxis_nova_york.png'))
plt.show()
