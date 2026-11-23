# Metricas locais: grau, proximidade, intermediacao, PageRank e coeficiente de agrupamento.
# Layout com semente fixa: a figura e a mesma a cada execucao.

import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# Grafo aleatorio: 20 nos, probabilidade 0,4 de aresta, semente 42
G = nx.erdos_renyi_graph(20, 0.4, seed=42)
print('Nos:', G.number_of_nodes(), '| Arestas:', G.number_of_edges())

metricas = pd.DataFrame({
    'grau': nx.degree_centrality(G),               # fracao dos outros nos a que esta ligado
    'proximidade': nx.closeness_centrality(G),     # 1 / distancia media ate os demais
    'intermediacao': nx.betweenness_centrality(G), # fracao dos caminhos mais curtos que passam por ele
    'pagerank': nx.pagerank(G),                    # importancia herdada dos vizinhos importantes
    'agrupamento': nx.clustering(G),               # fracao de pares de vizinhos que tambem sao vizinhos
})
print(metricas.round(3).sort_values('grau', ascending=False).head(8))

print('\nNo mais central segundo cada metrica:')
for coluna in metricas.columns:
    print(f'  {coluna:14s}: no {metricas[coluna].idxmax()} ({metricas[coluna].max():.3f})')
# As metricas nem sempre concordam: um no pode ter poucos vizinhos e ainda assim ser ponte (intermediacao alta).

print('\nCorrelacao entre as metricas:')
print(metricas.corr().round(2))

posicao = nx.spring_layout(G, seed=42)
fig, eixos = plt.subplots(1, 5, figsize=(16, 3.6))
for eixo, coluna in zip(eixos, metricas.columns):
    valores = metricas[coluna]
    tamanho = 100 + 900 * (valores - valores.min()) / (valores.max() - valores.min() + 1e-9)
    nx.draw_networkx_edges(G, posicao, ax=eixo, edge_color='#E6EBF0', width=1)
    nos = nx.draw_networkx_nodes(G, posicao, ax=eixo, node_size=tamanho, node_color=valores, cmap='Blues',
                                 edgecolors='#8794A3', linewidths=0.5)
    nx.draw_networkx_labels(G, posicao, ax=eixo, font_size=7, font_color='#20324A')
    eixo.set_title(f'{coluna}\n(maior: nó {valores.idxmax()})', fontsize=11)
    eixo.axis('off')
fig.suptitle('Cinco maneiras de perguntar "quem é importante?" no mesmo grafo (tamanho e cor = valor da métrica)',
             x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'metricas_locais.png'))
plt.show()

# Experimente: troque o grafo por nx.karate_club_graph(). Os nos 0 e 33 lideram em quais metricas?
