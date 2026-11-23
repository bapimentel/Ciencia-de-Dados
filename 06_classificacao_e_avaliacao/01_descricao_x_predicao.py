# Descrever nao e prever. Primeiro contato com uma tarefa de classificacao e com a linha de base.
# Dados: base de cancer de mama de Wisconsin (569 exames, 30 medidas, diagnostico maligno/benigno),
# dados reais incluidos no scikit-learn.

import os
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score

pasta = os.path.dirname(os.path.abspath(__file__))

base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
# No scikit-learn, 0 = maligno e 1 = benigno. Vamos deixar explicito: alvo = 1 quando maligno.
y = pd.Series((base.target == 0).astype(int), name='maligno')

print('Registros:', len(X), '| variaveis:', X.shape[1])
print('Alvo (1 = maligno):')
print(y.value_counts())
print(f'Proporcao de malignos: {y.mean():.3f}')

# DESCREVER: o que diferencia os grupos nesta amostra
print('\nMedia de algumas medidas por grupo:')
print(X[['mean radius', 'mean texture', 'mean concave points']].groupby(y).mean().round(2))
# Isso resume o passado. Nao diz ainda quao bem conseguimos acertar um exame NOVO.

# PREVER: separar o que o modelo ve (treino) do que ele nunca viu (teste)
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
print('\nTreino:', len(X_treino), '| Teste:', len(X_teste))
print('Proporcao de malignos no treino e no teste:', round(y_treino.mean(), 3), round(y_teste.mean(), 3))
# stratify=y mantem a proporcao das classes nas duas partes.

# Linha de base: um "modelo" que sempre responde a classe mais frequente
base_linha = DummyClassifier(strategy='most_frequent').fit(X_treino, y_treino)
previsao_base = base_linha.predict(X_teste)
print('\nAcuracia da linha de base (sempre "benigno"):', round(accuracy_score(y_teste, previsao_base), 3))
# Qualquer modelo precisa superar isso. Uma acuracia de 63% aqui nao vale nada.

# Uma regra manual, a partir da descricao: raio medio acima de 15 -> maligno
regra = (X_teste['mean radius'] > 15).astype(int)
print('Acuracia da regra "raio > 15":', round(accuracy_score(y_teste, regra), 3))
# Ja supera a linha de base. Os proximos scripts deixam o modelo descobrir regras melhores.

# Experimente: troque o limiar 15 por 13 e por 17. A acuracia sobe ou desce? Por que?
