# Complemento avancado (opcional): explicacoes SHAP para a floresta do script 03.
# Requer: pip install shap   (nao faz parte do requirements-basico.txt).
# O material original gerava graficos SHAP para os tres classificadores; aqui so para a floresta.

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

try:
    import shap
except ImportError:
    print('shap nao esta instalado. Instale com: pip install shap')
    raise SystemExit

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'))

variaveis = ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)', 'Dias ate registrar', 'Mes']
X = pd.get_dummies(dados[variaveis], dtype=int)
y = dados['Negada']
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
floresta = RandomForestClassifier(n_estimators=200, min_samples_leaf=3, random_state=0).fit(X_tr, y_tr)

# TreeExplainer e rapido para florestas; usamos uma amostra do teste
amostra = X_te.sample(400, random_state=0)
explicador = shap.TreeExplainer(floresta)
valores = explicador(amostra)
valores_negada = valores[:, :, 1]          # contribuicoes para a classe "negada"

shap.plots.beeswarm(valores_negada, max_display=12, show=False)
plt.title('Contribuição de cada variável para a previsão "negada" (amostra de 400 casos do teste)')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '06_shap_beeswarm.png'))
plt.close()
print('Salvo em figuras/06_shap_beeswarm.png')
