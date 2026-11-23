# Aplicacao adicional - Bicicletas compartilhadas. Passo 4: prever a demanda diaria.
# Pergunta: com calendario e clima, e possivel prever os alugueis do dia melhor que repetir a semana anterior?
# Separacao cronologica: treino ate 30/09/2012, teste = outubro a dezembro de 2012 (92 dias).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

dias = pd.read_csv(os.path.join(pasta, 'dados', 'day.csv'), parse_dates=['dteday']).set_index('dteday')
dias['temp_C'] = dias['temp'] * 47 - 8
# Defasagens: o que se sabia no dia anterior e uma semana antes
dias['cnt_ontem'] = dias['cnt'].shift(1)
dias['cnt_semana_passada'] = dias['cnt'].shift(7)
dias['media_7d'] = dias['cnt'].shift(1).rolling(7).mean()
dias = dias.dropna()

corte = pd.Timestamp('2012-10-01')
treino, teste = dias[dias.index < corte], dias[dias.index >= corte]
print('Treino:', len(treino), 'dias | teste:', len(teste), 'dias')

def mae(real, previsto):
    return float(np.mean(np.abs(np.asarray(real) - np.asarray(previsto))))

# Linhas de base
base_semana = teste['cnt_semana_passada']
base_media7 = teste['media_7d']
print(f'\nMesmo dia da semana passada:       MAE = {mae(teste["cnt"], base_semana):.0f}')
print(f'Media dos 7 dias anteriores:       MAE = {mae(teste["cnt"], base_media7):.0f}')

# Modelos com calendario + clima (clima OBSERVADO no dia; na pratica seria a previsao do tempo)
calendario = ['yr', 'mnth', 'weekday', 'workingday', 'holiday', 'season']
clima = ['temp_C', 'hum', 'windspeed', 'weathersit']
defasagens = ['cnt_ontem', 'cnt_semana_passada', 'media_7d']

conjuntos = {
    'linear: calendario + clima': (LinearRegression(), calendario + clima),
    'floresta: calendario + clima': (RandomForestRegressor(n_estimators=400, min_samples_leaf=3, random_state=0), calendario + clima),
    'floresta: + defasagens': (RandomForestRegressor(n_estimators=400, min_samples_leaf=3, random_state=0), calendario + clima + defasagens),
}
previsoes = {}
for nome, (modelo, variaveis) in conjuntos.items():
    modelo.fit(treino[variaveis], treino['cnt'])
    previsoes[nome] = pd.Series(modelo.predict(teste[variaveis]), index=teste.index)
    print(f'{nome:32s} MAE = {mae(teste["cnt"], previsoes[nome]):.0f}')

melhor = 'floresta: + defasagens'
importancia = pd.Series(conjuntos[melhor][0].feature_importances_, index=conjuntos[melhor][1]).sort_values()
print('\nImportancia das variaveis (floresta com defasagens):')
print(importancia.round(3).to_string())

fig, eixo = plt.subplots(figsize=(10, 4.2))
eixo.plot(teste.index, teste['cnt'], color='#20324A', linewidth=2, label='real')
eixo.plot(teste.index, base_semana, color='#8794A3', linestyle='--', label=f'semana passada (MAE {mae(teste["cnt"], base_semana):.0f})')
eixo.plot(teste.index, previsoes['floresta: calendario + clima'], color='#D69A35', linewidth=1.2,
          label=f'floresta: calendário + clima (MAE {mae(teste["cnt"], previsoes["floresta: calendario + clima"]):.0f})')
eixo.plot(teste.index, previsoes[melhor], color='#168A8A', linewidth=1.5, label=f'floresta + defasagens (MAE {mae(teste["cnt"], previsoes[melhor]):.0f})')
eixo.set_ylabel('Aluguéis por dia')
eixo.set_title('Outubro a dezembro de 2012: clima e defasagens reduzem o erro para ~950 por dia; dias atípicos escapam')
eixo.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2, fontsize=9)
sandy = pd.Timestamp('2012-10-29')
eixo.annotate('Sandy', xy=(sandy, teste.loc[sandy, 'cnt']), xytext=(0, -35), textcoords='offset points', ha='center', color='#BD5B58',
              arrowprops=dict(arrowstyle='-', color='#BD5B58'))
plt.savefig(os.path.join(pasta, 'figuras', '04_previsao_trimestre.png'))
plt.show()

# Leitura: o erro cai de ~1460 (mesmo dia da semana passada) para ~960 com clima, calendario e defasagens,
# num trimestre com media de ~5200 alugueis/dia (erro de ~18%). O modelo linear e a floresta empatam:
# a relacao com temperatura e quase linear. Dias de evento (Sandy, feriados) continuam errados.
# Para uso real, o clima teria de vir da previsao meteorologica, que tambem erra; o MAE aqui e otimista.
print(f'\nMedia de alugueis no teste: {teste["cnt"].mean():.0f}/dia')
