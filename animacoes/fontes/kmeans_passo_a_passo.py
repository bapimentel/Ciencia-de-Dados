# Animacao: k-means alternando atribuicao (cores) e atualizacao (centros se movem).
# Saidas: animacoes/geradas/kmeans_passo_a_passo.gif e .png. Dados simulados (make_blobs).

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from sklearn.datasets import make_blobs

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

X, _ = make_blobs(n_samples=240, centers=3, cluster_std=1.3, random_state=9)
k = 3
cores = np.array(['#2F648F', '#168A8A', '#D69A35'])
gerador = np.random.default_rng(3)
centros = X[gerador.choice(len(X), size=k, replace=False)].copy()

# Pre-calcula a sequencia de estados: (centros, grupos, fase)
estados = []
for iteracao in range(8):
    distancias = np.sqrt(((X[:, None, :] - centros[None, :, :]) ** 2).sum(axis=2))
    grupos = distancias.argmin(axis=1)
    estados.append((centros.copy(), grupos.copy(), f'Iteração {iteracao}: atribuição (cada ponto ao centro mais próximo)'))
    novos = np.array([X[grupos == j].mean(axis=0) if (grupos == j).any() else centros[j] for j in range(k)])
    estados.append((novos.copy(), grupos.copy(), f'Iteração {iteracao}: atualização (centro = média do grupo)'))
    if np.allclose(novos, centros):
        estados.append((novos.copy(), grupos.copy(), f'Convergiu na iteração {iteracao}: os centros não se movem mais'))
        break
    centros = novos

destacados = gerador.choice(len(X), size=6, replace=False)     # pontos cujas distancias serao desenhadas

fig, eixo = plt.subplots(figsize=(8, 4.5))
eixo.set_xlim(X[:, 0].min() - 1, X[:, 0].max() + 1)
eixo.set_ylim(X[:, 1].min() - 1, X[:, 1].max() + 1)
eixo.set_xticks([])
eixo.set_yticks([])
eixo.grid(False)
pontos = eixo.scatter(X[:, 0], X[:, 1], s=16, color='#8794A3', alpha=0.8)
marcas = eixo.scatter(centros[:, 0], centros[:, 1], s=220, marker='X', color=cores, edgecolor='#20324A', linewidth=1.2, zorder=5)
linhas = [eixo.plot([], [], color='#8794A3', linewidth=0.8)[0] for _ in destacados]
titulo = eixo.set_title('')

def quadro(i):
    c, g, fase = estados[i]
    pontos.set_color(cores[g])
    marcas.set_offsets(c)
    for linha, idx in zip(linhas, destacados):
        linha.set_data([X[idx, 0], c[g[idx], 0]], [X[idx, 1], c[g[idx], 1]])
    inercia = ((X - c[g]) ** 2).sum()
    titulo.set_text(f'{fase}\ninércia = {inercia:.0f}')
    return [pontos, marcas, titulo] + linhas

quadros = [0] * 2 + list(range(len(estados))) + [len(estados) - 1] * 5
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=900, blit=False)
animacao.save(os.path.join(saida, 'kmeans_passo_a_passo.gif'), writer=PillowWriter(fps=1.2), dpi=80)
quadro(len(estados) - 1)
plt.savefig(os.path.join(saida, 'kmeans_passo_a_passo.png'))
print('Salvo: animacoes/geradas/kmeans_passo_a_passo.gif e .png |', len(estados), 'estados')
