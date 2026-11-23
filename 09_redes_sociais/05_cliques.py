# Cliques: grupos em que todos se conhecem.
# Baseado em clique.py (material do capitulo 9). Mudancas: as arestas extras agora usam semente fixa,
# os cliques sao encontrados pelo algoritmo (nx.find_cliques) e nao so pela construcao.

import os
import random
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
random.seed(7)

# Construimos cliques de tamanho 1 a 7, encadeados: o ultimo no de um clique liga ao primeiro do proximo
G = nx.Graph()
indice = 0
cliques_construidos = []
for tamanho in range(1, 8):
    nos = list(range(indice, indice + tamanho))
    cliques_construidos.append(nos)
    G.add_nodes_from(nos)
    G.add_edges_from([(nos[i], nos[j]) for i in range(tamanho) for j in range(i + 1, tamanho)])
    if tamanho < 7:
        G.add_edge(nos[-1], indice + tamanho)
    indice += tamanho

# Dez arestas extras entre cliques diferentes
todos = list(G.nodes())
extras = 0
while extras < 10:
    a, b = random.sample(todos, 2)
    mesmo_clique = any(a in c and b in c for c in cliques_construidos)
    if not mesmo_clique and not G.has_edge(a, b):
        G.add_edge(a, b)
        extras += 1
print('Nos:', G.number_of_nodes(), '| Arestas:', G.number_of_edges())

# O algoritmo encontra os cliques maximais (que nao cabem dentro de outro clique)
maximais = sorted(nx.find_cliques(G), key=len, reverse=True)
print('Cliques maximais encontrados:', len(maximais))
print('Os cinco maiores:', [sorted(c) for c in maximais[:5]])
print('Tamanho do maior clique:', len(maximais[0]))
# Repare que as arestas extras podem criar triangulos novos entre cliques, que tambem aparecem na lista.

# Numero de triangulos por no e coeficiente de agrupamento
triangulos = nx.triangles(G)
print('Nos com mais triangulos:', sorted(triangulos.items(), key=lambda par: -par[1])[:5])

# Figura: uma cor por clique construido; arestas extras em cinza claro
paleta = ['#8794A3', '#2F648F', '#168A8A', '#D69A35', '#BD5B58', '#20324A', '#7A9CC6']
cor_no = {}
for i, clique in enumerate(cliques_construidos):
    for no in clique:
        cor_no[no] = paleta[i]
arestas_dentro = [(a, b) for a, b in G.edges() if cor_no[a] == cor_no[b]]
arestas_fora = [(a, b) for a, b in G.edges() if cor_no[a] != cor_no[b]]

posicao = nx.spring_layout(G, seed=42, k=0.9)
fig, eixo = plt.subplots(figsize=(8, 6))
nx.draw_networkx_edges(G, posicao, edgelist=arestas_fora, ax=eixo, edge_color='#E6EBF0', width=1.2)
nx.draw_networkx_edges(G, posicao, edgelist=arestas_dentro, ax=eixo, edge_color='#8794A3', width=1.6)
nx.draw_networkx_nodes(G, posicao, ax=eixo, node_color=[cor_no[n] for n in G.nodes()], node_size=420)
nx.draw_networkx_labels(G, posicao, ax=eixo, font_size=8, font_color='white', font_weight='bold')
eixo.set_title(f'Sete cliques (tamanhos 1 a 7) ligados em cadeia, mais {extras} arestas extras em cinza claro')
eixo.axis('off')
plt.savefig(os.path.join(pasta, 'figuras', 'cliques.png'))
plt.show()

# Um clique e a definicao mais exigente de "grupo": todo mundo ligado a todo mundo.
# Comunidades (script 06) relaxam essa exigencia: muitas ligacoes dentro, poucas fora.

# Experimente: mude random.seed(7) para outro valor. O maior clique continua com 7 nos? Quantos cliques maximais surgem?
