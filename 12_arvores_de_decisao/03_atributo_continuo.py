# Atributos continuos: a arvore transforma "temperatura" em perguntas do tipo "temperatura < c?".
# Os cortes candidatos ficam no meio entre valores vizinhos em que a classe muda.
# Parte 1: 6 dias (exemplo pequeno). Parte 2: o melhor corte de 'mean radius' na base de cancer de mama.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))


def entropia(classes):
    p = pd.Series(classes).value_counts(normalize=True)
    return float(-(p * np.log2(p)).sum())


def ganho_do_corte(valores, classes, corte):
    esquerda = classes[valores < corte]
    direita = classes[valores >= corte]
    restante = len(esquerda) / len(classes) * entropia(esquerda) + len(direita) / len(classes) * entropia(direita)
    return entropia(classes) - restante


# --- Parte 1
temperaturas = np.array([20, 24, 30, 32, 35, 37])
praia = np.array(['nao', 'nao', 'sim', 'sim', 'sim', 'nao'])
candidatos = [(temperaturas[i] + temperaturas[i + 1]) / 2 for i in range(len(temperaturas) - 1) if praia[i] != praia[i + 1]]
print('Cortes candidatos (onde a classe muda):', candidatos)
for c in candidatos:
    print(f'  temperatura < {c}: ganho {ganho_do_corte(temperaturas, praia, c):.3f}')

# --- Parte 2: base real
base = load_breast_cancer()
raio = base.data[:, list(base.feature_names).index('mean radius')]
classe = np.where(base.target == 0, 'maligno', 'benigno')
ordem = np.argsort(raio)
raio_ord, classe_ord = raio[ordem], classe[ordem]
cortes = np.unique([(raio_ord[i] + raio_ord[i + 1]) / 2 for i in range(len(raio_ord) - 1) if classe_ord[i] != classe_ord[i + 1]])
ganhos = np.array([ganho_do_corte(raio, classe, c) for c in cortes])
melhor = cortes[int(np.argmax(ganhos))]
print(f'\nmean radius: {len(cortes)} cortes candidatos; melhor corte = {melhor:.2f} (ganho {ganhos.max():.3f})')
print(pd.crosstab(np.where(raio < melhor, f'raio < {melhor:.2f}', f'raio >= {melhor:.2f}'), classe))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
esq.hist([raio[classe == 'benigno'], raio[classe == 'maligno']], bins=40, stacked=True, color=['#2F648F', '#BD5B58'], label=['benigno', 'maligno'])
esq.axvline(melhor, color='#D69A35', linewidth=2)
esq.text(melhor + 0.3, esq.get_ylim()[1] * 0.85, f'corte {melhor:.2f}', color='#D69A35')
esq.set_xlabel('Raio médio do núcleo')
esq.set_ylabel('Exames')
esq.set_title('O melhor corte separa a maior parte das classes', fontsize=11)
esq.legend()
dir.plot(cortes, ganhos, color='#2F648F')
dir.axvline(melhor, color='#D69A35', linestyle='--')
dir.set_xlabel('Corte candidato')
dir.set_ylabel('Ganho de informação')
dir.set_title(f'{len(cortes)} candidatos; o ganho é máximo em {melhor:.2f}', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'atributo_continuo.png'))
plt.show()
