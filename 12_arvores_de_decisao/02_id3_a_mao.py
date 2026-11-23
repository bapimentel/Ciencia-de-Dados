# O algoritmo ID3 escrito a mao, em poucas linhas: enquanto o no nao for puro, escolher o atributo de
# maior ganho de informacao, criar um ramo para cada valor e repetir em cada ramo.
# A funcao e recursiva (chama a si mesma) porque a propria arvore e recursiva: cada ramo e uma arvore menor.

import numpy as np
import pandas as pd

dias = pd.DataFrame({
    'temperatura': ['frio', 'frio', 'frio', 'frio', 'frio', 'quente', 'quente', 'quente', 'quente', 'quente'],
    'vento':       ['forte', 'forte', 'forte', 'forte', 'forte', 'forte', 'fraco', 'fraco', 'fraco', 'forte'],
    'nublado':     ['pouco', 'muito', 'muito', 'muito', 'muito', 'pouco', 'pouco', 'pouco', 'pouco', 'pouco'],
    'feriado':     ['nao', 'nao', 'nao', 'nao', 'nao', 'sim', 'nao', 'sim', 'sim', 'nao'],
    'praia':       ['sim', 'nao', 'nao', 'nao', 'nao', 'nao', 'sim', 'sim', 'sim', 'sim'],
})


def entropia(classes):
    p = classes.value_counts(normalize=True)
    return float(-(p * np.log2(p)).sum())


def ganho(tabela, atributo):
    restante = sum(len(g) / len(tabela) * entropia(g['praia']) for _, g in tabela.groupby(atributo))
    return entropia(tabela['praia']) - restante


def id3(tabela, atributos, nivel=0):
    recuo = '    ' * nivel
    classes = tabela['praia']
    # criterio de parada 1: no puro -> folha
    if classes.nunique() == 1:
        print(f'{recuo}-> {classes.iloc[0]}  ({len(tabela)} dias)')
        return classes.iloc[0]
    # criterio de parada 2: nao ha mais atributos -> folha com a classe majoritaria
    if not atributos:
        print(f'{recuo}-> {classes.mode()[0]}  (majoritaria entre {len(tabela)} dias)')
        return classes.mode()[0]
    ganhos = {a: ganho(tabela, a) for a in atributos}
    melhor = max(ganhos, key=ganhos.get)
    ramos = {}
    for valor, grupo in tabela.groupby(melhor):
        print(f'{recuo}{melhor} = {valor}  (ganho {ganhos[melhor]:.3f})')
        ramos[valor] = id3(grupo, [a for a in atributos if a != melhor], nivel + 1)
    return {melhor: ramos}


print('Arvore induzida pelo ID3:')
arvore = id3(dias, ['temperatura', 'vento', 'nublado', 'feriado'])
print('\nComo dicionario:', arvore)


def classificar(arvore, exemplo):
    while isinstance(arvore, dict):
        atributo = next(iter(arvore))
        arvore = arvore[atributo][exemplo[atributo]]
    return arvore


novo = {'temperatura': 'quente', 'vento': 'forte', 'nublado': 'muito', 'feriado': 'nao'}
print('\nDia novo:', novo, '->', classificar(arvore, novo))
# Repare: o dia novo e quente, mas a arvore nem olha a temperatura. A raiz pergunta a nebulosidade
# ("muito" -> nao), e a temperatura nunca e usada: os outros atributos ja separam todos os dias.
# Cada caminho da raiz a uma folha e uma regra "SE ... E ... ENTAO ...", facil de ler e de explicar.


def regras(arvore, condicoes=()):
    if not isinstance(arvore, dict):
        print('  SE ' + ' E '.join(condicoes) + f' ENTAO praia = {arvore}')
        return
    atributo = next(iter(arvore))
    for valor, sub in arvore[atributo].items():
        regras(sub, condicoes + (f'{atributo} = {valor}',))


print('\nRegras:')
regras(arvore)
# Atencao: a ultima regra (feriado = sim -> nao) se apoia em um unico dia. Uma arvore que cresce ate
# cada folha ficar pura acaba "decorando" casos isolados; a poda (script 04) trata esse problema.
