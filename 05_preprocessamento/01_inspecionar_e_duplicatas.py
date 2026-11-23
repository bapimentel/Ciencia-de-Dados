# Inspecionar uma base antes de usar: tipos, duplicatas e categorias inconsistentes.
# Dados: dados/Data.csv (10 clientes) com problemas acrescentados aqui de proposito.

import os
import pandas as pd

pasta = os.path.dirname(os.path.abspath(__file__))
clientes = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Data.csv'))
print(clientes)
print(clientes.dtypes)

# Simulamos tres problemas comuns em bases reais:
# 1) uma linha repetida; 2) a mesma categoria escrita de jeitos diferentes; 3) um valor impossivel
sujo = pd.concat([clientes, clientes.iloc[[1]]], ignore_index=True)      # duplicata da linha 1
sujo.loc[3, 'Region'] = 'brazil'                                           # minuscula
sujo.loc[8, 'Region'] = ' USA '                                            # espacos
sujo.loc[6, 'Age'] = 230                                                   # idade impossivel
print('\nBase "suja":')
print(sujo)

# Duplicatas: linhas inteiras iguais
print('\nLinhas duplicadas:', sujo.duplicated().sum())
print(sujo[sujo.duplicated(keep=False)])
limpo = sujo.drop_duplicates()
print('Depois de drop_duplicates:', limpo.shape)

# Categorias inconsistentes: value_counts revela
print('\nRegioes antes:', limpo['Region'].value_counts().to_dict())
limpo['Region'] = limpo['Region'].str.strip().str.upper()
limpo['Region'] = limpo['Region'].replace({'BRAZIL': 'Brazil', 'INDIA': 'India'})
print('Regioes depois:', limpo['Region'].value_counts().to_dict())

# Valores impossiveis: describe e um filtro simples
print('\nResumo de Age:')
print(limpo['Age'].describe())
suspeitos = limpo[limpo['Age'] > 120]
print('Idades suspeitas:')
print(suspeitos)
# O que fazer depende do contexto: corrigir se houver fonte, marcar como ausente ou descartar.
limpo.loc[limpo['Age'] > 120, 'Age'] = None
print('\nBase apos marcar a idade impossivel como ausente:')
print(limpo)

# Experimente: acrescente uma linha com Income negativo e trate-a do mesmo jeito.
