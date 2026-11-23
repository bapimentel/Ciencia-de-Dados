# Quantos grupos? Metodo do cotovelo (inercia) e silhueta.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

X, _ = make_blobs(n_samples=400, centers=4, cluster_std=1.0, random_state=7)

valores_k = range(2, 9)
inercias = []
silhuetas = []
for k in valores_k:
    modelo = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    inercias.append(modelo.inertia_)
    silhuetas.append(silhouette_score(X, modelo.labels_))
    print(f'k={k}: inercia={modelo.inertia_:8.1f}  silhueta={silhuetas[-1]:.3f}')

# Inercia sempre cai quando k cresce (mais centros, distancias menores). Procura-se o "cotovelo".
# Silhueta mede, para cada ponto, se ele esta mais perto do proprio grupo do que do vizinho (-1 a 1).
melhor_k = list(valores_k)[int(np.argmax(silhuetas))]
print('Maior silhueta em k =', melhor_k)

fig, (esq, dir) = plt.subplots(1, 2, figsize=(10, 3.6))
esq.plot(list(valores_k), inercias, marker='o', color='#2F648F')
esq.set_xlabel('k (número de grupos)')
esq.set_ylabel('Inércia')
esq.set_title('Cotovelo: a queda desacelera depois de k = 4')
dir.plot(list(valores_k), silhuetas, marker='o', color='#168A8A')
dir.axvline(melhor_k, color='#D69A35', linestyle='--')
dir.set_xlabel('k')
dir.set_ylabel('Silhueta média')
dir.set_title(f'Silhueta: máximo em k = {melhor_k}')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'escolher_k.png'))
plt.show()

# Os dois criterios concordam aqui porque os dados foram gerados com 4 grupos bem separados.
# Em dados reais eles costumam discordar, e a escolha final depende da pergunta.

# Experimente: gere os dados com cluster_std=2.5. O cotovelo continua visivel?
