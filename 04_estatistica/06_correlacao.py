# Correlacao: medir a relacao entre duas variaveis numericas e nao confundir com causa.
# Dados reais: dados/supermercado.csv.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

# Matriz de correlacao de Pearson entre colunas numericas
colunas = ['Unit price', 'Quantity', 'Total', 'Rating']
print(dados[colunas].corr().round(3))

# Leitura:
# - Total x Quantity (0.71) e Total x Unit price (0.63): esperado, Total e calculado a partir delas.
# - Unit price x Quantity (0.01): o preco unitario nao se relaciona com quantas unidades se leva.
# - Rating x qualquer coisa (~0): a avaliacao nao acompanha o valor da compra.

# Correlacao com valor-p (hipotese nula: correlacao igual a zero na populacao)
r, p = stats.pearsonr(dados['Unit price'], dados['Quantity'])
print(f'Unit price x Quantity: r={r:.3f}, p={p:.3f}')
r, p = stats.pearsonr(dados['Quantity'], dados['Total'])
print(f'Quantity x Total:      r={r:.3f}, p={p:.2e}')

# Spearman usa postos: resiste melhor a extremos e a relacoes nao lineares
rho, p = stats.spearmanr(dados['Quantity'], dados['Total'])
print(f'Quantity x Total (Spearman): rho={rho:.3f}')

fig, eixos = plt.subplots(1, 3, figsize=(11, 3.6))
pares = [('Quantity', 'Total'), ('Unit price', 'Quantity'), ('Rating', 'Total')]
for eixo, (x, y) in zip(eixos, pares):
    eixo.scatter(dados[x], dados[y], s=12, alpha=0.5, color='#2F648F')
    r = dados[x].corr(dados[y])
    eixo.set_title(f'{x} × {y}: r = {r:.2f}')
    eixo.set_xlabel(x)
    eixo.set_ylabel(y)
fig.suptitle('Três relações na mesma base: forte, nula e nula', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'correlacoes.png'))
plt.show()

# Correlacao nao e causa. Um exemplo construido com semente fixa:
# sorvetes vendidos e afogamentos crescem juntos porque ambos dependem do calor.
gerador = np.random.default_rng(7)
temperatura = gerador.uniform(18, 38, size=120)
sorvetes = 20 + 6 * temperatura + gerador.normal(0, 15, size=120)
afogamentos = 0.5 + 0.08 * temperatura + gerador.normal(0, 0.6, size=120)
print('Sorvetes x afogamentos: r =', round(np.corrcoef(sorvetes, afogamentos)[0, 1], 2),
      '(simulado; a causa comum e a temperatura)')

# Experimente: calcule a correlacao entre 'Tax 5%' e 'Total'. Por que e exatamente 1?
