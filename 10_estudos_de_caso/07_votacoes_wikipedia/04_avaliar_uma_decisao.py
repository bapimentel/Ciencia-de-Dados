# Aplicacao adicional - Rede de votacoes da Wikipedia. Etapa 4: que decisao e legitima com esta rede?
# A pergunta original ("ha coordenacao ou abuso nas votacoes?") NAO pode ser respondida: nao ha direcao do
# voto, data, nem resultado. O que a estrutura permite e priorizar uma revisao exploratoria e desenhar a
# coleta de dados que responderia a pergunta. Nenhum usuario e acusado por uma metrica.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

metricas = pd.read_csv(os.path.join(pasta, 'dados', 'centralidades.csv'), index_col=0)
comunidades = pd.read_csv(os.path.join(pasta, 'dados', 'comunidades.csv'), index_col=0)['comunidade']
arcos = pd.read_csv(os.path.join(pasta, 'dados', 'Wiki-Vote.txt'), sep='\t', comment='#', names=['de', 'para'])

# Um padrao estrutural que vale olhar: usuarios que votam muito e quase so dentro da propria comunidade
arcos['com_de'] = arcos['de'].map(comunidades)
arcos['com_para'] = arcos['para'].map(comunidades)
arcos = arcos.dropna()
por_usuario = arcos.groupby('de').agg(votos=('para', 'size'), dentro=('com_para', lambda s: (s == arcos.loc[s.index, 'com_de']).mean()))
geral = (arcos['com_de'] == arcos['com_para']).mean()
print(f'Fracao de votos dentro da propria comunidade, no geral: {geral:.2f}')
print(por_usuario['dentro'].describe().round(2))

# Criterio exploratorio (nao de culpa): pelo menos 30 votos dados e mais de 90% dentro da propria comunidade
candidatos = por_usuario[(por_usuario['votos'] >= 30) & (por_usuario['dentro'] > 0.9)]
print(f'\nUsuarios com >= 30 votos e > 90% dentro da propria comunidade: {len(candidatos)} de {(por_usuario["votos"] >= 30).sum()} com >= 30 votos')
print(candidatos.sort_values('votos', ascending=False).head(10).round(2))
# Esse padrao e compativel com varias explicacoes inocentes: votar nas eleicoes da propria area de interesse,
# ou de um periodo em que o usuario esteve ativo. So os dados que faltam (datas, direcao do voto) separariam isso.

fig, eixo = plt.subplots(figsize=(8, 4.2))
ativos = por_usuario[por_usuario['votos'] >= 5]
eixo.scatter(ativos['votos'], ativos['dentro'], s=8, alpha=0.4, color='#8794A3')
eixo.scatter(candidatos['votos'], candidatos['dentro'], s=14, color='#D69A35', label=f'critério exploratório (n={len(candidatos)})')
eixo.axhline(geral, color='#2F648F', linestyle='--', label=f'fração geral dentro da comunidade ({geral:.2f})')
eixo.set_xscale('log')
eixo.set_xlabel('Votos dados (escala log)')
eixo.set_ylabel('Fração dos votos dentro da própria comunidade')
eixo.set_title('Usuários com muitos votos concentrados em uma comunidade: ponto de partida, não conclusão')
eixo.legend(loc='lower left')
plt.savefig(os.path.join(pasta, 'figuras', '04_criterio_exploratorio.png'))
plt.show()

print(f'''
Achado: a rede tem cauda longa (poucos usuarios recebem ou dao centenas de votos), reciprocidade baixa (6%),
cinco comunidades grandes e porosas (modularidade 0,43 contra 0,13 em rede aleatoria equivalente, mas com
40% a 58% de arestas internas) e {geral:.0%} dos votos ficam dentro da propria comunidade.
Isso sugere que a estrutura sozinha nao separa comportamento coordenado de participacao normal por
area de interesse. Nao ha decisao legitima sobre usuarios a tomar com estes dados.
O que e legitimo: (1) usar um criterio estrutural transparente para escolher POR ONDE COMECAR uma
revisao exploratoria ({len(candidatos)} usuarios com >= 30 votos e > 90% na propria comunidade); (2) desenhar a
coleta complementar: data de cada voto, direcao (apoio/oposicao), resultado da eleicao e a sequencia
temporal dos votos. Com datas e direcao, a pergunta "votos em bloco no mesmo intervalo?" passa a ser testavel.
Avaliacao (proposta, so apos a coleta): fracao de eleicoes em que um subconjunto fixo de usuarios vota no
mesmo sentido em menos de uma hora, comparada com a esperada por acaso dado o volume de cada um
(metrica principal); tempo mediano entre votos do mesmo grupo (auxiliar).
Limites: recorte ate 2008, sem datas; comunidades vem de um algoritmo com semente e mudam com ela;
centralidade descreve posicao, nunca intencao. Nenhum usuario deve ser nomeado a partir desta analise.
''')
