# Limite do perceptron: ele so traca UMA reta. Problemas como o XOR (ou exclusivo) nao sao separaveis por uma reta.
# Exemplo do cotidiano com a mesma estrutura: dois segurancas, Antonio e Bento, alternam o plantao.
#   Antonio: Shopping de dia, Escola de noite.   Bento: Shopping de noite, Escola de dia.
# Codificando local (Shopping=0, Escola=1) e turno (Dia=0, Noite=1), "e o Bento?" e exatamente o XOR.

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

entradas = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
bento = np.array([0, 1, 1, 0])
rotulos = ['Shopping, dia', 'Shopping, noite', 'Escola, dia', 'Escola, noite']

# 1) O perceptron tenta, mas nunca acerta os 4 casos
pesos, vies = np.zeros(2), 0.0
melhor_acerto = 0
for epoca in range(100):
    for x, d in zip(entradas, bento):
        erro = d - int(x @ pesos + vies >= 0)
        pesos, vies = pesos + 0.1 * erro * x, vies + 0.1 * erro
    melhor_acerto = max(melhor_acerto, np.mean((entradas @ pesos + vies >= 0) == bento))
print(f'Perceptron, 100 epocas: melhor acerto {melhor_acerto:.0%} (nunca 100%: nenhuma reta separa as classes)')

# 2) Duas camadas resolvem: um neuronio oculto faz OU, outro faz NAO-E, e a saida faz E dos dois.
def limiar(v):
    return (v >= 0).astype(int)

oculto_ou = limiar(entradas @ np.array([1, 1]) - 0.5)
oculto_nao_e = limiar(entradas @ np.array([-1, -1]) + 1.5)
saida = limiar(oculto_ou + oculto_nao_e - 1.5)
print('\nRede 2-2-1 montada a mao:')
print('caso              OU  NAO-E  saida  Bento?')
for r, a, b, s, d in zip(rotulos, oculto_ou, oculto_nao_e, saida, bento):
    print(f'{r:16s}  {a}    {b}      {s}      {d}')
# A camada oculta transforma o problema: no espaco (OU, NAO-E) os casos passam a ser separaveis por uma reta.

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4.4))
cores = np.where(bento == 1, '#BD5B58', '#2F648F')
xx, yy = np.meshgrid(np.linspace(-0.5, 1.5, 300), np.linspace(-0.5, 1.5, 300))
grade = np.column_stack([xx.ravel(), yy.ravel()])
zona = limiar(limiar(grade @ np.array([1, 1]) - 0.5) + limiar(grade @ np.array([-1, -1]) + 1.5) - 1.5)
dir.contourf(xx, yy, zona.reshape(xx.shape), levels=[-0.5, 0.5, 1.5], colors=['#DCE6EF', '#F3DEDD'])
for eixo, titulo in [(esq, 'Uma reta não separa: o perceptron falha'), (dir, 'Duas retas (camada oculta) separam')]:
    eixo.scatter(entradas[:, 0], entradas[:, 1], c=cores, s=260, edgecolor='white', zorder=3)
    for (x, y), r in zip(entradas, rotulos):
        eixo.text(x, y - 0.2, r, ha='center', fontsize=9)
    eixo.set_xlim(-0.5, 1.5)
    eixo.set_ylim(-0.5, 1.5)
    eixo.set_xticks([0, 1], ['Shopping', 'Escola'])
    eixo.set_yticks([0, 1], ['Dia', 'Noite'])
    eixo.grid(False)
    eixo.set_title(titulo, fontsize=11)
for c in [0.5, 1.5]:
    dir.plot([-0.5, 1.5], [c + 0.5, c - 1.5], color='#20324A', linestyle='--', linewidth=1)
esq.plot([-0.5, 1.5], [1.1, 0.4], color='#8794A3', linestyle=':', linewidth=1.5)
esq.text(0.5, 0.35, 'qualquer reta erra\npelo menos um caso', ha='center', fontsize=9, color='#8794A3')
fig.text(0.5, -0.02, 'vermelho = Bento de plantão   ·   azul = Antônio de plantão', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'xor_camada_oculta.png'), bbox_inches='tight')
plt.show()
