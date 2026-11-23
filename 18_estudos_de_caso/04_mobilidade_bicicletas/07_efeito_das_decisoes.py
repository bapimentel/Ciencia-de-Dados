# Aplicacao adicional - Bicicletas compartilhadas. Passo 7: qual o efeito medido das duas decisoes?
# (a) Janela de manutencao 3h-5h: quantos alugueis acontecem na janela (os unicos que a manutencao pode afetar),
#     comparada com outras janelas de 3 horas. Medido em 2012, o ano mais recente.
# (b) Dimensionar a equipe do dia pela previsao: em cada trimestre de 2012, com o modelo treinado em tudo o que
#     veio antes (origem movel), quantos dias a demanda superou o planejado em mais de 20% (equipe subdimensionada)
#     e quantos ficou mais de 20% abaixo (equipe ociosa), contra a regra atual (media dos 7 dias anteriores).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
horas = pd.read_csv(os.path.join(pasta, 'dados', 'hour.csv'), parse_dates=['dteday'])
h2012 = horas[horas['yr'] == 1]

# (a) Janelas de 3 horas: participacao no uso de 2012 e maximo por hora
total = h2012['cnt'].sum()
janelas = {}
for inicio in range(0, 22):
    sel = h2012['hr'].between(inicio, inicio + 2)
    janelas[inicio] = (h2012.loc[sel, 'cnt'].sum() / total, h2012.loc[sel, 'cnt'].max())
janelas = pd.DataFrame(janelas, index=['participacao', 'maximo por hora']).T
print('Janelas de 3 horas em 2012 (todas os dias):')
print(janelas.sort_values('participacao').head(5).assign(participacao=lambda d: (100 * d['participacao']).round(2)).to_string())
j = janelas.loc[3]
print(f'Janela 3h-5h: {j["participacao"]:.2%} dos alugueis de 2012 ({int(h2012.loc[h2012["hr"].between(3, 5), "cnt"].sum())} de {total}); '
      f'maximo de {int(j["maximo por hora"])} alugueis numa hora, contra {h2012["cnt"].max()} no pico do ano')
pico = janelas['participacao'].idxmax()
print(f'Janela de 3 horas mais movimentada: {pico}h-{pico + 2}h, {janelas.loc[pico, "participacao"]:.1%} dos alugueis')

# (b) Dimensionamento diario pela previsao
dias = pd.read_csv(os.path.join(pasta, 'dados', 'day.csv'), parse_dates=['dteday']).set_index('dteday')
dias['temp_C'] = dias['temp'] * 47 - 8
dias['media_7d'] = dias['cnt'].shift(1).rolling(7).mean()
dias = dias.dropna()
variaveis = ['yr', 'mnth', 'weekday', 'workingday', 'holiday', 'season', 'temp_C', 'hum', 'windspeed', 'weathersit', 'media_7d']
linhas = []
for inicio in ['2012-01-01', '2012-04-01', '2012-07-01', '2012-10-01']:
    ini = pd.Timestamp(inicio)
    fim = ini + pd.DateOffset(months=3)
    treino, teste = dias[dias.index < ini], dias[(dias.index >= ini) & (dias.index < fim)]
    previsto = LinearRegression().fit(treino[variaveis], treino['cnt']).predict(teste[variaveis])
    for nome, plano in [('media dos 7 dias anteriores', teste['media_7d'].values), ('modelo', previsto)]:
        razao = teste['cnt'].values / plano
        linhas.append({'trimestre': f'{ini:%Y}-T{(ini.month - 1) // 3 + 1}', 'plano': nome, 'dias': len(teste),
                       'subdimensionado (>20%)': int((razao > 1.2).sum()), 'ocioso (>20%)': int((razao < 0.8).sum())})
tabela = pd.DataFrame(linhas)
tabela['dias fora da faixa de 20%'] = tabela['subdimensionado (>20%)'] + tabela['ocioso (>20%)']
print('\n' + tabela.to_string(index=False))
t234 = tabela[tabela['trimestre'] != '2012-T1'].groupby('plano')[['dias', 'subdimensionado (>20%)', 'ocioso (>20%)', 'dias fora da faixa de 20%']].sum()
print('\nT2 a T4 de 2012 (com pelo menos um ano de historico no treino):')
print(t234.to_string())
todos = tabela.groupby('plano')[['dias', 'dias fora da faixa de 20%']].sum()
print('\nOs quatro trimestres:')
print(todos.to_string())

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.3))
esq.bar(janelas.index, 100 * janelas['participacao'], color=['#D69A35' if i == 3 else '#8794A3' for i in janelas.index])
esq.set_xticks(range(0, 22, 2))
esq.set_xlabel('Hora de início da janela de 3 horas')
esq.set_ylabel('% dos aluguéis de 2012')
esq.set_title(f'Janela 3h–5h: {j["participacao"]:.1%} dos aluguéis do ano', fontsize=11)
x = np.arange(4)
for k, (nome, cor) in enumerate([('media dos 7 dias anteriores', '#8794A3'), ('modelo', '#2F648F')]):
    t = tabela[tabela['plano'] == nome]
    dir.bar(x + (k - 0.5) * 0.4, t['dias fora da faixa de 20%'], width=0.4, color=cor,
            label='média dos 7 dias anteriores' if k == 0 else 'previsão do modelo')
dir.set_xticks(x, tabela['trimestre'].unique())
dir.set_ylabel('Dias com demanda 20% acima ou abaixo do planejado')
dir.set_title('Dias em que a equipe planejada não bate com a demanda', fontsize=11)
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '07_efeito_das_decisoes.png'))
plt.show()
