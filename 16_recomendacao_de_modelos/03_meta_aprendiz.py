# Meta-aprendizado: recomendar um algoritmo para uma base NOVA olhando bases parecidas ja estudadas.
#   meta-exemplo = (meta-caracteristicas da base, desempenho de cada algoritmo nela)
#   meta-aprendiz = k vizinhos mais proximos no espaco das meta-caracteristicas; o ranking recomendado
#                   e o rank medio dos algoritmos nas k bases vizinhas.
# Avaliacao honesta: deixar uma base de fora (leave-one-dataset-out), recomendar sem olhar o desempenho
# dela, e medir quanto se perde em relacao ao melhor algoritmo daquela base.
# Le dados/desempenho.csv (script 01) e dados/metacaracteristicas.csv (script 02).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
desempenho = pd.read_csv(os.path.join(pasta, 'dados', 'desempenho.csv'), index_col=0)
meta = pd.read_csv(os.path.join(pasta, 'dados', 'metacaracteristicas.csv'), index_col=0).loc[desempenho.index]
ranks = desempenho.rank(axis=1, ascending=False)
melhor = desempenho.max(axis=1)

diretas = ['log_exemplos', 'log_atributos', 'classes', 'atributos_por_exemplo', 'entropia_classes',
           'correlacao_media', 'assimetria_media', 'curtose_media']
landmarkers = ['lm_1nn', 'lm_toco', 'lm_lda']


def recomendar(base, colunas, k=5):
    outras = meta.index != base
    treino = meta.loc[outras, colunas]
    media, desvio = treino.mean(), treino.std().replace(0, 1)          # padronizacao so com as outras bases
    z_treino = (treino - media) / desvio
    z_nova = (meta.loc[base, colunas] - media) / desvio
    distancias = np.sqrt(((z_treino - z_nova) ** 2).sum(axis=1))
    vizinhas = distancias.nsmallest(k).index
    return ranks.loc[vizinhas].mean().sort_values().index[0], list(vizinhas)


estrategias = {}
# Referencia 1: escolher sempre o algoritmo de melhor rank medio nas OUTRAS bases
estrategias['sempre o melhor em média'] = [ranks.drop(b).mean().idxmin() for b in desempenho.index]
# Referencia 2: escolher ao acaso (valor esperado = media da perda de todos os algoritmos)
# Meta-aprendiz com tres conjuntos de meta-caracteristicas
for nome, colunas in [('k-NN: diretas', diretas), ('k-NN: landmarkers', landmarkers), ('k-NN: diretas + landmarkers', diretas + landmarkers)]:
    estrategias[nome] = [recomendar(b, colunas)[0] for b in desempenho.index]

linhas = []
perdas = {}
for nome, escolhas in estrategias.items():
    perda = np.array([melhor[b] - desempenho.loc[b, a] for b, a in zip(desempenho.index, escolhas)])
    perdas[nome] = perda
    linhas.append({'estrategia': nome, 'perda media': perda.mean(), 'perda mediana': np.median(perda),
                   'acertou o melhor': np.mean(perda == 0), 'perda > 5 pontos': np.mean(perda > 0.05)})
perda_acaso = (melhor.values[:, None] - desempenho.values)
perdas['ao acaso (esperado)'] = perda_acaso.mean(axis=1)
linhas.append({'estrategia': 'ao acaso (esperado)', 'perda media': perda_acaso.mean(), 'perda mediana': np.median(perda_acaso.mean(axis=1)),
               'acertou o melhor': np.mean(perda_acaso == 0), 'perda > 5 pontos': np.mean(perda_acaso > 0.05)})
tabela = pd.DataFrame(linhas).set_index('estrategia')
print('Avaliacao deixando uma base de fora por vez (64 bases):')
print(tabela.round(3).to_string())

# Comparacao pareada, base a base: o meta-aprendiz contra a referencia "sempre o melhor em media"
dif = perdas['sempre o melhor em média'] - perdas['k-NN: diretas + landmarkers']
print(f'\nBase a base (diretas + landmarkers x sempre o melhor em media): meta-aprendiz melhor em {np.sum(dif > 0)}, '
      f'igual em {np.sum(dif == 0)}, pior em {np.sum(dif < 0)} bases')
reamostras = np.random.default_rng(0).choice(dif, size=(5000, len(dif)), replace=True).mean(axis=1)
print(f'Reducao media da perda: {100 * dif.mean():.2f} pontos; intervalo bootstrap de 95%: '
      f'[{100 * np.percentile(reamostras, 2.5):.2f}; {100 * np.percentile(reamostras, 97.5):.2f}]')

# Um exemplo concreto: a base de digitos
escolha, vizinhas = recomendar('digitos', diretas + landmarkers)
print(f'\nBase "digitos": vizinhas mais parecidas = {vizinhas}')
print(f'Recomendado: {escolha} ({desempenho.loc["digitos", escolha]:.3f}); '
      f'melhor de fato: {desempenho.loc["digitos"].idxmax()} ({melhor["digitos"]:.3f})')

fig, eixo = plt.subplots(figsize=(9, 4.3))
ordem = tabela['perda media'].sort_values().index
cores = ['#168A8A' if n.startswith('k-NN') else '#8794A3' for n in ordem]
eixo.barh(list(ordem)[::-1], [100 * tabela.loc[n, 'perda media'] for n in ordem][::-1], color=cores[::-1])
for i, n in enumerate(list(ordem)[::-1]):
    eixo.text(100 * tabela.loc[n, 'perda media'] + 0.05, i, f'{100 * tabela.loc[n, "perda media"]:.2f}', va='center')
eixo.set_xlabel('Perda média em relação ao melhor algoritmo de cada base (pontos de acurácia)')
eixo.set_title('Recomendar pela semelhança entre bases, avaliado deixando cada base de fora', fontsize=11)
eixo.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'meta_aprendiz.png'))
plt.show()
