# Animacao: a amostra cresce e o histograma vai revelando a distribuicao.
# Saidas: animacoes/geradas/histograma_crescendo.gif e .png. Dados simulados com semente fixa.

import os
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

gerador = np.random.default_rng(2)
amostra_total = gerador.normal(50, 5, size=5000)
tamanhos = [5, 10, 20, 30, 50, 75, 100, 150, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000]
bins = np.arange(30, 71, 1.5)
xs = np.linspace(30, 70, 300)
densidade = [math.exp(-(v - 50) ** 2 / (2 * 25)) / (math.sqrt(2 * math.pi) * 5) for v in xs]

fig, eixo = plt.subplots(figsize=(8, 4.5))
eixo.set_xlim(30, 70)
eixo.set_ylim(0, 0.12)
eixo.set_xlabel('valor')
eixo.set_ylabel('densidade')
eixo.plot(xs, densidade, color='#D69A35', linewidth=2, label='distribuição de onde a amostra vem')
eixo.legend(loc='upper right')
eixo.set_title('Com poucas observações o histograma é irregular; com muitas, a forma aparece')
texto = eixo.text(0.02, 0.92, '', transform=eixo.transAxes, fontsize=11, color='#20324A', va='top')
barras = []

def quadro(i):
    global barras
    for b in barras:
        b.remove()
    n = tamanhos[i]
    amostra = amostra_total[:n]
    _, _, barras = eixo.hist(amostra, bins=bins, density=True, color='#2F648F')
    barras = list(barras)
    texto.set_text(f'n = {n}\nmédia = {amostra.mean():.1f}   desvio = {amostra.std(ddof=1):.1f}')
    return barras

quadros = list(range(len(tamanhos))) + [len(tamanhos) - 1] * 6
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=450, blit=False)
animacao.save(os.path.join(saida, 'histograma_crescendo.gif'), writer=PillowWriter(fps=2), dpi=80)
quadro(len(tamanhos) - 1)
plt.savefig(os.path.join(saida, 'histograma_crescendo.png'))
print('Salvo: animacoes/geradas/histograma_crescendo.gif e .png')
