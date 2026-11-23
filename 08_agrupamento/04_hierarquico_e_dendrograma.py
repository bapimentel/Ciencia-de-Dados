# Agrupamento hierarquico: juntar os pares mais proximos ate sobrar um grupo; o dendrograma mostra a ordem.

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# Poucos pontos para o dendrograma ser legivel
X, _ = make_blobs(n_samples=30, centers=3, cluster_std=1.0, random_state=11)

# linkage calcula a sequencia de fusoes. 'ward' junta os grupos que menos aumentam a variancia interna
fusoes = linkage(X, method='ward')
print('Primeiras fusoes (indice A, indice B, distancia, tamanho do novo grupo):')
print(fusoes[:5].round(2))
# Cada linha junta dois grupos; indices >= 30 sao grupos criados em linhas anteriores.

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4))
dendrogram(fusoes, ax=esq, color_threshold=0, above_threshold_color='#2F648F', leaf_font_size=8)
esq.axhline(8, color='#D69A35', linestyle='--')
esq.set_title('Dendrograma: cortar na linha âmbar separa 3 grupos')
esq.set_ylabel('Distância de fusão (Ward)')
esq.set_xlabel('Pontos')
esq.grid(False)

# Cortar o dendrograma: 3 grupos
grupo = fcluster(fusoes, t=3, criterion='maxclust')
cores = np.array(['#2F648F', '#168A8A', '#D69A35'])
dir.scatter(X[:, 0], X[:, 1], color=cores[grupo - 1], s=40)
for i, (x, y) in enumerate(X):
    dir.text(x + 0.08, y + 0.08, str(i), fontsize=7, color='#8794A3')
dir.set_title('Os 3 grupos do corte, no plano')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'dendrograma.png'))
plt.show()

# Comparar com k-means: concordam?
kmeans = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
print('\nConcordancia hierarquico x k-means (ARI, 1 = identico):', round(adjusted_rand_score(grupo, kmeans.labels_), 3))

# Outros criterios de ligacao dao arvores diferentes
for metodo in ['single', 'complete', 'average', 'ward']:
    g = fcluster(linkage(X, method=metodo), t=3, criterion='maxclust')
    print(f'{metodo:9s}: tamanhos dos grupos {np.bincount(g)[1:]}')

# O hierarquico nao exige escolher k antes: a arvore inteira fica disponivel, e o corte e uma decisao posterior.

# Criterios de ligacao em dados com formato alongado: a escolha muda o resultado.
# single   = distancia entre os dois pontos MAIS PROXIMOS dos grupos (encadeia, segue formas alongadas)
# complete = distancia entre os dois pontos MAIS DISTANTES (prefere grupos compactos)
# average  = media de todas as distancias entre pontos dos dois grupos
# ward     = junta os grupos que menos aumentam a variancia interna
from sklearn.datasets import make_moons
luas, _ = make_moons(n_samples=200, noise=0.06, random_state=3)
fig, eixos = plt.subplots(1, 4, figsize=(15, 3.6))
for eixo, metodo in zip(eixos, ['single', 'complete', 'average', 'ward']):
    g = fcluster(linkage(luas, method=metodo), t=2, criterion='maxclust')
    eixo.scatter(luas[:, 0], luas[:, 1], color=cores[g - 1], s=12)
    eixo.set_title(f'ligação {metodo}', fontsize=11)
    eixo.set_xticks([])
    eixo.set_yticks([])
fig.suptitle('Mesmos pontos, quatro critérios de ligação, 2 grupos: só o single segue as "luas"', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'criterios_de_ligacao.png'))
plt.show()

# Experimente: mude o corte (axhline e t=) para 2 e para 5 grupos.
