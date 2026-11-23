# Aplicacao adicional - Bicicletas compartilhadas. Passo 2: padroes de demanda.
# Pergunta: em quais dias e horarios a demanda e maior, e quanto o clima pesa?

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

horas = pd.read_csv(os.path.join(pasta, 'dados', 'hour.csv'), parse_dates=['dteday'])
dias = pd.read_csv(os.path.join(pasta, 'dados', 'day.csv'), parse_dates=['dteday'])
dias['temp_C'] = dias['temp'] * 47 - 8

# Perfil horario em dias uteis e nao uteis, separando assinantes e avulsos
perfil = horas.groupby(['workingday', 'hr'])[['casual', 'registered']].mean().unstack(0)
print('Horas de pico (media de alugueis por hora):')
for tipo, nome in [(1, 'dia util'), (0, 'fim de semana/feriado')]:
    total = perfil['casual'][tipo] + perfil['registered'][tipo]
    print(f'  {nome:22s}: {total.idxmax()}h ({total.max():.0f}), vale {total.idxmin()}h ({total.min():.0f})')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4), sharey=True)
for eixo, tipo, titulo in [(esq, 1, 'Dias úteis: picos às 8h e 17–18h (deslocamento ao trabalho)'),
                           (dir, 0, 'Fins de semana e feriados: um só pico, à tarde')]:
    eixo.plot(perfil.index, perfil['registered'][tipo], color='#2F648F', marker='o', markersize=3, label='assinantes')
    eixo.plot(perfil.index, perfil['casual'][tipo], color='#168A8A', marker='o', markersize=3, label='avulsos')
    eixo.set_xticks(range(0, 24, 2))
    eixo.set_xlabel('Hora do dia')
    eixo.set_title(titulo, fontsize=11)
esq.set_ylabel('Aluguéis por hora (média 2011–2012)')
esq.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '02_perfil_horario.png'))
plt.show()

# Participacao das horas de pico no total dos dias uteis
uteis = horas[horas['workingday'] == 1]
pico = uteis[uteis['hr'].isin([7, 8, 9, 17, 18, 19])]['cnt'].sum() / uteis['cnt'].sum()
print(f'\nNos dias uteis, as horas 7-9 e 17-19 concentram {pico:.0%} dos alugueis')

# Dia da semana e mes
por_dia = dias.groupby('weekday')['cnt'].mean()
por_mes = dias.groupby('mnth')['cnt'].mean()
print('\nMedia por dia da semana (0 = domingo):')
print(por_dia.round(0).to_string())
print('\nMedia por mes:')
print(por_mes.round(0).to_string())

# Clima: temperatura e condicao do tempo
print('\nMedia de alugueis por condicao do tempo (dias):')
print(dias.groupby('weathersit')['cnt'].agg(['count', 'mean']).rename(index={1: 'limpo', 2: 'nublado/névoa', 3: 'chuva/neve leve'}).round(0))
r = dias['temp_C'].corr(dias['cnt'])
print(f'Correlacao temperatura x alugueis diarios: {r:.2f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
cores_ano = np.where(dias['yr'] == 1, '#2F648F', '#8794A3')
esq.scatter(dias['temp_C'], dias['cnt'], s=12, alpha=0.6, color=cores_ano)
esq.set_xlabel('Temperatura média do dia (°C)')
esq.set_ylabel('Aluguéis por dia')
esq.set_title(f'Mais quente, mais uso (r = {r:.2f}); 2012 (azul) acima de 2011 (cinza)')
dir.bar(por_mes.index, por_mes.values, color=['#2F648F' if m in (6, 7, 8, 9) else '#8794A3' for m in por_mes.index])
dir.set_xticks(range(1, 13))
dir.set_xlabel('Mês')
dir.set_ylabel('Aluguéis por dia (média)')
dir.set_title('Junho a setembro são os meses mais fortes')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '02_clima_e_mes.png'))
plt.show()

# Tres fatores se misturam: crescimento do sistema (2012 > 2011), estacao do ano e dia util.
# Qualquer previsao precisa separa-los; e o que o script 03 tenta.
