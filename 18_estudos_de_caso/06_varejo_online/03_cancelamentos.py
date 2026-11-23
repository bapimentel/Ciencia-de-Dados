# Aplicacao adicional - E-commerce. Passo 3: onde estao os cancelamentos?
# Pergunta: os cancelamentos se concentram em meses, paises, clientes ou produtos? Que parte do valor eles levam?

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

faturas = pd.read_csv(os.path.join(pasta, 'dados', 'faturas.csv'), parse_dates=['data'])
clientes = pd.read_csv(os.path.join(pasta, 'dados', 'clientes.csv'))
itens = pd.read_csv(os.path.join(pasta, 'dados', 'itens_cancelados.csv'))

vendas = faturas[~faturas['cancelamento']]
cancel = faturas[faturas['cancelamento']]
taxa_faturas = len(cancel) / len(faturas)
taxa_valor = -cancel['valor'].sum() / vendas['valor'].sum()
print(f'Faturas de cancelamento: {len(cancel)} de {len(faturas)} ({taxa_faturas:.1%})')
print(f'Valor cancelado: {-cancel["valor"].sum():,.0f} libras = {taxa_valor:.1%} do valor vendido')

# Por mes
faturas['mes'] = faturas['data'].dt.to_period('M')
por_mes = faturas.groupby('mes')['cancelamento'].agg(['sum', 'count'])
por_mes['taxa'] = por_mes['sum'] / por_mes['count']
print('\nTaxa de cancelamento por mes:')
print(por_mes.round(3).to_string())

# Por pais (com pelo menos 100 faturas)
por_pais = faturas.groupby('pais')['cancelamento'].agg(['sum', 'count'])
por_pais = por_pais[por_pais['count'] >= 100]
por_pais['taxa'] = por_pais['sum'] / por_pais['count']
print('\nTaxa por pais (>= 100 faturas):')
print(por_pais.sort_values('taxa', ascending=False).round(3).head(10))

# Por cliente: poucos clientes concentram os cancelamentos?
com_cancel = clientes[clientes['cancelamentos'] > 0]
print(f'\nClientes com algum cancelamento: {len(com_cancel)} de {len(clientes)} ({len(com_cancel) / len(clientes):.0%})')
ordenado = com_cancel.sort_values('valor_cancelado', ascending=False)
acumulado = ordenado['valor_cancelado'].cumsum() / ordenado['valor_cancelado'].sum()
n_80 = int((acumulado <= 0.8).sum()) + 1
print(f'{n_80} clientes ({n_80 / len(clientes):.1%} dos clientes) respondem por 80% do valor cancelado')

# Cancelamento x tamanho do pedido: faturas grandes sao mais canceladas?
# Comparamos o valor absoluto das faturas canceladas com o das vendas
print('\nValor mediano: vendas', round(vendas['valor'].median(), 1), '| cancelamentos', round(-cancel['valor'].median(), 1))
print('Itens por fatura (mediana): vendas', vendas['itens'].median(), '| cancelamentos', cancel['itens'].median())
# Cancelamentos sao faturas pequenas (poucos itens): estornos parciais de uma linha, nao pedidos inteiros.

# Produtos mais cancelados em relacao ao vendido (minimo de 500 unidades vendidas)
itens['fracao_cancelada'] = -itens['unidades'] / itens['unidades_vendidas']
frequentes = itens[itens['unidades_vendidas'] >= 500].sort_values('valor').head(10)
print('\nProdutos com maior valor cancelado (>= 500 unidades vendidas):')
print(frequentes[['Description', 'unidades_vendidas', 'unidades', 'valor', 'fracao_cancelada']].round(3).to_string(index=False))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4))
esq.plot(por_mes.index.astype(str), 100 * por_mes['taxa'], marker='o', color='#BD5B58')
esq.set_ylabel('% das faturas canceladas')
esq.set_title(f'Taxa de cancelamento por mês: estável em torno de {100 * taxa_faturas:.0f}%')
esq.tick_params(axis='x', labelrotation=45)
esq.set_ylim(0, 100 * por_mes['taxa'].max() * 1.3)
x = np.arange(1, len(ordenado) + 1) / len(clientes) * 100
dir.plot(x, 100 * acumulado.values, color='#2F648F')
dir.axhline(80, color='#D69A35', linestyle='--')
dir.axvline(100 * n_80 / len(clientes), color='#D69A35', linestyle='--')
dir.set_xlabel('% dos clientes (ordenados pelo valor cancelado)')
dir.set_ylabel('% do valor cancelado acumulado')
dir.set_title(f'{n_80 / len(clientes):.0%} dos clientes concentram 80% do valor cancelado')
dir.set_xlim(0, 30)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_cancelamentos.png'))
plt.show()
