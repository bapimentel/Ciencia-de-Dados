# Animacao: o limiar desliza sobre as probabilidades previstas e a matriz de confusao muda.
# Saidas: animacoes/geradas/limiar_matriz_confusao.gif e .png.
# Dados reais: base de cancer de mama do scikit-learn (classe positiva = maligno).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = (base.target == 0).astype(int)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
escala = StandardScaler().fit(X_tr)
modelo = LogisticRegression(max_iter=1000).fit(escala.transform(X_tr), y_tr)
prob = modelo.predict_proba(escala.transform(X_te))[:, 1]
y_te = np.asarray(y_te)

gerador = np.random.default_rng(0)
alturas = gerador.uniform(0.1, 0.9, size=len(prob))     # so para espalhar os pontos na vertical
limiares = np.round(np.arange(0.02, 0.99, 0.03), 2)

fig, (esq, dir) = plt.subplots(1, 2, figsize=(9, 4.5), gridspec_kw={'width_ratios': [1.7, 1]})
esq.set_xlim(0, 1)
esq.set_ylim(0, 1)
esq.set_yticks([])
esq.grid(False)
esq.set_xlabel('Probabilidade prevista de "maligno"')
pontos = esq.scatter(prob, alturas, s=22, alpha=0.85)
linha = esq.axvline(0.5, color='#D69A35', linewidth=3)
esq.text(0.02, 0.95, '● benigno real', color='#2F648F', transform=esq.transAxes, fontsize=10)
esq.text(0.02, 0.89, '● maligno real', color='#BD5B58', transform=esq.transAxes, fontsize=10)
esq.text(0.98, 0.95, 'à direita do limiar: previsto "maligno"', ha='right', transform=esq.transAxes, fontsize=9, color='#8794A3')

dir.set_xlim(0, 2)
dir.set_ylim(0, 2)
dir.set_xticks([0.5, 1.5])
dir.set_xticklabels(['prev. benigno', 'prev. maligno'])
dir.set_yticks([0.5, 1.5])
dir.set_yticklabels(['real\nmaligno', 'real\nbenigno'])
dir.yaxis.tick_right()
dir.grid(False)
celulas = {}
for (cx, cy, nome) in [(0.5, 1.5, 'VN'), (1.5, 1.5, 'FP'), (0.5, 0.5, 'FN'), (1.5, 0.5, 'VP')]:
    dir.add_patch(plt.Rectangle((cx - 0.5, cy - 0.5), 1, 1, facecolor='white', edgecolor='#8794A3'))
    celulas[nome] = dir.text(cx, cy, '', ha='center', va='center', fontsize=15, fontweight='bold')
titulo = fig.suptitle('', x=0.01, ha='left')

def quadro(i):
    limiar = limiares[i]
    previsto = prob >= limiar
    cores = np.where(y_te == 1, '#BD5B58', '#2F648F')
    pontos.set_color(cores)
    # pontos classificados errado ficam com borda escura
    errado = previsto != (y_te == 1)
    pontos.set_edgecolor(np.where(errado, '#20324A', 'none'))
    pontos.set_linewidths(np.where(errado, 1.2, 0))
    linha.set_xdata([limiar, limiar])
    vp = int((previsto & (y_te == 1)).sum())
    fp = int((previsto & (y_te == 0)).sum())
    fn = int((~previsto & (y_te == 1)).sum())
    vn = int((~previsto & (y_te == 0)).sum())
    celulas['VP'].set_text(f'VP\n{vp}')
    celulas['FP'].set_text(f'FP\n{fp}')
    celulas['FN'].set_text(f'FN\n{fn}')
    celulas['VN'].set_text(f'VN\n{vn}')
    celulas['FN'].set_color('#BD5B58' if fn else '#20324A')
    celulas['FP'].set_color('#D69A35' if fp else '#20324A')
    revocacao = vp / (vp + fn)
    precisao = vp / (vp + fp) if vp + fp else float('nan')
    titulo.set_text(f'Limiar = {limiar:.2f}   revocação = {revocacao:.2f}   precisão = {precisao:.2f}   '
                    f'(pontos com borda escura = erros)')
    return [pontos, linha, titulo]

quadros = list(range(len(limiares))) + [len(limiares) - 1] * 4
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=350, blit=False)
animacao.save(os.path.join(saida, 'limiar_matriz_confusao.gif'), writer=PillowWriter(fps=3), dpi=80)
quadro(int(np.where(limiares == 0.5)[0][0]) if 0.5 in limiares else len(limiares) // 2)
plt.savefig(os.path.join(saida, 'limiar_matriz_confusao.png'))
print('Salvo: animacoes/geradas/limiar_matriz_confusao.gif e .png')
