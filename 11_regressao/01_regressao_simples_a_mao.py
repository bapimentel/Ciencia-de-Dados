# Regressao linear simples pelo metodo dos minimos quadrados, com as formulas escritas a mao.
# Pergunta: quanto o aluguel diario de bicicletas aumenta, em media, a cada grau de temperatura?
# Dados: dados/bicicletas_dia.csv (Washington D.C., 2011-2012). Usamos so 2012 para nao misturar o
# crescimento do sistema entre os anos com o efeito da temperatura.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
dias = pd.read_csv(os.path.join(pasta, '..', 'dados', 'bicicletas_dia.csv'))
dias = dias[dias['yr'] == 1]
x = (dias['temp'] * 47 - 8).values            # temperatura em graus C
y = dias['cnt'].values                        # alugueis no dia
n = len(x)
print('Dias de 2012:', n)

# Modelo: y = alfa + beta * x + erro. Minimos quadrados escolhem alfa e beta que minimizam
# SQ = soma (y_i - alfa - beta * x_i)^2. Derivando e igualando a zero:
x_medio, y_medio = x.mean(), y.mean()
beta = (np.sum(x * y) - n * x_medio * y_medio) / (np.sum(x ** 2) - n * x_medio ** 2)
alfa = y_medio - beta * x_medio
print(f'beta (inclinacao) = {beta:.1f} alugueis por grau C')
print(f'alfa (intercepto) = {alfa:.0f} alugueis (a 0 grau C)')

# Conferencia com numpy
beta_np, alfa_np = np.polyfit(x, y, deg=1)
print(f'numpy.polyfit: beta = {beta_np:.1f}, alfa = {alfa_np:.0f}')

# Residuos e qualidade do ajuste
ajustado = alfa + beta * x
residuo = y - ajustado
sq_residuos = np.sum(residuo ** 2)
sq_total = np.sum((y - y_medio) ** 2)
r2 = 1 - sq_residuos / sq_total
print(f'R2 = {r2:.3f}  (fracao da variacao dos alugueis explicada pela temperatura)')
print(f'Desvio-padrao dos residuos = {residuo.std(ddof=2):.0f} alugueis')
print(f'Correlacao de Pearson ao quadrado = {np.corrcoef(x, y)[0, 1] ** 2:.3f}  (igual ao R2 na regressao simples)')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.4))
esq.scatter(x, y, s=10, alpha=0.5, color='#2F648F')
xs = np.linspace(x.min(), x.max(), 50)
esq.plot(xs, alfa + beta * xs, color='#D69A35', linewidth=2.5)
esq.text(0.03, 0.92, f'aluguéis = {alfa:.0f} + {beta:.0f} × temperatura\nR² = {r2:.2f}', transform=esq.transAxes, color='#D69A35')
esq.set_xlabel('Temperatura média do dia (°C)')
esq.set_ylabel('Aluguéis no dia (2012)')
esq.set_title(f'Cada grau a mais: cerca de {beta:.0f} aluguéis a mais, em média', fontsize=11)
# Residuos de alguns pontos, desenhados como segmentos verticais
amostra = np.random.default_rng(0).choice(n, 25, replace=False)
dir.scatter(x, y, s=8, alpha=0.2, color='#8794A3')
dir.plot(xs, alfa + beta * xs, color='#D69A35', linewidth=2)
for i in amostra:
    dir.plot([x[i], x[i]], [y[i], ajustado[i]], color='#BD5B58', linewidth=1)
    dir.scatter(x[i], y[i], s=14, color='#2F648F', zorder=3)
dir.set_xlabel('Temperatura média do dia (°C)')
dir.set_title('Resíduos (vermelho): o que a reta não explica', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'regressao_simples.png'))
plt.show()
