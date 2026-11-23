# Figura didatica: fronteiras de decisao de tres classificadores nos mesmos dados.
# Saida: figuras/geradas/fronteira_de_decisao.png. Base iris (petala), duas especies dificeis de separar.

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'estilo.mplstyle'))

iris = load_iris()
mascara = iris.target > 0                 # versicolor (1) e virginica (2)
X = iris.data[mascara][:, 2:4]            # comprimento e largura da petala
y = iris.target[mascara] - 1              # 0 = versicolor, 1 = virginica

modelos = [
    ('Regressão logística: uma reta', LogisticRegression().fit(X, y)),
    ('Árvore (profundidade 3): cortes em escada', DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, y)),
    ('K-NN (k = 7): segue os vizinhos', KNeighborsClassifier(n_neighbors=7).fit(X, y)),
]

xx, yy = np.meshgrid(np.linspace(2.5, 7.5, 300), np.linspace(0.8, 2.8, 300))
grade = np.column_stack([xx.ravel(), yy.ravel()])
fundo = ListedColormap(['#DCE6EF', '#D5E9E9'])
cores = np.array(['#2F648F', '#168A8A'])

fig, eixos = plt.subplots(1, 3, figsize=(12, 3.9), sharex=True, sharey=True)
for eixo, (nome, modelo) in zip(eixos, modelos):
    regiao = modelo.predict(grade).reshape(xx.shape)
    eixo.contourf(xx, yy, regiao, levels=[-0.5, 0.5, 1.5], cmap=fundo)
    eixo.scatter(X[:, 0], X[:, 1], c=cores[y], s=22, edgecolors='white', linewidths=0.5)
    acerto = (modelo.predict(X) == y).mean()
    eixo.set_title(f'{nome}\nacerto nos próprios dados: {acerto:.2f}', fontsize=10.5)
    eixo.set_xlabel('Comprimento da pétala (cm)')
    eixo.grid(False)
eixos[0].set_ylabel('Largura da pétala (cm)')
eixos[0].text(2.7, 2.6, 'virginica', color='#168A8A', fontweight='bold')
eixos[0].text(2.7, 0.95, 'versicolor', color='#2F648F', fontweight='bold')
fig.suptitle('A fronteira é o que o modelo aprendeu; formas mais flexíveis acertam mais aqui, mas generalizam?', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, '..', 'geradas', 'fronteira_de_decisao.png'))
print('Figura salva em figuras/geradas/fronteira_de_decisao.png')
