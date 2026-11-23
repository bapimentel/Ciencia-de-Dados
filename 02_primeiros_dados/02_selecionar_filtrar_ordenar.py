# Selecionar colunas, filtrar linhas e ordenar.

import os
import pandas as pd

pasta = os.path.dirname(os.path.abspath(__file__))
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

# Selecionar algumas colunas: lista de nomes dentro dos colchetes
resumo = dados[['City', 'Product line', 'Quantity', 'Total']]
print(resumo.head())

# Filtrar linhas: uma condicao dentro dos colchetes
so_yangon = dados[dados['City'] == 'Yangon']
print(len(so_yangon), 'vendas em Yangon')

# Duas condicoes: & para "e", | para "ou", cada uma entre parenteses
grandes_em_yangon = dados[(dados['City'] == 'Yangon') & (dados['Total'] > 500)]
print(len(grandes_em_yangon), 'vendas acima de 500 em Yangon')

# Ordenar pelo valor total, do maior para o menor
maiores = dados.sort_values('Total', ascending=False)
print(maiores[['City', 'Product line', 'Quantity', 'Total']].head(5))

# Selecionar por posicao (iloc) e por rotulo (loc)
print(dados.iloc[0])                 # primeira linha inteira
print(dados.loc[0, 'Total'])         # linha de indice 0, coluna Total

# Criar uma coluna nova a partir de outras
dados['Preco medio por item'] = dados['Total'] / dados['Quantity']
print(dados[['Unit price', 'Quantity', 'Total', 'Preco medio por item']].head())

# Repare: Total = Unit price * Quantity * 1.05 (ha 5% de imposto).
# Confira com uma conta:
diferenca = dados['Total'] - dados['Unit price'] * dados['Quantity'] * 1.05
print('Maior diferenca encontrada:', diferenca.abs().max())

# Experimente: filtre as vendas pagas em dinheiro (Payment == 'Cash') com Rating >= 9.
