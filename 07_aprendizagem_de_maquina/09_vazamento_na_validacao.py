# Vazamento na validacao: selecionar atributos (ou padronizar, imputar, aplicar PCA) com TODOS os dados
# antes da validacao cruzada produz desempenho falso. Demonstracao classica com dados SEM nenhum sinal.
# Dados simulados: 100 casos, 5000 colunas de puro ruido, alvo sorteado ao acaso. Nenhum modelo honesto
# deveria passar de 50% de acerto.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
gerador = np.random.default_rng(0)
X = gerador.normal(size=(100, 5000))
y = gerador.integers(0, 2, size=100)
dobras = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

# ERRADO: escolher as 20 colunas mais associadas ao alvo usando todos os dados, depois validar
X_escolhido = SelectKBest(f_classif, k=20).fit_transform(X, y)
errado = cross_val_score(LogisticRegression(max_iter=1000), X_escolhido, y, cv=dobras)
print(f'Selecao ANTES da validacao: acuracia {errado.mean():.2f}  <- parece um modelo bom, mas os dados sao ruido')

# CERTO: a selecao faz parte do modelo e e refeita dentro de cada dobra, so com o treino daquela dobra
pipeline = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000))
certo = cross_val_score(pipeline, X, y, cv=dobras)
print(f'Selecao DENTRO da validacao: acuracia {certo.mean():.2f}  <- o acaso, como deveria ser')

# Repetindo com 30 alvos sorteados para ver que nao e sorte
erradas, certas = [], []
for semente in range(30):
    y_sorteado = np.random.default_rng(semente + 100).integers(0, 2, size=100)
    Xe = SelectKBest(f_classif, k=20).fit_transform(X, y_sorteado)
    erradas.append(cross_val_score(LogisticRegression(max_iter=1000), Xe, y_sorteado, cv=dobras).mean())
    certas.append(cross_val_score(pipeline, X, y_sorteado, cv=dobras).mean())
print(f'30 repeticoes: errado {np.mean(erradas):.2f} | certo {np.mean(certas):.2f}')

fig, eixo = plt.subplots(figsize=(7.5, 4))
eixo.hist(certas, bins=np.arange(0.2, 1.01, 0.04), color='#2F648F', alpha=0.8, label='seleção dentro da validação (certo)')
eixo.hist(erradas, bins=np.arange(0.2, 1.01, 0.04), color='#BD5B58', alpha=0.8, label='seleção antes da validação (vazamento)')
eixo.axvline(0.5, color='#20324A', linestyle='--', linewidth=1)
eixo.text(0.51, eixo.get_ylim()[1] * 0.9, 'acaso', color='#20324A')
eixo.set_xlabel('Acurácia estimada por validação cruzada (dados sem nenhum sinal)')
eixo.set_ylabel('Repetições')
eixo.set_title('Com vazamento, ruído puro parece prever o alvo')
eixo.legend(fontsize=9, loc='upper left')
plt.savefig(os.path.join(pasta, 'figuras', 'vazamento_na_validacao.png'))
plt.show()

# Regra: tudo que aprende com os dados (selecao, padronizacao, imputacao, PCA) vai dentro do pipeline.
# Para escolher hiperparametros E estimar desempenho, use validacao cruzada aninhada (uma dentro da outra).
# Em series temporais, o futuro nunca ajuda a prever o passado. E pergunte sempre: esta coluna existira
# no momento de usar o modelo?
