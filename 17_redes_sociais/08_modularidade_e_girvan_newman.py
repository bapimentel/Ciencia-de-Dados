# Modularidade a mao e o algoritmo de Girvan-Newman passo a passo, no clube de karate.
# Modularidade Q = soma, sobre as comunidades c, de [ L_c / m - (D_c / 2m)^2 ]
#   L_c = arestas dentro de c;  D_c = soma dos graus dos nos de c;  m = total de arestas
#   (fracao de arestas internas) - (fracao esperada se as arestas fossem sorteadas mantendo os graus)
# Girvan-Newman: calcula a intermediacao de cada ARESTA, remove a maior e repete; cada vez que a rede se
# parte, ha uma nova divisao. Escolhemos a divisao de maior modularidade.

import os
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
G = nx.karate_club_graph()          # usamos a versao sem pesos: cada aresta conta 1
m = G.number_of_edges()
lado_real = [{n for n in G if G.nodes[n]['club'] == 'Mr. Hi'}, {n for n in G if G.nodes[n]['club'] != 'Mr. Hi'}]


def modularidade_a_mao(grupos):
    total = 0.0
    for c in grupos:
        internas = G.subgraph(c).number_of_edges()
        soma_graus = sum(dict(G.degree(c)).values())
        parcela = internas / m - (soma_graus / (2 * m)) ** 2
        total += parcela
        print(f'    comunidade de {len(c):2d} nos: {internas:2d} arestas internas, soma dos graus {soma_graus:3d} -> '
              f'{internas}/{m} - ({soma_graus}/{2 * m})^2 = {parcela:+.4f}')
    return total


print('Divisao real do clube em dois lados:')
q_real = modularidade_a_mao(lado_real)
print(f'  Q = {q_real:.4f} (networkx: {nx.community.modularity(G, lado_real, weight=None):.4f})')
print('Todos numa comunidade so:')
print(f'  Q = {modularidade_a_mao([set(G.nodes())]):.4f}  (nenhuma estrutura alem do acaso)')

# Girvan-Newman passo a passo
H = G.copy()
divisoes = []
removidas = 0
componentes = nx.number_connected_components(H)
print('\nGirvan-Newman: arestas removidas ate cada nova divisao')
while H.number_of_edges() > 0:
    intermediacao = nx.edge_betweenness_centrality(H)
    aresta = max(intermediacao, key=intermediacao.get)
    H.remove_edge(*aresta)
    removidas += 1
    if removidas <= 5:
        print(f'  remocao {removidas}: aresta {aresta} (intermediacao {intermediacao[aresta]:.3f})')
    if nx.number_connected_components(H) > componentes:
        componentes = nx.number_connected_components(H)
        grupos = [set(c) for c in nx.connected_components(H)]
        divisoes.append((removidas, componentes, nx.community.modularity(G, grupos, weight=None), grupos))
        if componentes <= 6:
            print(f'  -> apos {removidas} remocoes: {componentes} comunidades, Q = {divisoes[-1][2]:.4f}')
    if componentes >= 12:
        break
melhor = max(divisoes, key=lambda x: x[2])
print(f'\nMaior modularidade: {melhor[1]} comunidades (Q = {melhor[2]:.4f}), apos {melhor[0]} remocoes')
print('Tamanhos:', sorted(len(c) for c in melhor[3]))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.6))
esq.plot([d[1] for d in divisoes], [d[2] for d in divisoes], marker='o', color='#2F648F')
esq.axhline(q_real, color='#D69A35', linestyle='--', label=f'divisão real em 2 lados (Q = {q_real:.3f})')
esq.scatter(melhor[1], melhor[2], s=150, facecolor='none', edgecolor='#BD5B58', linewidth=2, zorder=3)
esq.set_xlabel('Número de comunidades')
esq.set_ylabel('Modularidade Q')
esq.set_title('Girvan-Newman: a modularidade sobe, atinge o máximo e cai', fontsize=11)
esq.legend(loc='lower center')
paleta = ['#2F648F', '#D69A35', '#168A8A', '#BD5B58', '#8794A3', '#20324A', '#7A9CC6']
cor = {n: paleta[i % len(paleta)] for i, c in enumerate(melhor[3]) for n in c}
posicao = nx.spring_layout(G, seed=4)
nx.draw_networkx_edges(G, posicao, ax=dir, edge_color='#E6EBF0')
nx.draw_networkx_nodes(G, posicao, ax=dir, node_color=[cor[n] for n in G], node_size=230, edgecolors='white')
nx.draw_networkx_labels(G, posicao, ax=dir, font_size=7, font_color='white', font_weight='bold')
dir.set_title(f'Divisão de maior modularidade: {melhor[1]} comunidades', fontsize=11)
dir.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'girvan_newman_modularidade.png'))
plt.show()
