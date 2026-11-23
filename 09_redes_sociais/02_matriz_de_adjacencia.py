# Matriz de adjacencia: o mesmo grafo escrito como tabela de zeros e uns.
# Baseado em grafoMatriz.py (material do capitulo 9), que imprimia a matriz em LaTeX.

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# O mesmo grafo do script 01
G = nx.Graph()
G.add_nodes_from(range(7))
G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (2, 5), (0, 3), (3, 6)])

# A[i, j] = 1 se ha aresta entre i e j, 0 caso contrario
A = nx.to_numpy_array(G, dtype=int)
print('Matriz de adjacencia A:')
print(A)

# Propriedades que se leem direto na matriz
print('\nSimetrica (grafo nao direcionado)?', bool((A == A.T).all()))
print('Soma de cada linha = grau do no:', A.sum(axis=1).tolist())
print('Soma de todas as entradas / 2 = arestas:', int(A.sum() / 2))
print('Diagonal zerada (sem lacos):', A.diagonal().tolist())

# A^2 conta caminhos de comprimento 2: quantos "amigos em comum" cada par tem
A2 = A @ A
print('\n(A^2)[0, 3] =', A2[0, 3], '-> vizinhos em comum de 0 e 3:', sorted(set(G.neighbors(0)) & set(G.neighbors(3))))

# Versao em LaTeX, como no script original (util para colar em um relatorio)
n = G.number_of_nodes()
linhas = ['\\[', 'A = ', '\\begin{array}{c|' + 'c' * n + '}', '    & ' + ' & '.join(str(i) for i in range(n)) + ' \\\\', '    \\hline']
for i in range(n):
    linhas.append(f'    {i} & ' + ' & '.join(str(A[i, j]) for j in range(n)) + ' \\\\')
linhas += ['\\end{array}', '\\]']
print('\nMatriz em LaTeX:')
print('\n'.join(linhas))

# Figura: grafo e matriz lado a lado, com a mesma cor para a aresta e a celula
posicao = nx.spring_layout(G, seed=42)
fig, (esq, dir) = plt.subplots(1, 2, figsize=(10, 4.4), gridspec_kw={'width_ratios': [1.2, 1]})
nx.draw_networkx_edges(G, posicao, ax=esq, edge_color='#8794A3', width=1.5)
nx.draw_networkx_nodes(G, posicao, ax=esq, node_color='#2F648F', node_size=800)
nx.draw_networkx_labels(G, posicao, ax=esq, font_color='white', font_weight='bold')
esq.set_title('Grafo')
esq.axis('off')

dir.imshow(A, cmap=plt.matplotlib.colors.ListedColormap(['white', '#2F648F']))
for i in range(n):
    for j in range(n):
        dir.text(j, i, str(A[i, j]), ha='center', va='center', color='white' if A[i, j] else '#8794A3', fontsize=11)
dir.set_xticks(range(n))
dir.set_yticks(range(n))
dir.set_xlabel('j')
dir.set_ylabel('i')
dir.set_title('Matriz de adjacência: A[i, j] = 1 se i e j são vizinhos')
dir.grid(False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'matriz_adjacencia.png'))
plt.show()

# No grafo direcionado a matriz deixa de ser simetrica: A[i, j] = 1 significa i -> j
D = nx.DiGraph([('Ana', 'Bia'), ('Bia', 'Ana'), ('Ana', 'Caio'), ('Caio', 'Bia'), ('Dani', 'Bia')])
print('\nDirecionado, ordem', list(D.nodes()))
print(nx.to_numpy_array(D, dtype=int))

# Experimente: calcule A @ A @ A e interprete (A^3)[0, 0]. Dica: triangulos.
