# Estudo de caso 1 - Reclamacoes por perdas (TSA). Passo 5: quando ha pagamento, quanto se paga?
# Descricao da distribuicao (cauda longa), comparacao por desfecho e por categoria com intervalos bootstrap
# para a mediana, e um modelo de valor comparado com a linha de base "prever a mediana".

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'))
gerador = np.random.default_rng(0)

pagas = dados[dados['Close Amount'] > 0].copy()
print('Reclamacoes com pagamento:', len(pagas), 'de', len(dados))
print('Casos nao negados com valor zero:', ((dados['Negada'] == 0) & (dados['Close Amount'] == 0)).sum())
print('\nValor pago (US$):')
print(pagas['Close Amount'].describe().round(1).to_string())
q = pagas['Close Amount'].quantile([0.5, 0.75, 0.9, 0.99])
print('Quantis 50/75/90/99%:', q.round(0).tolist())
total = pagas['Close Amount'].sum()
maiores = pagas['Close Amount'].nlargest(int(0.1 * len(pagas))).sum()
print(f'Os 10% maiores pagamentos somam {maiores / total:.0%} do total pago (US$ {total:,.0f})')


def ic_mediana(valores, reps=2000):
    medianas = [np.median(gerador.choice(valores, len(valores))) for _ in range(reps)]
    return np.percentile(medianas, [2.5, 97.5])


aprovadas = pagas.loc[pagas['Disposition'] == 'Approve in Full', 'Close Amount']
acordos = pagas.loc[pagas['Disposition'] == 'Settle', 'Close Amount']
teste = mannwhitneyu(aprovadas, acordos)
print(f'\nMediana aprovada integral: {aprovadas.median():.0f} (IC95% {ic_mediana(aprovadas.values).round(0)}) | '
      f'acordo: {acordos.median():.0f} (IC95% {ic_mediana(acordos.values).round(0)}) | Mann-Whitney p = {teste.pvalue:.1g}')

por_item = pagas.groupby('Item Category (agrupada)')['Close Amount'].agg(['count', 'median'])
por_item = por_item[por_item['count'] >= 20].sort_values('median')
ics = np.array([ic_mediana(pagas.loc[pagas['Item Category (agrupada)'] == c, 'Close Amount'].values) for c in por_item.index])
por_item['ic_inf'], por_item['ic_sup'] = ics[:, 0], ics[:, 1]
print('\nMediana por categoria de item (n >= 20), com IC 95% bootstrap:')
print(por_item.round(0).to_string())

fig, eixos = plt.subplots(1, 3, figsize=(16, 4.6), gridspec_kw={'width_ratios': [1, 1, 1.3]})
eixos[0].hist(np.log10(pagas['Close Amount']), bins=40, color='#2F648F')
eixos[0].set_xticks([0, 1, 2, 3], ['1', '10', '100', '1 000'])
eixos[0].set_xlabel('Valor pago (US$, escala log)')
eixos[0].set_ylabel('Reclamações')
eixos[0].set_title(f'Mediana {pagas["Close Amount"].median():.0f}, média {pagas["Close Amount"].mean():.0f}, '
                   f'máx. {pagas["Close Amount"].max():.0f}', fontsize=11)
eixos[1].boxplot([np.log10(aprovadas), np.log10(acordos)], tick_labels=[f'Aprovada integral\n(n={len(aprovadas)})', f'Acordo\n(n={len(acordos)})'],
                 medianprops={'color': '#D69A35', 'linewidth': 2})
eixos[1].set_yticks([0, 1, 2, 3], ['1', '10', '100', '1 000'])
eixos[1].set_ylabel('Valor pago (US$, escala log)')
eixos[1].set_title('Acordos pagam mais que aprovações integrais', fontsize=11)
eixos[2].errorbar(por_item['median'], range(len(por_item)), xerr=[por_item['median'] - por_item['ic_inf'], por_item['ic_sup'] - por_item['median']],
                  fmt='o', color='#2F648F', ecolor='#8794A3', capsize=3)
eixos[2].set_yticks(range(len(por_item)), [f'{c[:30]} (n={n})' for c, n in zip(por_item.index, por_item['count'])], fontsize=9)
eixos[2].set_xscale('log')
eixos[2].set_xticks([10, 30, 100, 300], ['10', '30', '100', '300'])
eixos[2].minorticks_off()
eixos[2].set_xlabel('Mediana do valor pago (US$, log) e IC 95%')
eixos[2].set_title('Por categoria de item', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '05_valores_pagos.png'))
plt.show()

# Prever o valor pago. Como a cauda e longa, o modelo e treinado no log do valor e avaliado em US$.
variaveis = ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)', 'Disposition', 'Dias ate registrar']
X = pd.get_dummies(pagas[variaveis], dtype=int)
y = pagas['Close Amount']
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
mae_base = mean_absolute_error(y_te, np.full(len(y_te), y_tr.median()))
floresta = RandomForestRegressor(n_estimators=300, min_samples_leaf=5, random_state=0).fit(X_tr, np.log(y_tr))
mae_floresta = mean_absolute_error(y_te, np.exp(floresta.predict(X_te)))
print(f'\nPrever o valor pago: MAE da mediana do treino ({y_tr.median():.0f}) = {mae_base:.0f} | MAE da floresta = {mae_floresta:.0f}')
print(f'Reducao do erro: {1 - mae_floresta / mae_base:.0%}')
