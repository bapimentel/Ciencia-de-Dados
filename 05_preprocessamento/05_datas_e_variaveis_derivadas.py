# Datas e variaveis derivadas: extrair informacao util de colunas de texto e de tempo.
# Dados: dados/supermercado.csv.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
vendas = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

# Data e hora vem como texto em colunas separadas. Juntamos e convertemos uma vez so.
vendas['Momento'] = pd.to_datetime(vendas['Date'] + ' ' + vendas['Time'], format='%m/%d/%Y %H:%M')
print(vendas[['Date', 'Time', 'Momento']].head(3))

# Variaveis derivadas do tempo
vendas['Dia da semana'] = vendas['Momento'].dt.day_name()
vendas['Hora'] = vendas['Momento'].dt.hour
vendas['Fim de semana'] = vendas['Momento'].dt.day_of_week >= 5
vendas['Periodo'] = pd.cut(vendas['Hora'], bins=[9, 12, 15, 18, 21], labels=['manhã', 'início da tarde', 'fim da tarde', 'noite'])
print(vendas[['Momento', 'Dia da semana', 'Hora', 'Fim de semana', 'Periodo']].head())

# Variaveis derivadas de outras colunas
vendas['Ticket por item'] = vendas['Total'] / vendas['Quantity']
vendas['Compra grande'] = vendas['Quantity'] >= 8
print(vendas[['Quantity', 'Total', 'Ticket por item', 'Compra grande']].head())

# Elas permitem perguntas novas: o movimento muda ao longo do dia?
por_hora = vendas.groupby('Hora').size()
print(por_hora)

fig, eixo = plt.subplots(figsize=(7, 3.6))
eixo.bar(por_hora.index, por_hora.values, color='#2F648F')
eixo.set_xlabel('Hora da venda')
eixo.set_ylabel('Vendas (3 meses)')
eixo.set_title('O movimento se concentra às 19h; o resto do dia é parecido')
eixo.set_xticks(por_hora.index)
plt.savefig(os.path.join(pasta, 'figuras', 'vendas_por_hora.png'))
plt.show()

# Cuidado: a hora foi registrada com minutos; agrupar por hora e uma escolha de agregacao.
# Com 1000 vendas em 11 horas de funcionamento, cada barra tem em torno de 90 vendas;
# diferencas de 10 ou 15 vendas podem ser so variacao.

# Experimente: compare o ticket medio ('Total') de fim de semana e de dias uteis.
print(vendas.groupby('Fim de semana')['Total'].agg(['count', 'mean']).round(1))
