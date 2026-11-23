# O limiar de decisao e o custo dos erros: a mesma probabilidade, decisoes diferentes.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

base = load_breast_cancer()
X = pd.DataFrame(base.data, columns=base.feature_names)
y = pd.Series((base.target == 0).astype(int), name='maligno')
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

escala = StandardScaler().fit(X_treino)
modelo = LogisticRegression(max_iter=1000).fit(escala.transform(X_treino), y_treino)
probabilidade = modelo.predict_proba(escala.transform(X_teste))[:, 1]

# Para cada limiar, contamos os quatro tipos de resultado
limiares = np.arange(0.05, 0.96, 0.05)
linhas = []
for limiar in limiares:
    previsao = (probabilidade >= limiar).astype(int)
    vn, fp, fn, vp = confusion_matrix(y_teste, previsao).ravel()
    linhas.append({'limiar': round(limiar, 2), 'FN': fn, 'FP': fp, 'VP': vp, 'VN': vn})
tabela = pd.DataFrame(linhas)

# Suponha custos (hipoteticos, para o exercicio): deixar passar um maligno custa 10; um alarme falso custa 1
CUSTO_FN = 10
CUSTO_FP = 1
tabela['custo'] = CUSTO_FN * tabela['FN'] + CUSTO_FP * tabela['FP']
print(tabela.to_string(index=False))

melhor = tabela.loc[tabela['custo'].idxmin()]
print(f'\nLimiar de menor custo: {melhor["limiar"]} (FN={int(melhor["FN"])}, FP={int(melhor["FP"])}, custo={int(melhor["custo"])})')
padrao = tabela[tabela['limiar'] == 0.5].iloc[0]
print(f'Limiar padrao 0.5:     FN={int(padrao["FN"])}, FP={int(padrao["FP"])}, custo={int(padrao["custo"])}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(10, 3.8))
esq.plot(tabela['limiar'], tabela['FN'], color='#BD5B58', marker='o', label='Falsos negativos (maligno dito benigno)')
esq.plot(tabela['limiar'], tabela['FP'], color='#D69A35', marker='o', label='Falsos positivos (benigno dito maligno)')
esq.set_xlabel('Limiar de probabilidade para dizer "maligno"')
esq.set_ylabel('Erros no teste (171 exames)')
esq.set_title('Baixar o limiar troca falsos negativos por falsos positivos')
esq.legend(fontsize=9)
dir.plot(tabela['limiar'], tabela['custo'], color='#2F648F', marker='o')
dir.axvline(melhor['limiar'], color='#D69A35', linestyle='--')
dir.axvline(0.5, color='#8794A3', linestyle=':')
dir.set_xlabel('Limiar')
dir.set_ylabel(f'Custo total (FN×{CUSTO_FN} + FP×{CUSTO_FP})')
dir.set_title(f'Com esses custos, o melhor limiar é {melhor["limiar"]}, não 0,5')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'limiar_e_custo.png'))
plt.show()

# A acuracia sozinha nao escolheria esse limiar. A decisao depende de quanto cada erro custa,
# e isso nao esta nos dados: vem do problema.

# Experimente: inverta os custos (FN=1, FP=10). Para onde vai o melhor limiar?
