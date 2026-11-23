# Aplicacao adicional - Educacao. Passo 5: a regra funciona em alunos que nao foram usados para cria-la?
# A regra "reprovou antes OU G1 < 10" e o modelo logistico foram construidos com a turma de PORTUGUES.
# Validacao externa: aplicamos os dois, sem nenhum ajuste, a turma de MATEMATICA (outros alunos, outra disciplina)
# e, separadamente, a cada uma das duas escolas.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
portugues = pd.read_csv(os.path.join(pasta, 'dados', 'student-por.csv'), sep=';')
matematica = pd.read_csv(os.path.join(pasta, 'dados', 'student-mat.csv'), sep=';')


def avaliar_regra(tabela, nome):
    reprovado = tabela['G3'] < 10
    regra = (tabela['failures'] > 0) | (tabela['G1'] < 10)
    alcancados = (reprovado & regra).sum()
    resultado = {'grupo': nome, 'alunos': len(tabela), 'reprovados': int(reprovado.sum()),
                 'taxa de reprovação': reprovado.mean(), 'alunos na lista': int(regra.sum()),
                 '% na lista': regra.mean(), 'reprovados alcançados': int(alcancados),
                 'cobertura': alcancados / reprovado.sum(), 'precisão da lista': alcancados / regra.sum()}
    return resultado


linhas = [avaliar_regra(portugues, 'português (onde a regra foi criada)'),
          avaliar_regra(matematica, 'matemática (validação externa)')]
for escola in ['GP', 'MS']:
    linhas.append(avaliar_regra(portugues[portugues['school'] == escola], f'português, escola {escola}'))
    linhas.append(avaliar_regra(matematica[matematica['school'] == escola], f'matemática, escola {escola}'))
tabela = pd.DataFrame(linhas).set_index('grupo')
print(tabela.to_string(float_format=lambda v: f'{v:.2f}'))

# O modelo logistico (inicio do ano + faltas + G1), treinado em portugues e aplicado a matematica
variaveis = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian',
             'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher',
             'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1']
X_por = pd.get_dummies(portugues[variaveis], dtype=int)
X_mat = pd.get_dummies(matematica[variaveis], dtype=int).reindex(columns=X_por.columns, fill_value=0)
modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, class_weight='balanced')).fit(X_por, portugues['G3'] < 10)
prob_mat = modelo.predict_proba(X_mat)[:, 1]
y_mat = (matematica['G3'] < 10).values
print(f'\nModelo treinado em portugues, aplicado a matematica: AUC = {roc_auc_score(y_mat, prob_mat):.3f}')
k = int(tabela.loc['matemática (validação externa)', 'alunos na lista'])
topo = np.argsort(-prob_mat)[:k]
print(f'Com a mesma quantidade de alunos da regra ({k}), o modelo alcanca {y_mat[topo].sum()} de {y_mat.sum()} reprovados '
      f'({y_mat[topo].sum() / y_mat.sum():.0%}); a regra alcanca {int(tabela.loc["matemática (validação externa)", "reprovados alcançados"])}')

# Quem a regra deixa de fora em matematica?
fora = matematica[(matematica['G3'] < 10) & ~((matematica['failures'] > 0) | (matematica['G1'] < 10))]
print(f'\nReprovados de matematica fora da lista: {len(fora)}; G1 deles: {sorted(fora["G1"].tolist())}; '
      f'com G3 = 0: {(fora["G3"] == 0).sum()}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.4))
grupos = ['português (onde a regra foi criada)', 'matemática (validação externa)', 'português, escola GP',
          'português, escola MS', 'matemática, escola GP', 'matemática, escola MS']
rotulos = ['Português\n(criação)', 'Matemática\n(externa)', 'Port. GP', 'Port. MS', 'Mat. GP', 'Mat. MS']
x = np.arange(len(grupos))
esq.bar(x - 0.2, 100 * tabela.loc[grupos, 'cobertura'], width=0.4, color='#2F648F', label='% dos reprovados alcançados')
esq.bar(x + 0.2, 100 * tabela.loc[grupos, '% na lista'], width=0.4, color='#8794A3', label='% dos alunos na lista')
esq.set_xticks(x, rotulos, fontsize=9)
esq.set_ylim(0, 110)
esq.set_ylabel('%')
esq.set_title('Regra "reprovou antes ou G1 < 10" em turmas e escolas diferentes', fontsize=11)
esq.legend(loc='upper right', fontsize=9)
dir.scatter(matematica['G1'], matematica['G3'], c=np.where(y_mat, '#BD5B58', '#2F648F'), s=16, alpha=0.6)
dir.axvline(9.5, color='#D69A35', linestyle='--')
dir.axhline(9.5, color='#8794A3', linestyle=':')
dir.set_xlabel('Nota do 1º período (G1), matemática')
dir.set_ylabel('Nota final (G3)')
dir.set_title('Matemática: G1 abaixo de 10 antecipa a maioria das reprovações', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '05_validacao_externa.png'))
plt.show()
