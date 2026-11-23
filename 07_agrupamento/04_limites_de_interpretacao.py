# Limites: o k-means sempre devolve k grupos, mesmo quando nao ha grupo nenhum.
# E a escala das variaveis decide o resultado.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
cores = np.array(['#2F648F', '#168A8A', '#D69A35'])

# --- 1. Dados uniformes, sem estrutura: o algoritmo "encontra" 3 grupos mesmo assim
gerador = np.random.default_rng(5)
uniforme = gerador.uniform(0, 10, size=(300, 2))
modelo = KMeans(n_clusters=3, n_init=10, random_state=0).fit(uniforme)
print('Dados uniformes: tamanhos', np.bincount(modelo.labels_),
      '| silhueta', round(silhouette_score(uniforme, modelo.labels_), 3))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(9, 3.8))
esq.scatter(uniforme[:, 0], uniforme[:, 1], s=12, color='#8794A3')
esq.set_title('Pontos uniformes: nenhum grupo natural')
dir.scatter(uniforme[:, 0], uniforme[:, 1], s=12, color=cores[modelo.labels_])
dir.set_title(f'K-means com k=3 divide assim mesmo (silhueta {silhouette_score(uniforme, modelo.labels_):.2f})')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'kmeans_sem_grupos.png'))
plt.show()
# Silhueta baixa (perto de 0,3 ou menos) e a pista de que a particao nao corresponde a grupos reais.

# --- 2. Escala: idade (anos) e renda (unidades monetarias) nos clientes de Data.csv
clientes = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Data.csv')).dropna()
X = clientes[['Age', 'Income']].values
sem_escala = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(X)
com_escala = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(StandardScaler().fit_transform(X))
print('\nGrupos sem padronizar:', sem_escala, '(decididos pela renda, que tem numeros maiores)')
print('Grupos padronizados:  ', com_escala)

fig, (esq, dir) = plt.subplots(1, 2, figsize=(9, 3.8))
esq.scatter(X[:, 0], X[:, 1], color=cores[sem_escala], s=60)
esq.set_title('Sem padronizar: a renda manda')
dir.scatter(X[:, 0], X[:, 1], color=cores[com_escala], s=60)
dir.set_title('Padronizado: idade e renda pesam igual')
for eixo in (esq, dir):
    eixo.set_xlabel('Idade')
    eixo.set_ylabel('Renda')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'kmeans_escala.png'))
plt.show()

# --- 3. Inicializacao: com um unico inicio (n_init=1), sementes diferentes podem dar particoes diferentes
from sklearn.datasets import make_blobs
X2, _ = make_blobs(n_samples=300, centers=5, cluster_std=1.3, random_state=2)
inercias = [KMeans(n_clusters=5, n_init=1, random_state=s).fit(X2).inertia_ for s in range(8)]
print('\nInercia com n_init=1 em 8 sementes:', np.round(inercias, 0))
print('Com n_init=10:', round(KMeans(n_clusters=5, n_init=10, random_state=0).fit(X2).inertia_, 0))

# Resumo: um agrupamento e uma particao proposta, nao uma categoria descoberta.
# Para dizer que os grupos "existem", e preciso validar: silhueta, estabilidade entre sementes
# e, sobretudo, se os grupos fazem sentido e sao uteis para a decisao.

# Experimente: rode o item 1 com k=2 e k=6. A silhueta ajuda a perceber o problema?
