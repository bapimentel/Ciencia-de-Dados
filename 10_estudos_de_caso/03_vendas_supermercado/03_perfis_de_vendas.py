# Estudo de caso 3 - Vendas em supermercado. Etapa 3: perfis de vendas (livro, secao 13.3).
# Pergunta: os cupons se agrupam em perfis com comportamento diferente?
# O analise.py original aplicava agrupamento hierarquico (Ward, 2 grupos) sobre variaveis numericas e
# categoricas codificadas como inteiros (Branch=0,1,2 etc.). Codificar categorias como inteiros impoe uma
# ordem que nao existe; aqui usamos as numericas e comparamos com a versao original.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score, adjusted_rand_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour

# --- Versao deste repositorio: so variaveis numericas (Total e Tax sao funcoes de preco x quantidade, ficam fora)
numericas = ['Unit price', 'Quantity', 'Rating', 'Hora']
X = StandardScaler().fit_transform(vendas[numericas])
fusoes = linkage(X, method='ward')
for k in [2, 3, 4]:
    rotulos = fcluster(fusoes, k, criterion='maxclust')
    print(f'k={k}: tamanhos {np.bincount(rotulos)[1:]} | silhueta {silhouette_score(X, rotulos):.3f}')

k = 2                                                        # o livro trabalha com 2 perfis
vendas['Perfil'] = fcluster(fusoes, k, criterion='maxclust')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={'width_ratios': [1.3, 1]})
dendrogram(fusoes, ax=esq, truncate_mode='lastp', p=30, color_threshold=0, above_threshold_color='#2F648F', no_labels=True)
esq.axhline(fusoes[-1, 2] * 0.6, color='#D69A35', linestyle='--')
esq.set_title('Dendrograma (Ward, últimas 30 fusões): o corte âmbar separa 2 perfis')
esq.set_ylabel('Distância de fusão')
esq.grid(False)
cores = np.array(['#2F648F', '#168A8A', '#D69A35', '#BD5B58'])
dir.scatter(vendas['Unit price'], vendas['Quantity'], color=cores[vendas['Perfil'] - 1], s=14, alpha=0.7)
dir.set_xlabel('Preço unitário')
dir.set_ylabel('Quantidade')
dir.set_title('Os dois perfis no plano preço × quantidade')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_dendrograma_perfis.png'))
plt.show()

# Descricao de cada perfil
perfil = vendas.groupby('Perfil').agg(cupons=('Invoice ID', 'count'), preco_medio=('Unit price', 'mean'),
                                      quantidade_media=('Quantity', 'mean'), total_medio=('Total', 'mean'),
                                      avaliacao_media=('Rating', 'mean'), hora_media=('Hora', 'mean')).round(2)
print('\nPerfis (variaveis numericas):')
print(perfil)
print('\nComposicao por linha de produto (%):')
print((100 * pd.crosstab(vendas['Perfil'], vendas['Product line'], normalize='index')).round(0))
print('\nComposicao por tipo de cliente e filial (%):')
print((100 * pd.crosstab(vendas['Perfil'], vendas['Customer type'], normalize='index')).round(0))
print((100 * pd.crosstab(vendas['Perfil'], vendas['Branch'], normalize='index')).round(0))
# Os perfis separam cupons por quantidade e preco; filial, produto e tipo de cliente se distribuem igual nos dois.

# --- Versao do original, para comparar: categorias como inteiros + Total e gross income
original = vendas.copy()
for coluna in ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']:
    original[coluna] = LabelEncoder().fit_transform(original[coluna])
colunas_original = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Unit price', 'Quantity', 'Total', 'gross income', 'Rating']
X_orig = StandardScaler().fit_transform(original[colunas_original])
rotulos_orig = fcluster(linkage(X_orig, method='ward'), 2, criterion='maxclust')
print(f'\nVersao original (categorias como inteiros): tamanhos {np.bincount(rotulos_orig)[1:]} | '
      f'silhueta {silhouette_score(X_orig, rotulos_orig):.3f} | concordancia com a nossa (ARI) {adjusted_rand_score(vendas["Perfil"], rotulos_orig):.2f}')
print('Branch/City no grupo original:')
print(pd.crosstab(rotulos_orig, vendas['City']))
# A versao original tende a separar pela cidade (0, 1, 2 viram uma "distancia"), o que e um artefato da codificacao.

vendas[['Invoice ID', 'Perfil']].to_csv(os.path.join(pasta, 'dados', 'perfis.csv'), index=False)
print('\nSalvo: dados/perfis.csv')
# Silhuetas baixas em todas as versoes: os perfis sao uma particao conveniente para descrever, nao grupos naturais.
