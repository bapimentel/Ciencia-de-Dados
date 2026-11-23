# "Nao existe almoco gratis" (No Free Lunch): nenhum algoritmo e o melhor em todos os problemas.
# Para ver isso na pratica, avaliamos 6 algoritmos em 64 bases de classificacao:
#   4 bases reais que vem com o scikit-learn (iris, vinhos, cancer de mama, digitos)
#   60 bases simuladas com caracteristicas variadas (tamanho, numero de atributos, ruido, separacao,
#   fronteiras lineares e curvas, atributos irrelevantes).
# Saidas: dados/bases.npz (as bases, usadas no script 02) e dados/desempenho.csv (acuracias, usadas no 03).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import (load_iris, load_wine, load_breast_cancer, load_digits, make_classification,
                              make_moons, make_circles, make_gaussian_quantiles)
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
os.makedirs(os.path.join(pasta, 'dados'), exist_ok=True)
gerador = np.random.default_rng(0)

# --- 1. Montar a colecao de bases
bases = {}
for nome, carregar in [('iris', load_iris), ('vinhos', load_wine), ('cancer_mama', load_breast_cancer), ('digitos', load_digits)]:
    b = carregar()
    bases[nome] = (b.data, b.target)

for i in range(60):
    n = int(gerador.choice([100, 200, 400, 600]))
    ruido_extra = int(gerador.choice([0, 2, 10]))           # atributos irrelevantes acrescentados
    tipo = gerador.choice(['linear', 'linear', 'curva'])
    if tipo == 'linear':
        p = int(gerador.choice([2, 5, 10, 20]))
        classes, grupos = int(gerador.choice([2, 3])), int(gerador.choice([1, 2]))
        if classes * grupos > 2 ** max(2, p // 2):     # com poucos atributos informativos nao cabem tantos grupos
            grupos = 1
        X, y = make_classification(n_samples=n, n_features=p, n_informative=max(2, p // 2), n_redundant=0,
                                   n_classes=classes, n_clusters_per_class=grupos,
                                   class_sep=float(gerador.choice([0.5, 1.0, 2.0])), flip_y=float(gerador.choice([0, 0.05, 0.2])),
                                   random_state=i)
    else:
        forma = gerador.choice(['luas', 'circulos', 'quantis'])
        if forma == 'luas':
            X, y = make_moons(n_samples=n, noise=float(gerador.choice([0.1, 0.3])), random_state=i)
        elif forma == 'circulos':
            X, y = make_circles(n_samples=n, noise=float(gerador.choice([0.05, 0.15])), factor=0.5, random_state=i)
        else:
            X, y = make_gaussian_quantiles(n_samples=n, n_features=int(gerador.choice([2, 4])), n_classes=2, random_state=i)
    if ruido_extra:
        X = np.column_stack([X, gerador.normal(0, 1, (n, ruido_extra))])
    # escalas diferentes por atributo, como em dados reais
    X = X * gerador.choice([1, 1, 10, 100], size=X.shape[1])
    bases[f'sim_{i:02d}_{tipo}'] = (X, y)
print(f'{len(bases)} bases montadas')
np.savez_compressed(os.path.join(pasta, 'dados', 'bases.npz'),
                    **{f'{nome}__X': X.astype(np.float32) for nome, (X, y) in bases.items()},
                    **{f'{nome}__y': y for nome, (X, y) in bases.items()})

# --- 2. Avaliar os algoritmos em todas as bases (validacao cruzada de 5 dobras)
algoritmos = {
    'k-NN': make_pipeline(StandardScaler(), KNeighborsClassifier(5)),
    'Naive Bayes': GaussianNB(),
    'Árvore': DecisionTreeClassifier(min_samples_leaf=5, random_state=0),
    'Reg. logística': make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    'SVM (RBF)': make_pipeline(StandardScaler(), SVC()),
    'Floresta': RandomForestClassifier(n_estimators=100, random_state=0),
}
dobras = StratifiedKFold(5, shuffle=True, random_state=0)
linhas = []
for nome, (X, y) in bases.items():
    linha = {'base': nome}
    for alg, modelo in algoritmos.items():
        linha[alg] = cross_val_score(modelo, X, y, cv=dobras).mean()
    linhas.append(linha)
desempenho = pd.DataFrame(linhas).set_index('base')
desempenho.to_csv(os.path.join(pasta, 'dados', 'desempenho.csv'))

# --- 3. Quem vence?
vencedor = desempenho.idxmax(axis=1)
ranks = desempenho.rank(axis=1, ascending=False)
resumo = pd.DataFrame({'vitorias': vencedor.value_counts().reindex(algoritmos).fillna(0).astype(int),
                       'rank medio': ranks.mean().round(2),
                       'acuracia media': desempenho.mean().round(3),
                       'pior distancia ao melhor': (desempenho.max(axis=1).values[:, None] - desempenho).max().round(3)})
print('\nResumo nas 64 bases:')
print(resumo.sort_values('rank medio'))
print('\nBases reais:')
print(desempenho.loc[['iris', 'vinhos', 'cancer_mama', 'digitos']].round(3))
# Mesmo o algoritmo de melhor rank medio perde em muitas bases, as vezes por margem grande.

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 5.5), gridspec_kw={'width_ratios': [1, 1.4]})
ordem = resumo.sort_values('rank medio').index
esq.barh(ordem[::-1], resumo.loc[ordem[::-1], 'vitorias'], color='#2F648F')
for i, v in enumerate(resumo.loc[ordem[::-1], 'vitorias']):
    esq.text(v + 0.3, i, str(v), va='center')
esq.set_xlabel('Bases em que o algoritmo foi o melhor (de 64)')
esq.set_title('Nenhum algoritmo vence em todas', fontsize=11)
esq.grid(axis='y', visible=False)
distancia = 100 * (desempenho.max(axis=1).values[:, None] - desempenho[ordem])
dir.boxplot([distancia[c] for c in ordem], tick_labels=list(ordem), orientation='horizontal', widths=0.5,
            medianprops={'color': '#D69A35', 'linewidth': 2}, flierprops={'markeredgecolor': '#BD5B58'})
dir.invert_yaxis()
dir.set_xlabel('Distância até o melhor algoritmo da base (pontos de acurácia)')
dir.set_title('Quanto se perde ao usar sempre o mesmo algoritmo', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'sem_almoco_gratis.png'))
plt.show()
