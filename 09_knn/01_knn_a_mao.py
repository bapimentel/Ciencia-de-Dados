# K-vizinhos mais proximos (k-NN) feito a mao: guardar os exemplos, medir distancias, votar.
# Dados reais: flores iris (150 flores, 3 especies), so as duas medidas da petala, em cm.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
iris = load_iris()
flores = pd.DataFrame(iris.data[:, 2:4], columns=['comprimento', 'largura'])
flores['especie'] = [iris.target_names[t] for t in iris.target]

# "Treinar" o k-NN e so guardar os exemplos. Nenhuma conta e feita aqui.
treino = flores

# Uma flor nova, de especie desconhecida
nova = np.array([4.9, 1.6])

# 1) distancia euclidiana da flor nova para cada flor guardada
diferencas = treino[['comprimento', 'largura']].values - nova
treino = treino.assign(distancia=np.sqrt((diferencas ** 2).sum(axis=1)))

# 2) ordenar e pegar as k mais proximas
vizinhos = treino.sort_values('distancia').head(7)
print('As 7 flores mais proximas da nova (4.9 x 1.6 cm):')
print(vizinhos.round(3).to_string())

# 3) votar: a especie mais frequente entre os k vizinhos
for k in [1, 3, 5, 7]:
    votos = vizinhos.head(k)['especie'].value_counts()
    print(f'k={k}: votos {dict((str(e), int(v)) for e, v in votos.items())} -> {votos.idxmax()}')
# A resposta e versicolor para todos esses k, mas o placar aperta: com k=7, 4 contra 3.
# A flor esta na fronteira entre versicolor e virginica; um k maior poderia virar o resultado.

# Conferencia com scikit-learn
for k in [1, 3, 5, 7]:
    modelo = KNeighborsClassifier(n_neighbors=k).fit(flores[['comprimento', 'largura']], flores['especie'])
    print(f'scikit-learn k={k}: {modelo.predict(pd.DataFrame([nova], columns=["comprimento", "largura"]))[0]}')

cores = {'setosa': '#8794A3', 'versicolor': '#2F648F', 'virginica': '#168A8A'}
fig, eixo = plt.subplots(figsize=(7.5, 4.8))
for especie, grupo in flores.groupby('especie'):
    eixo.scatter(grupo['comprimento'], grupo['largura'], s=22, color=cores[especie], alpha=0.7, label=especie)
for _, v in vizinhos.head(5).iterrows():
    eixo.plot([nova[0], v['comprimento']], [nova[1], v['largura']], color='#D69A35', linewidth=1)
raio = vizinhos.head(5)['distancia'].max()
eixo.add_patch(plt.Circle(nova, raio, fill=False, color='#D69A35', linestyle='--'))
eixo.scatter(*nova, marker='*', s=300, color='#D69A35', edgecolor='#20324A', zorder=5, label='flor nova')
eixo.set_xlabel('Comprimento da pétala (cm)')
eixo.set_ylabel('Largura da pétala (cm)')
eixo.set_aspect('equal')
eixo.set_title('k = 5: os cinco vizinhos mais próximos votam')
eixo.legend(fontsize=9, loc='upper left')
plt.savefig(os.path.join(pasta, 'figuras', 'knn_a_mao.png'))
plt.show()

# Custo: classificar UMA flor exige calcular n distancias de p dimensoes -> O(n*p).
# O k-NN e "preguicoso": nao aprende nada antes; todo o trabalho acontece na hora de classificar.
