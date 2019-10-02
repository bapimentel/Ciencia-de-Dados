# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:19:12 2019

@author: Bruno Pimentel
"""

# Bibliotecas
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

dataset = pd.read_csv('Dados/Data.csv') # importando os dados
# Dividindo os dados em atributos dependentes e independentes
X = dataset.iloc[:, :-1].values # atributos para determinar a classe
Y = dataset.iloc[:, -1].values # variavel dependente

# tratando valores faltantes: substituindo os valores NaN pela media
imputer = SimpleImputer(missing_values=np.nan, strategy='mean') 
imputer = imputer.fit(X[:, 1:])
X[:, 1:] = imputer.transform(X[:, 1:])

# codificando dados categoricos
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[:, 0] = labelencoder_X.fit_transform(X[:, 0])
onehotencoder = OneHotEncoder(categorical_features=[0])
X = onehotencoder.fit_transform(X).toarray()
labelencoder_Y = LabelEncoder()
Y = labelencoder_Y.fit_transform(Y)

# dividindo os dados em treinamento e teste
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# normalizando as variaveis
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)