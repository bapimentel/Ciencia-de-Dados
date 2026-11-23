# Estudo de caso 2 - Energia domestica. Passo 6: por que nao medir uma mudanca pelo "antes e depois"?
# Medimos a variacao NATURAL do consumo noturno (18h-23h) entre periodos, sem nenhuma intervencao.
# Metodo ("placebo"): em todos os periodos de 8 semanas da base, SEM nenhuma intervencao, comparamos o consumo
# noturno com (a) as 8 semanas anteriores e (b) as mesmas 8 semanas do ano anterior. As diferencas que
# aparecem sem intervencao mostram por que comparar periodos inteiros nao mede o efeito de uma acao (ver passo 7).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
horario = pd.read_csv(os.path.join(pasta, 'dados', 'energia_por_hora.csv'), index_col=0, parse_dates=True)
tarifa = horario['Custo'].sum() / horario['Consumo_kWh'].sum()
noite = horario.loc[horario.index.hour >= 18, 'Consumo_kWh'].resample('W-SUN').sum()
total = horario['Consumo_kWh'].resample('W-SUN').sum()
noite, total = noite.iloc[1:-1], total.iloc[1:-1]                  # semanas completas
print(f'{len(noite)} semanas completas | consumo noturno medio {noite.mean():.1f} kWh/semana')

# (a) 8 semanas x 8 semanas anteriores, e (b) 8 semanas x mesmas 8 semanas um ano antes (52 semanas)
janela = 8
media8 = noite.rolling(janela).mean()
dif_anterior = (media8 / media8.shift(janela) - 1).dropna()
dif_ano = (media8 / media8.shift(52) - 1).dropna()
for nome, d in [('8 semanas x 8 anteriores', dif_anterior), ('8 semanas x mesmo periodo do ano anterior', dif_ano)]:
    print(f'{nome:42s}: {len(d):3d} comparacoes sem intervencao | diferenca tipica (desvio) {d.std():.0%} | '
          f'90% entre {d.quantile(0.05):+.0%} e {d.quantile(0.95):+.0%}')

# O que isso implica: uma queda real de X% so se distingue do acaso se for maior que a queda que aparece
# sozinha em 95% das comparacoes placebo (5o percentil).
limite_ano = -dif_ano.quantile(0.05)
print(f'\nComparando com o mesmo periodo do ano anterior, quedas de ate {limite_ano:.0%} aparecem sem intervencao em 5% dos casos.')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.3))
esq.plot(noite.index, noite.values, color='#8794A3', linewidth=0.8, label='semana')
esq.plot(media8.index, media8.values, color='#2F648F', linewidth=2, label='média móvel de 8 semanas')
esq.set_ylabel('kWh às 18–23h por semana')
esq.set_title('Consumo noturno semanal: varia muito sem ninguém mudar nada', fontsize=11)
esq.legend()
dir.hist(100 * dif_anterior, bins=20, color='#D69A35', alpha=0.5, label='× 8 semanas anteriores')
dir.hist(100 * dif_ano, bins=20, color='#2F648F', alpha=0.85, label='× mesmo período do ano anterior')
dir.axvline(-100 * limite_ano, color='#BD5B58', linestyle='--')
dir.text(-100 * limite_ano - 1, dir.get_ylim()[1] * 0.9, f'−{limite_ano:.0%}', color='#BD5B58', ha='right')
dir.set_xlabel('Diferença no consumo noturno sem intervenção (%)')
dir.set_ylabel('Comparações')
dir.set_title('Diferenças "placebo": a meta tem de ficar além da linha vermelha', fontsize=11)
dir.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '06_variacao_natural.png'))
plt.show()
