# Aplicacao adicional - Bicicletas compartilhadas. Passo 5: a previsao funciona em outros periodos, e com
# a previsao do tempo em vez do clima observado?
# (a) Origem movel: repetimos a avaliacao nos quatro trimestres de 2012, sempre treinando com tudo o que veio antes.
# (b) Clima previsto: na pratica o modelo receberia a previsao do tempo, que erra. Simulamos isso somando um erro
#     de temperatura (desvio de 2 C, 3 C) e trocando a condicao do tempo em 20% dos dias.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
dias = pd.read_csv(os.path.join(pasta, 'dados', 'day.csv'), parse_dates=['dteday']).set_index('dteday')
dias['temp_C'] = dias['temp'] * 47 - 8
dias['media_7d'] = dias['cnt'].shift(1).rolling(7).mean()
dias = dias.dropna()
variaveis = ['yr', 'mnth', 'weekday', 'workingday', 'holiday', 'season', 'temp_C', 'hum', 'windspeed', 'weathersit', 'media_7d']


def mae(a, b):
    return float(np.mean(np.abs(np.asarray(a) - np.asarray(b))))


linhas = []
for inicio in ['2012-01-01', '2012-04-01', '2012-07-01', '2012-10-01']:
    ini = pd.Timestamp(inicio)
    fim = ini + pd.DateOffset(months=3)
    treino, teste = dias[dias.index < ini], dias[(dias.index >= ini) & (dias.index < fim)]
    modelo = LinearRegression().fit(treino[variaveis], treino['cnt'])
    linhas.append({'trimestre': f'{ini:%Y}-T{(ini.month - 1) // 3 + 1}', 'media do trimestre': teste['cnt'].mean(),
                   'linha de base (media 7 dias)': mae(teste['cnt'], teste['media_7d']),
                   'modelo (calendario + clima + media 7d)': mae(teste['cnt'], modelo.predict(teste[variaveis]))})
tabela = pd.DataFrame(linhas).set_index('trimestre')
tabela['reducao do erro'] = 1 - tabela['modelo (calendario + clima + media 7d)'] / tabela['linha de base (media 7 dias)']
print('Origem movel (treino = tudo antes do trimestre):')
print(tabela.round(2).to_string())

# (b) Clima com erro, no ultimo trimestre
ini = pd.Timestamp('2012-10-01')
treino, teste = dias[dias.index < ini], dias[dias.index >= ini]
modelo = LinearRegression().fit(treino[variaveis], treino['cnt'])
gerador = np.random.default_rng(0)
print('\nUltimo trimestre de 2012, com clima "previsto" (media de 200 simulacoes):')
cenarios = {}
for desvio in [0, 2, 3]:
    erros = []
    for _ in range(200):
        t = teste.copy()
        t['temp_C'] = t['temp_C'] + gerador.normal(0, desvio, len(t))
        if desvio > 0:
            trocar = gerador.random(len(t)) < 0.2
            t.loc[trocar, 'weathersit'] = gerador.choice([1, 2, 3], trocar.sum())
        erros.append(mae(t['cnt'], modelo.predict(t[variaveis])))
    cenarios[desvio] = np.mean(erros)
    print(f'  erro de temperatura com desvio {desvio} C: MAE = {cenarios[desvio]:.0f} '
          f'({cenarios[desvio] / teste["cnt"].mean():.0%} da media) | linha de base: {mae(teste["cnt"], teste["media_7d"]):.0f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.2))
x = np.arange(len(tabela))
esq.bar(x - 0.2, tabela['linha de base (media 7 dias)'], width=0.4, color='#8794A3', label='média dos 7 dias anteriores')
esq.bar(x + 0.2, tabela['modelo (calendario + clima + media 7d)'], width=0.4, color='#2F648F', label='modelo linear')
esq.set_xticks(x, tabela.index)
esq.set_ylabel('Erro médio (aluguéis por dia)')
esq.set_title('Origem móvel: o modelo ganha em 3 de 4 trimestres', fontsize=11)
esq.legend()
dir.bar([f'clima observado', 'previsão com\nerro de 2 °C', 'previsão com\nerro de 3 °C'], list(cenarios.values()),
        color=['#2F648F', '#7A9CC6', '#C9D3DD'])
dir.axhline(mae(teste['cnt'], teste['media_7d']), color='#8794A3', linestyle='--')
dir.text(2.45, mae(teste['cnt'], teste['media_7d']) + 20, 'linha de base', color='#8794A3', ha='right')
dir.set_ylabel('Erro médio (aluguéis por dia)')
dir.set_title('4º trimestre de 2012: com clima previsto, o ganho encolhe', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '05_validar_a_previsao.png'))
plt.show()
