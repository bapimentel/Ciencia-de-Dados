# Ler uma tabela com pandas e reconhecer linhas, colunas e tipos.
# Dados: dados/supermercado.csv (1000 vendas de um supermercado em tres cidades, 2019).

import os
import pandas as pd

pasta = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(pasta, '..', 'dados', 'supermercado.csv')

dados = pd.read_csv(arquivo)

# Quantas linhas e colunas? Cada linha e uma venda; cada coluna, uma informacao sobre ela
print(dados.shape)

# As primeiras linhas
print(dados.head())

# Os nomes das colunas
print(dados.columns.tolist())

# O tipo de cada coluna: numero inteiro, numero decimal ou texto (object/str)
print(dados.dtypes)

# Resumo numerico das colunas com numeros
print(dados.describe().round(2))

# Uma coluna sozinha e uma Series
print(dados['Product line'].head())

# Quantas vendas de cada linha de produto?
print(dados['Product line'].value_counts())

# Experimente: troque 'Product line' por 'City' ou 'Payment'.
