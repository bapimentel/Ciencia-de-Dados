# Rede de multiplas camadas (MLP) na pratica, com scikit-learn, em dados reais:
# 1797 imagens de digitos manuscritos, 8x8 pixels (64 entradas), 10 classes.
# Pontos de atencao: padronizar as entradas, separar validacao, acompanhar o sobreajuste ao longo das epocas.

import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.exceptions import ConvergenceWarning

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
warnings.filterwarnings('ignore', category=ConvergenceWarning)

digitos = load_digits()
X, y = digitos.data, digitos.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
X_tr, X_va, y_tr, y_va = train_test_split(X_tr, y_tr, test_size=0.25, random_state=0, stratify=y_tr)
escala = StandardScaler().fit(X_tr)               # media e desvio aprendidos so no treino
X_tr_p, X_va_p, X_te_p = escala.transform(X_tr), escala.transform(X_va), escala.transform(X_te)
print(f'Treino {len(X_tr)}, validacao {len(X_va)}, teste {len(X_te)} imagens')

# 1) Acompanhando treino e validacao epoca a epoca (partial_fit = uma passada nos dados)
rede = MLPClassifier(hidden_layer_sizes=(64,), learning_rate_init=0.001, random_state=0)
acc_tr, acc_va = [], []
for epoca in range(150):
    rede.partial_fit(X_tr_p, y_tr, classes=np.arange(10))
    acc_tr.append(rede.score(X_tr_p, y_tr))
    acc_va.append(rede.score(X_va_p, y_va))
melhor_epoca = int(np.argmax(acc_va)) + 1
print(f'Epoca de maior acerto na validacao: {melhor_epoca} ({max(acc_va):.3f}); '
      f'na epoca 150: treino {acc_tr[-1]:.3f}, validacao {acc_va[-1]:.3f}')

# 2) Quantos neuronios ocultos? Escolha pela validacao
print('\nNeuronios ocultos  treino  validacao')
for n in [2, 5, 10, 32, 64, 128]:
    m = MLPClassifier(hidden_layer_sizes=(n,), max_iter=300, random_state=0).fit(X_tr_p, y_tr)
    print(f'{n:17d}  {m.score(X_tr_p, y_tr):.3f}   {m.score(X_va_p, y_va):.3f}')

# 3) Comparacao com um modelo linear, e o efeito de NAO padronizar
final = MLPClassifier(hidden_layer_sizes=(64,), max_iter=300, random_state=0).fit(X_tr_p, y_tr)
linear = LogisticRegression(max_iter=2000).fit(X_tr_p, y_tr)
sem_escala = MLPClassifier(hidden_layer_sizes=(64,), max_iter=300, random_state=0).fit(X_tr, y_tr)
print(f'\nTeste | MLP 64 ocultos: {final.score(X_te_p, y_te):.3f} | regressao logistica: {linear.score(X_te_p, y_te):.3f}'
      f' | MLP sem padronizar: {sem_escala.score(X_te, y_te):.3f}')
# Aqui padronizar quase nao muda o resultado porque todos os pixels ja estao na mesma escala (0 a 16).
# Com variaveis em escalas muito diferentes (renda em reais e idade em anos), a diferenca costuma ser grande.
previsto = final.predict(X_te_p)
erros = np.flatnonzero(previsto != y_te)
print(f'Erros no teste: {len(erros)} de {len(y_te)}')
matriz = confusion_matrix(y_te, previsto)
np.fill_diagonal(matriz, 0)
i, j = np.unravel_index(matriz.argmax(), matriz.shape)
print(f'Confusao mais frequente: digito {i} lido como {j} ({matriz[i, j]} vezes)')

fig = plt.figure(figsize=(13, 4.3))
eixo = fig.add_subplot(1, 2, 1)
eixo.plot(range(1, 151), acc_tr, color='#2F648F', label='treino')
eixo.plot(range(1, 151), acc_va, color='#168A8A', label='validação')
eixo.set_xlabel('Época')
eixo.set_ylabel('Acurácia')
eixo.set_ylim(0.5, 1.01)
eixo.set_title(f'Treino chega a 100%; validação para em ~{max(acc_va):.0%}', fontsize=11)
eixo.legend()
for k, idx in enumerate(erros[:8]):
    ax = fig.add_subplot(2, 8, 5 + (k // 4) * 8 + (k % 4))
    ax.imshow(X_te[idx].reshape(8, 8), cmap='Greys')
    ax.set_title(f'{y_te[idx]} → {previsto[idx]}', fontsize=9, color='#BD5B58')
    ax.axis('off')
fig.text(0.73, 0.96, 'Erros no teste (verdadeiro → previsto)', ha='center', fontsize=11, weight='bold', color='#20324A')
plt.tight_layout(rect=(0, 0, 1, 0.93))
plt.savefig(os.path.join(pasta, 'figuras', 'mlp_digitos.png'))
plt.show()
