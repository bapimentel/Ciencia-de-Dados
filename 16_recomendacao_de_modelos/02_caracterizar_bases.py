# Caracterizar uma base de dados com meta-caracteristicas (meta-atributos), em duas familias:
#   diretas: medidas simples dos dados (tamanho, numero de atributos e classes, entropia das classes,
#            correlacao media entre atributos, assimetria e curtose medias, atributos por exemplo)
#   landmarking: acuracia de algoritmos rapidos e simples (1-NN, arvore de um no so, analise discriminante linear),
#            que "sondam" o tipo de fronteira da base
# Le dados/bases.npz (gerado pelo script 01) e salva dados/metacaracteristicas.csv.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
arquivo = np.load(os.path.join(pasta, 'dados', 'bases.npz'))
nomes = sorted({k.split('__')[0] for k in arquivo.files}, key=lambda n: (not n.startswith(('iris', 'vinhos', 'cancer', 'digitos')), n))
dobras = StratifiedKFold(5, shuffle=True, random_state=0)


def entropia_normalizada(y):
    p = np.bincount(y) / len(y)
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum() / np.log2(len(p))) if len(p) > 1 else 0.0


linhas = []
for nome in nomes:
    X, y = arquivo[f'{nome}__X'].astype(float), arquivo[f'{nome}__y']
    X = X[:, X.std(axis=0) > 0]                         # atributos constantes nao informam nada
    corr = np.corrcoef(X, rowvar=False) if X.shape[1] > 1 else np.array([[1.0]])
    fora_diagonal = np.abs(corr[~np.eye(len(corr), dtype=bool)]) if X.shape[1] > 1 else np.array([0.0])
    linhas.append({
        'base': nome,
        # diretas
        'log_exemplos': np.log10(len(X)),
        'log_atributos': np.log10(X.shape[1]),
        'classes': len(np.unique(y)),
        'atributos_por_exemplo': X.shape[1] / len(X),
        'entropia_classes': entropia_normalizada(y),
        'correlacao_media': float(np.nanmean(fora_diagonal)),
        'assimetria_media': float(np.mean(np.abs(skew(X, axis=0)))),
        'curtose_media': float(np.mean(kurtosis(X, axis=0))),
        # landmarking
        'lm_1nn': cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(1)), X, y, cv=dobras).mean(),
        'lm_toco': cross_val_score(DecisionTreeClassifier(max_depth=1), X, y, cv=dobras).mean(),
        'lm_lda': cross_val_score(LinearDiscriminantAnalysis(), X, y, cv=dobras).mean(),
    })
meta = pd.DataFrame(linhas).set_index('base')
meta.to_csv(os.path.join(pasta, 'dados', 'metacaracteristicas.csv'))
print(f'{len(meta)} bases x {meta.shape[1]} meta-caracteristicas')
print('\nAs quatro bases reais:')
print(meta.loc[['iris', 'vinhos', 'cancer_mama', 'digitos']].T.round(3))

# Uma leitura util dos landmarkers: quando o 1-NN vai muito melhor que o LDA (linear), a fronteira e curva.
meta['curvatura'] = meta['lm_1nn'] - meta['lm_lda']
desempenho = pd.read_csv(os.path.join(pasta, 'dados', 'desempenho.csv'), index_col=0).loc[meta.index]
ganho_svm = desempenho['SVM (RBF)'] - desempenho['Reg. logística']
print(f'\nCorrelacao entre (1-NN - LDA) e (SVM RBF - reg. logistica): {np.corrcoef(meta["curvatura"], ganho_svm)[0, 1]:.2f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.6))
reais = meta.index.isin(['iris', 'vinhos', 'cancer_mama', 'digitos'])
esq.scatter(meta['curvatura'][~reais], ganho_svm[~reais], color='#2F648F', s=30, label='bases simuladas')
esq.scatter(meta['curvatura'][reais], ganho_svm[reais], color='#D69A35', s=60, label='bases reais', zorder=3)
esq.axhline(0, color='#8794A3', linewidth=0.8)
esq.axvline(0, color='#8794A3', linewidth=0.8)
esq.set_xlabel('Landmarker: acurácia do 1-NN − acurácia do LDA')
esq.set_ylabel('Ganho do SVM (RBF) sobre a reg. logística')
esq.set_title('Uma sonda barata antecipa quando um modelo curvo compensa', fontsize=11)
esq.legend()
padronizado = (meta.drop(columns='curvatura') - meta.drop(columns='curvatura').mean()) / meta.drop(columns='curvatura').std()
imagem = dir.imshow(padronizado.iloc[:16].T, cmap='RdBu_r', vmin=-2.5, vmax=2.5, aspect='auto')
dir.set_yticks(range(padronizado.shape[1]), padronizado.columns, fontsize=8)
dir.set_xticks(range(16), [n.replace('sim_', 's') for n in padronizado.index[:16]], rotation=70, fontsize=8)
dir.set_title('Meta-características (padronizadas) das 16 primeiras bases', fontsize=11)
dir.grid(False)
plt.colorbar(imagem, ax=dir, shrink=0.8)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'metacaracteristicas.png'))
plt.show()
