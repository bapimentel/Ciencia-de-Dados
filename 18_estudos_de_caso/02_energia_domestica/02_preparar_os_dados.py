# Estudo de caso 2 - Energia domestica. Passo 2: preparar os dados.
# Juntar data e hora em um unico instante, converter o custo em numero, verificar o significado das
# colunas e gravar versoes agregadas por hora e por dia para as proximas etapas.
# Atencao: COST ja e o custo em dolares do intervalo. Multiplicar consumo por custo (kWh x dolar)
# nao teria significado; o que interessa e verificar se o custo e proporcional ao consumo.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

energia = pd.read_csv(os.path.join(pasta, 'dados', 'D202.csv'))

# 1) Instante = data + hora inicial do intervalo
energia['Instante'] = pd.to_datetime(energia['DATE'] + ' ' + energia['START TIME'], format='%m/%d/%Y %H:%M')

# 2) Custo: tirar o cifrao e converter
energia['Custo'] = energia['COST'].str.replace('$', '', regex=False).str.strip().astype(float)
energia = energia.rename(columns={'USAGE': 'Consumo_kWh'})[['Instante', 'Consumo_kWh', 'Custo']]
print(energia.head())
print(energia.dtypes)

# 3) Conferencias: duplicatas e intervalos faltando
print('\nInstantes duplicados:', energia['Instante'].duplicated().sum())
esperado = pd.date_range(energia['Instante'].min(), energia['Instante'].max(), freq='15min')
print('Intervalos esperados:', len(esperado), '| presentes:', len(energia), '| faltando:', len(esperado) - len(energia))
# Os 8 instantes duplicados e os dias com 92 ou 100 intervalos (script 01) sao as mudancas do horario
# de verao nos EUA: em novembro uma hora se repete, em marco uma hora e pulada. Como somamos por hora
# e por dia, esses casos nao atrapalham; ficam registrados aqui.

# 4) Significado do custo: e proporcional ao consumo?
total_kwh = energia['Consumo_kWh'].sum()
total_custo = energia['Custo'].sum()
print(f'\nConsumo total: {total_kwh:.0f} kWh | custo total: US$ {total_custo:.2f} | tarifa media: US$ {total_custo / total_kwh:.3f}/kWh')
# O custo por intervalo e arredondado ao centavo, entao a razao custo/consumo oscila muito em
# intervalos pequenos. Olhamos a tarifa implicita em agregados diarios.
diario = energia.set_index('Instante').resample('D').sum()
diario['Tarifa'] = diario['Custo'] / diario['Consumo_kWh']
print('Tarifa implicita diaria (US$/kWh):')
print(diario['Tarifa'].describe().round(3))
# Tarifa quase constante ao longo do periodo: o custo e, para fins praticos, consumo x tarifa fixa.
# Nao ha evidencia de tarifa horaria nesta base; reduzir custo = reduzir kWh.

fig, eixo = plt.subplots(figsize=(8, 3.4))
eixo.plot(diario.index, diario['Tarifa'], color='#8794A3', linewidth=0.8)
eixo.set_ylim(0, diario['Tarifa'].quantile(0.99) * 1.3)
eixo.set_ylabel('US$ por kWh (custo do dia / kWh do dia)')
eixo.set_title('A tarifa implícita é praticamente constante: custo acompanha consumo')
plt.savefig(os.path.join(pasta, 'figuras', '02_tarifa_implicita.png'))
plt.show()

# 5) Agregados para as proximas etapas
horario = energia.set_index('Instante').resample('h').sum()
horario.to_csv(os.path.join(pasta, 'dados', 'energia_por_hora.csv'))
diario[['Consumo_kWh', 'Custo']].to_csv(os.path.join(pasta, 'dados', 'energia_por_dia.csv'))
print('\nSalvos: dados/energia_por_hora.csv', horario.shape, 'e dados/energia_por_dia.csv', diario.shape)
