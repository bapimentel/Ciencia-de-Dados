# Aplicacao adicional - Educacao. Passo 3: um modelo de risco ANTES do fim do ano.
# Pergunta: com o que se sabe no inicio do ano (e, depois, com a nota do 1o periodo), da para apontar quem
# corre risco de reprovar? Alvo: G3 < 10. Validacao cruzada estratificada; nada de G2 (quase igual a G3).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import roc_auc_score, recall_score, precision_score, roc_curve

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
alunos = pd.read_csv(os.path.join(pasta, 'dados', 'student-por.csv'), sep=';')
alunos['risco'] = (alunos['G3'] < 10).astype(int)
print('Alunos:', len(alunos), '| reprovados:', alunos['risco'].sum(), f'({alunos["risco"].mean():.1%})')

# Variaveis disponiveis no inicio do ano (nada de notas)
inicio = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian',
          'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher',
          'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health']
# Apos o 1o periodo, acrescentam-se as faltas ate entao (aqui so temos o total do ano: aproximacao) e G1
primeiro_periodo = inicio + ['absences', 'G1']
# O que NAO entra: G2 (correlacao 0,92 com G3) e, claro, G3. Usar G2 seria prever a nota final com a nota final.

X_inicio = pd.get_dummies(alunos[inicio], dtype=int)
X_periodo = pd.get_dummies(alunos[primeiro_periodo], dtype=int)
y = alunos['risco']
dobras = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

def avaliar(nome, modelo, X):
    prob = cross_val_predict(modelo, X, y, cv=dobras, method='predict_proba')[:, 1]
    previsto = (prob >= 0.5).astype(int)
    print(f'{nome:48s} AUC={roc_auc_score(y, prob):.3f} | revocacao@0.5={recall_score(y, previsto, zero_division=0):.2f} '
          f'| precisao@0.5={precision_score(y, previsto, zero_division=0):.2f}')
    return prob

logistica = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight='balanced'))
floresta = RandomForestClassifier(n_estimators=400, min_samples_leaf=5, class_weight='balanced', random_state=0)

print('\nValidacao cruzada (5 dobras):')
avaliar('linha de base (sempre "sem risco")', DummyClassifier(strategy='most_frequent'), X_inicio)
prob_log_inicio = avaliar('logistica, inicio do ano', logistica, X_inicio)
prob_rf_inicio = avaliar('floresta, inicio do ano', floresta, X_inicio)
prob_log_periodo = avaliar('logistica, apos 1o periodo (+ faltas, G1)', logistica, X_periodo)
prob_rf_periodo = avaliar('floresta, apos 1o periodo (+ faltas, G1)', floresta, X_periodo)
# No inicio do ano o modelo separa razoavelmente (AUC ~0,7-0,8), sobretudo por "failures" e "higher".
# Com G1 a separacao melhora muito: a nota do primeiro periodo ja antecipa o fim do ano.

# O que pesa na logistica do inicio do ano
modelo = logistica.fit(X_inicio, y)
coeficientes = pd.Series(modelo[-1].coef_[0], index=X_inicio.columns).sort_values()
print('\nMaiores coeficientes (risco maior):')
print(coeficientes.tail(6).round(2).to_string())
print('Menores (risco menor):')
print(coeficientes.head(6).round(2).to_string())

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4.2))
for prob, nome, cor in [(prob_log_inicio, 'início do ano', '#2F648F'), (prob_log_periodo, 'após 1º período (com G1)', '#168A8A')]:
    tfp, tvp, _ = roc_curve(y, prob)
    esq.plot(tfp, tvp, color=cor, label=f'{nome} (AUC {roc_auc_score(y, prob):.2f})')
esq.plot([0, 1], [0, 1], linestyle='--', color='#8794A3')
esq.set_xlabel('Taxa de falsos positivos')
esq.set_ylabel('Revocação (reprovados encontrados)')
esq.set_title('Regressão logística: a nota do 1º período muda tudo')
esq.legend(loc='lower right')
top = pd.concat([coeficientes.head(5), coeficientes.tail(5)])
dir.barh(top.index, top.values, color=['#168A8A' if v < 0 else '#BD5B58' for v in top.values])
dir.axvline(0, color='#20324A', linewidth=0.8)
dir.set_xlabel('Coeficiente (variáveis padronizadas)')
dir.set_title('Início do ano: reprovações anteriores pesam mais')
dir.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_risco.png'))
plt.show()

pd.DataFrame({'prob_inicio': prob_log_inicio, 'prob_periodo': prob_log_periodo, 'risco': y}).to_csv(
    os.path.join(pasta, 'dados', 'probabilidades_validacao.csv'), index=False)
print('\nSalvo: dados/probabilidades_validacao.csv (probabilidades fora da amostra, para o script 04)')
