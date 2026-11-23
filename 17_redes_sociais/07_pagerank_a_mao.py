# PageRank calculado a mao, por iteracao de potencia, numa rede direcionada de 5 paginas (ou pessoas).
# Ideia: um "navegador aleatorio" segue um link ao acaso com probabilidade d (0,85) e, com probabilidade 1 - d,
# pula para qualquer no. O PageRank de um no e a fracao do tempo que o navegador passa nele.
#   PR(v) = (1 - d)/N + d * soma, sobre os nos u que apontam para v, de PR(u) / grau_de_saida(u)
# Ser apontado por muitos conta; ser apontado por quem e importante (e aponta para poucos) conta mais.

import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

nos = ['A', 'B', 'C', 'D', 'E']
arcos = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'A'), ('D', 'C'), ('E', 'C'), ('E', 'D'), ('D', 'E')]
G = nx.DiGraph(arcos)
N, d = len(nos), 0.85
grau_saida = {v: G.out_degree(v) for v in nos}
print('Grau de entrada:', {v: G.in_degree(v) for v in nos})
print('Grau de saida:  ', grau_saida)

pr = {v: 1 / N for v in nos}                   # comeca com todos iguais
historico = [list(pr.values())]
for iteracao in range(1, 51):
    novo = {v: (1 - d) / N + d * sum(pr[u] / grau_saida[u] for u in G.predecessors(v)) for v in nos}
    mudanca = sum(abs(novo[v] - pr[v]) for v in nos)
    pr = novo
    historico.append(list(pr.values()))
    if iteracao <= 3:
        print(f'Iteracao {iteracao}: ' + '  '.join(f'{v}={pr[v]:.3f}' for v in nos))
    if mudanca < 1e-8:
        print(f'Convergiu na iteracao {iteracao} (mudanca total {mudanca:.1e})')
        break
referencia = nx.pagerank(G, alpha=d)
print('\nPageRank final:')
for v in sorted(nos, key=pr.get, reverse=True):
    print(f'  {v}: a mao {pr[v]:.4f} | networkx {referencia[v]:.4f} | grau de entrada {G.in_degree(v)}')
# C recebe 4 links e fica em 1o. A recebe so 1 link, mas vem de C (o mais importante), e C so aponta para A:
# por isso A fica a frente de B, D e E, mesmo com o mesmo grau de entrada que eles.

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={'width_ratios': [1, 1.3]})
posicao = {'A': (0, 1), 'B': (1, 1.6), 'C': (1, 0.4), 'D': (2.2, 0.1), 'E': (2.2, 1.1)}
tamanhos = [9000 * pr[v] for v in G.nodes()]
nx.draw_networkx_edges(G, posicao, ax=esq, edge_color='#8794A3', arrowsize=18, node_size=tamanhos,
                       connectionstyle='arc3,rad=0.12')
nx.draw_networkx_nodes(G, posicao, ax=esq, node_size=tamanhos, node_color='#2F648F', edgecolors='white')
nx.draw_networkx_labels(G, posicao, ax=esq, labels={v: f'{v}\n{pr[v]:.2f}' for v in G.nodes()}, font_color='white', font_size=9)
esq.set_title('Tamanho do nó proporcional ao PageRank', fontsize=11)
esq.axis('off')
esq.margins(0.15)
historico = np.array(historico)
for j, v in enumerate(nos):
    dir.plot(historico[:, j], marker='o', markersize=3, label=v)
dir.set_xlabel('Iteração')
dir.set_ylabel('PageRank')
dir.set_title('Iteração de potência: os valores se estabilizam rapidamente', fontsize=11)
dir.legend(ncol=5, loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'pagerank_a_mao.png'))
plt.show()
