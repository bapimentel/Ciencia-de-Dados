# O k-NN depende inteiramente da distancia: atributos em escalas diferentes decidem sozinhos.
# Dados reais: vinhos (178 vinhos de 3 cultivares italianos, 13 medidas quimicas), incluidos no scikit-learn.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
vinhos = load_wine()
X = pd.DataFrame(vinhos.data, columns=vinhos.feature_names)
y = vinhos.target
print('Amplitude (max - min) de cada medida:')
amplitude = (X.max() - X.min()).sort_values(ascending=False)
print(amplitude.round(2))
# 'proline' varia mais de 1000 unidades; 'hue' varia ~1. Sem escala, a distancia e quase so 'proline'.

dobras = StratifiedKFold(10, shuffle=True, random_state=0)
sem_escala = cross_val_score(KNeighborsClassifier(n_neighbors=5), X, y, cv=dobras)
com_escala = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)), X, y, cv=dobras)
so_proline = cross_val_score(KNeighborsClassifier(n_neighbors=5), X[['proline']], y, cv=dobras)
print(f'\nk-NN (k=5) sem padronizar:   {sem_escala.mean():.3f}')
print(f'k-NN (k=5) so com proline:   {so_proline.mean():.3f}  <- quase o mesmo: as outras 12 medidas nao contavam')
print(f'k-NN (k=5) padronizado:      {com_escala.mean():.3f}')

# Contribuicao de cada atributo para a distancia ao quadrado entre dois vinhos quaisquer (media dos pares)
gerador = np.random.default_rng(0)
pares = gerador.integers(0, len(X), size=(2000, 2))
contrib_bruta = ((X.values[pares[:, 0]] - X.values[pares[:, 1]]) ** 2).mean(axis=0)
Xp = StandardScaler().fit_transform(X)
contrib_padr = ((Xp[pares[:, 0]] - Xp[pares[:, 1]]) ** 2).mean(axis=0)
peso_bruto = pd.Series(contrib_bruta / contrib_bruta.sum(), index=X.columns).sort_values()
peso_padr = pd.Series(contrib_padr / contrib_padr.sum(), index=X.columns).reindex(peso_bruto.index)

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True)
esq.barh(peso_bruto.index, 100 * peso_bruto.values, color=['#8794A3'] * 12 + ['#BD5B58'])
esq.set_xlabel('% da distância ao quadrado')
esq.set_title(f'Sem padronizar: proline responde por {100 * peso_bruto["proline"]:.0f}%\n(acurácia {sem_escala.mean():.2f})', fontsize=11)
dir.barh(peso_padr.index, 100 * peso_padr.values, color='#2F648F')
dir.set_xlabel('% da distância ao quadrado')
dir.set_title(f'Padronizado: as 13 medidas contribuem\n(acurácia {com_escala.mean():.2f})', fontsize=11)
for eixo in (esq, dir):
    eixo.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'escala_importa.png'))
plt.show()
