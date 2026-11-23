# Perceptron (Rosenblatt, 1958): o mesmo neuronio, mas os pesos sao APRENDIDOS com a regra delta.
#   erro e = d - y                     (d = classe desejada, y = saida do neuronio)
#   w_novo = w + taxa * e * x          (o vies e atualizado como um peso com entrada fixa +1)
# Exemplo: um biologo mede largura e altura de folhas de duas especies de arvore (X e Y).

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

folhas = np.array([[1, 6], [3, 5], [5, 6], [3, 2], [5, 4]], dtype=float)   # largura, altura
especie = np.array([1, 1, 1, 0, 0])                                         # 1 = X, 0 = Y

pesos = np.zeros(2)
vies = 0.0
taxa = 0.1
historico = [(pesos.copy(), vies)]
print('epoca folha  x        d  y  erro   pesos depois         vies')
for epoca in range(1, 21):
    erros_na_epoca = 0
    for i, (x, d) in enumerate(zip(folhas, especie), start=1):
        y = int(x @ pesos + vies >= 0)
        erro = d - y
        if erro != 0:
            pesos = pesos + taxa * erro * x
            vies = vies + taxa * erro
            erros_na_epoca += 1
            historico.append((pesos.copy(), vies))
        print(f'{epoca:5d} {i:5d}  {str(x):8s} {d}  {y}  {erro:+d}    {np.round(pesos, 2)!s:20s} {vies:+.2f}')
    if erros_na_epoca == 0:
        print(f'Epoca {epoca} sem nenhum erro: o perceptron convergiu.')
        break

print(f'\nFronteira aprendida: {pesos[0]:.2f}*largura + {pesos[1]:.2f}*altura + {vies:.2f} = 0')
print('Previsoes:', (folhas @ pesos + vies >= 0).astype(int), ' esperado:', especie)
# Teorema de convergencia do perceptron: se as classes sao linearmente separaveis (uma reta as separa),
# a regra delta encontra uma reta que separa em um numero finito de passos.

fig, eixo = plt.subplots(figsize=(6.5, 4.8))
xs = np.linspace(0, 6.5, 50)
for k, (w, b) in enumerate(historico[1:], start=1):
    if abs(w[1]) > 1e-9:
        final = k == len(historico) - 1
        eixo.plot(xs, -(w[0] * xs + b) / w[1], color='#2F648F' if final else '#C9D3DD',
                  linewidth=2.5 if final else 1, zorder=3 if final else 1)
for classe, cor, marca, nome in [(1, '#168A8A', 'o', 'espécie X'), (0, '#D69A35', 's', 'espécie Y')]:
    eixo.scatter(*folhas[especie == classe].T, color=cor, marker=marca, s=90, edgecolor='white', label=nome, zorder=4)
for i, (x, y) in enumerate(folhas, start=1):
    eixo.text(x + 0.12, y + 0.12, str(i), fontsize=9)
eixo.set_xlim(0, 6.5)
eixo.set_ylim(0, 8)
eixo.set_xlabel('Largura da folha')
eixo.set_ylabel('Altura da folha')
eixo.set_title(f'Retas intermediárias (cinza) até a fronteira final (azul): {len(historico) - 1} correções', fontsize=11)
eixo.legend(loc='upper right')
plt.savefig(os.path.join(pasta, 'figuras', 'perceptron_folhas.png'))
plt.show()
