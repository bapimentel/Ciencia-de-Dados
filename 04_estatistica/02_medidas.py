# Medidas de tendencia central e de dispersao, calculadas de tres jeitos:
# na mao, com o modulo statistics e com numpy/pandas.

import os
import statistics
import numpy as np
import pandas as pd
from scipy import stats

pasta = os.path.dirname(os.path.abspath(__file__))
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

# A variavel de interesse: valor total de cada uma das 1000 vendas
total = dados['Total']
print('Registros:', len(total))

# Media: soma dividida pela quantidade
media_na_mao = sum(total) / len(total)
print('Media (na mao):     ', round(media_na_mao, 2))
print('Media (statistics): ', round(statistics.mean(total), 2))
print('Media (pandas):     ', round(total.mean(), 2))

# Mediana: o valor do meio depois de ordenar
print('Mediana:', total.median())

# Quando media e mediana se afastam, a distribuicao e assimetrica.
# Aqui a media (323) e maior que a mediana (254): ha vendas grandes puxando a media.

# Quantis: pontos que dividem os dados ordenados
q1 = np.quantile(total, 0.25)
q2 = np.quantile(total, 0.50)
q3 = np.quantile(total, 0.75)
print('Quartis:', round(q1, 2), round(q2, 2), round(q3, 2))
print('25% das vendas ficam abaixo de', round(q1, 2), 'e 25% acima de', round(q3, 2))

# Dispersao: quanto os valores se espalham em torno do centro
amplitude = total.max() - total.min()
variancia = statistics.variance(total)
desvio_padrao = statistics.stdev(total)
coeficiente_variacao = stats.variation(total)     # desvio / media
print('Amplitude:', round(amplitude, 2))
print('Variancia:', round(variancia, 2))
print('Desvio-padrao:', round(desvio_padrao, 2))
print('Coeficiente de variacao:', round(coeficiente_variacao, 3))

# Intervalo interquartil: amplitude do "meio" dos dados, menos sensivel a extremos
print('IQR (Q3 - Q1):', round(q3 - q1, 2))

# As mesmas medidas por grupo, em uma linha de pandas
print(dados.groupby('Customer type')['Total'].agg(['count', 'mean', 'median', 'std']).round(2))

# Experimente: repita para a coluna 'Rating'. Media e mediana ficam proximas?
# O que isso diz sobre a forma da distribuicao das avaliacoes?
