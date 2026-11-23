# Aplicacao adicional - E-commerce. Passo 6: o que e, de fato, o valor cancelado? E uma regra simples o evitaria?
# O passo 5 mostrou que o valor cancelado nao vem de clientes fixos. Investigamos tres coisas:
#   (a) quanto do valor cancelado e CORRECAO imediata: a mesma linha (cliente, produto, quantidade) vendida e
#       estornada em menos de um dia;
#   (b) uma regra de bloqueio para linhas absurdamente grandes, com limite escolhido no 1o semestre
#       (10 x o percentil 99,9 das quantidades) e avaliada no 2o semestre;
#   (c) a taxa mensal de cancelamento sem essas linhas: a referencia para acompanhar o indicador.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
itens = pd.read_csv(os.path.join(pasta, 'dados', 'online_retail.csv.gz'), parse_dates=['InvoiceDate'], dtype={'InvoiceNo': str, 'StockCode': str})
itens = itens[itens['StockCode'].str[0].str.isdigit() & (itens['UnitPrice'] > 0)].copy()
itens['cancelamento'] = itens['InvoiceNo'].str.startswith('C')
itens = itens[~((itens['Quantity'] < 0) & ~itens['cancelamento'])]
itens['valor'] = itens['Quantity'] * itens['UnitPrice']
vendas, cancel = itens[~itens['cancelamento']], itens[itens['cancelamento']]
total_cancelado = -cancel['valor'].sum()
print(f'Valor cancelado no periodo: {total_cancelado:,.0f} libras')

# (a) Correcoes imediatas: estorno da mesma linha em ate 1 dia
pares = cancel.merge(vendas, on=['CustomerID', 'StockCode'], suffixes=('_c', '_v'))
pares = pares[(pares['InvoiceDate_v'] <= pares['InvoiceDate_c']) &
              (pares['InvoiceDate_c'] - pares['InvoiceDate_v'] <= pd.Timedelta(days=1)) &
              (pares['Quantity_v'] == -pares['Quantity_c'])].drop_duplicates(subset=['InvoiceNo_c', 'StockCode'])
minutos = (pares['InvoiceDate_c'] - pares['InvoiceDate_v']).dt.total_seconds() / 60
print(f'(a) Estornos exatos em ate 1 dia: {len(pares)} linhas, {-pares["valor_c"].sum():,.0f} libras '
      f'({-pares["valor_c"].sum() / total_cancelado:.0%} do valor cancelado); tempo mediano ate o estorno: {minutos.median():.0f} minutos')

# (b) Regra de bloqueio: limite escolhido no 1o semestre
corte = pd.Timestamp('2011-06-01')
p999 = vendas.loc[vendas['InvoiceDate'] < corte, 'Quantity'].quantile(0.999)
limite = int(round(10 * p999, -3))
print(f'\n(b) Percentil 99,9 das quantidades no 1o semestre: {p999:.0f} -> limite = 10 x {p999:.0f} ~ {limite} unidades')
for nome, sel_v, sel_c in [('1o semestre', vendas['InvoiceDate'] < corte, cancel['InvoiceDate'] < corte),
                           ('2o semestre', vendas['InvoiceDate'] >= corte, cancel['InvoiceDate'] >= corte)]:
    v, c = vendas[sel_v], cancel[sel_c]
    linhas_bloqueadas = v[v['Quantity'] >= limite]
    coberto = -c.loc[c['Quantity'] <= -limite, 'valor'].sum() / -c['valor'].sum()
    print(f'   {nome}: linhas vendidas >= {limite}: {len(linhas_bloqueadas)} | parte do valor cancelado em linhas desse tamanho: {coberto:.0%}')
grandes = vendas[vendas['Quantity'] >= limite][['InvoiceNo', 'CustomerID', 'InvoiceDate', 'StockCode', 'Quantity', 'valor']]
print('   Linhas que a regra teria segurado no ano:')
print(grandes.to_string(index=False))

# (c) Taxa mensal de cancelamento, com e sem as linhas acima do limite
itens['mes'] = itens['InvoiceDate'].dt.to_period('M')


def taxa_mensal(tabela):
    return -tabela[tabela['cancelamento']].groupby('mes')['valor'].sum() / tabela[~tabela['cancelamento']].groupby('mes')['valor'].sum()


bruta = taxa_mensal(itens)
sem_grandes = taxa_mensal(itens[itens['Quantity'].abs() < limite])
print('\n(c) Valor cancelado / valor vendido por mes:')
print(pd.DataFrame({'bruta': bruta, f'sem linhas >= {limite}': sem_grandes}).map(lambda x: f'{x:.1%}').to_string())
print(f'Sem as linhas gigantes: de {sem_grandes.min():.1%} a {sem_grandes.max():.1%}, mediana {sem_grandes.median():.1%}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.3))
esq.hist(minutos.clip(upper=600), bins=40, color='#2F648F')
esq.set_xlabel('Minutos entre a venda e o estorno (corte em 600)')
esq.set_ylabel('Linhas estornadas')
esq.set_title(f'Estornos em até 1 dia: {-pares["valor_c"].sum() / total_cancelado:.0%} do valor; '
              f'mediana {minutos.median():.0f} min', fontsize=11)
x = np.arange(len(bruta))
dir.bar(x - 0.2, 100 * bruta.values, width=0.4, color='#BD5B58', label='taxa bruta')
dir.bar(x + 0.2, 100 * sem_grandes.values, width=0.4, color='#2F648F', label=f'sem linhas ≥ {limite} unidades')
dir.set_xticks(x, [str(m)[2:] for m in bruta.index], rotation=45)
dir.set_ylabel('% do valor vendido no mês')
dir.set_title('Duas linhas gigantes distorcem o indicador em jan e dez', fontsize=11)
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '06_correcoes_e_regra.png'))
plt.show()
