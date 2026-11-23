# Estudo de caso 1 - Reclamacoes por perdas (TSA). Passo 4: um modelo antecipa o desfecho?
# Alvo: negada (1) x paga (0, aprovada ou acordo). Entradas: so o que se conhece no momento do registro.
# Comparamos tres modelos com a linha de base por validacao cruzada no treino e medimos no teste uma vez.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, confusion_matrix

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'))

variaveis = ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)', 'Dias ate registrar', 'Mes']
X = pd.get_dummies(dados[variaveis], dtype=int)
y = dados['Negada']
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
print(f'Treino: {len(X_tr)} | teste: {len(X_te)} | colunas apos one-hot: {X.shape[1]}')

modelos = {
    'linha de base (sempre "negada")': DummyClassifier(strategy='most_frequent'),
    'regressão logística': LogisticRegression(max_iter=3000),
    'árvore (profundidade 6)': DecisionTreeClassifier(max_depth=6, random_state=0),
    'floresta aleatória': RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0),
}
dobras = StratifiedKFold(5, shuffle=True, random_state=0)
linhas, curvas = [], {}
for nome, modelo in modelos.items():
    auc_cv = cross_val_score(modelo, X_tr, y_tr, cv=dobras, scoring='roc_auc')
    modelo.fit(X_tr, y_tr)
    prob = modelo.predict_proba(X_te)[:, 1]
    curvas[nome] = roc_curve(y_te, prob)
    linhas.append({'modelo': nome, 'AUC validação (média ± dp)': f'{auc_cv.mean():.3f} ± {auc_cv.std():.3f}',
                   'AUC teste': roc_auc_score(y_te, prob), 'acurácia teste': accuracy_score(y_te, modelo.predict(X_te))})
tabela = pd.DataFrame(linhas).set_index('modelo')
print(tabela.round(3).to_string())

floresta = modelos['floresta aleatória']
print('\nMatriz de confusao da floresta no teste (linhas: real paga, real negada):')
print(confusion_matrix(y_te, floresta.predict(X_te)))

# Quanto um modelo de AUC ~0,65 erra se usado para DECIDIR? Taxa de erro entre os previstos como negada:
previsto = floresta.predict(X_te)
print(f'Entre os casos que a floresta preveria como "negada", {np.mean(y_te[previsto == 1] == 0):.0%} terminaram pagos.')

importancia = pd.Series(floresta.feature_importances_, index=X.columns).sort_values().tail(10)
fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.6))
cores = {'linha de base (sempre "negada")': '#8794A3', 'regressão logística': '#168A8A',
         'árvore (profundidade 6)': '#D69A35', 'floresta aleatória': '#2F648F'}
for nome, (fpr, tpr, _) in curvas.items():
    esq.plot(fpr, tpr, color=cores[nome], label=f'{nome} (AUC {tabela.loc[nome, "AUC teste"]:.2f})')
esq.plot([0, 1], [0, 1], color='#8794A3', linestyle=':')
esq.set_xlabel('Fração das pagas marcadas como negadas')
esq.set_ylabel('Fração das negadas encontradas')
esq.set_title('Curvas ROC no teste: ganho real, mas modesto', fontsize=11)
esq.legend(loc='lower right', fontsize=9)
dir.barh([c[:40] for c in importancia.index], importancia.values, color=['#8794A3'] * 7 + ['#2F648F'] * 3)
dir.set_xlabel('Importância na floresta (redução média de impureza)')
dir.set_title('Variáveis mais usadas pela floresta', fontsize=11)
dir.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '04_modelos_desfecho.png'))
plt.show()
# Importancia nao e causa: "dias ate registrar" e numerica e oferece muitos cortes, o que infla sua importancia.
