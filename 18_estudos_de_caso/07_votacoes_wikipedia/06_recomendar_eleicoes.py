# Aplicacao adicional - Rede de votacoes da Wikipedia. Passo 6: que eleicoes mostrar a cada usuario?
# Uma decisao sobre o processo, nao sobre pessoas: no painel de "eleicoes em andamento", mostrar a cada usuario
# experiente as 10 eleicoes em que ele tem mais chance de querer participar. A base nao tem o sentido do voto,
# entao o sistema so sugere ONDE participar, nunca em quem votar.
# Avaliacao (padrao em sistemas de recomendacao): para cada usuario com >= 10 votos, escondemos 20% das eleicoes
# em que ele votou; cada metodo, vendo so o resto, sugere 10 eleicoes; contamos quantas das escondidas acertou.
#   - popularidade: as 10 eleicoes com mais votos (o que um painel simples mostraria);
#   - eleitores parecidos: eleicoes que tiveram muitos eleitores em comum com as que o usuario ja votou
#     (similaridade de cosseno entre eleicoes, calculada so com os votos visiveis).
# Tambem medimos dois efeitos colaterais: concentracao nos candidatos mais populares e "bolha" (fracao das
# sugestoes dentro da propria comunidade do usuario, comparada com a fracao dos votos reais escondidos).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import sparse

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
arcos = pd.read_csv(os.path.join(pasta, 'dados', 'Wiki-Vote.txt'), sep='\t', comment='#', names=['de', 'para'])
comunidade = pd.read_csv(os.path.join(pasta, 'dados', 'comunidades.csv'), index_col=0)['comunidade']
gerador = np.random.default_rng(0)

ativos = arcos.groupby('de').size()
ativos = ativos[ativos >= 10].index
arcos['oculto'] = arcos['de'].isin(ativos) & (gerador.random(len(arcos)) < 0.2)
visiveis, ocultos = arcos[~arcos['oculto']], arcos[arcos['oculto']]
print(f'Usuarios avaliados (>= 10 votos): {len(ativos)} | votos escondidos: {len(ocultos)} de {len(arcos)}')

eleitores = {u: i for i, u in enumerate(sorted(arcos['de'].unique()))}
candidatos = sorted(arcos['para'].unique())
indice = {c: j for j, c in enumerate(candidatos)}
M = sparse.csr_matrix((np.ones(len(visiveis)), (visiveis['de'].map(eleitores), visiveis['para'].map(indice))),
                      shape=(len(eleitores), len(candidatos)))
popularidade = np.asarray(M.sum(axis=0)).ravel()
norma = np.sqrt(popularidade) + 1e-9
similaridade = (M.T @ M).toarray().astype(float) / norma[:, None] / norma[None, :]
np.fill_diagonal(similaridade, 0)
top50 = set(np.argsort(-popularidade)[:50])
comunidade_cand = np.array([comunidade.get(c, -1) for c in candidatos])

k = 10
resultados = {m: {'acerto': [], 'populares': [], 'na_comunidade': []} for m in ['popularidade', 'eleitores parecidos', 'parecidos com 3 vagas de fora', 'sorteio']}
real_na_comunidade = []
for usuario, alvo in ocultos.groupby('de')['para']:
    alvo = set(alvo.map(indice))
    i = eleitores[usuario]
    ja_votou = M[i].indices
    sua = comunidade.get(usuario, -2)
    real_na_comunidade.append(np.mean([comunidade_cand[j] == sua for j in alvo]))
    for metodo in resultados:
        if metodo == 'popularidade':
            escore = popularidade.astype(float).copy()
        elif metodo in ('eleitores parecidos', 'parecidos com 3 vagas de fora'):
            escore = similaridade[ja_votou].sum(axis=0)
        else:
            escore = gerador.random(len(candidatos))
        escore[ja_votou] = -np.inf
        if metodo == 'parecidos com 3 vagas de fora':
            # 7 sugestoes livres + 3 reservadas a eleicoes de fora da comunidade do usuario (contra o efeito bolha)
            fora = np.where(comunidade_cand != sua, escore, -np.inf)
            reservadas = np.argsort(-fora)[:3]
            livres = [j for j in np.argsort(-escore) if j not in set(reservadas)][:k - 3]
            sugeridas = np.array(list(livres) + list(reservadas))
        else:
            sugeridas = np.argpartition(-escore, k)[:k]
        resultados[metodo]['acerto'].append(len(set(sugeridas) & alvo) / min(k, len(alvo)))
        resultados[metodo]['populares'].append(len(set(sugeridas) & top50) / k)
        resultados[metodo]['na_comunidade'].append(np.mean(comunidade_cand[sugeridas] == sua))

tabela = pd.DataFrame({m: {'acerto@10': np.mean(r['acerto']), 'sugestoes entre os 50 mais populares': np.mean(r['populares']),
                           'sugestoes na propria comunidade': np.mean(r['na_comunidade'])} for m, r in resultados.items()}).T
print(tabela.round(3).to_string())
print(f'Votos reais escondidos na propria comunidade do usuario: {np.mean(real_na_comunidade):.1%}')
a, b = tabela.loc['eleitores parecidos', 'acerto@10'], tabela.loc['popularidade', 'acerto@10']
print(f'Eleitores parecidos x popularidade: {a:.1%} x {b:.1%} das sugestoes certas ({a / b:.1f} vezes)')
# Intervalo por reamostragem dos usuarios
acertos = np.array(resultados['eleitores parecidos']['acerto']) - np.array(resultados['popularidade']['acerto'])
reamostras = [gerador.choice(acertos, len(acertos)).mean() for _ in range(2000)]
c = tabela.loc['parecidos com 3 vagas de fora', 'acerto@10']
print(f'Com 3 vagas de fora: acerto {c:.1%}; sugestoes na propria comunidade {tabela.loc["parecidos com 3 vagas de fora", "sugestoes na propria comunidade"]:.1%}')
print(f'Diferenca de acerto (parecidos - popularidade): {acertos.mean():.1%}, IC 95% [{np.percentile(reamostras, 2.5):.1%}; {np.percentile(reamostras, 97.5):.1%}]')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.3))
cores = ['#8794A3', '#2F648F', '#168A8A', '#C9D3DD']
rotulos = ['popularidade', 'eleitores\nparecidos', 'parecidos +\n3 vagas de fora', 'sorteio']
esq.bar(rotulos, 100 * tabela['acerto@10'], color=cores)
for i, v in enumerate(tabela['acerto@10']):
    esq.text(i, 100 * v + 0.4, f'{v:.1%}', ha='center')
esq.set_ylabel('% das 10 sugestões que o usuário de fato votou')
esq.set_title('Acerto nas eleições escondidas', fontsize=11)
x = np.arange(len(tabela))
dir.bar(x - 0.2, 100 * tabela['sugestoes entre os 50 mais populares'], width=0.4, color='#D69A35', label='entre os 50 candidatos mais populares')
dir.bar(x + 0.2, 100 * tabela['sugestoes na propria comunidade'], width=0.4, color='#168A8A', label='na comunidade do próprio usuário')
dir.axhline(100 * np.mean(real_na_comunidade), color='#168A8A', linestyle='--', linewidth=1)
dir.text(3.45, 100 * np.mean(real_na_comunidade) + 2, 'votos reais na própria comunidade', color='#168A8A', ha='right', fontsize=8.5)
dir.set_xticks(x, rotulos)
dir.set_ylabel('% das sugestões')
dir.set_title('Efeitos colaterais: concentração e bolha', fontsize=11)
dir.legend(fontsize=8.5, loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '06_recomendar_eleicoes.png'))
plt.show()
