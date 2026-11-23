import os
import networkx as nx
import matplotlib.pyplot as plt

# Cria a pasta "figuras" se não existir
if not os.path.exists("figuras"):
    os.makedirs("figuras")

# Cria um grafo de exemplo
G = nx.erdos_renyi_graph(20, 0.4, seed=42)

# Calcula as diferentes centralidades e coeficientes
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
pagerank = nx.pagerank(G)
clustering_coefficient = nx.clustering(G)

# Cria um gráfico simples para visualizar o grafo
pos = nx.spring_layout(G)  # Define a posição dos nós

# Função auxiliar para desenhar e salvar o grafo com diferentes métricas
def draw_and_save_graph(G, metric_dict, title, filename):
    plt.figure(figsize=(8, 6))
    nodes = nx.draw_networkx_nodes(G, pos, node_color=list(metric_dict.values()), 
                                   node_size=[v * 2000 for v in metric_dict.values()], 
                                   cmap=plt.cm.Blues)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    
    plt.title(title)
    plt.colorbar(nodes)  # Associa o mapa de cores aos nós
    plt.savefig(f'figuras/{filename}.png', format='png')  # Salva a figura na pasta "figuras"
    plt.close()  # Fecha a figura para evitar sobreposição

# Desenha o grafo com diferentes métricas e salva cada gráfico na pasta "figuras"
draw_and_save_graph(G, degree_centrality, 'Centralidade de Grau', 'grafo_grau')
draw_and_save_graph(G, closeness_centrality, 'Centralidade de Proximidade', 'grafo_proximidade')
draw_and_save_graph(G, betweenness_centrality, 'Centralidade de Intermediação', 'grafo_intermediacao')
draw_and_save_graph(G, pagerank, 'PageRank', 'grafo_pagerank')
draw_and_save_graph(G, clustering_coefficient, 'Coeficiente de Agrupamento', 'grafo_agrupamento')

# Mostra as métricas no console para comparação
print("Centralidade de Grau:", degree_centrality)
print("Centralidade de Proximidade:", closeness_centrality)
print("Centralidade de Intermediação:", betweenness_centrality)
print("PageRank:", pagerank)
print("Coeficiente de Agrupamento:", clustering_coefficient)
