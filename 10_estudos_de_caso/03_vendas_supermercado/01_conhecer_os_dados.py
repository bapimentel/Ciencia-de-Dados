# Estudo de caso 3 - Vendas em supermercado. Etapa 1: analise descritiva (livro, secao 13.1).
# Base: supermarket_sales - Sheet1.csv, 1000 cupons de tres filiais de um supermercado em Mianmar,
# janeiro a marco de 2019 (base publica, usada no livro). Reproduz estatisticas_globais_produtos do analise.py.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
print('Registros:', len(vendas), '| colunas:', vendas.shape[1])
print(vendas.dtypes)
print(vendas.head(3).to_string())

# O que cada coluna e: cupom, filial, cidade, tipo de cliente, genero, linha de produto, preco unitario,
# quantidade, imposto (5%), total, data, hora, pagamento, custo da mercadoria (cogs), margem bruta (%),
# receita bruta (gross income) e avaliacao do cliente.

# Conferencias de significado: o total e preco x quantidade x 1,05; a margem e sempre a mesma
print('\nTotal = Unit price x Quantity x 1.05? maior diferenca:',
      (vendas['Total'] - vendas['Unit price'] * vendas['Quantity'] * 1.05).abs().max().round(6))
print('gross margin percentage distintos:', vendas['gross margin percentage'].round(4).unique())
print('gross income = Tax 5%? ', (vendas['gross income'] - vendas['Tax 5%']).abs().max().round(6))
# Ou seja: "gross income" e identico ao imposto de 5% e a "margem" e uma constante.
# A base NAO mede custo real, margem liquida nem estoque. Nenhuma conclusao sobre lucro e possivel.

# Estatisticas globais e por linha de produto (como o original, para Price, Quantity e Rating)
for coluna in ['Unit price', 'Quantity', 'Rating']:
    print(f'\n=== {coluna}: global ===')
    print(f'media {vendas[coluna].mean():.2f} | mediana {vendas[coluna].median():.2f} | desvio {vendas[coluna].std():.2f}')
    print(vendas.groupby('Product line')[coluna].agg(['count', 'mean', 'median', 'std']).round(2))

resumo = vendas.groupby('Product line').agg(cupons=('Invoice ID', 'count'), unidades=('Quantity', 'sum'),
                                             faturamento=('Total', 'sum'), ticket_medio=('Total', 'mean'),
                                             avaliacao_media=('Rating', 'mean')).round(2)
resumo.to_csv(os.path.join(pasta, 'dados', 'resumo_por_linha_de_produto.csv'))
print('\nResumo por linha de produto (salvo em dados/resumo_por_linha_de_produto.csv):')
print(resumo)

# Por filial
print('\nPor filial:')
print(vendas.groupby(['Branch', 'City']).agg(cupons=('Invoice ID', 'count'), faturamento=('Total', 'sum'),
                                             avaliacao=('Rating', 'mean')).round(1))

# Figura: distribuicoes de preco, quantidade e avaliacao por linha de produto
linhas = sorted(vendas['Product line'].unique())
fig, eixos = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
for eixo, coluna in zip(eixos, ['Unit price', 'Quantity', 'Rating']):
    grupos = [vendas.loc[vendas['Product line'] == l, coluna] for l in linhas]
    eixo.boxplot(grupos, tick_labels=linhas, orientation='horizontal', medianprops=dict(color='#D69A35', linewidth=2))
    eixo.set_xlabel(coluna)
    eixo.grid(axis='y', visible=False)
fig.suptitle('Preço, quantidade e avaliação têm distribuições parecidas nas seis linhas de produto', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '01_distribuicoes_por_linha.png'))
plt.show()

# Mediana da avaliacao por produto, a figura do original refeita (ver tambem 04_visualizacao/06_antes_e_depois.py)
mediana = vendas.groupby('Product line')['Rating'].median().sort_values()
fig, eixo = plt.subplots(figsize=(8, 3.8))
eixo.barh(mediana.index, mediana.values, color=['#8794A3'] * 5 + ['#2F648F'])
for i, v in enumerate(mediana.values):
    eixo.text(v + 0.08, i, f'{v:.1f}', va='center')
eixo.set_xlim(0, 10)
eixo.set_xlabel('Mediana da avaliação (escala de 4 a 10)')
eixo.set_title('Avaliações medianas entre 6,7 e 7,3: nenhuma linha se destaca')
eixo.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '01_mediana_avaliacao.png'))
plt.show()
