# Estudo de caso 1 - Reclamacoes por perdas (TSA). Etapa 3: analise dos desfechos (livro, secao 11.3).
# Pergunta: em que situacoes as reclamacoes sao negadas? Um modelo consegue antecipar o desfecho?
# Reproduz predizer_Disposition_clf de leitura.py (negada x nao negada; regressao logistica,
# arvore e floresta), com separacao estratificada e semente fixa, linha de base e metricas por classe.

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, roc_auc_score, confusion_matrix

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'))
print('Registros:', len(dados), '| negadas:', dados['Negada'].sum(), f'({dados["Negada"].mean():.1%})')

# --- Descricao: taxa de negativa por categoria
for coluna in ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)']:
    tabela = dados.groupby(coluna)['Negada'].agg(['count', 'mean']).rename(columns={'count': 'n', 'mean': 'taxa de negativa'})
    tabela = tabela[tabela['n'] >= 30].sort_values('taxa de negativa')
    print(f'\nTaxa de negativa por {coluna} (grupos com n >= 30):')
    print(tabela.round(3))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
por_local = dados.groupby('Claim Site')['Negada'].agg(['count', 'mean'])
por_local = por_local[por_local['count'] >= 30].sort_values('mean')
esq.barh([f'{i} (n={n})' for i, n in zip(por_local.index, por_local['count'])], 100 * por_local['mean'], color='#2F648F')
esq.set_xlabel('% de reclamações negadas')
esq.set_title('Reclamações na inspeção são negadas com mais frequência')
esq.set_xlim(0, 100)
esq.grid(axis='y', visible=False)
por_item = dados.groupby('Item Category (agrupada)')['Negada'].agg(['count', 'mean']).sort_values('mean')
dir.barh([f'{i} (n={n})' for i, n in zip(por_item.index, por_item['count'])], 100 * por_item['mean'], color='#8794A3')
dir.set_xlabel('% de reclamações negadas')
dir.set_title('Por categoria de item, a variação é grande')
dir.set_xlim(0, 100)
dir.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_taxa_negativa_por_grupo.png'))
plt.show()

# --- Predicao: negada (1) x nao negada (0), com o que se sabe no momento do registro
variaveis = ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)', 'Dias ate registrar', 'Mes']
X = pd.get_dummies(dados[variaveis], dtype=int)
y = dados['Negada']
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
print('\nTreino:', len(X_tr), '| teste:', len(X_te), '| variaveis apos one-hot:', X.shape[1])

modelos = {
    'linha de base (classe mais comum)': DummyClassifier(strategy='most_frequent'),
    'regressao logistica': LogisticRegression(max_iter=2000),
    'arvore de decisao (prof. 6)': DecisionTreeClassifier(max_depth=6, random_state=0),
    'floresta aleatoria': RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0),
}
resultados = []
for nome, modelo in modelos.items():
    modelo.fit(X_tr, y_tr)
    previsto = modelo.predict(X_te)
    prob = modelo.predict_proba(X_te)[:, 1] if hasattr(modelo, 'predict_proba') else previsto
    resultados.append({
        'modelo': nome,
        'acuracia': accuracy_score(y_te, previsto),
        'revocacao (negadas)': recall_score(y_te, previsto, zero_division=0),
        'precisao (negadas)': precision_score(y_te, previsto, zero_division=0),
        'AUC': roc_auc_score(y_te, prob) if nome.startswith(('regressao', 'arvore', 'floresta')) else 0.5,
    })
tabela = pd.DataFrame(resultados).set_index('modelo')
print('\nDesempenho no teste:')
print(tabela.round(3))
# Leitura: os modelos superam a linha de base, mas por pouco. O desfecho depende de informacoes
# que a base nao tem (evidencias apresentadas, valor pedido, analise do caso).

floresta = modelos['floresta aleatoria']
matriz = confusion_matrix(y_te, floresta.predict(X_te))
print('\nMatriz de confusao da floresta (linhas = real [nao negada, negada]):')
print(matriz)

importancia = pd.Series(floresta.feature_importances_, index=X.columns).sort_values().tail(12)
fig, eixo = plt.subplots(figsize=(8, 4.5))
eixo.barh(importancia.index, importancia.values, color=['#8794A3'] * 9 + ['#2F648F'] * 3)
eixo.set_xlabel('Importância na floresta (redução média de impureza)')
eixo.set_title('O tempo até registrar e o local pesam mais que a companhia')
eixo.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_importancia_variaveis.png'))
plt.show()

# Importancia nao e causa: "dias ate registrar" pode refletir regras de prazo, nao a qualidade do pedido.
# Nenhum destes modelos justifica negar ou aprovar um pedido automaticamente (ver script 05).
