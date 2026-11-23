# Aplicacao adicional - Rede de votacoes da Wikipedia. Etapa 3: comunidades em uma rede real.
# Pergunta: ha subconjuntos de usuarios que votam mais entre si do que com o resto? Quao nitidos sao?

import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

arcos = pd.read_csv(os.path.join(pasta, 'dados', 'Wiki-Vote.txt'), sep='\t', comment='#', names=['de', 'para'])
G = nx.from_pandas_edgelist(arcos, 'de', 'para', create_using=nx.DiGraph())

# Comunidades sao calculadas na versao nao dirigida do maior componente (a direcao do voto e ignorada aqui)
maior = max(nx.weakly_connected_components(G), key=len)
U = G.subgraph(maior).to_undirected()
print('Componente analisado:', U.number_of_nodes(), 'nos,', U.number_of_edges(), 'arestas (sem direcao)')

comunidades = nx.community.louvain_communities(U, seed=0)
tamanhos = sorted((len(c) for c in comunidades), reverse=True)
modularidade = nx.community.modularity(U, comunidades)
print(f'Louvain: {len(comunidades)} comunidades | modularidade {modularidade:.3f}')
print('Tamanhos das 10 maiores:', tamanhos[:10])
print(f'As 5 maiores reunem {sum(tamanhos[:5]) / U.number_of_nodes():.0%} dos usuarios')

# Referencia: modularidade em uma rede aleatoria com os mesmos graus (modelo de configuracao)
aleatorio = nx.Graph(nx.configuration_model([d for _, d in U.degree()], seed=0))
aleatorio.remove_edges_from(nx.selfloop_edges(aleatorio))
mod_aleatoria = nx.community.modularity(aleatorio, nx.community.louvain_communities(aleatorio, seed=0))
print(f'Modularidade em rede aleatoria com os mesmos graus: {mod_aleatoria:.3f}')
# A modularidade real (cerca de 0,43) fica bem acima da aleatoria (cerca de 0,13): ha estrutura de comunidades.
# Mas ela e porosa: nas comunidades grandes, so 40% a 58% das arestas ficam dentro delas (tabela abaixo).

# Dentro de cada comunidade, que fracao das arestas fica dentro dela?
rotulo = {no: i for i, c in enumerate(comunidades) for no in c}
tabela = []
for i, c in sorted(enumerate(comunidades), key=lambda par: -len(par[1]))[:8]:
    internas = sum(1 for a, b in U.edges(c) if rotulo[a] == rotulo[b])
    total = sum(1 for _ in U.edges(c))
    tabela.append({'comunidade': i, 'usuarios': len(c), 'arestas internas': internas / total})
print('\nFracao de arestas internas nas 8 maiores comunidades:')
print(pd.DataFrame(tabela).round(2).to_string(index=False))

# Figura: tamanhos das comunidades e um recorte dos 300 usuarios de maior grau, coloridos por comunidade
fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={'width_ratios': [1, 1.4]})
esq.bar(range(1, len(tamanhos) + 1), tamanhos, color='#2F648F')
esq.set_xlabel('Comunidade (ordenada por tamanho)')
esq.set_ylabel('Usuários')
esq.set_title(f'{len(comunidades)} comunidades: cinco grandes, duas minúsculas')
principais = [no for no, _ in sorted(U.degree(), key=lambda par: -par[1])[:300]]
S = U.subgraph(principais)
grandes = [i for i, _ in sorted(enumerate(comunidades), key=lambda par: -len(par[1]))[:6]]
paleta = ['#2F648F', '#168A8A', '#D69A35', '#BD5B58', '#7A9CC6', '#20324A']
cor_no = [paleta[grandes.index(rotulo[n])] if rotulo[n] in grandes else '#E6EBF0' for n in S.nodes()]
posicao = nx.spring_layout(S, seed=1, k=0.08)
nx.draw_networkx_edges(S, posicao, ax=dir, edge_color='#E6EBF0', width=0.3, alpha=0.5)
nx.draw_networkx_nodes(S, posicao, ax=dir, node_color=cor_no, node_size=18, linewidths=0)
dir.set_title('300 usuários de maior grau; cor = comunidade: fronteiras porosas')
dir.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_comunidades.png'))
plt.show()

pd.Series(rotulo, name='comunidade').to_csv(os.path.join(pasta, 'dados', 'comunidades.csv'))
print('\nSalvo: dados/comunidades.csv')
# Comunidades aqui sao grupos de usuarios que participaram das mesmas eleicoes: podem refletir epoca,
# area de interesse ou simples coincidencia. Nao e possivel, com estes dados, dizer o que as une.
