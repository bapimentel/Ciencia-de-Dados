# Estudo de caso 2 - Energia domestica. Passo 1: conhecer os dados.
# Base: D202.csv, leituras de consumo eletrico de uma residencia a cada 15 minutos, de 22/10/2016 a 24/10/2018,
# com o custo informado pela concessionaria.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

energia = pd.read_csv(os.path.join(pasta, 'dados', 'D202.csv'))
print('Registros:', len(energia), '| colunas:', list(energia.columns))
print(energia.dtypes)
print(energia.head(4).to_string())
print(energia.tail(2).to_string())

# Colunas constantes ou vazias nao trazem informacao
print('\nTYPE:', energia['TYPE'].unique(), '| UNITS:', energia['UNITS'].unique(), '| NOTES vazios:', energia['NOTES'].isna().all())

# Cada dia deveria ter 96 intervalos de 15 minutos
por_dia = energia.groupby('DATE').size()
print('\nDias na base:', len(por_dia), '| intervalos por dia (min, max):', por_dia.min(), por_dia.max())
print('Dias com numero diferente de 96 intervalos:', (por_dia != 96).sum())

# USAGE e o consumo do intervalo em kWh; COST veio como texto com cifrao
print('\nConsumo por intervalo (kWh):')
print(energia['USAGE'].describe().round(3))
print('\nCOST (texto):', energia['COST'].head(3).tolist())
print('Intervalos com consumo zero:', (energia['USAGE'] == 0).sum())

# Primeiro olhar: consumo total por dia ao longo dos dois anos
energia['Data'] = pd.to_datetime(energia['DATE'], format='%m/%d/%Y')
diario = energia.groupby('Data')['USAGE'].sum()
fig, eixo = plt.subplots(figsize=(9, 3.8))
eixo.plot(diario.index, diario.values, color='#2F648F', linewidth=0.9)
eixo.set_ylabel('kWh por dia')
eixo.set_title('Consumo diário da residência: mais alto no inverno, com dias atípicos próximos de zero')
plt.savefig(os.path.join(pasta, 'figuras', '01_consumo_diario.png'))
plt.show()

print('\nConsumo diario (kWh):')
print(diario.describe().round(1))
print('Dias com menos de 2 kWh (casa vazia ou falha de medicao?):', (diario < 2).sum())

# Perguntas para as proximas etapas:
# - em que horas e dias o consumo se concentra?
# - o custo e proporcional ao consumo (tarifa unica) ou varia com a hora?
# - o historico permite prever o consumo dos proximos dias melhor que "repetir a semana passada"?
