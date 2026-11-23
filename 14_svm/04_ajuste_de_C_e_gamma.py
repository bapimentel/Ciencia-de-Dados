# Ajuste dos parametros da SVM com kernel RBF: C (custo das violacoes) e gamma (alcance de cada exemplo).
# gamma pequeno: cada vetor de suporte influencia uma regiao grande -> fronteira suave.
# gamma grande: influencia so a vizinhanca -> fronteira contorna cada ponto (sobreajuste).
# Parte 1: o efeito de gamma, visto em duas "luas" entrelacadas.
# Parte 2: busca em grade (grid search) com validacao cruzada na base real de cancer de mama.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, load_breast_cancer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Parte 1
X, y = make_moons(n_samples=300, noise=0.25, random_state=0)
X_tr, X_va, y_tr, y_va = train_test_split(X, y, test_size=0.4, random_state=0)
fig, eixos = plt.subplots(1, 4, figsize=(16, 3.9), sharey=True)
xx, yy = np.meshgrid(np.linspace(-1.6, 2.6, 250), np.linspace(-1.2, 1.7, 250))
print('gamma   treino  validacao  vetores de suporte')
for eixo, gamma in zip(eixos, [0.1, 1, 10, 100]):
    svm = SVC(kernel='rbf', gamma=gamma, C=1).fit(X_tr, y_tr)
    print(f'{gamma:<6}  {svm.score(X_tr, y_tr):.3f}   {svm.score(X_va, y_va):.3f}      {len(svm.support_)}')
    zona = svm.decision_function(np.column_stack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
    eixo.contourf(xx, yy, zona > 0, levels=[-0.5, 0.5, 1.5], colors=['#DCE6EF', '#F3DEDD'])
    eixo.contour(xx, yy, zona, levels=[0], colors='#20324A', linewidths=1)
    eixo.scatter(X_tr[:, 0], X_tr[:, 1], c=np.where(y_tr == 1, '#BD5B58', '#2F648F'), s=12, edgecolor='white', linewidth=0.3)
    eixo.set_title(f'γ = {gamma}: treino {svm.score(X_tr, y_tr):.0%}, validação {svm.score(X_va, y_va):.0%}', fontsize=10)
    eixo.grid(False)
plt.suptitle('γ pequeno: fronteira quase reta (subajuste). γ grande: ilhas em volta de cada ponto (sobreajuste)', fontsize=11, y=1.03)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'efeito_gamma.png'), bbox_inches='tight')
plt.show()

# --- Parte 2
base = load_breast_cancer()
X, y = base.data, base.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
modelo = make_pipeline(StandardScaler(), SVC(kernel='rbf'))
grade = {'svc__C': [0.01, 0.1, 1, 10, 100, 1000], 'svc__gamma': [0.0001, 0.001, 0.01, 0.1, 1, 10]}
busca = GridSearchCV(modelo, grade, cv=StratifiedKFold(5, shuffle=True, random_state=0)).fit(X_tr, y_tr)
tabela = pd.DataFrame(busca.cv_results_['params']).rename(columns=lambda c: c.replace('svc__', ''))
tabela['acerto'] = busca.cv_results_['mean_test_score']
mapa = tabela.pivot(index='C', columns='gamma', values='acerto')
print('\nValidacao cruzada (5 dobras) no treino, para cada par (C, gamma):')
print(mapa.round(3))
print(f'Melhor: {busca.best_params_} -> validacao {busca.best_score_:.3f}; teste {busca.score(X_te, y_te):.3f}')

# O melhor par caiu num canto da grade (maior C, menor gamma). Quando isso acontece, o otimo pode estar
# fora da grade: ampliamos a busca naquela direcao antes de concluir.
grade_ampliada = {'svc__C': [100, 1000, 10000, 100000], 'svc__gamma': [0.000001, 0.00001, 0.0001, 0.001]}
busca2 = GridSearchCV(modelo, grade_ampliada, cv=StratifiedKFold(5, shuffle=True, random_state=0)).fit(X_tr, y_tr)
print(f'Grade ampliada: melhor {busca2.best_params_} -> validacao {busca2.best_score_:.3f}; teste {busca2.score(X_te, y_te):.3f}')
# Repare na distancia entre a validacao do melhor par e o teste: ao escolher o maximo entre 36 combinacoes,
# a validacao do vencedor fica otimista. Por isso o teste, separado desde o inicio, e quem da a estimativa final.

sem_escala = SVC(kernel='rbf', C=busca.best_params_['svc__C'], gamma=busca.best_params_['svc__gamma']).fit(X_tr, y_tr)
print(f'Mesmos parametros SEM padronizar: teste {sem_escala.score(X_te, y_te):.3f}')
# A SVM com RBF mede distancias: sem padronizar, variaveis com valores grandes (area, ~1000) dominam as pequenas.

fig, eixo = plt.subplots(figsize=(7.5, 5))
imagem = eixo.imshow(mapa.values, cmap='Blues', vmin=0.6, vmax=1.0)
eixo.set_xticks(range(len(mapa.columns)), [str(g) for g in mapa.columns])
eixo.set_yticks(range(len(mapa.index)), [str(c) for c in mapa.index])
for i in range(mapa.shape[0]):
    for j in range(mapa.shape[1]):
        valor = mapa.values[i, j]
        eixo.text(j, i, f'{valor:.3f}', ha='center', va='center', fontsize=8.5,
                  color='white' if valor > 0.85 else '#20324A')
i_m = list(mapa.index).index(busca.best_params_['svc__C'])
j_m = list(mapa.columns).index(busca.best_params_['svc__gamma'])
eixo.add_patch(plt.Rectangle((j_m - 0.5, i_m - 0.5), 1, 1, fill=False, edgecolor='#D69A35', linewidth=3))
eixo.set_xlabel('γ')
eixo.set_ylabel('C')
eixo.grid(False)
eixo.set_title('Acerto na validação cruzada: uma faixa diagonal de bons pares', fontsize=11)
plt.colorbar(imagem, ax=eixo, shrink=0.8)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'grade_C_gamma.png'))
plt.show()
