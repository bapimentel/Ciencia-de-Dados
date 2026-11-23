# Regressao logistica: um primeiro classificador e a matriz de confusao.

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = pd.Series((base.target == 0).astype(int), name='maligno')
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

# Escala aprendida no treino (as 30 medidas tem unidades muito diferentes)
escala = StandardScaler()
X_treino_p = escala.fit_transform(X_treino)
X_teste_p = escala.transform(X_teste)

# O modelo: estima a probabilidade de "maligno" como funcao das medidas
modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_treino_p, y_treino)

previsao = modelo.predict(X_teste_p)
print('Acuracia no teste:', round(accuracy_score(y_teste, previsao), 3))
print('Acuracia no treino:', round(accuracy_score(y_treino, modelo.predict(X_treino_p)), 3))

# A matriz de confusao mostra ONDE o modelo erra
matriz = confusion_matrix(y_teste, previsao)
print('Matriz de confusao (linhas = real, colunas = previsto):')
print(matriz)
vn, fp, fn, vp = matriz.ravel()
print(f'Verdadeiros negativos: {vn} | Falsos positivos: {fp} | Falsos negativos: {fn} | Verdadeiros positivos: {vp}')
# Falso negativo aqui = exame maligno classificado como benigno. E o erro mais grave.

fig, eixo = plt.subplots(figsize=(4.5, 4))
ConfusionMatrixDisplay(matriz, display_labels=['benigno', 'maligno']).plot(ax=eixo, cmap='Blues', colorbar=False)
eixo.set_xlabel('Previsto')
eixo.set_ylabel('Real')
eixo.set_title(f'Regressão logística: {fn} malignos passaram como benignos')
eixo.grid(False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'matriz_confusao_logistica.png'))
plt.show()

# O modelo da probabilidades, nao so rotulos. O rotulo vem de um corte em 0,5 (script 05 muda isso)
probabilidade = modelo.predict_proba(X_teste_p)[:, 1]
print('Primeiras probabilidades de maligno:', probabilidade[:5].round(3))

# Coeficientes: sinal e tamanho indicam a direcao e a forca de cada medida (apos padronizacao)
coeficientes = pd.Series(modelo.coef_[0], index=X.columns).sort_values()
print('\nMedidas que mais puxam para "maligno":')
print(coeficientes.tail(5).round(2))
print('Medidas que mais puxam para "benigno":')
print(coeficientes.head(5).round(2))

# Experimente: remova a padronizacao (use X_treino e X_teste direto). O modelo converge? A acuracia muda?
