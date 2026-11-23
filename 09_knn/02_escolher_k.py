# Qual o melhor k? k pequeno: fronteira irregular, sensivel a ruido (alta variancia).
# k grande: fronteira suave demais, ignora detalhes (alto vies). Escolhemos k por validacao.
# Dados reais: cancer de mama (569 exames), com padronizacao dentro do pipeline.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
base = load_breast_cancer()
X, y = base.data, (base.target == 0).astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

valores_k = list(range(1, 52, 2))
acc_treino, acc_holdout, acc_cv = [], [], []
# Hold-out DENTRO do treino: separamos uma parte do treino para validar (o teste fica guardado)
X_ajuste, X_val, y_ajuste, y_val = train_test_split(X_tr, y_tr, test_size=0.3, random_state=1, stratify=y_tr)
for k in valores_k:
    modelo = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
    modelo.fit(X_ajuste, y_ajuste)
    acc_treino.append(modelo.score(X_ajuste, y_ajuste))
    acc_holdout.append(modelo.score(X_val, y_val))
    acc_cv.append(cross_val_score(modelo, X_tr, y_tr, cv=StratifiedKFold(10, shuffle=True, random_state=0)).mean())
melhor_k = valores_k[int(np.argmax(acc_cv))]
print(f'k escolhido pela validacao cruzada (10 dobras, no treino): {melhor_k}  (acuracia {max(acc_cv):.3f})')
final = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=melhor_k)).fit(X_tr, y_tr)
print(f'Acuracia no teste com k={melhor_k}: {final.score(X_te, y_te):.3f}')
print(f'Com k=1: treino {acc_treino[0]:.3f} (decora) | validacao {acc_holdout[0]:.3f}')

fig, eixo = plt.subplots(figsize=(8, 4.2))
eixo.plot(valores_k, acc_treino, marker='o', markersize=4, color='#8794A3', label='treino (o próprio ajuste)')
eixo.plot(valores_k, acc_holdout, marker='o', markersize=4, color='#2F648F', label='hold-out de validação')
eixo.plot(valores_k, acc_cv, marker='o', markersize=4, color='#168A8A', label='validação cruzada (10 dobras)')
eixo.axvline(melhor_k, color='#D69A35', linestyle='--')
eixo.set_xlabel('k (número de vizinhos)')
eixo.set_ylabel('Acurácia')
eixo.set_title(f'k = 1 decora o treino; a validação cruzada escolhe k = {melhor_k}')
eixo.legend()
plt.savefig(os.path.join(pasta, 'figuras', 'escolher_k.png'))
plt.show()

# Fronteiras em 2 dimensoes (duas medidas padronizadas), para VER vies e variancia
duas = StandardScaler().fit_transform(X[:, [0, 1]])        # raio medio e textura media
xx, yy = np.meshgrid(np.linspace(-2.5, 4, 300), np.linspace(-2.5, 4.5, 300))
grade = np.column_stack([xx.ravel(), yy.ravel()])
fig, eixos = plt.subplots(1, 3, figsize=(14, 4.2), sharey=True)
for eixo, k in zip(eixos, [1, 15, 101]):
    modelo = KNeighborsClassifier(n_neighbors=k).fit(duas, y)
    zona = modelo.predict(grade).reshape(xx.shape)
    eixo.contourf(xx, yy, zona, levels=[-0.5, 0.5, 1.5], colors=['#DCE6EF', '#F2DAD9'])
    eixo.scatter(duas[:, 0], duas[:, 1], c=np.where(y == 1, '#BD5B58', '#2F648F'), s=6, alpha=0.6)
    titulo = {1: 'k = 1: fronteira irregular (variância alta)', 15: 'k = 15: equilíbrio', 101: 'k = 101: suave demais (viés alto)'}[k]
    eixo.set_title(titulo, fontsize=11)
    eixo.set_xlabel('raio médio (padronizado)')
    eixo.grid(False)
eixos[0].set_ylabel('textura média (padronizada)')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'fronteiras_por_k.png'))
plt.show()
