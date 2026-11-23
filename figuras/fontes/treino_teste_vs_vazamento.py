# Figura didatica: separacao correta treino/teste x vazamento de dados, com um experimento pequeno.
# Saida: figuras/geradas/treino_teste_vs_vazamento.png. Dados simulados com semente fixa.

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'estilo.mplstyle'))

# Dados: 400 casos, 2 variaveis uteis e um alvo binario
gerador = np.random.default_rng(0)
n = 400
X = gerador.normal(size=(n, 2))
y = (X[:, 0] + 0.8 * X[:, 1] + gerador.normal(0, 0.9, size=n) > 0).astype(int)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

# Cenario A: correto
modelo = KNeighborsClassifier(n_neighbors=7).fit(X_tr, y_tr)
acuracia_correta = accuracy_score(y_te, modelo.predict(X_te))

# Cenario B: vazamento do alvo. Uma coluna "derivada" que so existe depois de conhecer y
# (ex.: "valor pago pelo seguro" para prever "houve sinistro"). Acuracia explode, mas e inutil.
vazada = y + gerador.normal(0, 0.3, size=n)
X_vaz = np.column_stack([X, vazada])
Xv_tr, Xv_te, _, _ = train_test_split(X_vaz, y, test_size=0.3, random_state=0, stratify=y)
acuracia_vazada = accuracy_score(y_te, KNeighborsClassifier(n_neighbors=7).fit(Xv_tr, y_tr).predict(Xv_te))

# Cenario C: avaliar no proprio treino (outro vazamento comum)
acuracia_treino = accuracy_score(y_tr, modelo.predict(X_tr))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={'width_ratios': [1.4, 1]})

# Esquerda: esquema
esq.axis('off')
esq.set_xlim(0, 10)
esq.set_ylim(0, 6)
def caixa(x, y, w, h, texto, cor, cor_texto='white'):
    esq.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.08', facecolor=cor, edgecolor='none'))
    esq.text(x + w / 2, y + h / 2, texto, ha='center', va='center', color=cor_texto, fontsize=10, fontweight='bold')
esq.text(0.2, 5.6, 'Correto', fontsize=12, fontweight='bold', color='#20324A')
caixa(0.2, 4.2, 3.3, 1.0, 'dados', '#8794A3')
caixa(4.2, 4.6, 3.0, 0.8, 'treino: aprende', '#2F648F')
caixa(4.2, 3.7, 3.0, 0.8, 'teste: só mede', '#168A8A')
esq.annotate('', xy=(4.15, 5.0), xytext=(3.55, 4.8), arrowprops=dict(arrowstyle='->', color='#20324A'))
esq.annotate('', xy=(4.15, 4.1), xytext=(3.55, 4.6), arrowprops=dict(arrowstyle='->', color='#20324A'))
esq.text(7.4, 4.95, 'média, escala, modelo\nvêm só daqui', fontsize=9, color='#2F648F', va='center')
esq.text(0.2, 2.9, 'Vazamento', fontsize=12, fontweight='bold', color='#BD5B58')
caixa(0.2, 1.5, 3.3, 1.0, 'dados', '#8794A3')
caixa(4.2, 1.9, 3.0, 0.8, 'treino', '#2F648F')
caixa(4.2, 1.0, 3.0, 0.8, 'teste', '#168A8A')
esq.annotate('', xy=(4.15, 2.3), xytext=(3.55, 2.1), arrowprops=dict(arrowstyle='->', color='#20324A'))
esq.annotate('', xy=(4.15, 1.4), xytext=(3.55, 1.9), arrowprops=dict(arrowstyle='->', color='#20324A'))
esq.annotate('', xy=(5.7, 1.85), xytext=(5.7, 0.4), arrowprops=dict(arrowstyle='->', color='#BD5B58', linewidth=2))
esq.text(6.0, 0.45, 'informação do teste (ou do futuro,\nou do próprio alvo) entra no treino', fontsize=9, color='#BD5B58', va='bottom')

# Direita: acuracias
nomes = ['correto', 'medido no\npróprio treino', 'coluna derivada\ndo alvo']
valores = [acuracia_correta, acuracia_treino, acuracia_vazada]
cores = ['#2F648F', '#BD5B58', '#BD5B58']
barras = dir.bar(nomes, valores, color=cores)
for barra, v in zip(barras, valores):
    dir.text(barra.get_x() + barra.get_width() / 2, v + 0.01, f'{v:.2f}', ha='center', color='#20324A')
dir.set_ylim(0, 1.05)
dir.set_ylabel('Acurácia aparente')
dir.set_title('O mesmo problema, três números diferentes')
plt.tight_layout()
plt.savefig(os.path.join(pasta, '..', 'geradas', 'treino_teste_vs_vazamento.png'))
print(f'correto={acuracia_correta:.3f} treino={acuracia_treino:.3f} vazado={acuracia_vazada:.3f}')
print('Figura salva em figuras/geradas/treino_teste_vs_vazamento.png')
