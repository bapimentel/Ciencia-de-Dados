# Classes desbalanceadas e validacao cruzada: quando a acuracia engana e como medir com menos sorte.

import os
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

pasta = os.path.dirname(os.path.abspath(__file__))

base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = pd.Series((base.target == 0).astype(int), name='maligno')

# --- Desbalanceamento: mantemos todos os benignos e so 25 malignos (cerca de 7%)
gerador = np.random.default_rng(0)
indices_malignos = y[y == 1].index
manter = gerador.choice(indices_malignos, size=25, replace=False)
indices = np.concatenate([y[y == 0].index, manter])
X_d, y_d = X.loc[indices], y.loc[indices]
print('Base desbalanceada:', y_d.value_counts().to_dict(), f'| proporcao de malignos: {y_d.mean():.3f}')

X_tr, X_te, y_tr, y_te = train_test_split(X_d, y_d, test_size=0.3, random_state=0, stratify=y_d)

ingenuo = DummyClassifier(strategy='most_frequent').fit(X_tr, y_tr)
print('\nSempre "benigno":  acuracia', round(accuracy_score(y_te, ingenuo.predict(X_te)), 3),
      '| revocacao', recall_score(y_te, ingenuo.predict(X_te)))
# 93% de acuracia sem encontrar um unico maligno.

modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_tr, y_tr)
p = modelo.predict(X_te)
print('Logistica:         acuracia', round(accuracy_score(y_te, p), 3), '| revocacao', round(recall_score(y_te, p), 3),
      '| precisao', round(precision_score(y_te, p, zero_division=0), 3))

# class_weight='balanced' penaliza mais os erros na classe rara
modelo_b = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight='balanced')).fit(X_tr, y_tr)
p = modelo_b.predict(X_te)
print('Logistica balanc.: acuracia', round(accuracy_score(y_te, p), 3), '| revocacao', round(recall_score(y_te, p), 3),
      '| precisao', round(precision_score(y_te, p, zero_division=0), 3))
# Com 8 malignos no teste, uma unidade a mais ou a menos muda muito a revocacao. Por isso...

# --- Validacao cruzada: varias divisoes, media e variacao da metrica
# make_pipeline garante que a escala e ajustada dentro de cada dobra, so com o treino daquela dobra.
dobras = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
for nome, estimador in [('logistica', make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))),
                        ('logistica balanceada', make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight='balanced')))]:
    f1 = cross_val_score(estimador, X_d, y_d, cv=dobras, scoring='f1')
    rev = cross_val_score(estimador, X_d, y_d, cv=dobras, scoring='recall')
    print(f'\n{nome}: F1 por dobra {f1.round(2)} -> media {f1.mean():.2f} ± {f1.std():.2f}')
    print(f'{" " * len(nome)}  revocacao por dobra {rev.round(2)} -> media {rev.mean():.2f} ± {rev.std():.2f}')

# A variacao entre dobras e parte do resultado. Um unico numero de acuracia esconde essa incerteza.

# Experimente: repita com a base completa (X, y). A variacao entre dobras diminui?
