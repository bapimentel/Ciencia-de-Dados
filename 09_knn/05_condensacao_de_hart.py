# Condensacao de Hart: reduzir o conjunto de treino do 1-NN sem perder acerto.
# Ideia: comecar com um exemplo; percorrer os demais; sempre que o 1-NN com o conjunto atual errar um
# exemplo, acrescenta-lo ao conjunto. Repetir ate uma passada sem erros. Os escolhidos ficam perto da fronteira.
# Dados simulados (duas classes em forma de lua), semente fixa.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
X, y = make_moons(n_samples=600, noise=0.2, random_state=4)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

def classificar_1nn(prototipos_x, prototipos_y, ponto):
    distancias = np.sqrt(((prototipos_x - ponto) ** 2).sum(axis=1))
    return prototipos_y[np.argmin(distancias)]

escolhidos = [0]                    # comeca com o primeiro exemplo
passada = 0
while True:
    passada += 1
    erros = 0
    for i in range(len(X_tr)):
        if i in escolhidos:
            continue
        if classificar_1nn(X_tr[escolhidos], y_tr[escolhidos], X_tr[i]) != y_tr[i]:
            escolhidos.append(i)    # errou: este exemplo carrega informacao nova
            erros += 1
    print(f'passada {passada}: {erros} erros, conjunto com {len(escolhidos)} exemplos')
    if erros == 0:
        break

completo = KNeighborsClassifier(n_neighbors=1).fit(X_tr, y_tr)
condensado = KNeighborsClassifier(n_neighbors=1).fit(X_tr[escolhidos], y_tr[escolhidos])
print(f'\n1-NN com todos os {len(X_tr)} exemplos: acuracia no teste {completo.score(X_te, y_te):.3f}')
print(f'1-NN com {len(escolhidos)} exemplos ({len(escolhidos) / len(X_tr):.0%}): acuracia no teste {condensado.score(X_te, y_te):.3f}')

cores = np.array(['#2F648F', '#168A8A'])
fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.4), sharey=True)
esq.scatter(X_tr[:, 0], X_tr[:, 1], c=cores[y_tr], s=10, alpha=0.6)
esq.set_title(f'Treino completo: {len(X_tr)} exemplos ({completo.score(X_te, y_te):.0%} no teste)', fontsize=11)
dir.scatter(X_tr[:, 0], X_tr[:, 1], color='#E6EBF0', s=10)
dir.scatter(X_tr[escolhidos, 0], X_tr[escolhidos, 1], c=cores[y_tr[escolhidos]], s=22, edgecolor='#20324A', linewidth=0.4)
dir.set_title(f'Condensado (Hart): {len(escolhidos)} exemplos, perto da fronteira ({condensado.score(X_te, y_te):.0%})', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'condensacao_de_hart.png'))
plt.show()
