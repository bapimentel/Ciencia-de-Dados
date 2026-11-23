import random
import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Cria a pasta "figuras" se não existir
if not os.path.exists("figuras"):
    os.makedirs("figuras")

# Inicializa um grafo vazio
G = nx.Graph()

# Variável para acompanhar o índice dos nós
node_index = 0
cliques = []  # Para armazenar todos os nós de cada clique

# Define cores diferentes para cada clique
colors = plt.cm.viridis(np.linspace(0, 1, 7))  # Gera 7 cores diferentes

# Adiciona cliques de tamanho 1 a 7 ao grafo
for clique_size in range(1, 8):
    # Cria um clique de tamanho clique_size
    clique_nodes = list(range(node_index, node_index + clique_size))
    cliques.append(clique_nodes)  # Armazena os nós do clique
    
    # Adiciona as arestas que formam o clique
    G.add_nodes_from(clique_nodes)
    G.add_edges_from([(clique_nodes[i], clique_nodes[j]) for i in range(clique_size) for j in range(i + 1, clique_size)])
    
    # Conecta o último nó do clique atual ao primeiro nó do próximo clique, se existir
    if clique_size < 7:
        G.add_edge(clique_nodes[-1], node_index + clique_size)
    
    # Atualiza o índice dos nós para o próximo clique
    node_index += clique_size

# Adiciona arestas aleatórias entre os nós de diferentes cliques
num_extra_edges = 10  # Número de arestas extras que você deseja adicionar

# Cria uma lista de todos os nós do grafo
all_nodes = list(G.nodes())

for _ in range(num_extra_edges):
    # Escolhe dois nós aleatórios diferentes
    node_a, node_b = random.sample(all_nodes, 2)

    # Garante que os nós escolhidos não estejam no mesmo clique
    if any(node_a in clique and node_b in clique for clique in cliques):
        continue  # Se estiverem no mesmo clique, escolha novamente

    G.add_edge(node_a, node_b)

# Desenha o grafo gerado
plt.figure(figsize=(8, 8))  # Cria uma nova figura
pos = nx.spring_layout(G, seed=42)  # Layout para a visualização

# Define a cor dos nós com base no clique
node_colors = []
for node in G.nodes():
    for clique_index, clique in enumerate(cliques):
        if node in clique:
            node_colors.append(colors[clique_index])  # Adiciona a cor correspondente ao clique

# Desenha o grafo
nx.draw(G, pos, with_labels=True, node_color=node_colors, 
        node_size=700, font_size=10, font_color='black', edge_color='gray')

# Ajusta a cor dos rótulos com base na cor do nó
for i, node in enumerate(G.nodes()):
    node_color = node_colors[i]
    label_color = 'white' if np.mean(node_color[:3]) < 0.5 else 'black'  # Branco para nós escuros e preto para nós claros
    plt.text(pos[node][0], pos[node][1], str(node), 
             color=label_color, fontsize=10, ha='center', va='center')

plt.title('Grafo contendo cliques de tamanho 1 a 7 com arestas adicionais e cores diferentes')
plt.axis('off')  # Desativa os eixos para uma visualização mais limpa

# Salva a figura na pasta "figuras" e remove espaços em branco
plt.savefig('figuras/grafo_cliques.png', format='png', bbox_inches='tight')  
plt.close()  # Fecha a figura para evitar sobreposição

# Mostra uma mensagem de confirmação
print("Figura salva na pasta 'figuras' como 'grafo_cliques.png'.")
