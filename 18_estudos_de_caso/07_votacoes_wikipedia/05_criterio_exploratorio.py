# Aplicacao adicional - Rede de votacoes da Wikipedia. Passo 5: o que distingue os usuarios do criterio estavel?
# O passo 4 encontrou usuarios que votam quase so dentro da propria comunidade em todas as 5 sementes.
# Aqui comparamos esse grupo com os demais usuarios ativos (>= 30 votos), usando as centralidades do passo 2.
# Nenhum usuario e acusado por uma metrica: o objetivo e descrever, e decidir por onde comecar uma revisao.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)
metricas = pd.read_csv(os.path.join(pasta, 'dados', 'centralidades.csv'), index_col=0)
comunidades = pd.read_csv(os.path.join(pasta, 'dados', 'comunidades.csv'), index_col=0)['comunidade']
estaveis = set(pd.read_csv(os.path.join(pasta, 'dados', 'criterio_estavel.csv'))['usuario'])
arcos = pd.read_csv(os.path.join(pasta, 'dados', 'Wiki-Vote.txt'), sep='\t', comment='#', names=['de', 'para'])

arcos['com_de'] = arcos['de'].map(comunidades)
arcos['com_para'] = arcos['para'].map(comunidades)
arcos = arcos.dropna()
arcos['dentro'] = arcos['com_de'] == arcos['com_para']
por_usuario = arcos.groupby('de').agg(votos=('para', 'size'), dentro=('dentro', 'mean'))
geral = arcos['dentro'].mean()
ativos = por_usuario[por_usuario['votos'] >= 30].join(metricas)
ativos['grupo'] = np.where(ativos.index.isin(estaveis), 'critério estável', 'demais ativos')
print(f'Votos dentro da propria comunidade (particao da semente 0): {geral:.0%}')
print(f'Usuarios ativos (>= 30 votos): {len(ativos)} | no criterio estavel: {(ativos["grupo"] == "critério estável").sum()}')
print('\nComparacao (medianas):')
print(ativos.groupby('grupo')[['votos', 'dentro', 'votos recebidos', 'pagerank']].median().round(4).to_string())
print('\nComunidades dos usuarios do criterio estavel:', ativos.loc[ativos['grupo'] == 'critério estável'].index.map(comunidades).value_counts().to_dict())
# Os usuarios do criterio votam menos que os demais ativos e recebem poucos votos: nao sao "lideres" da rede.

fig, eixo = plt.subplots(figsize=(8.5, 4.4))
outros = ativos[ativos['grupo'] == 'demais ativos']
grupo = ativos[ativos['grupo'] == 'critério estável']
eixo.scatter(outros['votos'], outros['dentro'], s=10, alpha=0.4, color='#8794A3', label=f'demais ativos (n={len(outros)})')
eixo.scatter(grupo['votos'], grupo['dentro'], s=18, color='#D69A35', label=f'critério em todas as sementes (n={len(grupo)})')
eixo.axhline(geral, color='#2F648F', linestyle='--', label=f'fração geral ({geral:.2f})')
eixo.set_xscale('log')
eixo.set_xlabel('Votos dados (escala log)')
eixo.set_ylabel('Fração dos votos na própria comunidade')
eixo.set_title('Ponto de partida para uma revisão, não conclusão', fontsize=11)
eixo.legend(loc='lower right', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '05_criterio_exploratorio.png'))
plt.show()
