# Linhas: para dados ordenados no tempo.
# Dados: dados/Drugs.csv, vendas mensais de medicamentos antidiabeticos na Australia
# (serie "a10", 1991-07 a 2008-06, em milhoes de dolares).

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

serie = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Drugs.csv'), parse_dates=['date'], index_col='date')
print(serie.head())
print('Periodo:', serie.index.min().date(), 'a', serie.index.max().date(), '| meses:', len(serie))

# A linha conecta observacoes consecutivas: faz sentido porque o tempo e continuo e ordenado
fig, eixo = plt.subplots()
eixo.plot(serie.index, serie['value'], color='#2F648F', linewidth=1.5)
eixo.set_title('Vendas mensais de antidiabéticos crescem e oscilam todo ano (Austrália, 1991–2008)')
eixo.set_ylabel('Milhões de dólares')
eixo.set_xlabel('')
# Anotar o ponto mais alto, em vez de deixar o leitor procurar
pico = serie['value'].idxmax()
eixo.annotate(f'{serie["value"].max():.1f} em {pico:%b/%Y}', xy=(pico, serie['value'].max()),
              xytext=(-120, -10), textcoords='offset points', color='#20324A',
              arrowprops=dict(arrowstyle='-', color='#8794A3'))
plt.savefig(os.path.join(pasta, 'figuras', 'linha_drugs.png'))
plt.show()

# O mesmo dado agregado por ano: menos ruido, menos detalhe
por_ano = serie['value'].resample('YE').sum()
print(por_ano.round(1).tail())

fig, (esq, dir) = plt.subplots(1, 2, figsize=(10, 3.6))
esq.plot(serie.index, serie['value'], color='#2F648F', linewidth=1)
esq.set_title('Mensal: a sazonalidade aparece')
esq.set_ylabel('Milhões de dólares')
dir.plot(por_ano.index.year[:-1], por_ano.values[:-1], color='#2F648F', marker='o')
dir.set_title('Anual: só a tendência (2008 incompleto, omitido)')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'linha_mensal_vs_anual.png'))
plt.show()

# Um erro comum: ligar com linha categorias que nao tem ordem
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
por_cidade = dados.groupby('City')['Total'].sum()
fig, (esq, dir) = plt.subplots(1, 2, figsize=(9, 3.4))
esq.plot(por_cidade.index, por_cidade.values, marker='o', color='#BD5B58')
esq.set_title('Linha entre cidades sugere uma tendência que não existe')
dir.bar(por_cidade.index, por_cidade.values, color='#2F648F')
dir.set_title('Barras: cidades são categorias, não uma sequência')
for eixo in (esq, dir):
    eixo.set_ylabel('Faturamento')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'linha_em_categorias.png'))
plt.show()

# Experimente: agregue a serie por trimestre com resample('QE').sum() e compare.
