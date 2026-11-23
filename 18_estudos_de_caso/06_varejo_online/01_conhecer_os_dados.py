# Aplicacao adicional - E-commerce: cancelamentos e comportamento de compra. Passo 1: conhecer os dados.
# Base: Online Retail (UCI, id 352), transacoes de um varejista on-line do Reino Unido (presentes e utilidades,
# muitos clientes atacadistas), 01/12/2010 a 09/12/2011. https://archive.ics.uci.edu/dataset/352/online-retail
# (licenca CC BY 4.0; acesso em 2026-11-23). O arquivo publicado e um .xlsx de 23 MB; dados/online_retail.csv.gz
# e a mesma tabela convertida para CSV comprimido (7 MB), sem nenhuma linha alterada.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

vendas = pd.read_csv(os.path.join(pasta, 'dados', 'online_retail.csv.gz'), parse_dates=['InvoiceDate'], dtype={'InvoiceNo': str, 'StockCode': str})
print('Linhas (itens de fatura):', len(vendas), '| colunas:', list(vendas.columns))
print(vendas.dtypes)
print(vendas.head(3).to_string())

# Cada linha e um ITEM de uma fatura: numero da fatura, codigo e descricao do produto, quantidade, data/hora,
# preco unitario (libras), cliente e pais. Uma fatura tem varias linhas.
print('\nFaturas distintas:', vendas['InvoiceNo'].nunique(), '| produtos distintos:', vendas['StockCode'].nunique(),
      '| clientes distintos:', vendas['CustomerID'].nunique())
print('Periodo:', vendas['InvoiceDate'].min(), 'a', vendas['InvoiceDate'].max())

# Ausentes e sinais de problema
print('\nAusentes por coluna:')
print(vendas.isna().sum())
print(f'Linhas sem CustomerID: {vendas["CustomerID"].isna().mean():.1%} (compras de visitantes ou registros incompletos)')

# Cancelamentos: faturas cujo numero comeca com C tem quantidades negativas
vendas['cancelamento'] = vendas['InvoiceNo'].str.startswith('C')
print('\nLinhas de cancelamento:', vendas['cancelamento'].sum(), '| faturas de cancelamento:', vendas.loc[vendas['cancelamento'], 'InvoiceNo'].nunique())
print('Quantidade negativa fora de cancelamentos:', ((vendas['Quantity'] < 0) & ~vendas['cancelamento']).sum(), '(ajustes de estoque, perdas)')
print('Preco unitario <= 0:', (vendas['UnitPrice'] <= 0).sum())
print('\nCodigos de produto que nao sao produtos (POST, D, M, BANK CHARGES...):')
print(vendas.loc[~vendas['StockCode'].str[0].str.isdigit(), 'StockCode'].value_counts().head(8))

print('\nPaises (linhas):')
print(vendas['Country'].value_counts().head(6))
print(f'Reino Unido: {(vendas["Country"] == "United Kingdom").mean():.0%} das linhas')

# Primeiro olhar: valor vendido por mes (sem cancelamentos, sem precos zero)
validas = vendas[(~vendas['cancelamento']) & (vendas['Quantity'] > 0) & (vendas['UnitPrice'] > 0)].copy()
validas['valor'] = validas['Quantity'] * validas['UnitPrice']
por_mes = validas.groupby(validas['InvoiceDate'].dt.to_period('M'))['valor'].sum() / 1000
fig, eixo = plt.subplots(figsize=(9, 3.8))
cores = ['#8794A3' if str(p) in ('2010-12', '2011-12') else '#2F648F' for p in por_mes.index]
eixo.bar(por_mes.index.astype(str), por_mes.values, color=cores)
eixo.set_ylabel('Milhares de libras')
eixo.set_title('Vendas por mês: forte alta até novembro de 2011 (dez/2010 e dez/2011 são meses incompletos)')
eixo.tick_params(axis='x', labelrotation=45)
plt.savefig(os.path.join(pasta, 'figuras', '01_vendas_por_mes.png'))
plt.show()

# O que a base NAO tem: carrinhos abandonados, frete, custo dos produtos, margem, motivo do cancelamento,
# estoque. "Cancelamento" aqui e uma fatura estornada, nao um carrinho que o cliente deixou de fechar.
