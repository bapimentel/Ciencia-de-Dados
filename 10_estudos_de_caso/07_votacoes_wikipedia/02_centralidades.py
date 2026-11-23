# Aplicacao adicional - Rede de votacoes da Wikipedia. Etapa 2: centralidades em um grafo dirigido grande.
# Pergunta: quem ocupa posicao central segundo definicoes diferentes, e as definicoes concordam?

import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

arcos = pd.read_csv(os.path.join(pasta, 'dados', 'Wiki-Vote.txt'), sep='\t', comment='#', names=['de', 'para'])
G = nx.from_pandas_edgelist(arcos, 'de', 'para', create_using=nx.DiGraph())

metricas = pd.DataFrame({
    'votos recebidos': dict(G.in_degree()),
    'votos dados': dict(G.out_degree()),
    'pagerank': nx.pagerank(G, alpha=0.85),
})
# Intermediacao exata em 7 mil nos demora; usamos uma amostra de 400 fontes (k) com semente, que da uma estimativa
metricas['intermediacao (aprox.)'] = pd.Series(nx.betweenness_centrality(G, k=400, seed=0))
print('Calculado. Dez primeiros por cada metrica:')
for coluna in metricas.columns:
    top = metricas[coluna].sort_values(ascending=False).head(10)
    print(f'\n{coluna}: ', ', '.join(f'{int(no)} ({valor:.3g})' for no, valor in top.items()))

# As listas concordam?
tops = {c: set(metricas[c].sort_values(ascending=False).head(50).index) for c in metricas.columns}
print('\nSobreposicao entre os 50 primeiros de cada metrica:')
nomes = list(tops)
for i in range(len(nomes)):
    for j in range(i + 1, len(nomes)):
        print(f'  {nomes[i]} x {nomes[j]}: {len(tops[nomes[i]] & tops[nomes[j]])} em comum')
print('\nCorrelacao de Spearman entre as metricas:')
print(metricas.corr(method='spearman').round(2))
# PageRank acompanha de perto os votos recebidos (e construido a partir dos arcos de entrada).
# Votos dados e uma coisa diferente: quem vota muito nao e quem recebe muito.

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4))
esq.scatter(metricas['votos recebidos'], metricas['pagerank'], s=6, alpha=0.4, color='#2F648F')
esq.set_xscale('symlog')
esq.set_yscale('log')
esq.set_xlabel('Votos recebidos')
esq.set_ylabel('PageRank')
esq.set_title('PageRank cresce com os votos recebidos, com dispersão')
dir.scatter(metricas['votos dados'], metricas['votos recebidos'], s=6, alpha=0.4, color='#8794A3')
dir.set_xscale('symlog')
dir.set_yscale('symlog')
dir.set_xlabel('Votos dados')
dir.set_ylabel('Votos recebidos')
dir.set_title('Dar e receber votos são papéis diferentes na rede')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '02_centralidades.png'))
plt.show()

metricas.to_csv(os.path.join(pasta, 'dados', 'centralidades.csv'))
print('\nSalvo: dados/centralidades.csv')
# Nenhuma dessas metricas diz se um usuario e "bom" administrador, se votou a favor ou contra, ou se
# agiu de forma coordenada. Elas descrevem posicao na estrutura, so isso.
