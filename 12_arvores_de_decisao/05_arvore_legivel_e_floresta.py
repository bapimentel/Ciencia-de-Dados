# Arvore de decisao e floresta aleatoria: regras legiveis, sobreajuste e importancia das variaveis.

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = pd.Series((base.target == 0).astype(int), name='maligno')
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
# Arvores nao precisam de padronizacao: cada corte olha uma variavel por vez.

# Arvore sem limite de profundidade: decora o treino
arvore_livre = DecisionTreeClassifier(random_state=0).fit(X_treino, y_treino)
print('Arvore livre  | treino:', round(accuracy_score(y_treino, arvore_livre.predict(X_treino)), 3),
      '| teste:', round(accuracy_score(y_teste, arvore_livre.predict(X_teste)), 3),
      '| profundidade:', arvore_livre.get_depth())

# Arvore rasa: menos acerto no treino, parecido ou melhor no teste
arvore_rasa = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_treino, y_treino)
print('Arvore rasa   | treino:', round(accuracy_score(y_treino, arvore_rasa.predict(X_treino)), 3),
      '| teste:', round(accuracy_score(y_teste, arvore_rasa.predict(X_teste)), 3))
# Acerto perfeito no treino e queda no teste = sobreajuste (overfitting).

# A arvore rasa pode ser lida como regras
fig, eixo = plt.subplots(figsize=(12, 5.5))
plot_tree(arvore_rasa, feature_names=list(X.columns), class_names=['benigno', 'maligno'],
          filled=False, impurity=False, proportion=True, rounded=True, fontsize=8, ax=eixo)
eixo.set_title('Árvore de profundidade 3: cada caixa é uma pergunta sobre uma medida')
plt.savefig(os.path.join(pasta, 'figuras', 'arvore_rasa.png'))
plt.show()

# Floresta aleatoria: muitas arvores em amostras diferentes, voto da maioria
floresta = RandomForestClassifier(n_estimators=200, random_state=0).fit(X_treino, y_treino)
print('Floresta      | treino:', round(accuracy_score(y_treino, floresta.predict(X_treino)), 3),
      '| teste:', round(accuracy_score(y_teste, floresta.predict(X_teste)), 3))

# Por que a floresta acerta mais? Cada arvore isolada erra de um jeito diferente (viu uma amostra diferente
# e, a cada no, so podia escolher entre algumas variaveis sorteadas). No voto, erros diferentes se cancelam.
acertos_individuais = [accuracy_score(y_teste, arv.predict(X_teste.values)) for arv in floresta.estimators_]
print(f'Arvores individuais da floresta: acerto no teste de {min(acertos_individuais):.3f} a {max(acertos_individuais):.3f} '
      f'(media {sum(acertos_individuais) / len(acertos_individuais):.3f})')
n_arvores = [1, 2, 5, 10, 25, 50, 100, 200]
acerto_por_tamanho = [accuracy_score(y_teste, RandomForestClassifier(n_estimators=n, random_state=0)
                                     .fit(X_treino, y_treino).predict(X_teste)) for n in n_arvores]
for n, a in zip(n_arvores, acerto_por_tamanho):
    print(f'  floresta com {n:3d} arvores: teste {a:.3f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
esq.hist(acertos_individuais, bins=15, color='#8794A3')
esq.axvline(accuracy_score(y_teste, floresta.predict(X_teste)), color='#2F648F', linewidth=2.5)
esq.text(accuracy_score(y_teste, floresta.predict(X_teste)) - 0.002, esq.get_ylim()[1] * 0.9, 'voto da floresta',
         color='#2F648F', ha='right')
esq.set_xlabel('Acerto no teste')
esq.set_ylabel('Árvores')
media_individual = sum(acertos_individuais) / len(acertos_individuais)
esq.set_title(f'Árvore sozinha: {media_individual:.1%} em média; voto: '
              f'{accuracy_score(y_teste, floresta.predict(X_teste)):.1%}', fontsize=11)
# Algumas arvores isoladas superam o voto neste teste, mas nao ha como saber de antemao quais:
# o voto e a escolha estavel, sem depender da sorte de pegar a arvore certa.
dir.plot(n_arvores, acerto_por_tamanho, marker='o', color='#168A8A')
dir.set_xscale('log')
dir.set_xlabel('Número de árvores (escala log)')
dir.set_ylabel('Acerto no teste')
dir.set_title('Ganho rápido nas primeiras árvores, depois estabiliza', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'floresta_voto.png'))
plt.show()

# Importancia das variaveis: quanto cada uma reduz a impureza, em media, nas arvores
importancia = pd.Series(floresta.feature_importances_, index=X.columns).sort_values()
print('\nDez medidas mais usadas pela floresta:')
print(importancia.tail(10).round(3))

fig, eixo = plt.subplots(figsize=(7, 4.5))
top = importancia.tail(10)
eixo.barh(top.index, top.values, color=['#8794A3'] * 7 + ['#2F648F'] * 3)
eixo.set_xlabel('Importância (redução média de impureza)')
eixo.set_title('Três medidas de "pontos côncavos" e tamanho concentram a decisão')
eixo.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'importancia_floresta.png'))
plt.show()

# Importancia nao e causa: diz o que o modelo usou, nao o que provoca o tumor.

# Experimente: varie max_depth de 1 a 10 e anote acuracia de treino e teste. Onde elas se separam?
