# Taxa de aprendizagem: o tamanho do passo do gradiente descendente.
# Exemplo de uma dimensao: minimizar E(w) = (w - 3)^2, cuja derivada e 2(w - 3).
# Passo pequeno demais: chega, mas devagar. Passo adequado: chega rapido. Passo grande demais: diverge.

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))


def descer(taxa, w=-2.0, passos=12):
    caminho = [w]
    for _ in range(passos):
        w = w - taxa * 2 * (w - 3)       # w_novo = w - taxa * dE/dw
        caminho.append(w)
    return np.array(caminho)


casos = [(0.05, 'pequena demais', '#8794A3'), (0.4, 'adequada', '#168A8A'), (1.05, 'grande demais', '#BD5B58')]
for taxa, nome, _ in casos:
    c = descer(taxa)
    print(f'taxa {taxa:4.2f} ({nome:14s}): w depois de 12 passos = {c[-1]:8.3f}   distancia do minimo = {abs(c[-1] - 3):.3f}')

fig, eixos = plt.subplots(1, 3, figsize=(14, 3.8), sharey=True)
w = np.linspace(-4, 10, 300)
for eixo, (taxa, nome, cor) in zip(eixos, casos):
    c = descer(taxa)
    eixo.plot(w, (w - 3) ** 2, color='#C9D3DD', linewidth=2)
    eixo.plot(c, (c - 3) ** 2, marker='o', markersize=4, color=cor)
    eixo.scatter(c[0], (c[0] - 3) ** 2, color='#20324A', zorder=3)
    eixo.set_xlim(-4, 10)
    eixo.set_ylim(-2, 60)
    eixo.set_xlabel('peso w')
    eixo.set_title(f'taxa {taxa}: {nome}', fontsize=11)
eixos[0].set_ylabel('erro E(w)')
plt.suptitle('Mesmo ponto de partida (preto), três tamanhos de passo', fontsize=11, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'taxa_de_aprendizagem.png'), bbox_inches='tight')
plt.show()
