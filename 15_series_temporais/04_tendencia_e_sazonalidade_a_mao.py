# Estimar tendencia e sazonalidade "a mao", em cinco etapas, na serie de vendas de imoveis:
#   1. tendencia preliminar por media movel centrada de 12 meses
#   2. sazonalidade: media dos desvios (serie - tendencia) para cada mes do ano, centrada em zero
#   3. serie dessazonalizada: d_t = x_t - s_t
#   4. tendencia final por minimos quadrados na serie dessazonalizada: m_t = a0 + a1 t (+ a2 t^2)
#   5. residuo: Y_t = x_t - m_t - s_t
# Depois, a sazonalidade como soma de senos e cossenos: s_t = soma (a_j cos(2 pi j t/12) + b_j sen(2 pi j t/12)).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

serie = pd.read_csv(os.path.join(pasta, '..', 'dados', 'SPCS20RPSNSA.csv'), index_col=0, parse_dates=True)
x = serie.iloc[:, 0].asfreq('MS')
t = np.arange(len(x))

# 1. media movel centrada de 12 meses (2x12: media de duas medias de 12 para ficar centrada no mes)
tendencia_mm = x.rolling(12, center=True).mean().rolling(2).mean().shift(-1)

# 2. sazonalidade
desvios = x - tendencia_mm
sazonal_mes = desvios.groupby(x.index.month).mean()
sazonal_mes = sazonal_mes - sazonal_mes.mean()
s = pd.Series(sazonal_mes.loc[x.index.month].values, index=x.index)
nomes = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
print('Efeito de cada mes (pares de vendas acima ou abaixo da tendencia):')
print(pd.Series(sazonal_mes.values.round(0), index=nomes).to_string())

# 3. dessazonalizar
d = x - s

# 4. tendencia por minimos quadrados: comparamos reta e parabola pelo erro quadratico
for grau in [1, 2, 3]:
    coef = np.polyfit(t, d, grau)
    sq = np.sum((d - np.polyval(coef, t)) ** 2)
    print(f'Tendencia polinomial de grau {grau}: soma dos quadrados dos residuos = {sq:.3e}')
coef = np.polyfit(t, d, 3)
m = pd.Series(np.polyval(coef, t), index=x.index)
# Um polinomio de grau baixo nao acompanha a queda de 2006-2011: a media movel descreve melhor esse formato.

# 5. residuo
Y = x - m - s
print(f'\nDesvio-padrao: serie {x.std():.0f} | dessazonalizada {d.std():.0f} | residuo {Y.std():.0f}')

# Sazonalidade por senos e cossenos (k harmonicos) ajustada por minimos quadrados aos desvios
validos = desvios.dropna()
tv = t[x.index.isin(validos.index)]
for k in [1, 2, 3]:
    colunas = [np.ones(len(tv))]
    for j in range(1, k + 1):
        colunas += [np.cos(2 * np.pi * j * tv / 12), np.sin(2 * np.pi * j * tv / 12)]
    A = np.column_stack(colunas)
    beta, *_ = np.linalg.lstsq(A, validos.values, rcond=None)
    ajuste = A @ beta
    r2 = 1 - np.sum((validos.values - ajuste) ** 2) / np.sum((validos.values - validos.mean()) ** 2)
    print(f'Sazonalidade com {k} harmonico(s): R2 sobre os desvios = {r2:.3f}')

fig, eixos = plt.subplots(3, 1, figsize=(10, 8.5), sharex=False)
eixos[0].plot(x.index, x, color='#C9D3DD', label='série')
eixos[0].plot(x.index, tendencia_mm, color='#2F648F', label='1. média móvel de 12 meses')
eixos[0].plot(x.index, m, color='#D69A35', linestyle='--', label='4. polinômio de grau 3 (mínimos quadrados)')
eixos[0].legend(loc='upper right', fontsize=9)
eixos[0].set_title('Tendência: a média móvel acompanha a crise; o polinômio só a suaviza', fontsize=11)
eixos[1].bar(nomes, sazonal_mes.values, color=np.where(sazonal_mes.values > 0, '#168A8A', '#BD5B58'))
eixos[1].axhline(0, color='#20324A', linewidth=0.8)
eixos[1].set_title('2. Sazonalidade: vendas acima da tendência de abril a agosto, abaixo no inverno', fontsize=11)
eixos[2].plot(x.index, Y, color='#8794A3', linewidth=1)
eixos[2].axhline(0, color='#20324A', linewidth=0.8)
eixos[2].set_title('5. Resíduo depois de tirar tendência polinomial e sazonalidade: ainda há estrutura', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'tendencia_sazonalidade_a_mao.png'))
plt.show()
