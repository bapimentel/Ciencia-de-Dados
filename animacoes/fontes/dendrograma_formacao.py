# Animacao: o agrupamento hierarquico junta os dois grupos mais proximos a cada passo;
# a esquerda os pontos vao sendo unidos, a direita o dendrograma cresce.
# Saidas: animacoes/geradas/dendrograma_formacao.gif e .png. Dados simulados (make_blobs).

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.datasets import make_blobs

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

X, _ = make_blobs(n_samples=14, centers=3, cluster_std=0.9, random_state=5)
n = len(X)
fusoes = linkage(X, method='average')

# Dendrograma completo, so para obter as coordenadas dos ramos e a ordem das folhas
fig_tmp = plt.figure()
dendro = dendrogram(fusoes, no_plot=True)
plt.close(fig_tmp)
ordem_folhas = [int(f) for f in dendro['ivl']]
posicao_x = {folha: 10 * i + 5 for i, folha in enumerate(ordem_folhas)}

fig, (esq, dir) = plt.subplots(1, 2, figsize=(9, 4.5))
esq.set_xticks([])
esq.set_yticks([])
esq.grid(False)
esq.set_xlim(X[:, 0].min() - 1, X[:, 0].max() + 1)
esq.set_ylim(X[:, 1].min() - 1, X[:, 1].max() + 1)
esq.scatter(X[:, 0], X[:, 1], s=60, color='#2F648F', zorder=3)
for i, (x, y) in enumerate(X):
    esq.text(x + 0.12, y + 0.12, str(i), fontsize=9, color='#20324A')
dir.set_xlim(0, 10 * n)
dir.set_ylim(0, fusoes[:, 2].max() * 1.1)
dir.set_xticks([posicao_x[f] for f in ordem_folhas])
dir.set_xticklabels([str(f) for f in ordem_folhas], fontsize=8)
dir.set_ylabel('Distância de fusão (ligação média)')
dir.set_title('Dendrograma crescendo')
esq.set_title('Pontos sendo unidos')
titulo = fig.suptitle('', x=0.01, ha='left')

# Cada grupo intermediario: conjunto de folhas, posicao x do seu ramo e altura
grupos = {i: {'folhas': [i], 'x': posicao_x[i], 'altura': 0.0} for i in range(n)}
desenhados = []

def quadro(passo):
    if passo < 0:
        titulo.set_text('Início: cada ponto é um grupo')
        return []
    if passo >= len(fusoes):
        titulo.set_text('Fim: um único grupo. Cortar a árvore em uma altura escolhe quantos grupos ficam.')
        return []
    a, b, distancia, tamanho = fusoes[passo]
    ga, gb = grupos[int(a)], grupos[int(b)]
    novo_x = (ga['x'] + gb['x']) / 2
    # Dendrograma: dois ramos verticais e a barra horizontal
    dir.plot([ga['x'], ga['x']], [ga['altura'], distancia], color='#2F648F', linewidth=1.6)
    dir.plot([gb['x'], gb['x']], [gb['altura'], distancia], color='#2F648F', linewidth=1.6)
    dir.plot([ga['x'], gb['x']], [distancia, distancia], color='#2F648F', linewidth=1.6)
    # Pontos: uma linha entre os centroides dos dois grupos unidos
    ca = X[ga['folhas']].mean(axis=0)
    cb = X[gb['folhas']].mean(axis=0)
    esq.plot([ca[0], cb[0]], [ca[1], cb[1]], color='#D69A35', linewidth=2, alpha=0.9)
    esq.scatter(X[ga['folhas'] + gb['folhas'], 0], X[ga['folhas'] + gb['folhas'], 1], s=60, color='#168A8A', zorder=4)
    grupos[n + passo] = {'folhas': ga['folhas'] + gb['folhas'], 'x': novo_x, 'altura': distancia}
    titulo.set_text(f'Passo {passo + 1}: une os grupos {sorted(ga["folhas"])} e {sorted(gb["folhas"])} '
                    f'(distância {distancia:.2f}); restam {n - passo - 1} grupos')
    return []

quadros = [-1] * 2 + list(range(len(fusoes))) + [len(fusoes)] * 5
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=1000, blit=False)
animacao.save(os.path.join(saida, 'dendrograma_formacao.gif'), writer=PillowWriter(fps=1), dpi=80)
plt.savefig(os.path.join(saida, 'dendrograma_formacao.png'))
print('Salvo: animacoes/geradas/dendrograma_formacao.gif e .png')
