# Aplicacao adicional - Bicicletas compartilhadas. Passo 6: janelas operacionais com faixas de variacao.
# Com o padrao confirmado no passo 3, calculamos para 2012 (o ano mais recente) a media e a faixa entre os
# percentis 10 e 90 de cada hora, em dias uteis e fins de semana: sao os numeros que uma escala de trabalho usaria.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
horas = pd.read_csv(os.path.join(pasta, 'dados', 'hour.csv'), parse_dates=['dteday'])
horas_2012 = horas[horas['yr'] == 1]

resumo = horas_2012.groupby(['workingday', 'hr'])['cnt'].agg(media='mean', p10=lambda s: s.quantile(0.1), p90=lambda s: s.quantile(0.9))
uteis, fds = resumo.loc[1], resumo.loc[0]
print('Dias uteis de 2012, horas com media acima de 300 alugueis:')
print(uteis[uteis['media'] > 300].round(0).to_string())
print('\nDias uteis: horas com media abaixo de 60 alugueis:', uteis[uteis['media'] < 60].index.tolist())
print('Fins de semana: horas com media acima de 300 alugueis:', fds[fds['media'] > 300].index.tolist())
hora_pico = uteis['media'].idxmax()
print(f'\nPico de dias uteis: {hora_pico}h, media {uteis.loc[hora_pico, "media"]:.0f}, '
      f'p10 {uteis.loc[hora_pico, "p10"]:.0f}, p90 {uteis.loc[hora_pico, "p90"]:.0f}')
# A faixa p10-p90 no pico e larga: o volume exato de um dia depende do clima (passo 2) e precisa da previsao diaria (passos 4 e 5).

fig, eixo = plt.subplots(figsize=(10, 4.2))
eixo.fill_between(uteis.index, uteis['p10'], uteis['p90'], color='#E6EBF0', label='faixa p10–p90 (dias úteis)')
eixo.plot(uteis.index, uteis['media'], color='#2F648F', marker='o', markersize=3, label='média, dias úteis')
eixo.plot(fds.index, fds['media'], color='#168A8A', marker='o', markersize=3, label='média, fins de semana e feriados')
eixo.axvspan(0.5, 5.5, color='#D69A35', alpha=0.12)
eixo.text(3, 300, 'janela de\nmanutenção', ha='center', color='#D69A35')
eixo.set_xticks(range(0, 24))
eixo.set_xlabel('Hora do dia')
eixo.set_ylabel('Aluguéis por hora (2012)')
eixo.set_title('Janelas operacionais em 2012: média e faixa de variação por hora')
eixo.legend(loc='upper center')
plt.savefig(os.path.join(pasta, 'figuras', '06_janelas_operacionais.png'))
plt.show()
