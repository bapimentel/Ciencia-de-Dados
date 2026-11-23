# Aplicacao adicional - Bicicletas compartilhadas. Etapa 4: que decisao os dados sustentam?
# Decisao candidata: planejar a capacidade operacional (manutencao, redistribuicao, equipe) pelas janelas
# de demanda baixa e alta. O que a base permite dizer, o que nao permite e como medir.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

horas = pd.read_csv(os.path.join(pasta, 'dados', 'hour.csv'), parse_dates=['dteday'])
horas_2012 = horas[horas['yr'] == 1]                   # o ano mais recente representa melhor o sistema atual

# Demanda media por hora em dias uteis e nao uteis, 2012, com faixa entre percentis 10 e 90
resumo = horas_2012.groupby(['workingday', 'hr'])['cnt'].agg(media='mean', p10=lambda s: s.quantile(0.1), p90=lambda s: s.quantile(0.9))
print('Dias uteis de 2012: horas com media acima de 300 alugueis:')
uteis = resumo.loc[1]
print(uteis[uteis['media'] > 300].round(0))
print('\nJanela de menor demanda em dias uteis (media < 60):', uteis[uteis['media'] < 60].index.tolist())

# Variabilidade no pico: o percentil 90 e quanto maior que a media?
hora_pico = uteis['media'].idxmax()
print(f'\nPico de dias uteis: {hora_pico}h, media {uteis.loc[hora_pico, "media"]:.0f}, p90 {uteis.loc[hora_pico, "p90"]:.0f}')

fig, eixo = plt.subplots(figsize=(10, 4.2))
eixo.fill_between(uteis.index, uteis['p10'], uteis['p90'], color='#E6EBF0', label='faixa p10–p90 (dias úteis)')
eixo.plot(uteis.index, uteis['media'], color='#2F648F', marker='o', markersize=3, label='média, dias úteis')
fds = resumo.loc[0]
eixo.plot(fds.index, fds['media'], color='#168A8A', marker='o', markersize=3, label='média, fins de semana e feriados')
eixo.axvspan(1.5, 5.5, color='#D69A35', alpha=0.12)
eixo.text(3.5, 300, 'janela de\nmanutenção', ha='center', color='#D69A35')
eixo.set_xticks(range(0, 24))
eixo.set_xlabel('Hora do dia')
eixo.set_ylabel('Aluguéis por hora (2012)')
eixo.set_title('Capacidade: o pico das 17h varia de dia para dia; das 2h às 5h quase não há uso')
eixo.legend(loc='upper center')
plt.savefig(os.path.join(pasta, 'figuras', '04_janelas_de_capacidade.png'))
plt.show()

print('''
Achado: em dias uteis a demanda tem dois picos (8h e 17-18h); as faixas 7-9h e 17-19h concentram 52% dos
alugueis; entre 0h e 5h o uso e quase nulo; fins de semana tem um pico unico a tarde (13h). O uso cresce
com a temperatura (r = 0,63) e despenca em dias de chuva ou eventos (furacao Sandy).
Isso sugere que a operacao (manutencao preventiva, redistribuicao de bicicletas, equipe de suporte) pode
ser organizada em torno dessas janelas: trabalho pesado entre 1h e 6h, reforco antes das 7h e das 16h
em dias uteis, e antes das 11h em fins de semana.
Recomendacao (hipotese operacional): concentrar a manutencao programada entre 1h e 6h e a redistribuicao
de bicicletas nas horas que antecedem os picos, com previsao diaria do volume (script 03) para dimensionar
a equipe.
Evidencia: perfis horarios de 2012 com faixas p10-p90; erro de previsao diaria de ~960 alugueis (18% da media).
O que a base NAO sustenta: realocar bicicletas entre estacoes especificas. Nao ha dados por estacao,
nem de bicicletas disponiveis, nem de viagens recusadas. "Demanda" aqui e uso realizado, que pode
estar limitado pela oferta justamente nos picos.
Avaliacao (proposta): com dados por estacao da operadora, medir apos 3 meses a fracao de horas de pico
em que estacoes centrais ficaram sem bicicleta ou sem vaga (metrica principal) e o numero de viagens
por bicicleta por dia (auxiliar). Sucesso proposto: reducao da fracao de horas de pico com estacao vazia
em relacao ao mesmo trimestre do ano anterior. Sem dados por estacao, a metrica nao pode ser calculada,
e a recomendacao deve ser tratada como ponto de partida para coleta, nao como conclusao.
''')
