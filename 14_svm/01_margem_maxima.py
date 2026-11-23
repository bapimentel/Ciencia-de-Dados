# Margem maxima: entre todas as retas que separam duas classes, a SVM escolhe a que fica mais longe
# dos pontos mais proximos de cada lado. Esses pontos sao os VETORES DE SUPORTE.
#   hiperplano: w . x + b = 0        margem = 2 / ||w||
#   restricao:  y_i (w . x_i + b) >= 1 para todo i  (y = +1 ou -1)
# Dados: 12 pontos ilustrativos em duas classes separaveis.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

X = np.array([[1, 2], [2, 3], [2, 1], [3, 2], [1.5, 3.5], [3, 3.6],
              [5, 5], [6, 4], [6, 6], [7, 5], [5.5, 6.5], [4.6, 4.2]], dtype=float)
y = np.array([-1] * 6 + [1] * 6)

# 1) Tres retas que separam as classes. Qual e melhor? Medimos a distancia ao ponto mais proximo.
def margem_da_reta(w, b):
    distancias = y * (X @ w + b) / np.linalg.norm(w)      # distancia com sinal: positiva se do lado certo
    return distancias.min()

retas = {'A': (np.array([1.0, 0.2]), -4.8), 'B': (np.array([0.2, 1.0]), -4.6), 'C': (np.array([1.0, 1.0]), -8.0)}
for nome, (w, b) in retas.items():
    print(f'Reta {nome}: menor distancia de um ponto a reta = {margem_da_reta(w, b):.3f}')

# 2) A SVM encontra a reta de margem maxima (C muito grande = nao tolera erros: margem "rigida")
svm = SVC(kernel='linear', C=1e6).fit(X, y)
w, b = svm.coef_[0], svm.intercept_[0]
print(f'\nSVM: w = {np.round(w, 3)}, b = {b:.3f}')
print(f'Margem = 2/||w|| = {2 / np.linalg.norm(w):.3f}  (distancia ao ponto mais proximo = {margem_da_reta(w, b):.3f})')
print('Vetores de suporte:', svm.support_vectors_.tolist())
print('y (w.x + b) para cada ponto:', np.round(y * (X @ w + b), 2))
# Os vetores de suporte sao exatamente os pontos com y(w.x+b) = 1. Todos os outros tem valor maior que 1.

# 3) A funcao de decisao so depende dos vetores de suporte: f(x) = soma alfa_i y_i (x_i . x) + b
novo = np.array([4.0, 4.0])
f_manual = np.sum(svm.dual_coef_[0] * (svm.support_vectors_ @ novo)) + b
print(f'\nPonto novo {novo}: f calculada so com os vetores de suporte = {f_manual:.3f}; '
      f'scikit-learn = {svm.decision_function([novo])[0]:.3f} -> classe {int(np.sign(f_manual))}')
# Retirar do treino um ponto que NAO e vetor de suporte nao muda nada:
sem_um = SVC(kernel='linear', C=1e6).fit(np.delete(X, 0, axis=0), np.delete(y, 0))
print('Retirando o ponto (1, 2), que nao e vetor de suporte: w =', np.round(sem_um.coef_[0], 3))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.8))
xs = np.linspace(0, 8, 100)
cores_pontos = np.where(y == 1, '#BD5B58', '#2F648F')
for eixo in (esq, dir):
    eixo.scatter(X[:, 0], X[:, 1], c=cores_pontos, s=60, edgecolor='white', zorder=3)
    eixo.set_xlim(0, 8)
    eixo.set_ylim(0, 8)
    eixo.set_xlabel('x1')
    eixo.set_ylabel('x2')
for (nome, (wr, br)), cor in zip(retas.items(), ['#8794A3', '#D69A35', '#168A8A']):
    esq.plot(xs, -(wr[0] * xs + br) / wr[1], color=cor, label=f'reta {nome}: folga {margem_da_reta(wr, br):.2f}')
esq.legend(loc='upper left')
esq.set_title('Três retas separam; a folga até o ponto mais próximo muda', fontsize=11)
for desloc, estilo in [(0, '-'), (1, '--'), (-1, '--')]:
    dir.plot(xs, -(w[0] * xs + b - desloc) / w[1], color='#20324A', linestyle=estilo, linewidth=1.5 if desloc == 0 else 1)
dir.scatter(*svm.support_vectors_.T, s=220, facecolor='none', edgecolor='#D69A35', linewidth=2, zorder=4,
            label='vetores de suporte')
dir.legend(loc='upper left')
dir.set_title(f'SVM: margem máxima = {2 / np.linalg.norm(w):.2f}', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'margem_maxima.png'))
plt.show()
