# Regressao linear multipla: varias variaveis explicativas ao mesmo tempo.
# beta = (X'X)^(-1) X'y calculado a mao com numpy, conferido com statsmodels, e avaliado em dados futuros.
# Dados: dados/bicicletas_dia.csv (2011-2012).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
dias = pd.read_csv(os.path.join(pasta, '..', 'dados', 'bicicletas_dia.csv'), parse_dates=['dteday'])
dias['temperatura'] = dias['temp'] * 47 - 8
dias['umidade'] = dias['hum'] * 100
dias['vento'] = dias['windspeed'] * 67
dias['dia_util'] = dias['workingday']
dias['ano_2012'] = dias['yr']
dias['chuva'] = (dias['weathersit'] == 3).astype(int)
variaveis = ['temperatura', 'umidade', 'vento', 'dia_util', 'ano_2012', 'chuva']

# Treino: ate setembro de 2012; teste: outubro a dezembro de 2012 (o futuro)
treino = dias[dias['dteday'] < '2012-10-01']
teste = dias[dias['dteday'] >= '2012-10-01']

# --- A mao: X com uma coluna de 1 (intercepto) e as variaveis; beta = (X'X)^-1 X'y
X = np.column_stack([np.ones(len(treino)), treino[variaveis].values])
y = treino['cnt'].values
beta = np.linalg.inv(X.T @ X) @ X.T @ y
print('Coeficientes a mao:')
for nome, b in zip(['intercepto'] + variaveis, beta):
    print(f'  {nome:12s} {b:9.1f}')

# --- statsmodels: mesmos coeficientes, com erro-padrao, IC e valor-p
modelo = sm.OLS(y, sm.add_constant(treino[variaveis])).fit()
print(modelo.summary().tables[1])
print(f'R2 no treino: {modelo.rsquared:.3f}')
# Leitura de um coeficiente: "mantidas as demais variaveis fixas, um dia de chuva tem em media
# cerca de 1 100 alugueis a menos". E uma associacao condicional, nao um efeito causal garantido.
# 'dia_util' tem p = 0,32: com temperatura, umidade, vento e ano no modelo, nao ha evidencia de diferenca
# no TOTAL diario entre dias uteis e nao uteis (o que muda e a distribuicao ao longo do dia).

# --- Avaliacao no futuro: o modelo preve bem outubro a dezembro?
previsto = modelo.predict(sm.add_constant(teste[variaveis], has_constant='add'))
mae = np.mean(np.abs(teste['cnt'] - previsto))
mae_base = np.mean(np.abs(teste['cnt'] - treino[treino['dteday'] >= '2012-07-01']['cnt'].mean()))
print(f'\nMAE no teste (out-dez 2012): {mae:.0f} alugueis | linha de base (media de jul-set): {mae_base:.0f}')

# --- Multicolinearidade: temperatura e sensacao termica ('atemp') medem quase a mesma coisa
print(f"\nCorrelacao temperatura x sensacao termica: {dias['temp'].corr(dias['atemp']):.3f}")
for colunas in [['temperatura'], ['temperatura', 'atemp']]:
    m = sm.OLS(y, sm.add_constant(treino[colunas])).fit()
    print(f'  com {colunas}: coef. temperatura = {m.params["temperatura"]:.0f} (erro-padrao {m.bse["temperatura"]:.0f})')
# Com as duas juntas, o coeficiente da temperatura muda muito e o erro-padrao explode: o modelo nao
# consegue separar o efeito de duas variaveis que andam juntas. (X'X quase nao tem inversa.)

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.4), gridspec_kw={'width_ratios': [1, 1.4]})
coef = modelo.params.drop('const')
ic = modelo.conf_int().drop('const')
# coeficientes em unidades diferentes: mostramos o efeito de uma mudanca TIPICA (1 desvio-padrao; 0->1 nas binarias)
escala = pd.Series({v: (treino[v].std() if treino[v].nunique() > 2 else 1) for v in variaveis})
efeito = coef * escala
erro = (ic[1] - ic[0]) / 2 * escala
ordem = efeito.sort_values().index
esq.barh(ordem, efeito[ordem], xerr=erro[ordem], color=['#BD5B58' if v < 0 else '#2F648F' for v in efeito[ordem]], capsize=4)
esq.axvline(0, color='#20324A', linewidth=0.8)
esq.set_xlabel('Aluguéis a mais por dia (IC 95%)')
esq.set_title('Efeito de uma mudança típica,\nmantendo as demais fixas', fontsize=11)
esq.grid(axis='y', visible=False)
dir.plot(teste['dteday'], teste['cnt'], color='#20324A', linewidth=1.8, label='real')
dir.plot(teste['dteday'], previsto, color='#168A8A', linewidth=1.5, label=f'regressão múltipla (MAE {mae:.0f})')
dir.set_ylabel('Aluguéis no dia')
dir.set_title('Previsão para out–dez de 2012 (dados que o modelo não viu)', fontsize=11)
dir.legend(fontsize=9)
dir.tick_params(axis='x', labelrotation=30)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'regressao_multipla.png'))
plt.show()
