# Aplicacao adicional - E-commerce. Passo 2: preparar os dados.
# Separar vendas de cancelamentos, remover linhas que nao sao produtos, calcular o valor de cada linha e
# gravar tabelas pequenas por fatura e por cliente para as proximas etapas.

import os
import pandas as pd

pasta = os.path.dirname(os.path.abspath(__file__))
vendas = pd.read_csv(os.path.join(pasta, 'dados', 'online_retail.csv.gz'), parse_dates=['InvoiceDate'], dtype={'InvoiceNo': str, 'StockCode': str})
inicio = len(vendas)

# 1) Linhas que nao sao produtos (postagem, descontos, taxas, ajustes manuais)
nao_produto = ~vendas['StockCode'].str[0].str.isdigit()
vendas = vendas[~nao_produto]
print(f'Removidas {nao_produto.sum()} linhas de codigos que nao sao produtos; restam {len(vendas)}')

# 2) Precos zero ou negativos (brindes, ajustes)
preco_invalido = vendas['UnitPrice'] <= 0
vendas = vendas[~preco_invalido]
print(f'Removidas {preco_invalido.sum()} linhas com preco <= 0; restam {len(vendas)}')

# 3) Valor da linha e marcacao de cancelamento
vendas['valor'] = vendas['Quantity'] * vendas['UnitPrice']
vendas['cancelamento'] = vendas['InvoiceNo'].str.startswith('C')
ajustes = (vendas['Quantity'] < 0) & ~vendas['cancelamento']
vendas = vendas[~ajustes]
print(f'Removidas {ajustes.sum()} linhas com quantidade negativa fora de cancelamentos; restam {len(vendas)} ({len(vendas) / inicio:.0%} da base)')

# 4) Tabela por fatura
faturas = vendas.groupby(['InvoiceNo', 'cancelamento']).agg(
    cliente=('CustomerID', 'first'), pais=('Country', 'first'), data=('InvoiceDate', 'min'),
    itens=('StockCode', 'nunique'), unidades=('Quantity', 'sum'), valor=('valor', 'sum')).reset_index()
faturas['valor'] = faturas['valor'].round(2)
print('\nFaturas:', len(faturas), '| vendas:', (~faturas['cancelamento']).sum(), '| cancelamentos:', faturas['cancelamento'].sum())
print(faturas[~faturas['cancelamento']]['valor'].describe().round(1))

# 5) Tabela por cliente (so com CustomerID): recencia, frequencia, valor e cancelamentos
com_cliente = faturas.dropna(subset=['cliente']).copy()
com_cliente['cliente'] = com_cliente['cliente'].astype(int)
referencia = faturas['data'].max() + pd.Timedelta(days=1)
compras = com_cliente[~com_cliente['cancelamento']]
clientes = compras.groupby('cliente').agg(
    pais=('pais', 'first'), primeira_compra=('data', 'min'), ultima_compra=('data', 'max'),
    frequencia=('InvoiceNo', 'nunique'), valor_total=('valor', 'sum'), ticket_medio=('valor', 'mean'))
clientes['recencia_dias'] = (referencia - clientes['ultima_compra']).dt.days
cancel = com_cliente[com_cliente['cancelamento']].groupby('cliente').agg(cancelamentos=('InvoiceNo', 'nunique'), valor_cancelado=('valor', 'sum'))
clientes = clientes.join(cancel).fillna({'cancelamentos': 0, 'valor_cancelado': 0})
clientes['valor_cancelado'] = -clientes['valor_cancelado']          # cancelamentos tem valor negativo
print('\nClientes com compras:', len(clientes))
print(clientes[['frequencia', 'valor_total', 'ticket_medio', 'recencia_dias', 'cancelamentos']].describe().round(1))

# 6) Itens cancelados (para a etapa 3), com descricao
itens_cancelados = vendas[vendas['cancelamento']].groupby(['StockCode', 'Description']).agg(
    linhas=('InvoiceNo', 'count'), unidades=('Quantity', 'sum'), valor=('valor', 'sum')).reset_index()
itens_vendidos = vendas[~vendas['cancelamento']].groupby('StockCode').agg(unidades_vendidas=('Quantity', 'sum')).reset_index()
itens_cancelados = itens_cancelados.merge(itens_vendidos, on='StockCode', how='left')

faturas.to_csv(os.path.join(pasta, 'dados', 'faturas.csv'), index=False)
clientes.to_csv(os.path.join(pasta, 'dados', 'clientes.csv'))
itens_cancelados.to_csv(os.path.join(pasta, 'dados', 'itens_cancelados.csv'), index=False)
print('\nSalvos: dados/faturas.csv, dados/clientes.csv, dados/itens_cancelados.csv')
