# Aplicacao adicional - Mobilidade urbana: bicicletas compartilhadas. Passo 1: conhecer os dados.
# Base: Bike Sharing Dataset (UCI, id 275), Capital Bikeshare, Washington D.C., 2011-2012.
# https://archive.ics.uci.edu/dataset/275/bike-sharing-dataset  (licenca CC BY 4.0; acesso em 2026-11-23)
# day.csv: 731 dias; hour.csv: 17379 horas. Variaveis descritas em dados/Readme.txt.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

dias = pd.read_csv(os.path.join(pasta, 'dados', 'day.csv'), parse_dates=['dteday'])
horas = pd.read_csv(os.path.join(pasta, 'dados', 'hour.csv'), parse_dates=['dteday'])
print('day.csv:', dias.shape, '| hour.csv:', horas.shape)
print(dias.dtypes)
print(dias.head(3).to_string())

# Dicionario (do Readme): season 1=inverno..4=outono; yr 0=2011, 1=2012; mnth; holiday; weekday 0=domingo;
# workingday 1 = dia util (nem fim de semana nem feriado); weathersit 1=limpo, 2=nublado/nevoa, 3=chuva/neve leve,
# 4=chuva forte/granizo; temp e atemp normalizadas (temp = (t+8)/47 em graus C); hum /100; windspeed /67;
# casual = usuarios avulsos; registered = assinantes; cnt = casual + registered.

# Desnormalizar para unidades legiveis
dias['temp_C'] = dias['temp'] * 47 - 8
dias['umidade_%'] = dias['hum'] * 100
dias['vento_kmh'] = dias['windspeed'] * 67
print('\nConferencia cnt = casual + registered:', (dias['cnt'] - dias['casual'] - dias['registered']).abs().max())
print('Periodo:', dias['dteday'].min().date(), 'a', dias['dteday'].max().date(), '| dias:', len(dias))
print('Dias faltando na sequencia:', len(pd.date_range(dias['dteday'].min(), dias['dteday'].max())) - len(dias))
print('Horas registradas de 17544 possiveis:', len(horas), '(horas sem nenhum aluguel nao aparecem)')

print('\nResumo diario:')
print(dias[['cnt', 'casual', 'registered', 'temp_C', 'umidade_%', 'vento_kmh']].describe().round(1))
print('\nMedia de alugueis por dia em cada ano:')
print(dias.groupby('yr')['cnt'].mean().rename({0: '2011', 1: '2012'}).round(0))
print('\nCondicao do tempo (dias):')
print(dias['weathersit'].map({1: 'limpo', 2: 'nublado/névoa', 3: 'chuva/neve leve', 4: 'chuva forte'}).value_counts())

fig, eixo = plt.subplots(figsize=(10, 4))
eixo.plot(dias['dteday'], dias['registered'], color='#2F648F', linewidth=0.9, label='assinantes (registered)')
eixo.plot(dias['dteday'], dias['casual'], color='#168A8A', linewidth=0.9, label='avulsos (casual)')
eixo.set_ylabel('Aluguéis por dia')
eixo.set_title('O sistema cresceu de 2011 para 2012 e tem forte sazonalidade anual; assinantes dominam')
eixo.legend()
sandy = pd.Timestamp('2012-10-29')
eixo.annotate('furacão Sandy', xy=(sandy, dias.loc[dias['dteday'] == sandy, 'cnt'].iloc[0]), xytext=(-110, 40),
              textcoords='offset points', color='#BD5B58', arrowprops=dict(arrowstyle='-', color='#BD5B58'))
plt.savefig(os.path.join(pasta, 'figuras', '01_serie_diaria.png'))
plt.show()

# O que a base NAO tem: estacoes, bicicletas disponiveis, viagens recusadas por falta de bicicleta ou vaga.
# Ela mede uso realizado, agregado para a cidade inteira. Nenhuma conclusao sobre realocacao entre
# estacoes e possivel com ela.
