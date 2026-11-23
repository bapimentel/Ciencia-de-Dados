# Naive Bayes calculado a mao em uma tabela pequena: ir a praia ou nao, conforme o tempo.
# Dados ilustrativos de 10 dias. Classe = 'praia'; atributos = temperatura, vento, nublado, feriado.

import pandas as pd

dias = pd.DataFrame({
    'temperatura': ['frio', 'frio', 'frio', 'frio', 'frio', 'quente', 'quente', 'quente', 'quente', 'quente'],
    'vento':       ['forte', 'forte', 'forte', 'forte', 'forte', 'forte', 'fraco', 'fraco', 'fraco', 'forte'],
    'nublado':     ['pouco', 'muito', 'muito', 'muito', 'muito', 'pouco', 'pouco', 'pouco', 'pouco', 'pouco'],
    'feriado':     ['nao', 'nao', 'nao', 'nao', 'nao', 'sim', 'nao', 'sim', 'sim', 'nao'],
    'praia':       ['sim', 'nao', 'nao', 'nao', 'nao', 'nao', 'sim', 'sim', 'sim', 'sim'],
})
print(dias)
atributos = ['temperatura', 'vento', 'nublado', 'feriado']

# 1) Probabilidades a priori das classes: P(c) = contagem da classe / total
priori = dias['praia'].value_counts(normalize=True)
print('\nP(c):', priori.to_dict())

# 2) Verossimilhancas: P(atributo = valor | classe), contando dentro de cada classe
for atributo in atributos:
    tabela = pd.crosstab(dias[atributo], dias['praia'], normalize='columns')
    print(f'\nP({atributo} | praia):')
    print(tabela.round(2))

# 3) Classificar um dia novo: quente, vento forte, muito nublado, nao e feriado
novo = {'temperatura': 'quente', 'vento': 'forte', 'nublado': 'muito', 'feriado': 'nao'}
print('\nDia novo:', novo)

def pontuacao(classe, suavizar=False):
    sub = dias[dias['praia'] == classe]
    valor = priori[classe]
    termos = [f'P({classe})={priori[classe]:.2f}']
    for atributo in atributos:
        conta = (sub[atributo] == novo[atributo]).sum()
        if suavizar:
            # estimativa-m com p = 1/(numero de valores possiveis) e m = numero de valores (equivale a Laplace)
            valores_possiveis = dias[atributo].nunique()
            prob = (conta + 1) / (len(sub) + valores_possiveis)
        else:
            prob = conta / len(sub)
        valor *= prob
        termos.append(f'P({atributo}={novo[atributo]}|{classe})={prob:.2f}')
    print('  ' + ' x '.join(termos) + f' = {valor:.4f}')
    return valor

print('\nSem suavizacao:')
sem = {c: pontuacao(c) for c in ['sim', 'nao']}
# Nenhum dia de praia foi "muito nublado": P(nublado=muito | sim) = 0 e o produto inteiro zera.
# Um unico atributo nunca visto com a classe veta a classe, por mais que o resto aponte para ela.

print('\nCom suavizacao (Laplace / estimativa-m):')
com = {c: pontuacao(c, suavizar=True) for c in ['sim', 'nao']}
total = sum(com.values())
print(f'Classe escolhida: {max(com, key=com.get)} | probabilidades normalizadas: '
      f'{ {c: round(float(v / total), 3) for c, v in com.items()} }')
# A palavra "naive" (ingenuo): supomos que, dada a classe, os atributos sao independentes, e por isso
# multiplicamos P(a1|c) x P(a2|c) x ... . Raramente e verdade (vento e nuvens nao sao independentes), mas
# o classificador costuma funcionar bem mesmo assim. As probabilidades em si e que nao merecem confianca.
