# Integracao de dados: juntar fontes diferentes sobre as mesmas entidades.
# Quatro problemas tipicos: (1) identificar a mesma entidade com nomes de coluna diferentes;
# (2) conflito de valores (unidades, moedas, escalas); (3) tuplas duplicadas; (4) atributos redundantes.
# Dados: dados/supermercado.csv + uma tabela de filiais criada aqui (exemplo didatico).

import os
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

pasta = os.path.dirname(os.path.abspath(__file__))
vendas = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

# Uma segunda fonte: cadastro das filiais, vindo de outro sistema (inventado para o exemplo).
# Repare: a chave se chama 'cod_filial' (e nao 'Branch'), a area esta em pes quadrados e a meta em kyat
# (moeda de Mianmar), enquanto as vendas estao em outra unidade monetaria.
filiais = pd.DataFrame({
    'cod_filial': ['A', 'B', 'C', 'C'],                 # a filial C aparece duas vezes (duplicata)
    'area_pes2': [12000, 9500, 15000, 15000],
    'meta_mensal_kyat': [52_000_000, 52_000_000, 54_000_000, 54_000_000],
    'gerente': ['Aye', 'Min', 'Thant', 'Thant'],
})
print('Cadastro de filiais (outra fonte):')
print(filiais)

# (3) Duplicatas na fonte: remover antes de juntar, senao cada venda da filial C apareceria duas vezes
print('\nDuplicatas no cadastro:', filiais.duplicated().sum())
filiais = filiais.drop_duplicates()

# (1) Identificacao de entidade: 'Branch' e 'cod_filial' sao a mesma coisa (metadados ou conversa com quem
# conhece os sistemas confirmam isso). O merge precisa dizer explicitamente qual coluna casa com qual.
integrado = vendas.merge(filiais, left_on='Branch', right_on='cod_filial', how='left', validate='many_to_one')
print('\nLinhas antes e depois do merge:', len(vendas), len(integrado))
# validate='many_to_one' faz o pandas reclamar se a duplicata nao tivesse sido removida.

# (2) Conflito de valores: padronizar unidades antes de comparar
integrado['area_m2'] = integrado['area_pes2'] * 0.092903
TAXA_KYAT = 0.00048        # taxa de cambio ilustrativa: 1 kyat em unidades da moeda das vendas
integrado['meta_mensal'] = integrado['meta_mensal_kyat'] * TAXA_KYAT
resumo = integrado.groupby('Branch').agg(area_m2=('area_m2', 'first'), meta_mensal=('meta_mensal', 'first'),
                                         faturamento_3_meses=('Total', 'sum'))
resumo['faturamento_mensal'] = resumo['faturamento_3_meses'] / 3
resumo['faturamento por m2'] = resumo['faturamento_mensal'] / resumo['area_m2']
print('\nDepois de padronizar as unidades:')
print(resumo.round(1))
# Sem a conversao, comparariamos faturamento com meta em moedas diferentes e area em pes com m2.

# (4) Redundancia: atributos que sao derivados de outros. Numericos -> correlacao; nominais -> qui-quadrado
print('\nCorrelacao entre colunas numericas das vendas (procurando redundancia):')
numericas = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income']
correlacao = vendas[numericas].corr()
print(correlacao.round(3))
pares_redundantes = [(a, b) for i, a in enumerate(numericas) for b in numericas[i + 1:] if correlacao.loc[a, b] > 0.999]
print('Pares com correlacao ~1 (um deriva do outro):', pares_redundantes)
# Tax 5%, Total, cogs e gross income sao todos multiplos uns dos outros: manter so um deles.

tabela = pd.crosstab(vendas['Branch'], vendas['City'])
qui2, p, _, _ = chi2_contingency(tabela)
print('\nBranch x City:')
print(tabela)
print(f'Qui-quadrado = {qui2:.0f}, p = {p:.1e}: as duas colunas carregam a mesma informacao (cada filial fica em uma cidade)')
