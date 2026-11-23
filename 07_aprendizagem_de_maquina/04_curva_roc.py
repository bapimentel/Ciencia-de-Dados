# Curva ROC construida a mao, passo a passo, e depois para modelos reais.
# Parte 1: 20 instancias com a probabilidade prevista de serem positivas (exemplo didatico classico).
# Parte 2: regressao logistica e floresta aleatoria na base de cancer de mama.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Parte 1. Algoritmo: ordenar pela probabilidade; comecar em (0, 0); para cada instancia,
# se for positiva, subir 1/P; se for negativa, andar 1/N para a direita.
classes = ['P', 'P', 'N', 'P', 'P', 'P', 'N', 'N', 'P', 'N', 'P', 'N', 'P', 'N', 'N', 'N', 'P', 'N', 'P', 'N']
probabilidades = [0.90, 0.80, 0.70, 0.60, 0.56, 0.55, 0.54, 0.53, 0.52, 0.51, 0.40, 0.39, 0.38, 0.37, 0.36, 0.35, 0.34, 0.32, 0.30, 0.10]
P = classes.count('P')
N = classes.count('N')
tvp, tfp = [0.0], [0.0]
for classe in classes:                      # ja estao em ordem decrescente de probabilidade
    if classe == 'P':
        tvp.append(tvp[-1] + 1 / P)
        tfp.append(tfp[-1])
    else:
        tvp.append(tvp[-1])
        tfp.append(tfp[-1] + 1 / N)
tabela = pd.DataFrame({'classe': classes, 'prob': probabilidades, 'TFP depois': np.round(tfp[1:], 2), 'TVP depois': np.round(tvp[1:], 2)})
print(tabela.to_string(index=False))

# AUC: area sob a curva = soma dos retangulos dos passos para a direita
auc = sum((tfp[i + 1] - tfp[i]) * tvp[i] for i in range(len(tfp) - 1))
y_bin = [1 if c == 'P' else 0 for c in classes]
print(f'\nAUC a mao: {auc:.3f} | scikit-learn: {roc_auc_score(y_bin, probabilidades):.3f}')
# Interpretacao: AUC = probabilidade de um positivo sorteado receber nota maior que um negativo sorteado.
pares = [(p, n) for p, cp in zip(probabilidades, classes) if cp == 'P' for n, cn in zip(probabilidades, classes) if cn == 'N']
print(f'Fracao de pares (positivo, negativo) em que o positivo tem nota maior: {np.mean([p > n for p, n in pares]):.3f}')

# --- Parte 2. Modelos reais
base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = (base.target == 0).astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
escala = StandardScaler().fit(X_tr)
prob_log = LogisticRegression(max_iter=1000).fit(escala.transform(X_tr), y_tr).predict_proba(escala.transform(X_te))[:, 1]
prob_rf = RandomForestClassifier(n_estimators=200, random_state=0).fit(X_tr, y_tr).predict_proba(X_te)[:, 1]
prob_ruim = X_te['mean texture'].values          # uma "nota" fraca: so a textura media
for nome, prob in [('regressao logistica', prob_log), ('floresta aleatoria', prob_rf), ('so a textura media', prob_ruim)]:
    print(f'{nome:22s} AUC = {roc_auc_score(y_te, prob):.3f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12.5, 4.8))
esq.plot(tfp, tvp, color='#2F648F', marker='o', markersize=4, drawstyle='steps-post')
for i in [0, 1, 2]:
    esq.annotate(f'{i + 1}º: {probabilidades[i]:.2f} ({classes[i]})', xy=(tfp[i + 1], tvp[i + 1]), xytext=(10, -4 - 10 * (i == 2)),
                 textcoords='offset points', fontsize=8.5, color='#8794A3')
esq.plot([0, 1], [0, 1], linestyle='--', color='#8794A3', linewidth=1)
esq.fill_between(tfp, tvp, step='post', color='#2F648F', alpha=0.10)
esq.set_xlabel('Taxa de falsos positivos (FP / N)')
esq.set_ylabel('Taxa de verdadeiros positivos (VP / P)')
esq.set_title(f'À mão: positivo sobe, negativo anda (AUC {auc:.2f})')
for nome, prob, cor in [('Regressão logística', prob_log, '#2F648F'), ('Floresta aleatória', prob_rf, '#168A8A'), ('Só a textura média', prob_ruim, '#D69A35')]:
    a, b, _ = roc_curve(y_te, prob)
    dir.plot(a, b, color=cor, label=f'{nome} (AUC {roc_auc_score(y_te, prob):.2f})')
dir.plot([0, 1], [0, 1], linestyle='--', color='#8794A3', linewidth=1, label='aleatório (AUC 0,5)')
dir.set_xlabel('Taxa de falsos positivos')
dir.set_ylabel('Taxa de verdadeiros positivos')
dir.set_title('Modelos reais: mais perto do canto, melhor')
dir.legend(loc='lower right', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'curva_roc.png'))
plt.show()
