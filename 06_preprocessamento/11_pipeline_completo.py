# Pipeline completo de pre-processamento, na ordem correta:
# separar treino e teste -> imputar ausentes -> codificar categorias -> padronizar -> juntar.
# Tudo o que e aprendido dos dados (medias, categorias, escala) e aprendido SO no treino.
# O alvo e codificado com map, que deixa claro o que vira 0 e 1.

import os
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

pasta = os.path.dirname(os.path.abspath(__file__))
dataset = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Data.csv'))

# Atributos (X) e variavel dependente (Y)
X = dataset[['Region', 'Age', 'Income']]
Y = dataset['Online Shopper'].map({'No': 0, 'Yes': 1})

# 1) Separar treino e teste ANTES de qualquer ajuste
X_treino, X_teste, Y_treino, Y_teste = train_test_split(X, Y, test_size=0.2, random_state=0)
print('Treino:', X_treino.shape, '| Teste:', X_teste.shape)

# 2) Valores faltantes nas colunas numericas: media aprendida no treino
imputador = SimpleImputer(missing_values=np.nan, strategy='mean')
numericas_treino = imputador.fit_transform(X_treino[['Age', 'Income']])
numericas_teste = imputador.transform(X_teste[['Age', 'Income']])

# 3) Categoria 'Region': one-hot aprendido no treino
codificador = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
regiao_treino = codificador.fit_transform(X_treino[['Region']])
regiao_teste = codificador.transform(X_teste[['Region']])

# 4) Escala das numericas: media e desvio do treino
escala = StandardScaler()
numericas_treino = escala.fit_transform(numericas_treino)
numericas_teste = escala.transform(numericas_teste)

# 5) Juntar tudo em matrizes prontas para um modelo
X_treino_pronto = np.hstack([regiao_treino, numericas_treino])
X_teste_pronto = np.hstack([regiao_teste, numericas_teste])
nomes = list(codificador.get_feature_names_out(['Region'])) + ['Age_z', 'Income_z']

print(pd.DataFrame(X_treino_pronto, columns=nomes).round(2))
print(pd.DataFrame(X_teste_pronto, columns=nomes).round(2))
print('Y_treino:', Y_treino.tolist(), '| Y_teste:', Y_teste.tolist())

# Com 10 linhas, nenhum modelo faria sentido; o objetivo aqui e a sequencia das etapas.
# A unidade 07 aplica a mesma sequencia a uma base com centenas de registros.
