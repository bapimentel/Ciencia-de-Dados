# Deteccao de comunidades no clube de karate: Girvan-Newman, Louvain e espectral (secao 9.3 do livro).
# Baseado em comunidades_karate.py (material do capitulo 9). Mudancas: Louvain agora vem do networkx
# (sem python-louvain), o K-means sobre node2vec foi retirado (dependencia pesada, resultado instavel),
# layout com semente e modularidade calculada para comparar os metodos.

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# Rede classica: 34 membros de um clube de karate (Zachary, 1977) e quem interagia fora do clube.
# O clube se dividiu em dois; o atributo 'club' registra para que lado cada um foi.
G = nx.karate_club_graph()
lado_real = [0 if G.nodes[n]['club'] == 'Mr. Hi' else 1 for n in G.nodes()]
print('Nos:', G.number_of_nodes(), '| Arestas:', G.number_of_edges())

# 1) Girvan-Newman: remove repetidamente a aresta de maior intermediacao; a primeira divisao da 2 grupos
divisoes = nx.community.girvan_newman(G)
gn = tuple(sorted(c) for c in next(divisoes))
rotulo_gn = {no: i for i, grupo in enumerate(gn) for no in grupo}

# 2) Louvain: maximiza a modularidade por movimentos locais; o numero de comunidades sai do metodo
louvain = nx.community.louvain_communities(G, seed=0)
rotulo_louvain = {no: i for i, grupo in enumerate(louvain) for no in grupo}

# 3) Espectral: autovetores da matriz de adjacencia + k-means; k precisa ser escolhido
A = nx.to_numpy_array(G)
espectral = SpectralClustering(n_clusters=2, affinity='precomputed', random_state=0).fit(A)
rotulo_espectral = {no: int(r) for no, r in zip(G.nodes(), espectral.labels_)}

# Modularidade: quanto mais arestas dentro das comunidades do que o esperado ao acaso (max teorico 1)
def modularidade(rotulos):
    grupos = {}
    for no, r in rotulos.items():
        grupos.setdefault(r, set()).add(no)
    return nx.community.modularity(G, list(grupos.values()))

def concordancia_com_a_divisao_real(rotulos):
    # fracao de pares de nos classificados juntos/separados igual a divisao real (indice de Rand)
    nos = list(G.nodes())
    iguais = 0
    total = 0
    for i in range(len(nos)):
        for j in range(i + 1, len(nos)):
            mesmo_pred = rotulos[nos[i]] == rotulos[nos[j]]
            mesmo_real = lado_real[i] == lado_real[j]
            iguais += mesmo_pred == mesmo_real
            total += 1
    return iguais / total

resultados = {'Girvan-Newman (1ª divisão)': rotulo_gn, 'Louvain': rotulo_louvain, 'Espectral (k=2)': rotulo_espectral}
print(f'\n{"método":28s} {"comunidades":>12s} {"modularidade":>13s} {"concord. c/ divisão real":>25s}')
for nome, rot in resultados.items():
    print(f'{nome:28s} {len(set(rot.values())):12d} {modularidade(rot):13.3f} {concordancia_com_a_divisao_real(rot):25.3f}')
print('Divisao real do clube: modularidade', round(modularidade({no: lado_real[i] for i, no in enumerate(G.nodes())}), 3))
# Louvain encontra mais comunidades e modularidade maior; isso nao quer dizer que ele "acertou":
# a divisao real tinha dois lados, e a modularidade premia particoes mais finas.

paleta = np.array(['#2F648F', '#D69A35', '#168A8A', '#BD5B58', '#8794A3', '#20324A'])
posicao = nx.spring_layout(G, seed=4)
fig, eixos = plt.subplots(2, 2, figsize=(11, 9))
paineis = [('Divisão real do clube (2 lados)', {no: lado_real[i] for i, no in enumerate(G.nodes())})] + list(resultados.items())
for eixo, (nome, rot) in zip(eixos.ravel(), paineis):
    cores = paleta[[rot[n] for n in G.nodes()]]
    nx.draw_networkx_edges(G, posicao, ax=eixo, edge_color='#E6EBF0', width=1)
    nx.draw_networkx_nodes(G, posicao, ax=eixo, node_color=cores, node_size=260, edgecolors='white')
    nx.draw_networkx_labels(G, posicao, ax=eixo, font_size=7, font_color='white', font_weight='bold')
    eixo.set_title(f'{nome}: modularidade {modularidade(rot):.3f}', fontsize=11)
    eixo.axis('off')
fig.suptitle('Mesmo layout, mesmas cores por comunidade: compare onde os métodos discordam', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'comunidades_karate.png'))
plt.show()

# Experimente: rode SpectralClustering com n_clusters=4 e compare com o Louvain.
# Depois mude seed=0 do Louvain. A particao e sempre a mesma?
