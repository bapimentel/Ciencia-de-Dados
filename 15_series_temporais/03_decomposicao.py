# Decompor uma serie em tendencia, sazonalidade e residuo.

import os
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

serie = pd.read_csv(os.path.join(pasta, '..', 'dados', 'SPCS20RPSNSA.csv'), index_col=0, parse_dates=True)
serie.columns = ['vendas']
serie = serie.asfreq('MS')

# Modelo aditivo: serie = tendencia + sazonalidade + residuo
decomposicao = seasonal_decompose(serie['vendas'], model='additive', period=12)
tendencia = decomposicao.trend
sazonalidade = decomposicao.seasonal
residuo = decomposicao.resid

print('Componente sazonal (mesmo valor todo ano, em pares de vendas):')
print(sazonalidade[:12].round(0).to_string())
print('\nAmplitude da sazonalidade:', round(sazonalidade.max() - sazonalidade.min()), 'pares de vendas')
print('Desvio-padrao do residuo:', round(residuo.std()))

fig, eixos = plt.subplots(4, 1, figsize=(9, 8), sharex=True)
eixos[0].plot(serie.index, serie['vendas'], color='#2F648F')
eixos[0].set_title('Série original')
eixos[1].plot(tendencia.index, tendencia, color='#2F648F')
eixos[1].set_title('Tendência (média móvel centrada de 12 meses)')
eixos[2].plot(sazonalidade.index, sazonalidade, color='#168A8A')
eixos[2].set_title('Sazonalidade (padrão médio de cada mês, repetido)')
eixos[3].plot(residuo.index, residuo, color='#8794A3', linewidth=1)
eixos[3].axhline(0, color='#20324A', linewidth=0.8)
eixos[3].set_title('Resíduo (o que sobra)')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'decomposicao.png'))
plt.show()

# Leitura: a sazonalidade e estavel (cerca de 60 mil pares entre o vale de fevereiro e o pico de junho);
# a tendencia carrega a crise de 2008; o residuo e maior justamente em 2008-2010, quando o padrao quebrou.

# Quando a oscilacao cresce junto com o nivel da serie, o modelo multiplicativo descreve melhor.
# Exemplo: as vendas de antidiabeticos (dados/Drugs.csv) oscilam mais a medida que crescem.
drugs = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Drugs.csv'), index_col=0, parse_dates=True).asfreq('MS')
multiplicativa = seasonal_decompose(drugs['value'], model='multiplicative', period=12)
print('\nFatores sazonais de Drugs.csv (1 = mes tipico):')
print(multiplicativa.seasonal[:12].round(2).to_string())
# Janeiro vende cerca de 30% acima do tipico; fevereiro, cerca de 20% abaixo.

# Experimente: decomponha Drugs.csv com model='additive' e compare o residuo dos dois modelos.
