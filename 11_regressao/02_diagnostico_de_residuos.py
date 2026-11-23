# Diagnostico: o grafico de residuos x valores ajustados revela o que a reta nao captura.
# Mesmos dados (bicicletas, 2012). Se os residuos formam uma curva, a relacao nao e linear.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
dias = pd.read_csv(os.path.join(pasta, '..', 'dados', 'bicicletas_dia.csv'))
dias = dias[dias['yr'] == 1]
x = (dias['temp'] * 47 - 8).values
y = dias['cnt'].values

def ajustar(grau):
    coef = np.polyfit(x, y, deg=grau)
    ajustado = np.polyval(coef, x)
    residuo = y - ajustado
    r2 = 1 - np.sum(residuo ** 2) / np.sum((y - y.mean()) ** 2)
    return coef, ajustado, residuo, r2

coef1, aj1, res1, r2_1 = ajustar(1)
coef2, aj2, res2, r2_2 = ajustar(2)
print(f'Reta:     R2 = {r2_1:.3f}')
print(f'Parabola: R2 = {r2_2:.3f} | coeficientes (x^2, x, 1) = {np.round(coef2, 1)}')
temperatura_pico = -coef2[1] / (2 * coef2[0])
print(f'A parabola tem maximo em {temperatura_pico:.1f} graus C: acima disso, mais calor reduz o uso')

# Media dos residuos da reta por faixa de temperatura: deveria ser ~0 em todas as faixas
faixas = pd.cut(x, bins=6)
print('\nMedia dos residuos da reta por faixa de temperatura:')
print(pd.Series(res1).groupby(faixas, observed=True).mean().round(0))

fig, eixos = plt.subplots(1, 3, figsize=(15, 4.2))
xs = np.linspace(x.min(), x.max(), 100)
eixos[0].scatter(x, y, s=8, alpha=0.4, color='#2F648F')
eixos[0].plot(xs, np.polyval(coef1, xs), color='#8794A3', linewidth=2, label=f'reta (R² {r2_1:.2f})')
eixos[0].plot(xs, np.polyval(coef2, xs), color='#D69A35', linewidth=2, label=f'parábola (R² {r2_2:.2f})')
eixos[0].set_xlabel('Temperatura (°C)')
eixos[0].set_ylabel('Aluguéis no dia')
eixos[0].set_title('Os dados se curvam nos dias mais quentes', fontsize=11)
eixos[0].legend(fontsize=9)
for eixo, ajustado, residuo, titulo in [(eixos[1], aj1, res1, 'Resíduos da reta: formam um arco'),
                                       (eixos[2], aj2, res2, 'Resíduos da parábola: sem padrão claro')]:
    eixo.scatter(ajustado, residuo, s=8, alpha=0.5, color='#2F648F')
    eixo.axhline(0, color='#20324A', linewidth=0.8)
    ordem = np.argsort(ajustado)
    suave = pd.Series(residuo[ordem]).rolling(40, center=True, min_periods=10).mean()
    eixo.plot(ajustado[ordem], suave, color='#BD5B58', linewidth=2)
    eixo.set_xlabel('Valor ajustado')
    eixo.set_ylabel('Resíduo')
    eixo.set_title(titulo, fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'diagnostico_de_residuos.png'))
plt.show()
# O que procurar no grafico de residuos: curvatura (relacao nao linear), funil (variancia que cresce com o
# nivel, heterocedasticidade) e pontos isolados muito longe de zero (observacoes influentes ou atipicas).
