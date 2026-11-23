# Metodos de estimacao de desempenho: hold-out, subamostragem aleatoria, k-fold, leave-one-out e bootstrap.
# Todos respondem "quao bem este modelo deve ir em dados novos?", com custos e vieses diferentes.
# Modelo: arvore de decisao de profundidade 3; dados: cancer de mama (569 exames).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, ShuffleSplit, StratifiedKFold, LeaveOneOut, cross_val_score
from sklearn.metrics import accuracy_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
base = load_breast_cancer()
X, y = base.data, (base.target == 0).astype(int)
modelo = DecisionTreeClassifier(max_depth=3, random_state=0)

# 1) Hold-out: uma divisao 2/3 treino, 1/3 teste. Barato, mas o resultado depende da sorte da divisao.
holdouts = []
for semente in range(20):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=1 / 3, random_state=semente, stratify=y)
    holdouts.append(accuracy_score(y_te, modelo.fit(X_tr, y_tr).predict(X_te)))
print(f'Hold-out com 20 sementes diferentes: de {min(holdouts):.3f} a {max(holdouts):.3f}  <- um unico numero esconde isso')

# 2) Subamostragem aleatoria: repetir o hold-out k vezes e tirar a media
sub = cross_val_score(modelo, X, y, cv=ShuffleSplit(n_splits=30, test_size=1 / 3, random_state=0))
print(f'Subamostragem (30 repeticoes): {sub.mean():.3f} +- {sub.std():.3f}')

# 3) k-fold: k partes disjuntas; cada uma e teste uma vez. Todos os exemplos sao testados exatamente uma vez.
kfold = cross_val_score(modelo, X, y, cv=StratifiedKFold(n_splits=10, shuffle=True, random_state=0))
print(f'10-fold estratificado: {kfold.mean():.3f} +- {kfold.std():.3f}')

# 4) Leave-one-out: k = n. Cada exemplo e o teste sozinho. Sem aleatoriedade, mas n ajustes (569 aqui).
loo = cross_val_score(modelo, X, y, cv=LeaveOneOut())
print(f'Leave-one-out ({len(loo)} ajustes): {loo.mean():.3f}')

# 5) Bootstrap: sortear n exemplos COM reposicao para treino; os nao sorteados (~36,8%) sao o teste.
# Estimativa .632: combina o erro no teste (otimista demais? nao: pessimista) com o do treino (otimista).
gerador = np.random.default_rng(0)
n = len(y)
estimativas = []
fracao_fora = []
for _ in range(100):
    indices = gerador.integers(0, n, size=n)
    fora = np.setdiff1d(np.arange(n), indices)
    fracao_fora.append(len(fora) / n)
    modelo.fit(X[indices], y[indices])
    acc_teste = accuracy_score(y[fora], modelo.predict(X[fora]))
    acc_treino = accuracy_score(y[indices], modelo.predict(X[indices]))
    estimativas.append(0.632 * acc_teste + 0.368 * acc_treino)
print(f'Bootstrap .632 (100 repeticoes): {np.mean(estimativas):.3f} +- {np.std(estimativas):.3f}')
print(f'Fracao media de exemplos fora da amostra bootstrap: {np.mean(fracao_fora):.3f}  (teoria: (1 - 1/n)^n -> 0,368)')

resultados = pd.DataFrame({
    'método': ['hold-out (20 sementes)', 'subamostragem (30)', '10-fold', 'leave-one-out', 'bootstrap .632 (100)'],
    'média': [np.mean(holdouts), sub.mean(), kfold.mean(), loo.mean(), np.mean(estimativas)],
    'desvio': [np.std(holdouts), sub.std(), kfold.std(), 0, np.std(estimativas)],
    'ajustes': [1, 30, 10, len(loo), 100],
})
print('\n', resultados.round(3).to_string(index=False))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={'width_ratios': [1.2, 1]})
esq.axis('off')
esq.set_xlim(0, 10)
esq.set_ylim(0, 6)
# desenho dos esquemas: cada linha e uma rodada; azul = treino, ambar = teste
esq.text(0, 5.6, 'hold-out', fontweight='bold', color='#20324A')
esq.add_patch(plt.Rectangle((2.2, 5.4), 5.0, 0.4, color='#2F648F'))
esq.add_patch(plt.Rectangle((7.2, 5.4), 2.5, 0.4, color='#D69A35'))
esq.text(0, 4.6, '5-fold', fontweight='bold', color='#20324A')
for rodada in range(5):
    for parte in range(5):
        cor = '#D69A35' if parte == rodada else '#2F648F'
        esq.add_patch(plt.Rectangle((2.2 + parte * 1.5, 4.5 - rodada * 0.45), 1.45, 0.38, color=cor))
esq.text(0, 1.6, 'bootstrap', fontweight='bold', color='#20324A')
pontos = gerador.integers(0, 20, size=20)
for i in range(20):
    usado = i in pontos
    esq.add_patch(plt.Rectangle((2.2 + i * 0.375, 1.4), 0.33, 0.4, color='#2F648F' if usado else '#D69A35'))
esq.text(2.2, 0.9, 'azul: sorteados (com repetição) para treino;\nâmbar: nunca sorteados, viram teste', fontsize=9, color='#20324A', va='top')
esq.set_title('Azul = treino, âmbar = teste')
dir.errorbar(resultados['média'], range(5), xerr=resultados['desvio'], fmt='o', color='#2F648F', capsize=4)
dir.set_yticks(range(5))
dir.set_yticklabels(resultados['método'])
dir.invert_yaxis()
dir.set_xlabel('Acurácia estimada (média ± desvio)')
dir.set_title('As estimativas concordam; a variação é que muda')
dir.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'metodos_de_avaliacao.png'))
plt.show()
