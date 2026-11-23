# Consulta simples x pergunta de Ciencia de Dados, com os mesmos dados.
# Dados: dados/supermercado.csv (1000 vendas de tres filiais, jan-mar de 2019).
# Nao se preocupe com a sintaxe do pandas ainda: ela e explicada na unidade 03.
# Aqui o objetivo e ver a DIFERENCA entre os dois tipos de pergunta.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
vendas = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour
vendas['Mes'] = vendas['Data'].dt.month

# --- 1. Uma CONSULTA: a resposta ja existe na tabela, so precisa ser contada.
# "Quantas unidades de 'Health and beauty' foram vendidas em 5 de janeiro?"
filtro = (vendas['Product line'] == 'Health and beauty') & (vendas['Data'] == '2019-01-05')
print('Consulta: unidades de Health and beauty em 05/01/2019 =', vendas.loc[filtro, 'Quantity'].sum())
# Um banco de dados ou uma planilha responde isso. Nao ha incerteza, nao ha decisao.

# --- 2. Uma PERGUNTA de Ciencia de Dados: a resposta exige comparar, medir incerteza e decidir.
# "Em que horario a loja deveria reforcar os caixas?"
# Primeiro passo: o faturamento medio por hora em cada mes. Se o horario de pico mudar de mes
# para mes, a resposta "reforce as 19h" nao e confiavel.
por_mes_e_hora = vendas.groupby(['Mes', 'Hora'])['Total'].sum().unstack(0)
por_mes_e_hora.columns = ['janeiro', 'fevereiro', 'marco']
print('\nFaturamento por hora em cada mes:')
print(por_mes_e_hora.round(0))
print('\nHora de maior faturamento em cada mes:')
print(por_mes_e_hora.idxmax())
# O pico muda de mes para mes (13h em janeiro, 15h em fevereiro, 19h em marco). Olhando so marco,
# alguem diria "reforce as 19h"; olhando os tres meses, a resposta honesta e "ainda nao sabemos".
# A pergunta "em que horario reforcar?" precisa de mais dados, de um criterio (faturamento? numero de
# clientes?) e de uma avaliacao depois. Uma consulta nunca levantaria essa duvida.

fig, eixo = plt.subplots(figsize=(8, 4.2))
cores = {'janeiro': '#2F648F', 'fevereiro': '#168A8A', 'marco': '#D69A35'}
for mes in por_mes_e_hora.columns:
    eixo.plot(por_mes_e_hora.index, por_mes_e_hora[mes], marker='o', color=cores[mes], label=mes)
eixo.set_xticks(por_mes_e_hora.index)
eixo.set_xlabel('Hora da venda')
eixo.set_ylabel('Faturamento no mês')
eixo.set_title('O horário de maior faturamento muda de mês para mês: 13h, 15h e 19h')
eixo.legend()
plt.savefig(os.path.join(pasta, 'figuras', 'consulta_ou_pergunta.png'))
plt.show()

# Resumo da diferenca:
# consulta  -> resposta exata, sem incerteza, nao exige modelo nem decisao;
# pergunta  -> exige comparar grupos, olhar variacao, decidir com incerteza e verificar depois.
# O curso inteiro e sobre o segundo tipo.
