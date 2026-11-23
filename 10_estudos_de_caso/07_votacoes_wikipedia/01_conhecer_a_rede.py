# Aplicacao adicional - Rede de votacoes da Wikipedia. Etapa 1: conhecer a rede.
# Base: Wikipedia vote network (Stanford SNAP), https://snap.stanford.edu/data/wiki-Vote.html
# Votacoes para promocao de usuarios a administrador ate janeiro de 2008. Um arco A -> B significa que o
# usuario A votou na eleicao de B. NAO e amizade, nem "seguir", nem influencia: e um voto em uma eleicao.
# O arquivo dados/Wiki-Vote.txt veio com o material do livro e corresponde ao arquivo do SNAP (7115 nos, 103689 arcos).

import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

# Ler os arcos, pulando as linhas de comentario
arcos = pd.read_csv(os.path.join(pasta, 'dados', 'Wiki-Vote.txt'), sep='\t', comment='#', names=['de', 'para'])
print('Arcos lidos:', len(arcos))
G = nx.from_pandas_edgelist(arcos, 'de', 'para', create_using=nx.DiGraph())
print('Nos:', G.number_of_nodes(), '| arcos:', G.number_of_edges(), '| confere com o cabecalho do SNAP (7115, 103689)')

# Grau de saida = votos dados; grau de entrada = votos recebidos
saida = pd.Series(dict(G.out_degree()), name='votos dados')
entrada = pd.Series(dict(G.in_degree()), name='votos recebidos')
print('\nVotos dados por usuario:')
print(saida.describe().round(1))
print('\nVotos recebidos por usuario:')
print(entrada.describe().round(1))

so_votam = ((saida > 0) & (entrada == 0)).sum()
so_recebem = ((saida == 0) & (entrada > 0)).sum()
ambos = ((saida > 0) & (entrada > 0)).sum()
print(f'\nUsuarios que so votaram: {so_votam} | que so receberam votos (candidatos que nao votaram): {so_recebem} | ambos: {ambos}')

# Reciprocidade e componentes
print('Reciprocidade (fracao de arcos com arco de volta):', round(nx.reciprocity(G), 3))
fraco = max(nx.weakly_connected_components(G), key=len)
forte = max(nx.strongly_connected_components(G), key=len)
print(f'Maior componente fracamente conexo: {len(fraco)} nos ({len(fraco) / G.number_of_nodes():.0%}); fortemente conexo: {len(forte)} nos')
print('Densidade:', round(nx.density(G), 4))

# Distribuicoes de grau em escala log-log: poucos usuarios com muitos votos, muitos com poucos
fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
for eixo, serie, titulo, cor in [(esq, entrada[entrada > 0], 'Votos recebidos (grau de entrada)', '#2F648F'),
                                 (dir, saida[saida > 0], 'Votos dados (grau de saída)', '#168A8A')]:
    contagem = serie.value_counts().sort_index()
    eixo.scatter(contagem.index, contagem.values, s=12, color=cor)
    eixo.set_xscale('log')
    eixo.set_yscale('log')
    eixo.set_xlabel('grau')
    eixo.set_ylabel('usuários')
    eixo.set_title(f'{titulo}: máximo {serie.max()}')
fig.suptitle('Distribuições de grau com cauda longa (escalas logarítmicas)', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '01_distribuicao_grau.png'))
plt.show()

# O que a base NAO tem: a direcao do voto (a favor ou contra), a data, o resultado da eleicao, quem venceu.
# Com isso, "receber muitos votos" nao significa ser aprovado, e "dar muitos votos" nao significa influencia.
