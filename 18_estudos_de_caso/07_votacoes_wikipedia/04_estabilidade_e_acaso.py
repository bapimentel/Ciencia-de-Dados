# Aplicacao adicional - Rede de votacoes da Wikipedia. Passo 4: as comunidades sao estaveis? O padrao
# "votar quase so dentro da propria comunidade" e mais frequente do que o acaso produziria?
# (a) Rodamos o Louvain com 5 sementes e comparamos as particoes (informacao mutua normalizada, NMI: 1 = identicas).
# (b) Para cada semente, contamos os usuarios com >= 30 votos e > 90% dos votos na propria comunidade,
#     e verificamos quantos aparecem em TODAS as sementes.
# (c) Referencia de acaso: embaralhamos os destinos dos votos (cada usuario mantem quantos votos deu e cada
#     candidato, quantos recebeu) e contamos quantos usuarios atingiriam o mesmo criterio.

import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics import normalized_mutual_info_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
arcos = pd.read_csv(os.path.join(pasta, 'dados', 'Wiki-Vote.txt'), sep='\t', comment='#', names=['de', 'para'])
G = nx.from_pandas_edgelist(arcos, 'de', 'para', create_using=nx.DiGraph())
maior = max(nx.weakly_connected_components(G), key=len)
U = G.subgraph(maior).to_undirected()
arcos = arcos[arcos['de'].isin(maior) & arcos['para'].isin(maior)].reset_index(drop=True)
nos = sorted(U.nodes())


def criterio(tabela_arcos, rotulo, minimo=30, limite=0.9):
    dentro = tabela_arcos['de'].map(rotulo).values == tabela_arcos['para'].map(rotulo).values
    por_usuario = pd.DataFrame({'de': tabela_arcos['de'], 'dentro': dentro}).groupby('de')['dentro'].agg(['size', 'mean'])
    return set(por_usuario[(por_usuario['size'] >= minimo) & (por_usuario['mean'] > limite)].index), dentro.mean()


particoes, conjuntos = {}, {}
for semente in range(5):
    comunidades = nx.community.louvain_communities(U, seed=semente)
    rotulo = {no: i for i, c in enumerate(comunidades) for no in c}
    particoes[semente] = [rotulo[n] for n in nos]
    conjuntos[semente], fracao = criterio(arcos, rotulo)
    print(f'semente {semente}: {len(comunidades)} comunidades | modularidade {nx.community.modularity(U, comunidades):.3f} | '
          f'votos dentro da comunidade {fracao:.0%} | usuarios no criterio: {len(conjuntos[semente])}')

nmi = [normalized_mutual_info_score(particoes[a], particoes[b]) for a in range(5) for b in range(a + 1, 5)]
print(f'\n(a) NMI entre as particoes de sementes diferentes: de {min(nmi):.2f} a {max(nmi):.2f}')
em_todas = set.intersection(*conjuntos.values())
em_alguma = set.union(*conjuntos.values())
print(f'(b) Usuarios no criterio em pelo menos uma semente: {len(em_alguma)} | em todas as cinco: {len(em_todas)}')

# (c) Acaso: embaralhar os destinos, com a particao da semente 0 fixa
comunidades0 = nx.community.louvain_communities(U, seed=0)
rotulo0 = {no: i for i, c in enumerate(comunidades0) for no in c}
gerador = np.random.default_rng(0)
contagens = []
for _ in range(50):
    embaralhado = arcos.copy()
    embaralhado['para'] = gerador.permutation(embaralhado['para'].values)
    contagens.append(len(criterio(embaralhado, rotulo0)[0]))
print(f'(c) Com destinos embaralhados (50 vezes): usuarios no criterio = de {min(contagens)} a {max(contagens)} '
      f'(real, semente 0: {len(conjuntos[0])})')

pd.Series(sorted(em_todas), name='usuario').to_csv(os.path.join(pasta, 'dados', 'criterio_estavel.csv'), index=False)

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
esq.bar([f'semente {s}' for s in range(5)], [len(conjuntos[s]) for s in range(5)], color='#8794A3', label='no critério nessa semente')
esq.axhline(len(em_todas), color='#2F648F', linewidth=2, label=f'em todas as 5 sementes ({len(em_todas)})')
esq.set_ylabel('Usuários')
esq.set_title('O critério depende da semente do algoritmo', fontsize=11)
esq.legend(loc='lower right')
dir.hist(contagens, bins=range(0, max(max(contagens), len(conjuntos[0])) + 3), color='#C9D3DD', label='destinos embaralhados')
dir.axvline(len(conjuntos[0]), color='#BD5B58', linewidth=2, label=f'rede real ({len(conjuntos[0])})')
dir.set_xlabel('Usuários no critério')
dir.set_ylabel('Simulações')
dir.set_title('Comparação com o acaso', fontsize=11)
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '04_estabilidade_e_acaso.png'))
plt.show()
