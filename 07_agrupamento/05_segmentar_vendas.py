# Agrupamento em dados reais: ha perfis de compra no supermercado?
# Dados: dados/supermercado.csv. Variaveis numericas: preco unitario, quantidade, avaliacao, hora.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

vendas = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour
variaveis = ['Unit price', 'Quantity', 'Rating', 'Hora']
X = StandardScaler().fit_transform(vendas[variaveis])      # escalas diferentes: padronizar e obrigatorio

# Quantos grupos? Silhueta para k de 2 a 7
for k in range(2, 8):
    rotulos = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
    print(f'k={k}: silhueta={silhouette_score(X, rotulos):.3f}')
# Silhuetas baixas (abaixo de 0,25) em todos os k: os dados nao tem grupos nitidos nessas variaveis.

# Ainda assim, uma particao em 3 pode servir para descrever "tipos de cupom", desde que
# se diga que e uma divisao conveniente, nao uma descoberta.
k = 3
modelo = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
vendas['Grupo'] = modelo.labels_

perfil = vendas.groupby('Grupo')[variaveis + ['Total']].mean().round(2)
perfil['n'] = vendas['Grupo'].value_counts().sort_index()
print('\nPerfil medio de cada grupo:')
print(perfil)

# Composicao por linha de produto dentro de cada grupo (em %)
composicao = pd.crosstab(vendas['Grupo'], vendas['Product line'], normalize='index').round(2) * 100
print('\nLinha de produto por grupo (%):')
print(composicao)

cores = np.array(['#2F648F', '#168A8A', '#D69A35'])
fig, (esq, dir) = plt.subplots(1, 2, figsize=(10, 3.8))
esq.scatter(vendas['Unit price'], vendas['Quantity'], color=cores[vendas['Grupo']], s=14, alpha=0.7)
esq.set_xlabel('Preço unitário')
esq.set_ylabel('Quantidade')
esq.set_title('Os grupos cortam o plano preço × quantidade')
dir.scatter(vendas['Hora'], vendas['Rating'], color=cores[vendas['Grupo']], s=14, alpha=0.7)
dir.set_xlabel('Hora da compra')
dir.set_ylabel('Avaliação')
dir.set_title('… e também hora × avaliação: são cortes, não ilhas')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'segmentos_vendas.png'))
plt.show()

# Leitura honesta: os grupos separam cupons caros/baratos e grandes/pequenos, o que ja se sabia
# olhando as variaveis. Isso nao e inutil (pode organizar um relatorio), mas nao e um "perfil de cliente":
# a base nao identifica clientes, so cupons.
# O estudo de caso 03 (vendas em supermercado, capitulo 13 do livro) usa agrupamento hierarquico
# com mais variaveis e discute o que fazer com os perfis.

# Experimente: retire 'Hora' e 'Rating' das variaveis. A silhueta melhora? O que os grupos passam a significar?
