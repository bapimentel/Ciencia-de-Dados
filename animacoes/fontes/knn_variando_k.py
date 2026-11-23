# Animacao: a fronteira de decisao do k-NN conforme k cresce de 1 a 75.
# Saidas: animacoes/geradas/knn_variando_k.gif e .png. Dados simulados (make_moons), semente fixa.

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

X, y = make_moons(n_samples=300, noise=0.3, random_state=2)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)
xx, yy = np.meshgrid(np.linspace(-2, 3, 160), np.linspace(-1.6, 2.1, 160))
grade = np.column_stack([xx.ravel(), yy.ravel()])
valores_k = [1, 2, 3, 5, 7, 9, 13, 17, 25, 35, 50, 75]

fig, eixo = plt.subplots(figsize=(8, 4.5))

def quadro(i):
    eixo.clear()
    k = valores_k[i]
    modelo = KNeighborsClassifier(n_neighbors=k).fit(X_tr, y_tr)
    zona = modelo.predict(grade).reshape(xx.shape)
    eixo.contourf(xx, yy, zona, levels=[-0.5, 0.5, 1.5], colors=['#DCE6EF', '#D5E9E9'])
    eixo.scatter(X_tr[:, 0], X_tr[:, 1], c=np.where(y_tr == 1, '#168A8A', '#2F648F'), s=14)
    eixo.set_xticks([])
    eixo.set_yticks([])
    eixo.grid(False)
    eixo.set_title(f'k = {k}: acerto no treino {modelo.score(X_tr, y_tr):.0%}, no teste {modelo.score(X_te, y_te):.0%}')
    return []

quadros = list(range(len(valores_k))) + [len(valores_k) - 1] * 3
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=900, blit=False)
animacao.save(os.path.join(saida, 'knn_variando_k.gif'), writer=PillowWriter(fps=1.1), dpi=70)
quadro(4)
plt.savefig(os.path.join(saida, 'knn_variando_k.png'))
print('Salvo: animacoes/geradas/knn_variando_k.gif e .png')
