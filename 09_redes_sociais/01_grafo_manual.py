# Um grafo construido a mao: nos, arestas e grau.
# Baseado em grafoMatriz.py (material do capitulo 9). O original sorteava 12 arestas entre 7 nos
# e intitulava a figura "Grafo com 6 Nos e 8 Arestas"; aqui as arestas sao fixas e o titulo confere.

import os
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# Uma rede pequena: 7 pessoas (0 a 6) e quem conhece quem
G = nx.Graph()
G.add_nodes_from(range(7))
arestas = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (2, 5), (0, 3), (3, 6)]
G.add_edges_from(arestas)

print('Nos:', G.number_of_nodes(), '| Arestas:', G.number_of_edges())
print('Vizinhos de cada no:')
for no in G.nodes():
    print(f'  {no}: {sorted(G.neighbors(no))}')

# Grau = numero de vizinhos
grau = dict(G.degree())
print('Grau:', grau)
print('Soma dos graus:', sum(grau.values()), '= 2 x arestas =', 2 * G.number_of_edges())

# Desenho com posicao fixa (seed) para que a figura seja sempre a mesma
posicao = nx.spring_layout(G, seed=42)
fig, eixo = plt.subplots(figsize=(6, 4.5))
nx.draw_networkx_edges(G, posicao, ax=eixo, edge_color='#8794A3', width=1.5)
nx.draw_networkx_nodes(G, posicao, ax=eixo, node_color='#2F648F', node_size=900)
nx.draw_networkx_labels(G, posicao, ax=eixo, font_color='white', font_size=13, font_weight='bold')
eixo.set_title(f'Grafo não direcionado com {G.number_of_nodes()} nós e {G.number_of_edges()} arestas')
eixo.axis('off')
plt.savefig(os.path.join(pasta, 'figuras', 'grafo_manual.png'))
plt.show()

# Grafo direcionado: a relacao tem sentido (A segue B, A vota em B, A envia e-mail para B)
D = nx.DiGraph()
D.add_edges_from([('Ana', 'Bia'), ('Bia', 'Ana'), ('Ana', 'Caio'), ('Caio', 'Bia'), ('Dani', 'Bia')])
print('\nGrafo direcionado:')
print('Grau de entrada (quantos apontam para o no):', dict(D.in_degree()))
print('Grau de saida (para quantos o no aponta):   ', dict(D.out_degree()))

fig, eixo = plt.subplots(figsize=(5, 3.8))
posicao_d = nx.circular_layout(D)
nx.draw_networkx(D, posicao_d, ax=eixo, node_color='#168A8A', node_size=1400, font_color='white',
                 edge_color='#8794A3', arrowsize=18, width=1.5, connectionstyle='arc3,rad=0.12')
eixo.set_title('Direcionado: Bia recebe 3 arestas e envia 1')
eixo.axis('off')
plt.savefig(os.path.join(pasta, 'figuras', 'grafo_direcionado.png'))
plt.show()

# Experimente: remova a aresta (2, 5) e veja o que acontece com o grau de 2 e de 5
# e com o caminho mais curto entre 0 e 6 (nx.shortest_path(G, 0, 6)).
print('\nCaminho mais curto de 0 a 6:', nx.shortest_path(G, 0, 6))
