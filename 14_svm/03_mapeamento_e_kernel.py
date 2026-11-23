# Problemas que nenhuma reta separa podem ficar separaveis num espaco de dimensao maior.
# Parte 1: em 1 dimensao, a classe positiva fica no meio. Mapeando x -> (x, x^2), uma reta separa.
# Parte 2: o "truque do kernel". A SVM so precisa de produtos internos phi(a).phi(b); um kernel calcula
#          esse produto direto no espaco original, sem construir phi.
#          Polinomial de grau 2: K(a, b) = (a.b + 1)^2
#          Gaussiano (RBF):      K(a, b) = exp(-gamma ||a - b||^2)
# Parte 3: dois circulos concentricos, separados por SVM com kernel RBF.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.svm import SVC

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Parte 1
x = np.array([-4, -3, -2.5, -1, -0.5, 0, 0.5, 1.2, 2.6, 3, 4])
y = np.where(np.abs(x) < 2, 1, -1)
linear_1d = SVC(kernel='linear', C=1e6).fit(x.reshape(-1, 1), y)
print(f'Em 1D, uma reta (um ponto de corte) acerta {linear_1d.score(x.reshape(-1, 1), y):.0%} dos pontos')
mapeado = np.column_stack([x, x ** 2])
linear_2d = SVC(kernel='linear', C=1e6).fit(mapeado, y)
w, b = linear_2d.coef_[0], linear_2d.intercept_[0]
print(f'Depois de mapear para (x, x^2): acerto {linear_2d.score(mapeado, y):.0%}; '
      f'fronteira {w[0]:.2f} x + {w[1]:.2f} x^2 + {b:.2f} = 0')

# --- Parte 2: o kernel polinomial de grau 2 e o produto interno de um mapeamento de 6 dimensoes
def phi(v):
    a, c = v
    r2 = np.sqrt(2)
    return np.array([1, r2 * a, r2 * c, a ** 2, c ** 2, r2 * a * c])

a, c = np.array([1.0, 2.0]), np.array([3.0, -1.0])
print(f'\nphi(a).phi(b) calculado em 6 dimensoes = {phi(a) @ phi(c):.1f}')
print(f'(a.b + 1)^2 calculado em 2 dimensoes    = {(a @ c + 1) ** 2:.1f}')
# Mesmo numero, sem nunca construir phi. O kernel RBF corresponde a um espaco de dimensao infinita.

# --- Parte 3
Xc, yc = make_circles(n_samples=300, noise=0.08, factor=0.45, random_state=0)
linear = SVC(kernel='linear').fit(Xc, yc)
rbf = SVC(kernel='rbf', gamma=1.0, C=1.0).fit(Xc, yc)
print(f'\nCirculos: SVM linear acerta {linear.score(Xc, yc):.2f}; SVM com kernel RBF acerta {rbf.score(Xc, yc):.2f}')

fig, eixos = plt.subplots(1, 3, figsize=(15, 4.3))
cor1 = np.where(y == 1, '#BD5B58', '#2F648F')
eixos[0].scatter(x, np.zeros_like(x), c=cor1, s=70, edgecolor='white', zorder=3)
eixos[0].set_yticks([])
eixos[0].set_ylim(-1, 1)
eixos[0].set_xlabel('x')
eixos[0].set_title('1D: a classe vermelha fica no meio', fontsize=11)
eixos[1].scatter(x, x ** 2, c=cor1, s=70, edgecolor='white', zorder=3)
xs = np.linspace(-4.5, 4.5, 100)
eixos[1].plot(xs, -(w[0] * xs + b) / w[1], color='#20324A', linestyle='--')
eixos[1].set_xlabel('x')
eixos[1].set_ylabel('x²')
eixos[1].set_ylim(-1, 17)
eixos[1].set_title('Com x² como 2ª coordenada, uma reta separa', fontsize=11)
xx, yy = np.meshgrid(np.linspace(-1.5, 1.5, 300), np.linspace(-1.5, 1.5, 300))
zona = rbf.decision_function(np.column_stack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
eixos[2].contourf(xx, yy, zona > 0, levels=[-0.5, 0.5, 1.5], colors=['#DCE6EF', '#F3DEDD'])
eixos[2].contour(xx, yy, zona, levels=[0], colors='#20324A', linewidths=1.2)
eixos[2].scatter(Xc[:, 0], Xc[:, 1], c=np.where(yc == 1, '#BD5B58', '#2F648F'), s=14, edgecolor='white', linewidth=0.3)
eixos[2].set_title(f'Kernel RBF: fronteira circular (acerto {rbf.score(Xc, yc):.0%})', fontsize=11)
eixos[2].grid(False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'mapeamento_e_kernel.png'))
plt.show()
