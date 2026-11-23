# Matriz de confusao e as medidas que saem dela, primeiro a mao (7 casos) e depois em dados reais.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, fbeta_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- 1. A mao: 7 casos, classe positiva = 1
real = np.array([0, 0, 0, 0, 0, 1, 1])
predita = np.array([0, 1, 1, 0, 1, 1, 1])
VP = int(((real == 1) & (predita == 1)).sum())    # verdadeiro positivo: era 1, disse 1
FN = int(((real == 1) & (predita == 0)).sum())    # falso negativo: era 1, disse 0
FP = int(((real == 0) & (predita == 1)).sum())    # falso positivo: era 0, disse 1
VN = int(((real == 0) & (predita == 0)).sum())    # verdadeiro negativo: era 0, disse 0
P, N = VP + FN, FP + VN
print(f'VP={VP} FN={FN} FP={FP} VN={VN}  (P={P} positivos reais, N={N} negativos reais)')

acuracia = (VP + VN) / (P + N)
erro = (FP + FN) / (P + N)
revocacao = VP / P                     # sensibilidade: dos positivos, quantos encontrei
especificidade = VN / N                # dos negativos, quantos reconheci como negativos
precisao = VP / (VP + FP)              # dos que chamei de positivo, quantos eram
f1 = 2 * precisao * revocacao / (precisao + revocacao)
print(f'acuracia={acuracia:.3f} erro={erro:.3f} revocacao={revocacao:.3f} especificidade={especificidade:.3f} '
      f'precisao={precisao:.3f} F1={f1:.3f}')
# Este classificador encontrou TODOS os positivos (revocacao 1) a custa de 3 alarmes falsos (precisao 0,4).

# F-beta: beta > 1 da mais peso a revocacao; beta < 1, a precisao
for beta in [0.5, 1, 2]:
    fb = (1 + beta ** 2) * precisao * revocacao / (beta ** 2 * precisao + revocacao)
    print(f'F{beta}: {fb:.3f} (scikit-learn: {fbeta_score(real, predita, beta=beta):.3f})')

# --- 2. Em dados reais: exames de cancer de mama (positivo = maligno)
base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = (base.target == 0).astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
escala = StandardScaler().fit(X_tr)
modelo = LogisticRegression(max_iter=1000).fit(escala.transform(X_tr), y_tr)
previsto = modelo.predict(escala.transform(X_te))
matriz = confusion_matrix(y_te, previsto)
print('\nRegressao logistica no teste (linhas = real; colunas = previsto):')
print(matriz)
print(classification_report(y_te, previsto, target_names=['benigno', 'maligno'], digits=3))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4.4))
esq.axis('off')
esq.set_xlim(0, 3)
esq.set_ylim(0, 3)
textos = [[('VN', 'era 0, disse 0', '#2F648F'), ('FP', 'era 0, disse 1\n(alarme falso)', '#D69A35')],
          [('FN', 'era 1, disse 0\n(passou despercebido)', '#BD5B58'), ('VP', 'era 1, disse 1', '#2F648F')]]
for i in range(2):
    for j in range(2):
        sigla, descricao, cor = textos[i][j]
        esq.add_patch(plt.Rectangle((1 + j, 1 - i), 1, 1, facecolor=cor, alpha=0.18, edgecolor='white', linewidth=3))
        esq.text(1.5 + j, 1.62 - i, sigla, ha='center', fontsize=18, fontweight='bold', color=cor)
        esq.text(1.5 + j, 1.25 - i, descricao, ha='center', va='center', fontsize=9, color='#20324A')
esq.text(1.5, 2.15, 'previsto 0', ha='center')
esq.text(2.5, 2.15, 'previsto 1', ha='center')
esq.text(0.95, 1.5, 'real 0', ha='right', va='center')
esq.text(0.95, 0.5, 'real 1', ha='right', va='center')
esq.text(0.1, 2.75, 'revocação = VP / (VP + FN)     precisão = VP / (VP + FP)\nespecificidade = VN / (VN + FP)', fontsize=9.5, color='#20324A')
esq.set_title('Os quatro resultados possíveis')
ConfusionMatrixDisplay(matriz, display_labels=['benigno', 'maligno']).plot(ax=dir, cmap='Blues', colorbar=False)
dir.set_xlabel('Previsto')
dir.set_ylabel('Real')
dir.set_title(f'Regressão logística, 171 exames: {matriz[1, 0]} malignos passaram')
dir.grid(False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'matriz_de_confusao.png'))
plt.show()
