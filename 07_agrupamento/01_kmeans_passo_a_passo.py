# K-means passo a passo: atribuir cada ponto ao centro mais proximo, mover os centros, repetir.
# Dados sinteticos (make_blobs, semente fixa), para que o algoritmo fique visivel.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# 300 pontos em 3 grupos (os rotulos verdadeiros sao ignorados: agrupamento nao os usa)
X, _ = make_blobs(n_samples=300, centers=3, cluster_std=1.1, random_state=4)
print('Pontos:', X.shape)

k = 3
gerador = np.random.default_rng(1)
centros = X[gerador.choice(len(X), size=k, replace=False)]      # centros iniciais: 3 pontos sorteados
cores = np.array(['#2F648F', '#168A8A', '#D69A35'])

fig, eixos = plt.subplots(1, 4, figsize=(13, 3.4), sharex=True, sharey=True)
for passo, eixo in enumerate(eixos):
    # 1) atribuicao: distancia de cada ponto a cada centro; fica com o menor
    distancias = np.sqrt(((X[:, None, :] - centros[None, :, :]) ** 2).sum(axis=2))
    grupo = distancias.argmin(axis=1)
    eixo.scatter(X[:, 0], X[:, 1], s=12, color=cores[grupo], alpha=0.7)
    eixo.scatter(centros[:, 0], centros[:, 1], s=160, marker='X', color=cores, edgecolor='#20324A', linewidth=1.2)
    inercia = (distancias.min(axis=1) ** 2).sum()
    eixo.set_title(f'Iteração {passo}: inércia {inercia:.0f}')
    # 2) atualizacao: cada centro vai para a media dos seus pontos
    novos_centros = np.array([X[grupo == j].mean(axis=0) for j in range(k)])
    print(f'Iteracao {passo}: inercia={inercia:.1f}, deslocamento dos centros={np.abs(novos_centros - centros).sum():.3f}')
    centros = novos_centros
fig.suptitle('K-means: os X são os centros; a cada passo eles vão para a média do seu grupo', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'kmeans_passos.png'))
plt.show()

# A inercia (soma das distancias ao quadrado ate o centro) so diminui. Quando os centros param, acabou.

# O mesmo com scikit-learn. n_init repete com varios inicios e guarda o melhor; random_state reproduz.
modelo = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
print('\nscikit-learn: inercia final', round(modelo.inertia_, 1), '| iteracoes', modelo.n_iter_)
print('Tamanho dos grupos:', np.bincount(modelo.labels_))
print('Centros:\n', modelo.cluster_centers_.round(2))

# Experimente: troque a semente do gerador (default_rng(1)) por outra. Os grupos finais mudam?
# E se cluster_std for 3.0 em vez de 1.1?
