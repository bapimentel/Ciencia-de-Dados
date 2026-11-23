# Estudo de caso 1 - Reclamacoes por perdas (TSA). Etapa 4: valores recebidos (livro, secao 11.4).
# Pergunta: quando ha pagamento, quanto se paga? O valor depende do tipo de item, do local, do desfecho?
# Reproduz descrever_todos/descrever_filtro e predizer_CloseAmount de leitura.py, com a linha de base
# que faltava (prever a mediana) e separacao com semente fixa.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'))

# Negadas tem valor zero por definicao. O interesse e o valor pago nas aprovadas e nos acordos.
pagas = dados[dados['Close Amount'] > 0].copy()
print('Reclamacoes com pagamento:', len(pagas), 'de', len(dados))
print('\nDistribuicao do valor pago (todas):')
print(pagas['Close Amount'].describe().round(1))
print('\nPor desfecho:')
print(pagas.groupby('Disposition')['Close Amount'].describe().round(1))
# Cauda longa: a mediana (cerca de 100) e muito menor que a media; poucos casos passam de mil.

# As figuras originais cortavam em 300 para ver o grosso da distribuicao. Mantemos o corte e dizemos quanto fica de fora.
corte = 300
print(f'\nAcima de {corte}: {(pagas["Close Amount"] > corte).sum()} casos ({(pagas["Close Amount"] > corte).mean():.1%})')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
esq.hist(pagas['Close Amount'], bins=60, color='#2F648F')
esq.set_xlabel('Valor pago (US$)')
esq.set_ylabel('Reclamações')
esq.set_title(f'Cauda longa: mediana {pagas["Close Amount"].median():.0f}, máximo {pagas["Close Amount"].max():.0f}')
ate_corte = pagas[pagas['Close Amount'] <= corte]
grupos = [ate_corte.loc[ate_corte['Disposition'] == d, 'Close Amount'] for d in ['Approve in Full', 'Settle']]
dir.boxplot(grupos, tick_labels=[f'Aprovada integral\n(n={len(grupos[0])})', f'Acordo\n(n={len(grupos[1])})'], orientation='horizontal',
            medianprops=dict(color='#D69A35', linewidth=2))
dir.set_xlabel(f'Valor pago (US$), só casos até {corte}')
dir.set_title('Acordos pagam mais que aprovações integrais')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '04_distribuicao_valores.png'))
plt.show()

# Mediana por categoria de item e por local
print('\nMediana do valor pago por categoria de item (n >= 20):')
por_item = pagas.groupby('Item Category (agrupada)')['Close Amount'].agg(['count', 'median', 'mean'])
print(por_item[por_item['count'] >= 20].sort_values('median').round(1))
print('\nMediana por local:')
print(pagas.groupby('Claim Site')['Close Amount'].agg(['count', 'median']).round(1))

# --- Prever o valor pago: o original usava floresta aleatoria nos casos < 300, sem linha de base
alvo = pagas[pagas['Close Amount'] < corte]
variaveis = ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)', 'Disposition', 'Dias ate registrar']
X = pd.get_dummies(alvo[variaveis], dtype=int)
y = alvo['Close Amount']
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

mediana_treino = y_tr.median()
mae_base = mean_absolute_error(y_te, np.full(len(y_te), mediana_treino))
floresta = RandomForestRegressor(n_estimators=300, min_samples_leaf=5, random_state=0).fit(X_tr, y_tr)
mae_floresta = mean_absolute_error(y_te, floresta.predict(X_te))
print(f'\nPrever o valor (casos < {corte}): MAE da linha de base (mediana = {mediana_treino:.0f}) = {mae_base:.1f}'
      f' | MAE da floresta = {mae_floresta:.1f}')
# O ganho sobre a mediana e pequeno: as variaveis registradas explicam pouco do valor pago.

importancia = pd.Series(floresta.feature_importances_, index=X.columns).sort_values().tail(10)
fig, eixo = plt.subplots(figsize=(8, 4))
eixo.barh(importancia.index, importancia.values, color='#8794A3')
eixo.set_xlabel('Importância na floresta')
eixo.set_title(f'Prever o valor pago: erro médio de {mae_floresta:.0f} contra {mae_base:.0f} da mediana')
eixo.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '04_importancia_valor.png'))
plt.show()
