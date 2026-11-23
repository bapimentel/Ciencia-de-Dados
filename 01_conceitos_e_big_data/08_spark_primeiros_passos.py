# Spark, primeiros passos: o MapReduce do script 05, agora automatico e em paralelo.
# requer: pyspark
# As mesmas vendas sinteticas do script 05 (loja, produto, quantidade, preco), mas com 20 milhoes de
# linhas geradas pelo proprio Spark, em paralelo, sem passar pela memoria do Python (semente fixa).
# Quatro ideias: (1) particoes: cada nucleo do computador trabalha em um pedaco dos dados;
# (2) avaliacao preguicosa: transformacoes so montam um plano, acoes o executam;
# (3) o plano de um groupBy e exatamente map -> shuffle -> reduce;
# (4) a mediana exata custa caro em dados distribuidos; o Spark oferece uma aproximacao barata.

import io
import os
import time
import contextlib
import matplotlib.pyplot as plt
from pyspark.sql import functions as F
from spark_ambiente import iniciar_spark, coletar, ESTILO, PASTA_FIGURAS

plt.style.use(ESTILO)
spark = iniciar_spark('primeiros_passos')
nucleos = spark.sparkContext.defaultParallelism
n = 20_000_000
produtos = F.array(*[F.lit(p) for p in ['pao', 'leite', 'cafe', 'arroz', 'feijao']])


def gerar_vendas(particoes, linhas=n):
    # spark.range cria os numeros 0..linhas-1 ja divididos em particoes; cada coluna e sorteada em paralelo.
    return spark.range(linhas, numPartitions=particoes).select(
        (F.floor(F.rand(1) * 50) + 1).cast('int').alias('loja'),
        F.element_at(produtos, (F.floor(F.rand(2) * 5) + 1).cast('int')).alias('produto'),
        (F.floor(F.rand(3) * 10) + 1).cast('int').alias('quantidade'),
        (F.rand(4) * 49 + 1).alias('preco'))


spark.range(1).collect()      # aquecimento: a primeira chamada carrega as classes do Java

# --- (2) Avaliacao preguicosa: definir nao custa nada; so a acao (collect, count, show, write) trabalha
vendas = gerar_vendas(nucleos)
inicio = time.perf_counter()
por_produto = vendas.groupBy('produto').agg(F.sum('quantidade').alias('quantidade'),
                                            F.avg('preco').alias('preco_medio'))
print(f'Definir o groupBy sobre 20 milhoes de vendas: {(time.perf_counter() - inicio) * 1000:.0f} ms '
      '(nenhuma linha existe ainda; o Spark so montou um plano)')
inicio = time.perf_counter()
resultado = coletar(por_produto.orderBy('produto'))
print(f'Executar o plano (acao collect): {time.perf_counter() - inicio:.1f} s, usando {nucleos} nucleos')
print(resultado.round(3).to_string(index=False))

# --- (3) O plano fisico: o Spark escreve sozinho o MapReduce que o script 05 fez a mao
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    por_produto.explain()
print('\nPlano fisico (de baixo para cima e a ordem de execucao):')
for linha in saida.getvalue().splitlines():
    if any(chave in linha for chave in ('HashAggregate', 'Exchange', 'Range')):
        print('  ', linha.strip()[:110])
print('''Leitura do plano:
   Range ................................ gera/le as linhas, cada particao em um nucleo
   HashAggregate(partial_sum, partial_avg) MAP: cada particao resume sozinha (soma, e soma+contagem p/ media)
   Exchange hashpartitioning(produto) ... SHUFFLE: os resumos do mesmo produto vao para o mesmo lugar
   HashAggregate(sum, avg) .............. REDUCE: combina os resumos parciais''')

# Quantas linhas passam por cada etapa? O "map" reduz 20 milhoes a (particoes x produtos) linhas.
com_particao = vendas.withColumn('particao', F.spark_partition_id())
linhas_do_map = com_particao.groupBy('particao', 'produto').count().count()
etapas = {'lidas\n(map)': n, 'resumos parciais\n(atravessam o shuffle)': linhas_do_map,
          'resultado\n(reduce)': len(resultado)}
print(f'\nLinhas lidas: {n:,}; resumos parciais que atravessam o shuffle: {linhas_do_map} '
      f'({nucleos} particoes x 5 produtos); linhas no resultado: {len(resultado)}')

# --- (1) Particoes e paralelismo: a mesma conta, com 60 milhoes de linhas, usando 1, 2, 4, ... particoes
linhas_tempo = 60_000_000
tempos = {}
gerar_vendas(nucleos, linhas_tempo).groupBy('produto').agg(F.sum('preco')).collect()      # aquecimento
for particoes in [1, 2, 4, 8, nucleos]:
    inicio = time.perf_counter()
    gerar_vendas(particoes, linhas_tempo).groupBy('produto').agg(F.sum('preco')).collect()
    tempos[particoes] = time.perf_counter() - inicio
    print(f'{particoes:>2} particao(oes): {tempos[particoes]:.2f} s')
ganho = tempos[1] / tempos[nucleos]
print(f'Com {nucleos} particoes a conta ficou {ganho:.1f} vezes mais rapida que com 1.')
# O ganho nao e proporcional ao numero de nucleos: parte do trabalho nao se divide (planejar, juntar
# os resultados) e os nucleos de um notebook nao sao todos iguais. Num cluster, cada particao poderia
# estar em uma maquina diferente, e o mesmo codigo continuaria valendo.

# --- (4) Media se divide (soma e contagem); mediana nao. A mediana exata (F.median) precisa reunir
# num so lugar todos os valores distintos de cada grupo: aqui, 20 milhoes de precos. Com os 2 GB que
# demos ao Spark, ela estoura a memoria (experimente). percentile_approx guarda, de cada particao,
# so um resumo de tamanho fixo, e garante erro de no maximo 1/precisao da posicao na ordenacao.
inicio = time.perf_counter()
medianas = coletar(vendas.groupBy('produto').agg(F.percentile_approx('preco', 0.5, 1000).alias('mediana'))
                   .orderBy('produto'))
print(f'\nMediana aproximada do preco (precisao 1000): {time.perf_counter() - inicio:.1f} s ->',
      dict(zip(medianas['produto'], medianas['mediana'].round(2))))
print('Valor teorico para precos uniformes entre 1 e 50: 25,50')
spark.stop()

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
x = list(tempos)
esq.plot(range(len(x)), list(tempos.values()), marker='o', color='#2F648F')
esq.set_xticks(range(len(x)))
esq.set_xticklabels(x)
esq.set_ylim(0, max(tempos.values()) * 1.15)
esq.set_xlabel('Partições (núcleos trabalhando ao mesmo tempo)')
esq.set_ylabel('Tempo do groupBy (s)')
esq.set_title(f'{nucleos} partições: {ganho:.1f}× mais rápido que 1')
for i, valor in enumerate(tempos.values()):
    esq.annotate(f'{valor:.1f} s', (i, valor), textcoords='offset points', xytext=(7, 7), ha='left', fontsize=9)
cores = ['#8794A3', '#D69A35', '#2F648F']
barras = dir.barh(list(etapas)[::-1], list(etapas.values())[::-1], color=cores[::-1])
dir.set_xscale('log')
dir.set_xlabel('Linhas (escala log)')
dir.grid(axis='x', color='#E6EBF0')
dir.grid(axis='y', visible=False)
for barra, valor in zip(barras, list(etapas.values())[::-1]):
    dir.text(barra.get_width() * 1.3, barra.get_y() + barra.get_height() / 2, f'{valor:,}'.replace(',', '.'),
             va='center', fontsize=10)
dir.set_xlim(1, n * 40)
dir.set_title(f'O map resume antes do shuffle: só {linhas_do_map} linhas trafegam')
plt.tight_layout()
plt.savefig(os.path.join(PASTA_FIGURAS, 'spark_primeiros_passos.png'))
plt.show()
