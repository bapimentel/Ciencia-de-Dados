# Margem suave: quando as classes se sobrepoem, nenhuma reta separa tudo. A SVM passa a aceitar
# violacoes (variaveis de folga xi_i), pagando um custo C por elas:
#   minimizar  ||w||^2 / 2 + C * soma(xi_i)     sujeito a  y_i (w . x_i + b) >= 1 - xi_i,  xi_i >= 0
# C pequeno: margem larga, muitas violacoes toleradas. C grande: margem estreita, tenta acertar todo o treino.
# Dados reais: duas medidas (petala) de duas especies de iris que se sobrepoem (versicolor x virginica).

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, StratifiedKFold

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

iris = load_iris()
filtro = iris.target > 0
X = iris.data[filtro][:, 2:4]
y = np.where(iris.target[filtro] == 2, 1, -1)
dobras = StratifiedKFold(5, shuffle=True, random_state=0)

print('C        margem  vetores de suporte  acerto treino  validacao cruzada')
resultados = {}
for C in [0.01, 0.1, 1, 10, 100, 1000]:
    svm = SVC(kernel='linear', C=C).fit(X, y)
    margem = 2 / np.linalg.norm(svm.coef_[0])
    cv = cross_val_score(SVC(kernel='linear', C=C), X, y, cv=dobras).mean()
    resultados[C] = svm
    print(f'{C:<8} {margem:6.2f}  {len(svm.support_):18d}  {svm.score(X, y):13.2f}  {cv:17.3f}')

fig, eixos = plt.subplots(1, 3, figsize=(15, 4.4), sharey=True)
xs = np.linspace(2.8, 7.2, 100)
cores = np.where(y == 1, '#BD5B58', '#2F648F')
for eixo, C in zip(eixos, [0.01, 1, 100]):
    svm = resultados[C]
    w, b = svm.coef_[0], svm.intercept_[0]
    eixo.scatter(X[:, 0], X[:, 1], c=cores, s=22, edgecolor='white', linewidth=0.4, zorder=3)
    eixo.scatter(*svm.support_vectors_.T, s=70, facecolor='none', edgecolor='#D69A35', linewidth=1.2, zorder=4)
    for desloc, estilo in [(0, '-'), (1, '--'), (-1, '--')]:
        eixo.plot(xs, -(w[0] * xs + b - desloc) / w[1], color='#20324A', linestyle=estilo, linewidth=1.3)
    eixo.set_xlim(2.8, 7.2)
    eixo.set_ylim(0.8, 2.7)
    eixo.set_xlabel('Comprimento da pétala (cm)')
    eixo.set_title(f'C = {C}: margem {2 / np.linalg.norm(w):.2f}, {len(svm.support_)} vetores de suporte', fontsize=11)
eixos[0].set_ylabel('Largura da pétala (cm)')
plt.suptitle('Versicolor (azul) × virginica (vermelho). Círculos âmbar: vetores de suporte', fontsize=11, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'margem_suave.png'), bbox_inches='tight')
plt.show()
