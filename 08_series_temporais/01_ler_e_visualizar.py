# Ler uma serie temporal, dar frequencia a ela e olhar antes de modelar.
# Dados: dados/SPCS20RPSNSA.csv, numero mensal de pares de vendas de imoveis do indice
# S&P/Case-Shiller (20 cidades, EUA), sem ajuste sazonal. Fonte: FRED, https://fred.stlouisfed.org/series/SPCS20RPSNSA
# (arquivo ja presente no repositorio de 2019, usado em series_temporais.py).

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

serie = pd.read_csv(os.path.join(pasta, '..', 'dados', 'SPCS20RPSNSA.csv'), index_col=0, parse_dates=True)
serie.columns = ['vendas']
serie = serie.asfreq('MS')          # MS = inicio de mes; declara que ha uma observacao por mes
print(serie.head())
print('Periodo:', serie.index.min().date(), 'a', serie.index.max().date(), '| meses:', len(serie))
print('Meses faltando:', serie['vendas'].isna().sum())
print(serie['vendas'].describe().round(0))

# A serie inteira: tendencia (queda apos 2006, recuperacao apos 2011) e oscilacao anual
fig, eixo = plt.subplots()
eixo.plot(serie.index, serie['vendas'], color='#2F648F', linewidth=1.3)
eixo.set_title('Vendas de imóveis em 20 cidades dos EUA: queda após 2006 e oscilação todo ano')
eixo.set_ylabel('Pares de vendas no mês')
plt.savefig(os.path.join(pasta, 'figuras', 'serie_completa.png'))
plt.show()

# Media movel de 12 meses: suaviza a sazonalidade e deixa a tendencia visivel
serie['media_12m'] = serie['vendas'].rolling(window=12, center=True).mean()
fig, eixo = plt.subplots()
eixo.plot(serie.index, serie['vendas'], color='#8794A3', linewidth=1, label='mensal')
eixo.plot(serie.index, serie['media_12m'], color='#2F648F', linewidth=2.2, label='média móvel de 12 meses')
eixo.set_title('A média móvel mostra a tendência sem o vaivém do calendário')
eixo.set_ylabel('Pares de vendas no mês')
eixo.legend()
plt.savefig(os.path.join(pasta, 'figuras', 'media_movel.png'))
plt.show()

# Grafico sazonal: um ano por linha, meses no eixo x
serie['ano'] = serie.index.year
serie['mes'] = serie.index.month
tabela = serie.pivot_table(index='mes', columns='ano', values='vendas')
print('\nMedia por mes do ano (todos os anos):')
print(tabela.mean(axis=1).round(0))

fig, eixo = plt.subplots()
for ano in tabela.columns:
    cor = '#2F648F' if ano in (2005, 2009, 2018) else '#E6EBF0'
    largura = 2 if ano in (2005, 2009, 2018) else 1
    eixo.plot(tabela.index, tabela[ano], color=cor, linewidth=largura)
    if ano in (2005, 2009, 2018):
        eixo.text(12.2, tabela.loc[12, ano], str(ano), color='#2F648F', va='center')
eixo.set_xticks(range(1, 13))
eixo.set_xlabel('Mês do ano')
eixo.set_ylabel('Pares de vendas')
eixo.set_title('O mesmo desenho todo ano: pico no meio do ano, vale em janeiro e fevereiro')
eixo.set_xlim(1, 13)
plt.savefig(os.path.join(pasta, 'figuras', 'grafico_sazonal.png'))
plt.show()

# Experimente: agregue por trimestre (resample('QS').sum()) e refaca o primeiro grafico.
