# Estudo de caso 2 - Energia domestica. Passo 4: o padrao e estavel? O que muda no inverno?
# Antes de recomendar uma mudanca de habito, verificamos duas coisas nos dados:
#   (a) o perfil horario do primeiro ano se repete no segundo? (se nao, recomendar com base nele e arriscado)
#   (b) quando o consumo sobe no inverno, em que horas esse aumento acontece? (indica onde ha mais a ganhar)

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
horario = pd.read_csv(os.path.join(pasta, 'dados', 'energia_por_hora.csv'), index_col=0, parse_dates=True)
horario['Hora'] = horario.index.hour

# (a) Dois anos completos: 22/10/2016 a 21/10/2017 e 22/10/2017 a 21/10/2018
ano1 = horario.loc['2016-10-22':'2017-10-21']
ano2 = horario.loc['2017-10-22':'2018-10-21']
perfil1 = ano1.groupby('Hora')['Consumo_kWh'].mean()
perfil2 = ano2.groupby('Hora')['Consumo_kWh'].mean()
print(f'Consumo total: ano 1 = {ano1["Consumo_kWh"].sum():.0f} kWh | ano 2 = {ano2["Consumo_kWh"].sum():.0f} kWh')
print(f'Correlacao entre os perfis horarios dos dois anos: {np.corrcoef(perfil1, perfil2)[0, 1]:.3f}')
for nome, ano in [('ano 1', ano1), ('ano 2', ano2)]:
    noite = ano.loc[ano['Hora'].between(18, 23), 'Consumo_kWh'].sum() / ano['Consumo_kWh'].sum()
    print(f'{nome}: noite (18-23h) = {noite:.1%} do consumo | pico as {ano.groupby("Hora")["Consumo_kWh"].mean().idxmax()}h')

# Participacao da noite mes a mes (o padrao vale em todas as estacoes?)
mensal = horario.groupby([horario.index.to_period('M'), horario['Hora'].between(18, 23)])['Consumo_kWh'].sum().unstack()
participacao_mes = (mensal[True] / mensal.sum(axis=1)).iloc[1:-1]          # descarta os meses incompletos das pontas
print(f'\nParticipacao da noite por mes: de {participacao_mes.min():.0%} a {participacao_mes.max():.0%} '
      f'(mediana {participacao_mes.median():.0%})')

# (b) Inverno (dez-fev) x verao (jun-ago): kWh medio por hora do dia
inverno = horario[horario.index.month.isin([12, 1, 2])].groupby('Hora')['Consumo_kWh'].mean()
verao = horario[horario.index.month.isin([6, 7, 8])].groupby('Hora')['Consumo_kWh'].mean()
excesso = inverno - verao
print(f'\nConsumo diario medio: inverno {inverno.sum():.1f} kWh | verao {verao.sum():.1f} kWh | diferenca {excesso.sum():.1f} kWh')
faixas = {'madrugada (0-5h)': range(0, 6), 'manha (6-11h)': range(6, 12), 'tarde (12-17h)': range(12, 18), 'noite (18-23h)': range(18, 24)}
print('Onde esta o excesso do inverno:')
for nome, horas in faixas.items():
    print(f'  {nome:17s}: {excesso[list(horas)].sum():5.2f} kWh/dia ({excesso[list(horas)].sum() / excesso.sum():.0%} do excesso)')

fig, eixos = plt.subplots(1, 3, figsize=(16, 4.3))
eixos[0].plot(perfil1.index, perfil1, color='#2F648F', marker='o', markersize=3, label='ano 1 (out/16 a out/17)')
eixos[0].plot(perfil2.index, perfil2, color='#168A8A', marker='o', markersize=3, label='ano 2 (out/17 a out/18)')
eixos[0].set_xticks(range(0, 24, 3))
eixos[0].set_xlabel('Hora do dia')
eixos[0].set_ylabel('kWh por hora')
eixos[0].set_title(f'O desenho se repete (correlação {np.corrcoef(perfil1, perfil2)[0, 1]:.2f})', fontsize=11)
eixos[0].legend()
eixos[1].plot(participacao_mes.index.to_timestamp(), 100 * participacao_mes.values, marker='o', color='#2F648F')
eixos[1].set_ylim(0, 60)
eixos[1].set_ylabel('% do consumo do mês às 18–23h')
eixos[1].set_title('A noite pesa em todos os meses', fontsize=11)
eixos[1].tick_params(axis='x', labelrotation=45)
eixos[2].plot(inverno.index, inverno, color='#2F648F', label='inverno (dez–fev)')
eixos[2].plot(verao.index, verao, color='#D69A35', label='verão (jun–ago)')
eixos[2].fill_between(inverno.index, verao, inverno, color='#2F648F', alpha=0.12)
eixos[2].set_xticks(range(0, 24, 3))
eixos[2].set_xlabel('Hora do dia')
eixos[2].set_title('O excesso do inverno (área azul), hora a hora', fontsize=11)
eixos[2].legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '04_estabilidade_e_estacoes.png'))
plt.show()
