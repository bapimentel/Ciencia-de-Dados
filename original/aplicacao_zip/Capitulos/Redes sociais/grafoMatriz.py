import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

# Inicializa um grafo vazio
G = nx.Graph()

# Adiciona 6 nós ao grafo
G.add_nodes_from(range(7))

# Adiciona arestas até que haja 8 arestas
while G.number_of_edges() < 12:
    # Escolhe dois nós aleatórios diferentes
    node_a, node_b = random.sample(G.nodes(), 2)
    
    # Adiciona a aresta se ainda não existir
    if not G.has_edge(node_a, node_b):
        G.add_edge(node_a, node_b)

# Desenha o grafo gerado
plt.figure(figsize=(8, 6))  # Cria uma nova figura
pos = nx.spring_layout(G, seed=42)  # Layout para a visualização

# Aumenta o tamanho dos vértices
node_size = 1200  # Tamanho dos nós
font_size = 16    # Tamanho da fonte dos rótulos

# Desenha o grafo
nx.draw(G, pos, with_labels=True, node_color='skyblue', 
        node_size=node_size, font_size=font_size, font_color='black', edge_color='gray')

plt.title('Grafo com 6 Nós e 8 Arestas')
plt.axis('off')  # Desativa os eixos para uma visualização mais limpa

# Salva a figura na pasta "figuras" e remove espaços em branco
plt.savefig('figuras/grafo1.png', format='png', bbox_inches='tight')  
plt.close()  # Fecha a figura para evitar sobreposição

# Gera a matriz de adjacência
adjacency_matrix = nx.adjacency_matrix(G).todense()  # Converte para matriz densa

# Formata a matriz de adjacência para LaTeX
latex_matrix = "\\[\nA = \n\\begin{array}{c|ccccccc}\n"
latex_matrix += "    & " + " & ".join([str(i) for i in range(G.number_of_nodes())]) + " \\\\\n"
latex_matrix += "    \\hline\n"

for i in range(G.number_of_nodes()):
    row = [str(int(adjacency_matrix[i, j])) for j in range(G.number_of_nodes())]
    latex_matrix += f"    {i} & " + " & ".join(row) + " \\\\\n"

latex_matrix += "\\end{array}\n\\]"

# Exibe a matriz em formato LaTeX
print("Matriz de Adjacência em LaTeX:")
print(latex_matrix)

# Mostra uma mensagem de confirmação
print("Figura salva na pasta 'figuras' como 'grafo_6_nos_8_arestas.png'.")
