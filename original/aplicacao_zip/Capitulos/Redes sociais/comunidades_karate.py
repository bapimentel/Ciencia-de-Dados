import networkx as nx
import matplotlib.pyplot as plt
from community import community_louvain
from node2vec import Node2Vec
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
import os

# Criação da pasta "figuras" se não existir
if not os.path.exists("figuras"):
    os.makedirs("figuras")

# Carregar o grafo do Karate Club
G = nx.karate_club_graph()

# Métodos de detecção de comunidades
metodos = {
    "Louvain": community_louvain.best_partition,
    "Newman": None,  # Placeholder para Newman
    "K-Means": None,  # Placeholder para K-Means
    "Spectral": None  # Placeholder para Spectral
}

# Detectar comunidades usando o método Louvain
particoes = metodos["Louvain"](G)
cores_louvain = [particoes[n] for n in G.nodes()]

# Visualizar e salvar o gráfico de Louvain
pos = nx.spring_layout(G)
plt.figure(figsize=(12, 8))
nx.draw(G, pos, node_color=cores_louvain, with_labels=True, font_weight='bold', node_size=700, font_size=10, cmap=plt.cm.Set3)

# Adicionando uma legenda para as comunidades
for community_id in set(cores_louvain):
    plt.scatter([], [], color=plt.cm.Set3(community_id / max(cores_louvain)), label=f'Comunidade {community_id + 1}')

plt.legend(scatterpoints=1, loc='best', fontsize=16)  # Aumentando o tamanho da fonte da legenda
plt.title("Rede Social do Karate Club - Método Louvain")
plt.savefig("figuras/grafo_redesocial_louvain.png", format='png')
plt.close()

print("Figura salva em 'figuras/grafo_redesocial_louvain.png'")

# Detectar comunidades usando o método Newman (Girvan-Newman)
comunidades_newman = list(nx.community.girvan_newman(G))
comunidades_newman = list(comunidades_newman[0])

# Atribuindo cores a cada nó com base nas comunidades
cores_newman = []
for n in G.nodes():
    for idx, comunidade in enumerate(comunidades_newman):
        if n in comunidade:
            cores_newman.append(idx)
            break

# Visualizar e salvar o gráfico de Newman
plt.figure(figsize=(12, 8))
nx.draw(G, pos, node_color=cores_newman, with_labels=True, font_weight='bold', node_size=700, font_size=10, cmap=plt.cm.Set3)

# Adicionando uma legenda para as comunidades
for community_id in set(cores_newman):
    plt.scatter([], [], color=plt.cm.Set3(community_id / max(cores_newman)), label=f'Comunidade {community_id + 1}')

plt.legend(scatterpoints=1, loc='best', fontsize=16)  # Aumentando o tamanho da fonte da legenda
plt.title("Rede Social do Karate Club - Método Newman (Girvan-Newman)")
plt.savefig("figuras/grafo_redesocial_newman.png", format='png')
plt.close()

print("Figura salva em 'figuras/grafo_redesocial_newman.png'")

# Gerar embeddings usando Node2Vec
node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=4)
model = node2vec.fit()

# Obter os vetores dos nós
X = [model.wv[str(node)] for node in G.nodes()]

# Aplicar K-Means
kmeans = KMeans(n_clusters=3)  # Ajuste o número de clusters conforme necessário
kmeans.fit(X)
cores_kmeans = kmeans.labels_

# Visualizar e salvar o gráfico de K-Means
plt.figure(figsize=(12, 8))
nx.draw(G, pos, node_color=cores_kmeans, with_labels=True, font_weight='bold', node_size=700, font_size=10, cmap=plt.cm.Set3)

# Adicionando uma legenda para as comunidades
for community_id in set(cores_kmeans):
    plt.scatter([], [], color=plt.cm.Set3(community_id / max(cores_kmeans)), label=f'Comunidade {community_id + 1}')

plt.legend(scatterpoints=1, loc='best', fontsize=16)  # Aumentando o tamanho da fonte da legenda
plt.title("Rede Social do Karate Club - Método K-Means")
plt.savefig("figuras/grafo_redesocial_kmeans.png", format='png')
plt.close()

print("Figura salva em 'figuras/grafo_redesocial_kmeans.png'")

# Aplicar o método Spectral Clustering
spectral = SpectralClustering(n_clusters=3, affinity='precomputed')
adjacency_matrix = nx.to_numpy_array(G)  # Obter a matriz de adjacência
spectral.fit(adjacency_matrix)
cores_spectral = spectral.labels_

# Visualizar e salvar o gráfico de Spectral Clustering
plt.figure(figsize=(12, 8))
nx.draw(G, pos, node_color=cores_spectral, with_labels=True, font_weight='bold', node_size=700, font_size=10, cmap=plt.cm.Set3)

# Adicionando uma legenda para as comunidades
for community_id in set(cores_spectral):
    plt.scatter([], [], color=plt.cm.Set3(community_id / max(cores_spectral)), label=f'Comunidade {community_id + 1}')

plt.legend(scatterpoints=1, loc='best', fontsize=16)  # Aumentando o tamanho da fonte da legenda
plt.title("Rede Social do Karate Club - Método Spectral Clustering")
plt.savefig("figuras/grafo_redesocial_spectral.png", format='png')
plt.close()

print("Figura salva em 'figuras/grafo_redesocial_spectral.png'")
