# Validacao com janelas deslizantes: varias "datas de corte" em vez de uma so.
# Um unico teste pode cair em um periodo facil ou dificil; varias janelas dao uma medida mais honesta.

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings('ignore')
pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

serie = pd.read_csv(os.path.join(pasta, '..', 'dados', 'SPCS20RPSNSA.csv'), index_col=0, parse_dates=True)
serie.columns = ['vendas']
serie = serie.asfreq('MS')['vendas']

horizonte = 12                       # prever 12 meses a frente
cortes = ['2013-01-01', '2014-01-01', '2015-01-01', '2016-01-01', '2017-01-01', '2018-01-01']

def mae(real, previsto):
    return float(np.mean(np.abs(real - previsto)))

resultados = []
for corte in cortes:
    treino = serie[:corte].iloc[:-1]                 # tudo antes do corte
    teste = serie[corte:].iloc[:horizonte]           # 12 meses a partir do corte
    sazonal = pd.Series(treino.iloc[-12:].values, index=teste.index)
    sarima = ARIMA(treino, order=(1, 1, 2), seasonal_order=(0, 1, 1, 12)).fit().forecast(steps=horizonte)
    resultados.append({'corte': corte[:4], 'sazonal ingenua': mae(teste, sazonal), 'SARIMA': mae(teste, sarima)})
    print(f'corte {corte[:7]}: treino ate {treino.index[-1]:%Y-%m} | MAE sazonal={resultados[-1]["sazonal ingenua"]:.0f} | MAE SARIMA={resultados[-1]["SARIMA"]:.0f}')

tabela = pd.DataFrame(resultados).set_index('corte')
print('\nMedia dos MAE nas janelas:')
print(tabela.mean().round(0))
print('Desvio entre janelas:')
print(tabela.std().round(0))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={'width_ratios': [1.6, 1]})
# Esquerda: as janelas sobre a serie
esq.plot(serie.index, serie, color='#E6EBF0', linewidth=1.5)
for i, corte in enumerate(cortes):
    inicio = pd.Timestamp(corte)
    fim = inicio + pd.DateOffset(months=horizonte)
    esq.axvspan(inicio, fim, ymin=0.05 + 0.15 * i, ymax=0.17 + 0.15 * i, color='#168A8A', alpha=0.6)
    esq.plot(serie[:corte].index, [esq.get_ylim()[0] + (0.11 + 0.15 * i) * (esq.get_ylim()[1] - esq.get_ylim()[0])] * len(serie[:corte]),
             color='#2F648F', linewidth=3, solid_capstyle='butt')
esq.set_title('Treino (azul) até o corte; teste (verde) nos 12 meses seguintes')
esq.set_yticks([])
esq.set_xlim(pd.Timestamp('2006-01-01'), serie.index[-1])
# Direita: erro por janela
dir.plot(tabela.index, tabela['sazonal ingenua'], marker='o', color='#8794A3', label='sazonal ingênua')
dir.plot(tabela.index, tabela['SARIMA'], marker='o', color='#168A8A', label='SARIMA')
dir.set_ylabel('MAE (pares de vendas)')
dir.set_xlabel('Ano do corte')
dir.set_title('O erro varia com a janela: compare médias')
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'janelas_de_validacao.png'))
plt.show()

# Experimente: acrescente o corte '2012-01-01' (logo apos a crise). O que acontece com os erros?
