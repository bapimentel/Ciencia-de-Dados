# Escala: por que padronizar e por que ajustar a transformacao so no treino.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

clientes = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Data.csv')).dropna()
print(clientes[['Age', 'Income']].describe().round(1))

# Idade varia em dezenas; renda, em dezenas de milhares. Uma distancia entre dois clientes
# seria dominada pela renda. Metodos baseados em distancia (K-NN, K-means) sofrem com isso.
a = clientes.iloc[0][['Age', 'Income']].astype(float).values
b = clientes.iloc[1][['Age', 'Income']].astype(float).values
print('Diferenca de idade:', abs(a[0] - b[0]), '| diferenca de renda:', abs(a[1] - b[1]))
print('Distancia euclidiana sem escala:', round(float(np.sqrt(((a - b) ** 2).sum())), 1), '(quase so renda)')

# Padronizacao: (valor - media) / desvio. Cada coluna passa a ter media 0 e desvio 1
padronizador = StandardScaler()
padronizado = padronizador.fit_transform(clientes[['Age', 'Income']])
print(pd.DataFrame(padronizado, columns=['Age_z', 'Income_z']).round(2))

# Min-max: leva para o intervalo [0, 1]
minmax = MinMaxScaler().fit_transform(clientes[['Age', 'Income']])
print(pd.DataFrame(minmax, columns=['Age_01', 'Income_01']).round(2))

# O significado nao se perde: a ordem e as distancias relativas dentro de cada coluna sao as mesmas
fig, (esq, dir) = plt.subplots(1, 2, figsize=(9, 3.6))
esq.scatter(clientes['Age'], clientes['Income'], color='#2F648F')
esq.set_xlabel('Idade (anos)')
esq.set_ylabel('Renda')
esq.set_title('Antes: escalas incomparáveis')
dir.scatter(padronizado[:, 0], padronizado[:, 1], color='#168A8A')
dir.set_xlabel('Idade (desvios da média)')
dir.set_ylabel('Renda (desvios da média)')
dir.set_title('Depois da padronização: mesma forma, mesma escala')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'padronizacao.png'))
plt.show()

# A regra que mais importa: fit no TREINO, transform no treino e no teste.
# Se a media e o desvio forem calculados com o teste junto, informacao do teste vaza para o treino.
X = clientes[['Age', 'Income']]
y = clientes['Online Shopper']
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=0)

padronizador = StandardScaler()
X_treino_p = padronizador.fit_transform(X_treino)     # aprende media e desvio do treino
X_teste_p = padronizador.transform(X_teste)           # aplica os MESMOS numeros ao teste
print('Media aprendida no treino:', padronizador.mean_.round(1))
print('Media do teste depois de transformar:', X_teste_p.mean(axis=0).round(2), '(nao precisa ser zero)')

# Experimente: padronize usando fit_transform no conjunto inteiro e compare as medias.
# A diferenca e pequena aqui, mas a pratica errada se repete em bases grandes com o mesmo efeito.
