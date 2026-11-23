# Histogramas e boxplots: para ver a forma de uma distribuicao.
# Reescreve o exemplo "Histograma" de estatistica.py (2019) e aplica a dados reais.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Exemplo original: 10000 valores simulados de QI (media 100, desvio 15)
gerador = np.random.default_rng(1)
qi = 100 + 15 * gerador.standard_normal(10000)
fig, eixo = plt.subplots(figsize=(6, 3.6))
eixo.hist(qi, bins=50, density=True, color='#2F648F')
eixo.set_xlim(40, 160)
eixo.set_xlabel('QI (simulado)')
eixo.set_ylabel('Densidade')
eixo.set_title('Histograma de 10 000 valores simulados: forma de sino')
plt.savefig(os.path.join(pasta, 'figuras', 'histograma_qi.png'))
plt.show()

# --- Dados reais: o valor total das vendas
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
total = dados['Total']

# O numero de intervalos (bins) muda o que se ve
fig, eixos = plt.subplots(1, 3, figsize=(11, 3.4), sharey=False)
for eixo, bins in zip(eixos, [5, 20, 100]):
    eixo.hist(total, bins=bins, color='#2F648F')
    eixo.set_title(f'{bins} intervalos')
    eixo.set_xlabel('Total da venda')
eixos[0].set_ylabel('Vendas')
fig.suptitle('Poucos intervalos escondem a forma; muitos mostram ruído', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'histograma_bins.png'))
plt.show()

# A forma: assimetrica a direita (muitas vendas pequenas, poucas grandes)
print('Media:', round(total.mean(), 1), '| Mediana:', round(total.median(), 1))

# Boxplot por grupo: compara distribuicoes inteiras, nao so medias
grupos = [dados.loc[dados['Product line'] == p, 'Total'] for p in sorted(dados['Product line'].unique())]
fig, eixo = plt.subplots(figsize=(8, 4))
eixo.boxplot(grupos, tick_labels=sorted(dados['Product line'].unique()), orientation='horizontal',
             medianprops=dict(color='#D69A35', linewidth=2))
eixo.set_xlabel('Total da venda')
eixo.set_title('As seis linhas de produto têm distribuições de valor parecidas')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'boxplot_por_produto.png'))
plt.show()

# Histogramas sobrepostos: so funcionam com poucos grupos e transparencia
fig, eixo = plt.subplots(figsize=(7, 3.6))
for tipo, cor in [('Member', '#2F648F'), ('Normal', '#168A8A')]:
    eixo.hist(dados.loc[dados['Customer type'] == tipo, 'Total'], bins=25, alpha=0.6, color=cor, label=tipo)
eixo.legend()
eixo.set_xlabel('Total da venda')
eixo.set_ylabel('Vendas')
eixo.set_title('Membros e não membros: distribuições quase iguais')
plt.savefig(os.path.join(pasta, 'figuras', 'histograma_por_tipo.png'))
plt.show()

# Experimente: troque 'Total' por 'Rating'. A forma e a mesma?
