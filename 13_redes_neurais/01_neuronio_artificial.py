# O neuronio artificial: soma ponderada das entradas mais um vies, seguida de uma funcao de ativacao.
#   v = w1*x1 + w2*x2 + ... + b        y = phi(v)
# Neuronio de McCulloch e Pitts (1943): pesos fixos, escolhidos a mao, e ativacao de limiar (1 se v >= 0).

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))


def limiar(v):
    return (v >= 0).astype(int)


def neuronio(x, pesos, vies):
    return limiar(x @ np.array(pesos) + vies)


entradas = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# Com pesos 1 e 1, o vies decide quantas entradas precisam estar ativas:
#   vies -1.5 -> precisa das duas (E);  vies -0.5 -> basta uma (OU)
for nome, pesos, vies in [('E   ', [1, 1], -1.5), ('OU  ', [1, 1], -0.5), ('NAO-E', [-1, -1], 1.5)]:
    print(f'{nome}: pesos {pesos}, vies {vies:+.1f} ->', neuronio(entradas, pesos, vies))
# O vies pode ser visto como um peso a mais, ligado a uma entrada fixa igual a +1.

# Funcoes de ativacao mais usadas
v = np.linspace(-5, 5, 400)
funcoes = {
    'Limiar (degrau)': (v >= 0).astype(float),
    'Sigmoide logística': 1 / (1 + np.exp(-v)),
    'Tangente hiperbólica': np.tanh(v),
    'ReLU': np.maximum(0, v),
}
fig, eixos = plt.subplots(1, 4, figsize=(14, 3.4), sharex=True)
cores = ['#8794A3', '#2F648F', '#168A8A', '#D69A35']
for eixo, (nome, y), cor in zip(eixos, funcoes.items(), cores):
    eixo.plot(v, y, color=cor, linewidth=2.2)
    eixo.axhline(0, color='#8794A3', linewidth=0.8)
    eixo.axvline(0, color='#8794A3', linewidth=0.8)
    eixo.set_title(nome, fontsize=11)
    eixo.set_xlabel('v (soma ponderada)')
eixos[0].set_ylabel('saída y = φ(v)')
plt.suptitle('O degrau não tem derivada útil; a sigmoide e a tangente são suaves e permitem aprender por gradiente',
             fontsize=11, y=1.03)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'funcoes_de_ativacao.png'), bbox_inches='tight')
plt.show()
