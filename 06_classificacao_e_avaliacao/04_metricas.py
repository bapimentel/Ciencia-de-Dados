# Alem da acuracia: precisao, revocacao, F1 e curva ROC.

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             classification_report, roc_curve, roc_auc_score)

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = pd.Series((base.target == 0).astype(int), name='maligno')
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

escala = StandardScaler().fit(X_treino)
logistica = LogisticRegression(max_iter=1000).fit(escala.transform(X_treino), y_treino)
floresta = RandomForestClassifier(n_estimators=200, random_state=0).fit(X_treino, y_treino)

prob_logistica = logistica.predict_proba(escala.transform(X_teste))[:, 1]
prob_floresta = floresta.predict_proba(X_teste)[:, 1]

for nome, prob in [('Regressao logistica', prob_logistica), ('Floresta aleatoria', prob_floresta)]:
    previsao = (prob >= 0.5).astype(int)
    print(f'\n{nome}')
    print('  acuracia :', round(accuracy_score(y_teste, previsao), 3))
    print('  precisao :', round(precision_score(y_teste, previsao), 3), '  (dos que chamei de maligno, quantos eram)')
    print('  revocacao:', round(recall_score(y_teste, previsao), 3), '  (dos malignos, quantos encontrei)')
    print('  F1       :', round(f1_score(y_teste, previsao), 3), '  (media harmonica das duas)')
    print('  AUC      :', round(roc_auc_score(y_teste, prob), 3), '  (ordenacao das probabilidades, independe do corte)')

# O relatorio por classe
print('\nRelatorio da regressao logistica:')
print(classification_report(y_teste, (prob_logistica >= 0.5).astype(int), target_names=['benigno', 'maligno']))

# Curva ROC: taxa de verdadeiros positivos x taxa de falsos positivos para todos os cortes possiveis
fig, eixo = plt.subplots(figsize=(5, 4.5))
for nome, prob, cor in [('Regressão logística', prob_logistica, '#2F648F'), ('Floresta aleatória', prob_floresta, '#168A8A')]:
    tfp, tvp, _ = roc_curve(y_teste, prob)
    eixo.plot(tfp, tvp, color=cor, label=f'{nome} (AUC {roc_auc_score(y_teste, prob):.3f})')
eixo.plot([0, 1], [0, 1], color='#8794A3', linestyle='--', linewidth=1, label='Aleatório (AUC 0,5)')
eixo.set_xlabel('Taxa de falsos positivos')
eixo.set_ylabel('Taxa de verdadeiros positivos (revocação)')
eixo.set_title('Curva ROC: os dois modelos separam bem as classes')
eixo.legend(loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'curva_roc.png'))
plt.show()

# Qual metrica importa depende do custo de cada erro:
# - deixar passar um maligno (falso negativo) pede revocacao alta;
# - encaminhar benignos para biopsia (falso positivo) tem custo menor, mas nao e zero.
# O script 05 transforma isso em uma escolha de limiar.

# Experimente: calcule precisao e revocacao tratando "benigno" como classe positiva (pos_label=0).
