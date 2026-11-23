# k-NN ponderado pela distancia: vizinhos mais proximos votam com mais forca, peso w = 1 / d^2.
# Parte 1: um exemplo pequeno em que o voto simples e o ponderado discordam.
# Parte 2: comparacao em dados reais (vinhos, padronizados).

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Parte 1. 5 vizinhos: 2 azuis bem perto, 3 verdes mais longe
novo = np.array([0.0, 0.0])
vizinhos = np.array([[0.3, 0.2], [-0.2, 0.3], [1.5, 1.1], [-1.4, 1.2], [1.2, -1.5]])
classes = np.array(['azul', 'azul', 'verde', 'verde', 'verde'])
d = np.sqrt(((vizinhos - novo) ** 2).sum(axis=1))
pesos = 1 / d ** 2
print('distancias:', d.round(2), '| pesos 1/d^2:', pesos.round(2))
print('Voto simples:', {c: int((classes == c).sum()) for c in ['azul', 'verde']}, '-> verde')
soma = {c: round(float(pesos[classes == c].sum()), 2) for c in ['azul', 'verde']}
print('Voto ponderado:', soma, '->', max(soma, key=soma.get))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4.4))
for ponto, classe, peso in zip(vizinhos, classes, pesos):
    cor = '#2F648F' if classe == 'azul' else '#168A8A'
    esq.scatter(*ponto, s=60 + 40 * peso, color=cor, zorder=3)
    esq.plot([0, ponto[0]], [0, ponto[1]], color='#E6EBF0')
    esq.text(ponto[0] + 0.08, ponto[1] + 0.08, f'w={peso:.1f}', fontsize=9, color=cor)
esq.scatter(0, 0, marker='*', s=300, color='#D69A35', edgecolor='#20324A', zorder=4)
esq.set_aspect('equal')
esq.set_title('Simples: 3 verdes × 2 azuis → verde\nPonderado: azuis pesam mais → azul', fontsize=11)

# --- Parte 2. Dados reais
vinhos = load_wine()
dobras = StratifiedKFold(10, shuffle=True, random_state=0)
ks = list(range(1, 40, 2))
simples, ponderado = [], []
for k in ks:
    simples.append(cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k)), vinhos.data, vinhos.target, cv=dobras).mean())
    ponderado.append(cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k, weights='distance')),
                                     vinhos.data, vinhos.target, cv=dobras).mean())
print(f'\nVinhos: melhor simples {max(simples):.3f} | melhor ponderado {max(ponderado):.3f}')
print(f'Com k=39: simples {simples[-1]:.3f} | ponderado {ponderado[-1]:.3f}')
dir.plot(ks, simples, marker='o', markersize=4, color='#8794A3', label='voto simples')
dir.plot(ks, ponderado, marker='o', markersize=4, color='#2F648F', label='voto ponderado (1/d)')
dir.set_xlabel('k')
dir.set_ylabel('Acurácia (validação cruzada)')
dir.set_title('Vinhos: aqui o peso quase não muda nada', fontsize=11)
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'knn_ponderado.png'))
plt.show()
# Leitura honesta: nos vinhos as classes ja se separam bem depois da padronizacao, e o voto ponderado
# empata com o simples. A ponderacao ajuda quando ha vizinhos de classes diferentes a distancias muito
# diferentes, como no exemplo da Parte 1. Nem toda variante "melhorada" melhora em todo problema.
# Observacao: o scikit-learn usa peso 1/d (nao 1/d^2) quando weights='distance'. A ideia e a mesma.
# Com ponderacao, ate e possivel usar TODOS os exemplos como vizinhos: os distantes quase nao pesam.
