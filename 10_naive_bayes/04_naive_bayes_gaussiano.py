# Naive Bayes com atributos numericos (gaussiano): cada atributo, dentro de cada classe, e modelado por
# uma normal. Bom classificador, mau estimador de probabilidades: veremos as duas coisas.
# Dados reais: cancer de mama (569 exames, 30 medidas).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.calibration import calibration_curve

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = (base.target == 0).astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

# O que o modelo aprende: media e variancia de cada atributo em cada classe
nb = GaussianNB().fit(X_tr, y_tr)
print('Media de "mean radius" por classe (benigno, maligno):', nb.theta_[:, 0].round(2))
print('Variancia de "mean radius" por classe:', nb.var_[:, 0].round(2))

dobras = StratifiedKFold(10, shuffle=True, random_state=0)
print(f'\nAcuracia (validacao cruzada): Naive Bayes {cross_val_score(GaussianNB(), X, y, cv=dobras).mean():.3f} | '
      f'regressao logistica {cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), X, y, cv=dobras).mean():.3f}')

# Probabilidades: o Naive Bayes multiplica 30 verossimilhancas como se fossem independentes. Como raio,
# perimetro e area medem quase a mesma coisa, a mesma evidencia e contada tres vezes -> excesso de confianca.
prob_nb = nb.predict_proba(X_te)[:, 1]
logistica = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_tr, y_tr)
prob_log = logistica.predict_proba(X_te)[:, 1]
extremas_nb = np.mean((prob_nb < 0.01) | (prob_nb > 0.99))
extremas_log = np.mean((prob_log < 0.01) | (prob_log > 0.99))
print(f'Fracao de probabilidades abaixo de 1% ou acima de 99%: Naive Bayes {extremas_nb:.0%} | logistica {extremas_log:.0%}')
erros_confiantes = int(((prob_nb > 0.99) & (y_te == 0)).sum() + ((prob_nb < 0.01) & (y_te == 1)).sum())
print(f'Erros do Naive Bayes com probabilidade > 99% na classe errada: {erros_confiantes}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
bins = np.linspace(0, 1, 21)
esq.hist(prob_nb, bins=bins, color='#D69A35', alpha=0.8, label='Naive Bayes')
esq.hist(prob_log, bins=bins, color='#2F648F', alpha=0.6, label='regressão logística')
esq.set_xlabel('Probabilidade prevista de maligno')
esq.set_ylabel('Exames (teste)')
esq.set_title('Naive Bayes empurra quase tudo para 0 ou 1', fontsize=11)
esq.legend()
for prob, nome, cor in [(prob_nb, 'Naive Bayes', '#D69A35'), (prob_log, 'regressão logística', '#2F648F')]:
    real, prevista = calibration_curve(y_te, prob, n_bins=6, strategy='quantile')
    dir.plot(prevista, real, marker='o', color=cor, label=nome)
dir.plot([0, 1], [0, 1], linestyle='--', color='#8794A3', label='calibração perfeita')
dir.set_xlabel('Probabilidade prevista (média da faixa)')
dir.set_ylabel('Fração real de malignos')
dir.set_title('Calibração: "70%" deveria acontecer 70% das vezes', fontsize=11)
dir.legend(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'naive_bayes_gaussiano.png'))
plt.show()
# Use o Naive Bayes pela classe que ele escolhe (rapido, bom com muitos atributos, como em texto),
# mas nao leve a serio o valor da probabilidade.
