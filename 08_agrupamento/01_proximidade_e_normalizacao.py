# Antes de agrupar: escolher atributos e uma medida de proximidade, e colocar os atributos na mesma escala.
# Exemplo pequeno (4 familias, numero de filhos e renda) para fazer as contas a mao.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

familias = pd.DataFrame({'filhos': [2, 3, 8, 7], 'renda': [1500, 2200, 2000, 3000]}, index=['A', 'B', 'C', 'D'])
print(familias)

def distancia(a, b):
    return float(np.sqrt(((a - b) ** 2).sum()))     # distancia euclidiana

print(f"\nSem normalizar: d(A,B) = {distancia(familias.loc['A'], familias.loc['B']):.2f} | "
      f"d(A,C) = {distancia(familias.loc['A'], familias.loc['C']):.2f}")
# A parece mais perto de C (500) do que de B (700): so porque a renda tem numeros maiores.
# A diferenca de 6 filhos entre A e C quase nao conta.

# Normalizacao min-max: (x - min) / (max - min), cada atributo entre 0 e 1
normalizado = (familias - familias.min()) / (familias.max() - familias.min())
print('\nNormalizado (min-max):')
print(normalizado.round(3))
print(f"Normalizado: d(A,B) = {distancia(normalizado.loc['A'], normalizado.loc['B']):.2f} | "
      f"d(A,C) = {distancia(normalizado.loc['A'], normalizado.loc['C']):.2f}")
# Agora A fica perto de B (familias pequenas, renda baixa) e longe de C. A conclusao se inverteu.

# Matriz de distancias entre todos os pares, nas duas escalas
def matriz_distancias(tabela):
    return pd.DataFrame([[distancia(tabela.loc[i], tabela.loc[j]) for j in tabela.index] for i in tabela.index],
                        index=tabela.index, columns=tabela.index)

print('\nDistancias sem normalizar:')
print(matriz_distancias(familias).round(0))
print('\nDistancias normalizadas:')
print(matriz_distancias(normalizado).round(2))

# Outras medidas de proximidade: Manhattan (soma das diferencas absolutas) e cosseno (angulo entre vetores)
a, c = normalizado.loc['A'].values, normalizado.loc['C'].values
print(f"\nManhattan normalizada d(A,C) = {np.abs(a - c).sum():.2f}")

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4.2))
for eixo, tabela, titulo in [(esq, familias, 'Sem normalizar: renda domina a distância'),
                             (dir, normalizado, 'Normalizado: filhos e renda pesam igual')]:
    eixo.scatter(tabela['filhos'], tabela['renda'], s=120, color='#2F648F', zorder=3)
    for nome, linha in tabela.iterrows():
        eixo.text(linha['filhos'], linha['renda'], f'  {nome}', va='center', fontsize=13, color='#20324A')
    for par, cor in [(('A', 'B'), '#168A8A'), (('A', 'C'), '#D69A35')]:
        p1, p2 = tabela.loc[par[0]], tabela.loc[par[1]]
        eixo.plot([p1['filhos'], p2['filhos']], [p1['renda'], p2['renda']], color=cor, linewidth=2)
        eixo.text((p1['filhos'] + p2['filhos']) / 2, (p1['renda'] + p2['renda']) / 2,
                  f' d={distancia(p1, p2):.2f}', color=cor, fontsize=10)
    eixo.set_xlabel('filhos')
    eixo.set_ylabel('renda')
    eixo.set_title(titulo, fontsize=11)
# No grafico da esquerda os eixos tem escalas muito diferentes; o desenho engana o olho, mas a conta nao.
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'proximidade_e_normalizacao.png'))
plt.show()
