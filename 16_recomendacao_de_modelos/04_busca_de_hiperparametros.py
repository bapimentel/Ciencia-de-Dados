# Escolhido o algoritmo, falta escolher os hiperparametros. Duas estrategias com o mesmo orcamento
# (36 avaliacoes por validacao cruzada), no SVM com kernel RBF, na base real de digitos manuscritos:
#   busca em grade: 6 valores de C x 6 valores de gamma, todos os pares
#   busca aleatoria: 36 pares sorteados em escala logaritmica nos mesmos intervalos
# Repetimos a busca aleatoria com 20 sementes para ver a variacao.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
X, y = load_digits(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
dobras = StratifiedKFold(3, shuffle=True, random_state=0)
cache = {}


def avaliar(C, gamma):
    chave = (round(np.log10(C), 6), round(np.log10(gamma), 6))
    if chave not in cache:
        modelo = make_pipeline(StandardScaler(), SVC(C=C, gamma=gamma))
        cache[chave] = cross_val_score(modelo, X_tr, y_tr, cv=dobras).mean()
    return cache[chave]


Cs = np.logspace(-2, 3, 6)
gammas = np.logspace(-5, 0, 6)
grade = [(C, g) for C in Cs for g in gammas]
gerador = np.random.default_rng(0)
grade = [grade[i] for i in gerador.permutation(len(grade))]     # a ordem de visita da grade e arbitraria
curva_grade = np.maximum.accumulate([avaliar(C, g) for C, g in grade])
melhor_grade = max(grade, key=lambda par: avaliar(*par))
print(f'Grade: melhor validacao {curva_grade[-1]:.4f} com C={melhor_grade[0]:g}, gamma={melhor_grade[1]:g}')

curvas_aleatorias = []
for semente in range(20):
    g = np.random.default_rng(semente)
    pares = [(10 ** g.uniform(-2, 3), 10 ** g.uniform(-5, 0)) for _ in range(36)]
    curvas_aleatorias.append(np.maximum.accumulate([avaliar(C, gm) for C, gm in pares]))
curvas_aleatorias = np.array(curvas_aleatorias)
print(f'Aleatoria (20 repeticoes): melhor validacao final mediana {np.median(curvas_aleatorias[:, -1]):.4f} '
      f'(de {curvas_aleatorias[:, -1].min():.4f} a {curvas_aleatorias[:, -1].max():.4f})')
for orcamento in [5, 10, 20, 36]:
    print(f'  com {orcamento:2d} avaliacoes: grade {curva_grade[orcamento - 1]:.4f} | '
          f'aleatoria mediana {np.median(curvas_aleatorias[:, orcamento - 1]):.4f}')

final = make_pipeline(StandardScaler(), SVC(C=melhor_grade[0], gamma=melhor_grade[1])).fit(X_tr, y_tr)
print(f'Modelo escolhido pela grade, no teste: {final.score(X_te, y_te):.4f}')

fig, eixo = plt.subplots(figsize=(8.5, 4.3))
x = np.arange(1, 37)
eixo.fill_between(x, np.percentile(curvas_aleatorias, 10, axis=0), np.percentile(curvas_aleatorias, 90, axis=0),
                  color='#168A8A', alpha=0.15, label='aleatória: faixa de 80% das 20 repetições')
eixo.plot(x, np.median(curvas_aleatorias, axis=0), color='#168A8A', linewidth=2, label='aleatória: mediana')
eixo.step(x, curva_grade, where='post', color='#2F648F', linewidth=2, label='grade (ordem de visita sorteada)')
eixo.set_xlabel('Número de combinações avaliadas')
eixo.set_ylabel('Melhor acurácia de validação até aqui')
eixo.set_ylim(0.8, 1.0)
eixo.set_title('Mesmo orçamento: quanto cada busca encontra a cada avaliação', fontsize=11)
eixo.legend(loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'busca_de_hiperparametros.png'))
plt.show()
