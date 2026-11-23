# Estudo de caso 2 - Energia domestica. Etapa 3: padroes de consumo (livro, secao 12.3).
# Pergunta: quando o consumo se concentra? Hora do dia, dia da semana, mes do ano.
# Reproduz os agrupamentos por hora/dia/mes do analise.py original, com medias (nao somas) para que
# periodos com quantidades diferentes de dias sejam comparaveis, e acrescenta o mapa hora x dia da semana.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

horario = pd.read_csv(os.path.join(pasta, 'dados', 'energia_por_hora.csv'), index_col=0, parse_dates=True)
horario['Hora'] = horario.index.hour
horario['Dia da semana'] = horario.index.day_of_week          # 0 = segunda
horario['Mes'] = horario.index.month
horario['Fim de semana'] = horario['Dia da semana'] >= 5

# Perfil medio por hora do dia
por_hora = horario.groupby('Hora')['Consumo_kWh'].mean()
print('Consumo medio por hora do dia (kWh):')
print(por_hora.round(3).to_string())
pico_manha = por_hora[5:12].idxmax()
pico_noite = por_hora[16:24].idxmax()
print(f'\nPicos: {pico_manha}h ({por_hora[pico_manha]:.2f} kWh) e {pico_noite}h ({por_hora[pico_noite]:.2f} kWh); '
      f'vale: {por_hora.idxmin()}h ({por_hora.min():.2f} kWh)')

# Participacao de cada faixa do dia no consumo total
faixas = pd.cut(horario['Hora'], bins=[-1, 5, 11, 17, 23], labels=['madrugada (0-5h)', 'manhã (6-11h)', 'tarde (12-17h)', 'noite (18-23h)'])
participacao = horario.groupby(faixas, observed=True)['Consumo_kWh'].sum() / horario['Consumo_kWh'].sum()
print('\nParticipacao no consumo total:')
print((100 * participacao).round(1).to_string())

# Dia util x fim de semana, por hora
perfil = horario.groupby(['Fim de semana', 'Hora'])['Consumo_kWh'].mean().unstack(0)
fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4))
esq.plot(perfil.index, perfil[False], color='#2F648F', marker='o', markersize=3, label='dias úteis')
esq.plot(perfil.index, perfil[True], color='#168A8A', marker='o', markersize=3, label='fins de semana')
esq.set_xticks(range(0, 24, 2))
esq.set_xlabel('Hora do dia')
esq.set_ylabel('kWh por hora (média de 2 anos)')
esq.set_title(f'Dois picos: {pico_manha}h e {pico_noite}h; o da noite é o maior')
esq.legend()

# Mapa hora x dia da semana
mapa = horario.pivot_table(index='Hora', columns='Dia da semana', values='Consumo_kWh', aggfunc='mean')
imagem = dir.imshow(mapa.values, aspect='auto', cmap='Blues', origin='lower')
dir.set_yticks(range(0, 24, 2))
dir.set_xticks(range(7))
dir.set_xticklabels(['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom'])
dir.set_ylabel('Hora do dia')
dir.set_title('Mapa hora × dia da semana: a noite é escura em todos os dias')
dir.grid(False)
plt.colorbar(imagem, ax=dir, label='kWh por hora')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_perfil_horario.png'))
plt.show()

# Variacao ao longo do ano
diario = pd.read_csv(os.path.join(pasta, 'dados', 'energia_por_dia.csv'), index_col=0, parse_dates=True)
por_mes = diario.groupby(diario.index.month)['Consumo_kWh'].mean()
print('\nConsumo medio diario por mes do ano (kWh):')
print(por_mes.round(1).to_string())

fig, eixo = plt.subplots(figsize=(8, 3.6))
eixo.bar(por_mes.index, por_mes.values, color=['#2F648F' if m in (12, 1, 2) else '#8794A3' for m in por_mes.index])
eixo.set_xticks(range(1, 13))
eixo.set_xticklabels(['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'])
eixo.set_ylabel('kWh por dia (média)')
eixo.set_title('Dezembro a fevereiro consomem mais: o inverno do hemisfério norte pesa na conta')
plt.savefig(os.path.join(pasta, 'figuras', '03_consumo_por_mes.png'))
plt.show()

# O que a base NAO diz: quais aparelhos estao ligados, a temperatura externa, quantas pessoas estao em casa.
# O pico da noite e compativel com varias explicacoes (cozinhar, aquecimento, iluminacao, lavanderia);
# a base nao permite escolher entre elas.
