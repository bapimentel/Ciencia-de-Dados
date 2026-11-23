# Reducao de dados: menos colunas (dimensionalidade) ou menos linhas (numerosidade), perdendo o minimo.
# (1) PCA; (2) selecao de atributos; (3) amostragem simples e estratificada.
# Dados: base de cancer de mama de Wisconsin (569 exames, 30 medidas), incluida no scikit-learn.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = pd.Series((base.target == 0).astype(int), name='maligno')
print('Dimensao original:', X.shape)

# --- 1. PCA: novas variaveis (componentes) que sao combinacoes das originais, ordenadas pela variancia
# que explicam. As 30 medidas sao muito correlacionadas (raio, perimetro e area medem quase o mesmo).
print('Correlacao media absoluta entre as 30 medidas:', round(X.corr().abs().values[np.triu_indices(30, 1)].mean(), 2))
X_padronizado = StandardScaler().fit_transform(X)       # PCA exige escalas comparaveis
pca = PCA().fit(X_padronizado)
acumulada = np.cumsum(pca.explained_variance_ratio_)
for k in [1, 2, 3, 5, 7, 10]:
    print(f'{k:2d} componentes explicam {acumulada[k - 1]:.1%} da variancia')
k_90 = int(np.argmax(acumulada >= 0.90)) + 1
print(f'Componentes necessarios para 90%: {k_90} (de 30)')

# O que o primeiro componente "mede"? Os pesos (cargas) das variaveis originais
cargas = pd.Series(pca.components_[0], index=X.columns).sort_values()
print('\nMaiores cargas no 1o componente:')
print(cargas.tail(5).round(2))

# --- 2. Selecao de atributos: manter as originais mais informativas sobre o alvo (aqui, teste F da ANOVA).
# IMPORTANTE: escolher atributos olhando o alvo deve ser feito SO no treino (senao ha vazamento).
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
seletor = SelectKBest(f_classif, k=5).fit(X_tr, y_tr)
print('\nCinco atributos selecionados (no treino):', list(X.columns[seletor.get_support()]))

# --- 3. Amostragem: reduzir linhas. A estratificada preserva a proporcao das classes.
gerador = np.random.default_rng(0)
amostra_simples = X.sample(60, random_state=1)
proporcao_simples = y.loc[amostra_simples.index].mean()
_, amostra_estratificada, _, y_estrat = train_test_split(X, y, test_size=60, random_state=1, stratify=y)
print(f'\nProporcao de malignos: populacao {y.mean():.3f} | amostra simples de 60: {proporcao_simples:.3f} | '
      f'estratificada de 60: {y_estrat.mean():.3f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
esq.bar(range(1, 11), 100 * pca.explained_variance_ratio_[:10], color='#8794A3', label='cada componente')
esq.plot(range(1, 11), 100 * acumulada[:10], marker='o', color='#2F648F', label='acumulado')
esq.axhline(90, color='#D69A35', linestyle='--', linewidth=1)
esq.set_xlabel('Componente principal')
esq.set_ylabel('% da variância explicada')
esq.set_title(f'{k_90} de 30 componentes guardam 90% da variância')
esq.legend()
projecao = pca.transform(X_padronizado)[:, :2]
cores = np.where(y == 1, '#BD5B58', '#2F648F')
dir.scatter(projecao[:, 0], projecao[:, 1], c=cores, s=10, alpha=0.6)
dir.set_xlabel(f'Componente 1 ({pca.explained_variance_ratio_[0]:.0%} da variância)')
dir.set_ylabel(f'Componente 2 ({pca.explained_variance_ratio_[1]:.0%})')
dir.set_title('30 medidas vistas em 2 dimensões: as classes já se separam')
dir.text(0.02, 0.95, '● maligno', color='#BD5B58', transform=dir.transAxes)
dir.text(0.02, 0.89, '● benigno', color='#2F648F', transform=dir.transAxes)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'pca.png'))
plt.show()
