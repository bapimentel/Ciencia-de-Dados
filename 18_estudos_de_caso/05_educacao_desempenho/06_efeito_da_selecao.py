# Aplicacao adicional - Educacao. Passo 6: qual o efeito medido de escolher os alunos pela regra?
# A decisao da escola e A QUEM oferecer o acompanhamento, com vagas limitadas. Comparamos, na turma de matematica
# (que nao foi usada para criar a regra), o que cada criterio de selecao teria produzido:
#   - regra "reprovou antes OU G1 < 10" (criada com a turma de portugues);
#   - criterios usados com frequencia na pratica: muitas faltas (> 10), so reprovacao anterior, so G1 < 10;
#   - modelo logistico (treinado em portugues) e uma lista sorteada, ambos com o mesmo numero de alunos da regra.
# Medidas: reprovados alcancados, alunos acompanhados por reprovado alcancado (esforco), reprovados deixados de fora.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
portugues = pd.read_csv(os.path.join(pasta, 'dados', 'student-por.csv'), sep=';')
matematica = pd.read_csv(os.path.join(pasta, 'dados', 'student-mat.csv'), sep=';')
reprovou = (matematica['G3'] < 10).values
n_reprovados = int(reprovou.sum())

variaveis = ['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian',
             'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher',
             'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1']
X_por = pd.get_dummies(portugues[variaveis], dtype=int)
X_mat = pd.get_dummies(matematica[variaveis], dtype=int).reindex(columns=X_por.columns, fill_value=0)
modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000, class_weight='balanced')).fit(X_por, portugues['G3'] < 10)
prob = modelo.predict_proba(X_mat)[:, 1]

regra = ((matematica['failures'] > 0) | (matematica['G1'] < 10)).values
k = int(regra.sum())
criterios = {
    'regra: reprovou antes ou G1 < 10': regra,
    'só G1 < 10': (matematica['G1'] < 10).values,
    'só reprovou antes': (matematica['failures'] > 0).values,
    'mais de 10 faltas': (matematica['absences'] > 10).values,
    f'modelo logístico ({k} alunos)': np.isin(np.arange(len(matematica)), np.argsort(-prob)[:k]),
}
linhas = []
for nome, lista in criterios.items():
    alcancados = int((lista & reprovou).sum())
    linhas.append({'critério': nome, 'alunos na lista': int(lista.sum()), 'reprovados alcançados': alcancados,
                   'cobertura': alcancados / n_reprovados, 'reprovados fora da lista': n_reprovados - alcancados,
                   'alunos por reprovado alcançado': lista.sum() / max(alcancados, 1)})
# Lista sorteada com o mesmo tamanho da regra: media de 2000 sorteios
gerador = np.random.default_rng(0)
sorteios = [reprovou[gerador.choice(len(matematica), k, replace=False)].sum() for _ in range(2000)]
linhas.append({'critério': f'lista sorteada ({k} alunos)', 'alunos na lista': k, 'reprovados alcançados': float(np.mean(sorteios)),
               'cobertura': np.mean(sorteios) / n_reprovados, 'reprovados fora da lista': n_reprovados - np.mean(sorteios),
               'alunos por reprovado alcançado': k / np.mean(sorteios)})
tabela = pd.DataFrame(linhas).set_index('critério')
print(f'Turma de matematica: {len(matematica)} alunos, {n_reprovados} reprovados')
pd.set_option('display.width', 200)
print(tabela.round(2).to_string())

r = tabela.loc['regra: reprovou antes ou G1 < 10']
f = tabela.loc['mais de 10 faltas']
s = tabela.loc[f'lista sorteada ({k} alunos)']
print(f'\nRegra x lista sorteada do mesmo tamanho: {r["reprovados alcançados"]:.0f} x {s["reprovados alcançados"]:.0f} reprovados alcancados '
      f'(+{r["reprovados alcançados"] - s["reprovados alcançados"]:.0f})')
print(f'Regra x "mais de 10 faltas": cobertura {r["cobertura"]:.0%} x {f["cobertura"]:.0%}')

fig, eixo = plt.subplots(figsize=(10, 4.6))
ordem = tabela.sort_values('cobertura')
cores = ['#2F648F' if n.startswith('regra') else '#168A8A' if n.startswith('modelo') else '#8794A3' for n in ordem.index]
eixo.barh(ordem.index, 100 * ordem['cobertura'], color=cores)
for i, (nome, linha) in enumerate(ordem.iterrows()):
    eixo.text(100 * linha['cobertura'] + 1, i, f'{linha["cobertura"]:.0%}  ({linha["alunos na lista"]:.0f} alunos na lista)', va='center', fontsize=9)
eixo.set_xlim(0, 115)
eixo.set_xlabel(f'% dos {n_reprovados} reprovados da turma de matemática que estariam na lista')
eixo.set_title('Turma de matemática (não usada para criar a regra): quem cada critério alcança', fontsize=11)
eixo.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '06_efeito_da_selecao.png'))
plt.show()
