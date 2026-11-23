# Animacao: uma arvore de decisao divide o plano com cortes paralelos aos eixos, um no por vez.
# Saidas: animacoes/geradas/arvore_particionando.gif e .png. Dados reais: iris (petala), 3 especies.

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

iris = load_iris()
X, y = iris.data[:, 2:4], iris.target
cores = np.array(['#8794A3', '#2F648F', '#168A8A'])
fundos = ['#EEF0F3', '#DCE6EF', '#D5E9E9']
xx, yy = np.meshgrid(np.linspace(0.5, 7.2, 250), np.linspace(0, 2.7, 250))
grade = np.column_stack([xx.ravel(), yy.ravel()])

fig, eixo = plt.subplots(figsize=(8, 4.5))

def quadro(i):
    eixo.clear()
    folhas = i + 1
    if folhas == 1:
        zona = np.zeros(len(grade), dtype=int)       # um unico no: tudo e a classe majoritaria
        acerto = np.mean(y == 0)
    else:
        arvore = DecisionTreeClassifier(max_leaf_nodes=folhas, random_state=0).fit(X, y)
        zona = arvore.predict(grade)
        acerto = arvore.score(X, y)
    eixo.contourf(xx, yy, zona.reshape(xx.shape), levels=[-0.5, 0.5, 1.5, 2.5], colors=fundos)
    eixo.scatter(X[:, 0], X[:, 1], c=cores[y], s=16, edgecolor='white', linewidth=0.3)
    eixo.set_xlabel('Comprimento da pétala (cm)')
    eixo.set_ylabel('Largura da pétala (cm)')
    eixo.grid(False)
    eixo.set_title(f'{folhas} folha(s): cada nova pergunta corta uma região em duas (acerto {acerto:.0%})')
    return []

quadros = [0, 1, 2, 3, 4, 5, 6, 7] + [7] * 3
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=1200, blit=False)
animacao.save(os.path.join(saida, 'arvore_particionando.gif'), writer=PillowWriter(fps=0.9), dpi=70)
quadro(3)
plt.savefig(os.path.join(saida, 'arvore_particionando.png'))
print('Salvo: animacoes/geradas/arvore_particionando.gif e .png')
