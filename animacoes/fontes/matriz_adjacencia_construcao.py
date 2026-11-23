# Animacao: as arestas de um grafo pequeno entram uma a uma e a matriz de adjacencia vai sendo preenchida.
# Saidas: animacoes/geradas/matriz_adjacencia_construcao.gif e .png. Mesmo grafo da unidade 17.

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

arestas = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (2, 5), (0, 3), (3, 6)]
n = 7
G_final = nx.Graph()
G_final.add_nodes_from(range(n))
G_final.add_edges_from(arestas)
posicao = nx.spring_layout(G_final, seed=42)

fig, (esq, dir) = plt.subplots(1, 2, figsize=(9, 4.5), gridspec_kw={'width_ratios': [1.2, 1]})
esq.axis('off')
nx.draw_networkx_nodes(G_final, posicao, ax=esq, node_color='#2F648F', node_size=700)
nx.draw_networkx_labels(G_final, posicao, ax=esq, font_color='white', font_weight='bold')
dir.set_xticks(range(n))
dir.set_yticks(range(n))
dir.set_xlabel('j')
dir.set_ylabel('i')
dir.grid(False)
dir.set_xlim(-0.5, n - 0.5)
dir.set_ylim(n - 0.5, -0.5)
celulas = [[dir.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor='white', edgecolor='#E6EBF0')) for j in range(n)] for i in range(n)]
textos = [[dir.text(j, i, '0', ha='center', va='center', color='#8794A3', fontsize=11) for j in range(n)] for i in range(n)]
graus = [dir.text(n - 0.2, i, '', va='center', ha='left', color='#20324A', fontsize=9) for i in range(n)]
dir.text(n - 0.2, -0.9, 'grau', ha='left', fontsize=9, color='#20324A')
titulo = fig.suptitle('', x=0.01, ha='left')
arestas_desenhadas = []

def quadro(k):
    if k == 0:
        titulo.set_text('Sem arestas: a matriz é toda zero')
        return []
    if k > len(arestas):
        titulo.set_text(f'{len(arestas)} arestas: a matriz é simétrica e a soma de cada linha é o grau do nó')
        return []
    a, b = arestas[k - 1]
    for antiga in arestas_desenhadas:
        antiga.set_color('#8794A3')
    nova = esq.plot([posicao[a][0], posicao[b][0]], [posicao[a][1], posicao[b][1]], color='#D69A35', linewidth=3, zorder=0)[0]
    arestas_desenhadas.append(nova)
    for linha in arestas_desenhadas[:-1]:
        linha.set_linewidth(1.5)
    for (i, j) in [(a, b), (b, a)]:
        celulas[i][j].set_facecolor('#2F648F')
        textos[i][j].set_text('1')
        textos[i][j].set_color('white')
    for antigo in [c for linha in celulas for c in linha if c.get_facecolor()[:3] == (0.0, 0.0, 0.0)]:
        pass
    A = np.zeros((n, n), dtype=int)
    for (i, j) in arestas[:k]:
        A[i, j] = A[j, i] = 1
    for i in range(n):
        graus[i].set_text(str(A[i].sum()))
    titulo.set_text(f'Aresta {k} de {len(arestas)}: ({a}, {b}) acende A[{a},{b}] e A[{b},{a}]')
    return []

quadros = [0] * 2 + list(range(1, len(arestas) + 1)) + [len(arestas) + 1] * 5
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=900, blit=False)
animacao.save(os.path.join(saida, 'matriz_adjacencia_construcao.gif'), writer=PillowWriter(fps=1.2), dpi=80)
plt.savefig(os.path.join(saida, 'matriz_adjacencia_construcao.png'))
print('Salvo: animacoes/geradas/matriz_adjacencia_construcao.gif e .png')
