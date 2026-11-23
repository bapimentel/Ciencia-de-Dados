# Sobreajuste e poda: deixar a arvore crescer ate o fim e depois podar os ramos que nao compensam.
# Poda por custo-complexidade: para cada valor de alfa, remove-se a subarvore com menor ganho de erro por folha,
# alfa = (R(t) - R(T_t)) / (|folhas de T_t| - 1). Escolhemos alfa por validacao cruzada no treino.
# Dados reais: cancer de mama.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
base = load_breast_cancer()
X, y = base.data, (base.target == 0).astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

completa = DecisionTreeClassifier(random_state=0).fit(X_tr, y_tr)
print(f'Arvore completa: {completa.get_n_leaves()} folhas, profundidade {completa.get_depth()} | '
      f'treino {completa.score(X_tr, y_tr):.3f} | teste {completa.score(X_te, y_te):.3f}')

# Caminho de poda: a sequencia de alfas em que cada subarvore deixa de compensar
caminho = completa.cost_complexity_pruning_path(X_tr, y_tr)
alfas = caminho.ccp_alphas[:-1]           # o ultimo alfa poda tudo ate a raiz
dobras = StratifiedKFold(5, shuffle=True, random_state=0)
folhas, acc_cv, ep_cv, acc_te = [], [], [], []
for a in alfas:
    arvore = DecisionTreeClassifier(random_state=0, ccp_alpha=a).fit(X_tr, y_tr)
    folhas.append(arvore.get_n_leaves())
    notas = cross_val_score(DecisionTreeClassifier(random_state=0, ccp_alpha=a), X_tr, y_tr, cv=dobras)
    acc_cv.append(notas.mean())
    ep_cv.append(notas.std(ddof=1) / np.sqrt(len(notas)))   # erro padrao da media das 5 dobras
    acc_te.append(arvore.score(X_te, y_te))
print('\n alfa    folhas  validacao  (erro padrao)')
for a, f, m, e in zip(alfas, folhas, acc_cv, ep_cv):
    print(f'{a:.4f}   {f:5d}   {m:.3f}      ({e:.3f})')

maior_cv = int(np.argmax(acc_cv))
# Regra de um erro padrao: entre as arvores cuja validacao fica a menos de 1 erro padrao da melhor,
# escolhemos a MENOR. A diferenca entre elas cabe no ruido da propria validacao; a menor e mais legivel.
limite = acc_cv[maior_cv] - ep_cv[maior_cv]
melhor = max(i for i in range(len(alfas)) if acc_cv[i] >= limite)
podada = DecisionTreeClassifier(random_state=0, ccp_alpha=alfas[melhor]).fit(X_tr, y_tr)
print(f'\nMaior validacao: {acc_cv[maior_cv]:.3f} com {folhas[maior_cv]} folhas; limite de 1 erro padrao = {limite:.3f}')
print(f'Arvore escolhida: alfa {alfas[melhor]:.4f} -> {podada.get_n_leaves()} folhas | '
      f'validacao {acc_cv[melhor]:.3f} | teste {podada.score(X_te, y_te):.3f}')

# Alternativa: interromper o crescimento antes (profundidade maxima, minimo de exemplos por folha)
for minimo in [1, 5, 10, 20]:
    a = DecisionTreeClassifier(random_state=0, min_samples_leaf=minimo).fit(X_tr, y_tr)
    print(f'min_samples_leaf={minimo:2d}: {a.get_n_leaves():2d} folhas | teste {a.score(X_te, y_te):.3f}')

fig, eixo = plt.subplots(figsize=(8, 4.2))
eixo.errorbar(folhas, acc_cv, yerr=ep_cv, marker='o', markersize=4, color='#168A8A', capsize=3, label='validação cruzada (± 1 erro padrão)')
eixo.plot(folhas, acc_te, marker='o', markersize=4, color='#BD5B58', label='teste (só para conferir)')
eixo.axhline(limite, color='#8794A3', linestyle=':', label='limite de 1 erro padrão')
eixo.axvline(folhas[melhor], color='#D69A35', linestyle='--')
eixo.text(folhas[melhor] + 0.3, min(acc_te) + 0.005, f'{folhas[melhor]} folhas', color='#D69A35')
eixo.set_xlabel('Número de folhas depois da poda')
eixo.set_ylabel('Acurácia')
eixo.set_title(f'Árvore completa: {completa.get_n_leaves()} folhas; escolhida pela regra de 1 erro padrão: {podada.get_n_leaves()}', fontsize=11)
eixo.legend()
plt.savefig(os.path.join(pasta, 'figuras', 'poda.png'))
plt.show()
