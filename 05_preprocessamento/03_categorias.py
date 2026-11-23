# Transformar categorias em numeros: codificacao one-hot e de rotulos.
# Atualiza o trecho de LabelEncoder/OneHotEncoder de preprocessamento.py (2019):
# o parametro categorical_features deixou de existir; hoje o OneHotEncoder recebe a coluna de texto direto.

import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

pasta = os.path.dirname(os.path.abspath(__file__))
clientes = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Data.csv'))
print(clientes)

# Por que codificar? Modelos fazem contas; 'India' e 'USA' nao entram em uma conta.
# Errado para categorias sem ordem: trocar por 0, 1, 2 inventa uma ordem (India < USA < Brazil?).

# One-hot: uma coluna 0/1 para cada categoria
codificador = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
regiao_codificada = codificador.fit_transform(clientes[['Region']])
colunas = codificador.get_feature_names_out(['Region'])
print(pd.DataFrame(regiao_codificada, columns=colunas).astype(int))

# O mesmo com pandas, em uma linha
print(pd.get_dummies(clientes, columns=['Region'], dtype=int))

# Variavel-alvo com duas classes: LabelEncoder (ou um simples map)
codificador_alvo = LabelEncoder()
alvo = codificador_alvo.fit_transform(clientes['Online Shopper'])
print('Classes:', list(codificador_alvo.classes_), '->', alvo)
print('Com map:', clientes['Online Shopper'].map({'No': 0, 'Yes': 1}).tolist())

# Categorias COM ordem (ordinal) podem virar numeros que respeitam a ordem
tamanhos = pd.Series(['P', 'M', 'G', 'M', 'P'])
ordem = {'P': 1, 'M': 2, 'G': 3}
print(tamanhos.map(ordem).tolist())

# handle_unknown='ignore' importa: se aparecer uma regiao nova nos dados de teste,
# o codificador gera zeros em vez de quebrar.
novo = pd.DataFrame({'Region': ['Chile']})
print(codificador.transform(novo))

# Experimente: codifique 'Product line' de dados/supermercado.csv. Quantas colunas surgem?
