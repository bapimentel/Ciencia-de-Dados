# Estudo de caso 2 - Energia domestica. Passo 5: prever o consumo diario.
# Pergunta: o historico permite prever os proximos dias melhor que uma regra simples?
# Separacao cronologica, duas linhas de base, SARIMA semanal e floresta com defasagens.
# (O custo NAO entra como variavel de entrada: ele e o proprio consumo vezes a tarifa.)

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor

warnings.filterwarnings('ignore')
pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

diario = pd.read_csv(os.path.join(pasta, 'dados', 'energia_por_dia.csv'), index_col=0, parse_dates=True)['Consumo_kWh'].asfreq('D')
print('Dias:', len(diario), '| de', diario.index.min().date(), 'a', diario.index.max().date())

# Teste = ultimos 60 dias; treino = o resto
horizonte = 60
treino, teste = diario[:-horizonte], diario[-horizonte:]

def mae(real, previsto):
    return float(np.mean(np.abs(np.asarray(real) - np.asarray(previsto))))

# Linha de base 1: repetir a ultima semana (sazonal ingenua, periodo 7)
ultima_semana = treino.iloc[-7:].values
base_semana = pd.Series(np.tile(ultima_semana, horizonte // 7 + 1)[:horizonte], index=teste.index)
# Linha de base 2: media das ultimas 4 semanas, mesmo dia da semana
ultimas4 = treino.iloc[-28:]
media_dia = ultimas4.groupby(ultimas4.index.day_of_week).mean()
base_4sem = pd.Series([media_dia[d] for d in teste.index.day_of_week], index=teste.index)
print(f'\nRepetir a ultima semana:         MAE = {mae(teste, base_semana):.2f} kWh')
print(f'Media das 4 ultimas semanas:     MAE = {mae(teste, base_4sem):.2f} kWh')

# SARIMA com sazonalidade semanal
sarima = ARIMA(treino, order=(1, 0, 1), seasonal_order=(1, 0, 1, 7)).fit()
prev_sarima = sarima.get_forecast(steps=horizonte)
sarima_media = prev_sarima.predicted_mean
intervalo = prev_sarima.conf_int()
print(f'SARIMA (1,0,1)(1,0,1,7):          MAE = {mae(teste, sarima_media):.2f} kWh')

# Floresta com defasagens: o que se sabia ate o dia anterior + calendario
def montar_tabela(serie):
    tabela = pd.DataFrame({'y': serie})
    for d in [1, 2, 7, 14]:
        tabela[f'lag{d}'] = serie.shift(d)
    tabela['media7'] = serie.shift(1).rolling(7).mean()
    tabela['dia_semana'] = serie.index.day_of_week
    tabela['mes'] = serie.index.month
    return tabela.dropna()

tabela = montar_tabela(diario)
tab_treino = tabela[tabela.index < teste.index[0]]
tab_teste = tabela[tabela.index >= teste.index[0]]
variaveis = [c for c in tabela.columns if c != 'y']
floresta = RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=0).fit(tab_treino[variaveis], tab_treino['y'])
prev_floresta = pd.Series(floresta.predict(tab_teste[variaveis]), index=tab_teste.index)
print(f'Floresta com defasagens (1 dia a frente): MAE = {mae(tab_teste["y"], prev_floresta):.2f} kWh')
# Atencao: a floresta preve um dia a frente usando o dia anterior REAL (tarefa mais facil);
# o SARIMA e as linhas de base preveem os 60 dias de uma vez. Compare com esse cuidado.

fig, eixo = plt.subplots(figsize=(10, 4.2))
eixo.plot(treino.index[-90:], treino.iloc[-90:], color='#2F648F', linewidth=1.2, label='treino (últimos 90 dias)')
eixo.plot(teste.index, teste, color='#20324A', linewidth=2, label='teste (real)')
eixo.plot(teste.index, base_4sem, color='#8794A3', linestyle='--', label=f'média das 4 últimas semanas (MAE {mae(teste, base_4sem):.1f})')
eixo.plot(teste.index, sarima_media, color='#168A8A', label=f'SARIMA semanal (MAE {mae(teste, sarima_media):.1f})')
eixo.fill_between(teste.index, intervalo.iloc[:, 0].clip(lower=0), intervalo.iloc[:, 1], color='#168A8A', alpha=0.12)
eixo.plot(prev_floresta.index, prev_floresta, color='#D69A35', linewidth=1.2, label=f'floresta, 1 dia à frente (MAE {mae(tab_teste["y"], prev_floresta):.1f})')
eixo.set_ylabel('kWh por dia')
eixo.set_title('Prever 60 dias: a média das 4 últimas semanas erra 2,4 kWh por dia (30% do consumo médio)')
eixo.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize=9)
plt.savefig(os.path.join(pasta, 'figuras', '05_previsao_60_dias.png'))
plt.show()

print(f'\nPara dar escala: consumo medio diario no teste = {teste.mean():.1f} kWh; desvio = {teste.std():.1f} kWh')
# O erro das previsoes e da ordem do desvio diario: o consumo desta casa varia muito de um dia para o outro
# por razoes que a base nao registra (temperatura, presenca, aparelhos). Prever a media semanal e mais
# razoavel que prever cada dia.
