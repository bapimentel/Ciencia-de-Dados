# ARIMA com a API atual do statsmodels, comparado com a linha de base sazonal.
# ARIMA(p, d, q): AR = a serie e regredida nos proprios valores passados (p defasagens);
# I = trabalha-se com a serie diferenciada d vezes; MA = o erro e combinacao dos q erros anteriores.
# API atual: statsmodels.tsa.arima.model.ARIMA e get_forecast() (em tutoriais antigos aparece
# statsmodels.tsa.arima_model.ARIMA e plot_predict, que foram removidos).

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings('ignore')     # avisos de convergencia do otimizador nao ajudam aqui
pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

serie = pd.read_csv(os.path.join(pasta, '..', 'dados', 'SPCS20RPSNSA.csv'), index_col=0, parse_dates=True)
serie.columns = ['vendas']
serie = serie.asfreq('MS')['vendas']

horizonte = 24
treino, teste = serie[:-horizonte], serie[-horizonte:]

def mae(real, previsto):
    return float(np.mean(np.abs(real - previsto)))

# Linha de base sazonal (mesmo mes do ano anterior)
sazonal = pd.Series(treino.iloc[-12:].values.tolist() * 2, index=teste.index)
print('Sazonal ingenua            MAE =', round(mae(teste, sazonal)))

# ARIMA(1,1,2): AR de ordem 1, uma diferenca (a serie nao e estacionaria, ver script 05), MA de ordem 2
modelo = ARIMA(treino, order=(1, 1, 2)).fit()
print(modelo.summary().tables[1])
previsao = modelo.get_forecast(steps=horizonte)
arima_112 = previsao.predicted_mean
intervalo = previsao.conf_int()
print('ARIMA(1,1,2)               MAE =', round(mae(teste, arima_112)))
# Sem componente sazonal, o ARIMA(1,1,2) nao reproduz o ciclo anual: perde para a linha de base.

# SARIMA: acrescenta a parte sazonal (periodo 12)
sarima = ARIMA(treino, order=(1, 1, 2), seasonal_order=(0, 1, 1, 12)).fit()
previsao_s = sarima.get_forecast(steps=horizonte)
sarima_prev = previsao_s.predicted_mean
intervalo_s = previsao_s.conf_int()
print('SARIMA(1,1,2)(0,1,1,12)    MAE =', round(mae(teste, sarima_prev)))

fig, eixo = plt.subplots(figsize=(9, 4.2))
eixo.plot(treino.index[-48:], treino.iloc[-48:], color='#2F648F', label='treino (últimos 4 anos)')
eixo.plot(teste.index, teste, color='#20324A', linewidth=2.2, label='teste (real)')
eixo.plot(teste.index, sazonal, color='#8794A3', linestyle='--', label=f'sazonal ingênua (MAE {mae(teste, sazonal):.0f})')
eixo.plot(teste.index, arima_112, color='#D69A35', label=f'ARIMA(1,1,2) (MAE {mae(teste, arima_112):.0f})')
eixo.plot(teste.index, sarima_prev, color='#168A8A', label=f'SARIMA (MAE {mae(teste, sarima_prev):.0f})')
eixo.fill_between(teste.index, intervalo_s.iloc[:, 0], intervalo_s.iloc[:, 1], color='#168A8A', alpha=0.12,
                  label='SARIMA: intervalo de 95%')
eixo.set_ylabel('Pares de vendas no mês')
eixo.set_title('Sem a parte sazonal, o ARIMA perde para "repetir o ano passado"')
eixo.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=9)
plt.savefig(os.path.join(pasta, 'figuras', 'arima_vs_linha_de_base.png'))
plt.show()

# Residuos do SARIMA no treino: devem parecer ruido (sem padrao)
residuos = sarima.resid[13:]        # os primeiros valores sao afetados pelas diferencas
fig, (esq, dir) = plt.subplots(1, 2, figsize=(10, 3.4))
esq.plot(residuos.index, residuos, color='#8794A3', linewidth=1)
esq.axhline(0, color='#20324A', linewidth=0.8)
esq.set_title('Resíduos do SARIMA ao longo do tempo')
dir.hist(residuos, bins=30, color='#2F648F')
dir.set_title('Distribuição dos resíduos')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'residuos_sarima.png'))
plt.show()

# Experimente: troque seasonal_order por (1, 1, 1, 12) ou order por (2, 1, 1). O MAE no teste melhora?
# Cuidado: escolher a ordem olhando o teste e usar o teste para treinar. O script 08 mostra a alternativa.
