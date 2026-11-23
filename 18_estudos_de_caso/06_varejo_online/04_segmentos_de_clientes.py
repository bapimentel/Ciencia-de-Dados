# Aplicacao adicional - E-commerce. Passo 4: segmentos de clientes por recencia, frequencia e valor (RFM).
# Pergunta: quais segmentos tem maior recorrencia ou valor observado? Onde estao os cancelamentos?

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

clientes = pd.read_csv(os.path.join(pasta, 'dados', 'clientes.csv'))
print('Clientes:', len(clientes))

# Frequencia e valor tem cauda longa (poucos atacadistas enormes): log antes de padronizar
rfm = pd.DataFrame({
    'recencia': np.log1p(clientes['recencia_dias']),
    'frequencia': np.log1p(clientes['frequencia']),
    'valor': np.log1p(clientes['valor_total']),
})
X = StandardScaler().fit_transform(rfm)

for k in range(2, 7):
    rotulos = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
    print(f'k={k}: silhueta {silhouette_score(X, rotulos, sample_size=2000, random_state=0):.3f}')

k = 4
modelo = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
clientes['segmento'] = modelo.labels_

perfil = clientes.groupby('segmento').agg(
    clientes=('frequencia', 'size'), recencia_mediana=('recencia_dias', 'median'), frequencia_mediana=('frequencia', 'median'),
    valor_mediano=('valor_total', 'median'), valor_total=('valor_total', 'sum'),
    com_cancelamento=('cancelamentos', lambda s: (s > 0).mean()), valor_cancelado=('valor_cancelado', 'sum')).round(1)
perfil['parte do valor'] = (perfil['valor_total'] / perfil['valor_total'].sum()).round(3)
perfil['cancelado/vendido'] = (perfil['valor_cancelado'] / perfil['valor_total']).round(3)
perfil = perfil.sort_values('valor_mediano', ascending=False)
print('\nPerfil dos segmentos:')
print(perfil.to_string())

# Nomes descritivos a partir dos numeros (nao antes): maior valor mediano, menor valor mediano e,
# entre os dois do meio, o mais recente e o mais antigo
nomes = {}
ordem = perfil.index.tolist()
nomes[ordem[0]] = 'recorrentes de alto valor'
nomes[ordem[-1]] = 'compra única, antiga'
meio = sorted(ordem[1:-1], key=lambda s: perfil.loc[s, 'recencia_mediana'])
nomes[meio[0]] = 'recentes de baixo valor'
nomes[meio[1]] = 'recorrentes de valor médio'
clientes['nome do segmento'] = clientes['segmento'].map(nomes)
print('\nNomes atribuidos:', nomes)

cores = {ordem[0]: '#2F648F', ordem[-1]: '#8794A3', meio[0]: '#D69A35', meio[1]: '#168A8A'}
fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
for s in ordem:
    grupo = clientes[clientes['segmento'] == s]
    esq.scatter(grupo['recencia_dias'], grupo['valor_total'], s=8, alpha=0.5, color=cores[s], label=f'{nomes[s]} (n={len(grupo)})')
esq.set_yscale('log')
esq.set_xlabel('Dias desde a última compra')
esq.set_ylabel('Valor total comprado (libras, escala log)')
esq.set_title('Segmentos no plano recência × valor')
esq.legend(fontsize=8, loc='lower left')
dir.bar([nomes[s] for s in ordem], 100 * perfil.loc[ordem, 'parte do valor'], color=[cores[s] for s in ordem])
dir.set_ylabel('% do valor vendido a clientes identificados')
dir.set_title('Os recorrentes de alto valor concentram a maior parte do faturamento')
dir.tick_params(axis='x', labelrotation=15)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '04_segmentos.png'))
plt.show()

clientes[['cliente', 'segmento', 'nome do segmento']].to_csv(os.path.join(pasta, 'dados', 'segmentos.csv'), index=False)
print('Salvo: dados/segmentos.csv')
# Os segmentos descrevem o que ja aconteceu com clientes identificados (25% das linhas nao tem cliente).
# Silhueta moderada: as fronteiras entre segmentos sao escolhas, nao grupos naturais.
