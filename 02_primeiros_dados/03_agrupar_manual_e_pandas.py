# Agrupar: a mesma conta feita "na mao" (como na unidade 01) e com pandas.
# Pergunta: qual linha de produto vendeu mais unidades? E qual cidade fatura mais?

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

# --- Versao manual: percorrer linha a linha e acumular em um dicionario
total_por_produto = {}
for produto, quantidade in zip(dados['Product line'], dados['Quantity']):
    total_por_produto[produto] = total_por_produto.get(produto, 0) + quantidade
print('Manual:', total_por_produto)

# --- Versao pandas: groupby agrupa, sum soma dentro de cada grupo
por_produto = dados.groupby('Product line')['Quantity'].sum()
print('pandas:')
print(por_produto)

# Os numeros sao os mesmos; o pandas poupa o laco e ja devolve uma tabela.

# Mais de uma estatistica por grupo
resumo = dados.groupby('Product line')['Total'].agg(['count', 'sum', 'mean', 'median'])
print(resumo.round(2))

# Agrupar por duas colunas
por_cidade_e_tipo = dados.groupby(['City', 'Customer type'])['Total'].sum()
print(por_cidade_e_tipo.round(2))

# Ordenar o resultado para ler mais facil
por_produto_ordenado = por_produto.sort_values()
print(por_produto_ordenado)

# Um primeiro grafico: a tabela agrupada vira barras com uma linha de codigo.
# A unidade 04 discute quando cada tipo de grafico ajuda.
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
por_produto_ordenado.plot(kind='barh', color='#2F648F')
plt.xlabel('Unidades vendidas (soma de 1000 vendas, 2019)')
plt.ylabel('')
plt.title('As seis linhas de produto vendem quantidades parecidas')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'unidades_por_produto.png'))
plt.show()

# Experimente: a diferenca entre a linha que mais vende e a que menos vende
# e grande ou pequena? Compare com o total geral de unidades.
print('Total geral de unidades:', dados['Quantity'].sum())
