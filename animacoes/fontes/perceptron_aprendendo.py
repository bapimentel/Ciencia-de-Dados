# Animacao: o perceptron corrige a fronteira a cada erro (regra delta), nos dados de folhas X e Y.
# Saidas: animacoes/geradas/perceptron_aprendendo.gif e .png

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

folhas = np.array([[1, 6], [3, 5], [5, 6], [3, 2], [5, 4]], dtype=float)
especie = np.array([1, 1, 1, 0, 0])

# Registra cada exemplo apresentado: pesos antes, exemplo, se errou
passos = []
pesos, vies = np.zeros(2), 0.0
for epoca in range(1, 21):
    errou_alguma = False
    for i, (x, d) in enumerate(zip(folhas, especie)):
        erro = d - int(x @ pesos + vies >= 0)
        if erro != 0:
            pesos, vies = pesos + 0.1 * erro * x, vies + 0.1 * erro
            errou_alguma = True
        passos.append((epoca, i, erro, pesos.copy(), vies))
    if not errou_alguma:
        break

fig, eixo = plt.subplots(figsize=(6.5, 4.8))
xs = np.linspace(0, 6.5, 50)


def quadro(k):
    eixo.clear()
    epoca, i, erro, w, b = passos[k]
    if abs(w[1]) > 1e-9:
        eixo.plot(xs, -(w[0] * xs + b) / w[1], color='#2F648F', linewidth=2)
    for classe, cor, marca in [(1, '#168A8A', 'o'), (0, '#D69A35', 's')]:
        eixo.scatter(*folhas[especie == classe].T, color=cor, marker=marca, s=90, edgecolor='white', zorder=3)
    eixo.scatter(*folhas[i], s=320, facecolor='none', edgecolor='#BD5B58' if erro else '#20324A', linewidth=2, zorder=4)
    eixo.set_xlim(0, 6.5)
    eixo.set_ylim(0, 8)
    eixo.set_xlabel('Largura da folha')
    eixo.set_ylabel('Altura da folha')
    estado = 'errou → corrige a reta' if erro else 'acertou → nada muda'
    eixo.set_title(f'Época {epoca}, folha {i + 1}: {estado}', fontsize=11)
    return []


quadros = list(range(len(passos))) + [len(passos) - 1] * 4
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=500)
animacao.save(os.path.join(saida, 'perceptron_aprendendo.gif'), writer=PillowWriter(fps=2), dpi=70)
quadro(len(passos) - 1)
plt.savefig(os.path.join(saida, 'perceptron_aprendendo.png'))
print(f'Salvo: animacoes/geradas/perceptron_aprendendo.gif e .png ({len(passos)} passos)')
