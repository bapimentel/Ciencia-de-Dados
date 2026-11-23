# Animacao: um valor extremo entra na amostra e cresce; a media se move, a mediana quase nao.
# Saidas: animacoes/geradas/media_e_mediana.gif e media_e_mediana.png (quadro final).
# Dados simulados com semente fixa.

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

gerador = np.random.default_rng(10)
base = gerador.normal(100, 8, size=29).round(0)          # 29 vendas diarias em torno de 100
extremos = np.linspace(100, 600, 40)                      # o 30o valor cresce de 100 a 600

fig, eixo = plt.subplots(figsize=(8, 4.5))
eixo.set_xlim(60, 620)
eixo.set_ylim(0, 1.6)
eixo.set_yticks([])
eixo.set_xlabel('Vendas no dia')
eixo.grid(False)
pontos = eixo.scatter(base, np.full(len(base), 0.5), s=40, color='#2F648F', alpha=0.8, zorder=3)
extremo = eixo.scatter([100], [0.5], s=90, color='#BD5B58', zorder=4)
linha_media = eixo.axvline(base.mean(), color='#D69A35', linewidth=3, label='média')
linha_mediana = eixo.axvline(np.median(base), color='#168A8A', linewidth=3, linestyle='--', label='mediana')
texto = eixo.text(0.02, 0.08, '', transform=eixo.transAxes, fontsize=11, color='#20324A', va='bottom',
                  bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#E6EBF0'))
eixo.legend(loc='upper right')
eixo.set_title('Um único valor extremo arrasta a média; a mediana resiste')

def quadro(i):
    valores = np.append(base, extremos[i])
    media = valores.mean()
    mediana = np.median(valores)
    extremo.set_offsets([[extremos[i], 0.5]])
    linha_media.set_xdata([media, media])
    linha_mediana.set_xdata([mediana, mediana])
    texto.set_text(f'30 valores; o vermelho vale {extremos[i]:.0f}\n'
                   f'média = {media:.1f}    mediana = {mediana:.1f}    desvio-padrão = {valores.std(ddof=1):.1f}')
    return extremo, linha_media, linha_mediana, texto

# Segura o ultimo quadro por alguns instantes repetindo-o
quadros = list(range(len(extremos))) + [len(extremos) - 1] * 8
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=120, blit=False)
animacao.save(os.path.join(saida, 'media_e_mediana.gif'), writer=PillowWriter(fps=8), dpi=80)
quadro(len(extremos) - 1)
plt.savefig(os.path.join(saida, 'media_e_mediana.png'))
print('Salvo: animacoes/geradas/media_e_mediana.gif e .png')
