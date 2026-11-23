# Tipos de dados, datas e valores ausentes.
# Dados: dados/Data.csv (10 clientes, com lacunas) e dados/supermercado.csv (datas como texto).

import os
import pandas as pd

pasta = os.path.dirname(os.path.abspath(__file__))

# --- Valores ausentes
clientes = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Data.csv'))
print(clientes)

# NaN ("not a number") marca o que falta. isna() mostra onde; sum() conta por coluna
print(clientes.isna())
print(clientes.isna().sum())

# Linhas com pelo menos um ausente
print(clientes[clientes.isna().any(axis=1)])

# A media ignora os ausentes por padrao; o tamanho da amostra muda
print('Media de idade:', clientes['Age'].mean(), 'com', clientes['Age'].count(), 'valores')

# Duas saidas possiveis (a unidade 05 discute quando usar cada uma):
sem_ausentes = clientes.dropna()
print('Depois de dropna:', sem_ausentes.shape)
preenchido = clientes.fillna({'Age': clientes['Age'].median(), 'Income': clientes['Income'].median()})
print(preenchido)

# --- Datas: no arquivo elas sao texto; para calcular com elas, converta
vendas = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
print(vendas['Date'].head(3), vendas['Date'].dtype)

vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
print(vendas['Data'].head(3), vendas['Data'].dtype)

# Com datas de verdade, da para extrair partes e agrupar por elas
vendas['Mes'] = vendas['Data'].dt.month
vendas['Dia da semana'] = vendas['Data'].dt.day_name()
print(vendas.groupby('Mes')['Total'].sum().round(2))
print(vendas.groupby('Dia da semana')['Total'].sum().round(2).sort_values())

# Periodo coberto pela base
print('De', vendas['Data'].min().date(), 'a', vendas['Data'].max().date())

# Experimente: a hora da venda esta em 'Time' (texto 'HH:MM').
# Converta com pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour e agrupe por hora.
