# Estudo de caso 3 - Vendas em supermercado. Etapa 2: analise temporal (livro, secao 13.2).
# Pergunta: ha periodos de maior movimento? Dias da semana ou horas se destacam?
# Reproduz analise_serie_temporal do analise.py (media diaria da quantidade, decomposicao, picos) e
# acrescenta o teste de que o padrao semanal e distinguivel do acaso.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.signal import find_peaks
from scipy import stats

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour
print('Periodo:', vendas['Data'].min().date(), 'a', vendas['Data'].max().date(), '| dias com vendas:', vendas['Data'].nunique())

# Serie diaria: quantidade media por cupom (como o original) e tambem numero de cupons e faturamento
diario = vendas.groupby('Data').agg(cupons=('Invoice ID', 'count'), quantidade_media=('Quantity', 'mean'), faturamento=('Total', 'sum'))
diario = diario.asfreq('D')
print('Dias sem nenhuma venda:', diario['cupons'].isna().sum())
print(diario.describe().round(1))

# Decomposicao com periodo semanal (7 dias), como o original
decomposicao = seasonal_decompose(diario['quantidade_media'].interpolate(), model='additive', period=7)
sazonal = decomposicao.seasonal
picos, _ = find_peaks(sazonal.values)
print('\nComponente sazonal semanal (quantidade media por cupom):')
print(sazonal[:7].round(2).to_string())
print('Picos da componente sazonal caem em:', sorted(set(sazonal.index[picos].day_name()))[:3], '...')

fig, eixos = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
eixos[0].plot(diario.index, diario['quantidade_media'], color='#2F648F')
eixos[0].set_title('Quantidade média por cupom, por dia (89 dias)')
eixos[1].plot(decomposicao.trend.index, decomposicao.trend, color='#2F648F')
eixos[1].set_title('Tendência (média móvel de 7 dias): sem direção clara')
eixos[2].plot(sazonal.index, sazonal, color='#168A8A')
eixos[2].set_title('Componente semanal: amplitude de cerca de 1 unidade por cupom')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '02_decomposicao_semanal.png'))
plt.show()

# O padrao semanal e distinguivel do acaso? Compare os dias da semana com um teste
vendas['Dia da semana'] = vendas['Data'].dt.day_name()
ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
por_dia = vendas.groupby('Dia da semana').agg(cupons=('Invoice ID', 'count'), faturamento=('Total', 'sum'),
                                              quantidade_media=('Quantity', 'mean')).reindex(ordem)
por_dia['dias no periodo'] = [int((diario.index.day_name() == d).sum()) for d in ordem]
por_dia['cupons por dia'] = (por_dia['cupons'] / por_dia['dias no periodo']).round(1)
print('\nPor dia da semana:')
print(por_dia)
grupos = [vendas.loc[vendas['Dia da semana'] == d, 'Quantity'] for d in ordem]
h, p = stats.kruskal(*grupos)
print(f'\nKruskal-Wallis para quantidade por cupom entre dias da semana: H={h:.2f}, p={p:.3f}')
# p alto: a quantidade por cupom nao difere de forma detectavel entre os dias. O "pico" sazonal da
# decomposicao e pequeno demais para orientar uma decisao.

# Por hora do dia, a diferenca e mais clara
por_hora = vendas.groupby('Hora').agg(cupons=('Invoice ID', 'count'), faturamento=('Total', 'sum'))
por_hora['faturamento por dia'] = por_hora['faturamento'] / diario['cupons'].notna().sum()
print('\nPor hora:')
print(por_hora.round(0))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
esq.bar(range(7), por_dia['cupons por dia'], color=['#8794A3'] * 5 + ['#2F648F'] * 2)
esq.set_xticks(range(7))
esq.set_xticklabels(['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom'])
esq.set_ylabel('Cupons por dia')
esq.set_title('Sábado e terça têm mais cupons por dia; a quantidade por cupom não muda (p = %.2f)' % p)
dir.bar(por_hora.index, por_hora['faturamento por dia'], color=['#2F648F' if h == por_hora['faturamento por dia'].idxmax() else '#8794A3' for h in por_hora.index])
dir.set_xticks(por_hora.index)
dir.set_xlabel('Hora')
dir.set_ylabel('Faturamento médio por dia')
dir.set_title('Às 19h o faturamento por hora é o maior do dia')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '02_dia_da_semana_e_hora.png'))
plt.show()

# Com 89 dias, qualquer tendencia de 3 meses e fragil; a base nao cobre um ano para falar de sazonalidade anual.
