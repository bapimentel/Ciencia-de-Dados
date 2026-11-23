# Sobreajuste (overfitting): quando o modelo decora o treino e perde a capacidade de generalizar.
# Parte 1 (simulado): polinomios de grau crescente ajustados a poucos pontos com ruido.
# Parte 2 (real): arvores de profundidade crescente na base de cancer de mama.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
gerador = np.random.default_rng(1)

# --- Parte 1. Verdade: y = sen(x) + ruido. Treino com 15 pontos; teste com 200.
def verdade(x):
    return np.sin(x)

x_tr = np.sort(gerador.uniform(0, 6, 15))
y_tr = verdade(x_tr) + gerador.normal(0, 0.3, 15)
x_te = gerador.uniform(0, 6, 200)
y_te = verdade(x_te) + gerador.normal(0, 0.3, 200)
graus = range(0, 13)
erro_tr, erro_te = [], []
for g in graus:
    coef = np.polyfit(x_tr, y_tr, g)
    erro_tr.append(np.mean((np.polyval(coef, x_tr) - y_tr) ** 2))
    erro_te.append(np.mean((np.polyval(coef, x_te) - y_te) ** 2))
    print(f'grau {g:2d}: erro no treino {erro_tr[-1]:.3f} | erro no teste {erro_te[-1]:.3f}')
melhor = int(np.argmin(erro_te))

fig, eixos = plt.subplots(1, 4, figsize=(15, 3.8))
xs = np.linspace(0, 6, 300)
for eixo, g, titulo in [(eixos[0], 1, 'grau 1: simples demais'), (eixos[1], 3, 'grau 3: equilibrado'), (eixos[2], 12, 'grau 12: decorou o treino')]:
    coef = np.polyfit(x_tr, y_tr, g)
    eixo.scatter(x_tr, y_tr, color='#2F648F', zorder=3, label='treino')
    eixo.plot(xs, verdade(xs), color='#8794A3', linestyle='--', label='verdade')
    eixo.plot(xs, np.polyval(coef, xs), color='#D69A35' if g != 12 else '#BD5B58', linewidth=2)
    eixo.set_ylim(-2.2, 2.2)
    eixo.set_title(titulo, fontsize=11)
eixos[0].legend(fontsize=8)
eixos[3].plot(list(graus), erro_tr, marker='o', color='#2F648F', label='treino')
eixos[3].plot(list(graus), erro_te, marker='o', color='#BD5B58', label='teste')
eixos[3].axvline(melhor, color='#D69A35', linestyle='--')
eixos[3].set_yscale('log')
eixos[3].set_xlabel('grau do polinômio (complexidade)')
eixos[3].set_ylabel('erro quadrático médio')
eixos[3].set_title('Treino só melhora; teste piora depois de um ponto', fontsize=11)
eixos[3].legend(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'sobreajuste_polinomios.png'))
plt.show()

# --- Parte 2. Arvores na base real
base = load_breast_cancer()
X, y = base.data, (base.target == 0).astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
profundidades = range(1, 16)
acc_tr, acc_te, acc_cv = [], [], []
for p in profundidades:
    arvore = DecisionTreeClassifier(max_depth=p, random_state=0).fit(X_tr, y_tr)
    acc_tr.append(arvore.score(X_tr, y_tr))
    acc_te.append(arvore.score(X_te, y_te))
    acc_cv.append(cross_val_score(DecisionTreeClassifier(max_depth=p, random_state=0), X_tr, y_tr,
                                  cv=StratifiedKFold(5, shuffle=True, random_state=0)).mean())
melhor_p = list(profundidades)[int(np.argmax(acc_cv))]
print(f'\nProfundidade escolhida pela validacao cruzada no treino: {melhor_p} '
      f'(acuracia no teste com ela: {acc_te[melhor_p - 1]:.3f}; com profundidade 15: {acc_te[-1]:.3f})')

fig, eixo = plt.subplots(figsize=(8, 4.2))
eixo.plot(list(profundidades), acc_tr, marker='o', color='#2F648F', label='treino')
eixo.plot(list(profundidades), acc_cv, marker='o', color='#168A8A', label='validação cruzada (no treino)')
eixo.plot(list(profundidades), acc_te, marker='o', color='#BD5B58', label='teste (só para conferir)')
eixo.axvline(melhor_p, color='#D69A35', linestyle='--')
eixo.set_xlabel('Profundidade máxima da árvore')
eixo.set_ylabel('Acurácia')
eixo.set_title('O treino chega a 100%; validação e teste param perto de 91–94%')
eixo.legend()
plt.savefig(os.path.join(pasta, 'figuras', 'sobreajuste_arvores.png'))
plt.show()
# Leitura: a partir de profundidade ~4 o acerto no treino chega a 99-100%, mas o de validacao e o de teste
# param de subir. A diferenca entre treino e teste (6 a 9 pontos) e o sinal do sobreajuste: o que a arvore
# aprende a mais e especifico do treino. Nesta base o prejuizo e pequeno; no exemplo dos polinomios, enorme.
# A complexidade e escolhida pela VALIDACAO (dentro do treino), nunca pelo teste: o teste so confere no fim.
