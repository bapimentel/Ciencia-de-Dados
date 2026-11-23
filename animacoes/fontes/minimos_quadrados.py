# Animacao: o que "minimos quadrados" minimiza. A reta gira; os quadrados dos residuos aparecem no
# grafico e a soma deles (SQ) e acompanhada ao lado; o minimo coincide com a reta de regressao.
# Saidas: animacoes/geradas/minimos_quadrados.gif e .png. Dados simulados (12 pontos, semente fixa).

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

gerador = np.random.default_rng(8)
x = np.linspace(1, 9, 12)
y = 2 + 0.8 * x + gerador.normal(0, 0.9, size=12)
beta_otimo, alfa_otimo = np.polyfit(x, y, 1)
inclinacoes = np.concatenate([np.linspace(0.1, 1.5, 22), np.linspace(1.5, beta_otimo, 12)])

def sq(beta):
    alfa = y.mean() - beta * x.mean()        # para cada inclinacao, o melhor intercepto passa pelo ponto medio
    return np.sum((y - alfa - beta * x) ** 2), alfa

curva_b = np.linspace(0.0, 1.6, 200)
curva_sq = [sq(b)[0] for b in curva_b]

fig, (esq, dir) = plt.subplots(1, 2, figsize=(10, 4.5), gridspec_kw={'width_ratios': [1.2, 1]})

def quadro(i):
    esq.clear()
    beta = inclinacoes[i]
    total, alfa = sq(beta)
    esq.scatter(x, y, color='#2F648F', zorder=3)
    xs = np.array([0, 10])
    esq.plot(xs, alfa + beta * xs, color='#D69A35', linewidth=2)
    for xi, yi in zip(x, y):
        r = yi - (alfa + beta * xi)
        esq.add_patch(Rectangle((xi, alfa + beta * xi), abs(r) * 0.35, r, color='#BD5B58', alpha=0.25))
    esq.set_xlim(0, 10)
    esq.set_ylim(-2, 14)
    esq.set_title(f'inclinação {beta:.2f}: soma dos quadrados = {total:.1f}', fontsize=11)
    esq.set_xlabel('x')
    esq.set_ylabel('y')
    dir.clear()
    dir.plot(curva_b, curva_sq, color='#8794A3')
    dir.scatter([beta], [total], color='#D69A35', s=60, zorder=3)
    dir.axvline(beta_otimo, color='#2F648F', linestyle='--', linewidth=1)
    dir.set_xlabel('inclinação da reta')
    dir.set_ylabel('soma dos quadrados dos resíduos')
    dir.set_title(f'o mínimo está em {beta_otimo:.2f} (mínimos quadrados)', fontsize=11)
    return []

quadros = list(range(len(inclinacoes))) + [len(inclinacoes) - 1] * 6
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=250, blit=False)
animacao.save(os.path.join(saida, 'minimos_quadrados.gif'), writer=PillowWriter(fps=4), dpi=70)
quadro(len(inclinacoes) - 1)
plt.tight_layout()
plt.savefig(os.path.join(saida, 'minimos_quadrados.png'))
print('Salvo: animacoes/geradas/minimos_quadrados.gif e .png')
