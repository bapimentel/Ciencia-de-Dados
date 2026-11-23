# Aplicacao adicional - Educacao: frequencia, desempenho e acompanhamento. Etapa 1: conhecer os dados.
# Base: Student Performance (UCI, id 320), alunos do ensino secundario de duas escolas de Portugal,
# ano letivo 2005-2006 (Cortez e Silva, 2008). https://archive.ics.uci.edu/dataset/320/student-performance
# (licenca CC BY 4.0; acesso em 2026-11-23). Dois arquivos: student-por.csv (portugues, 649 alunos)
# e student-mat.csv (matematica, 395 alunos). Variaveis descritas em dados/student.txt.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)

portugues = pd.read_csv(os.path.join(pasta, 'dados', 'student-por.csv'), sep=';')
matematica = pd.read_csv(os.path.join(pasta, 'dados', 'student-mat.csv'), sep=';')
print('Portugues:', portugues.shape, '| Matematica:', matematica.shape)
print(portugues.dtypes.value_counts())
print(portugues.head(3).to_string())

# As colunas que esta analise usa (definicoes em dados/student.txt):
# school (GP ou MS), sex, age, address (U urbano / R rural), Medu/Fedu (escolaridade dos pais, 0-4),
# studytime (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h por semana), failures (reprovacoes anteriores, 0-3),
# schoolsup/famsup (apoio escolar/familiar), higher (quer ensino superior), internet, absences (faltas),
# G1, G2, G3 (notas do 1o, 2o e 3o periodo, 0-20). G3 e a nota final.

print('\nValores ausentes:', int(portugues.isna().sum().sum()))
print('\nNota final G3 (portugues):')
print(portugues['G3'].describe().round(2))
print('Alunos com G3 = 0:', (portugues['G3'] == 0).sum(), '(zero costuma indicar abandono ou ausencia na prova, nao nota zero)')
print('Reprovados (G3 < 10):', (portugues['G3'] < 10).sum(), f'({(portugues["G3"] < 10).mean():.1%})')
print('\nFaltas:')
print(portugues['absences'].describe().round(1))
print('\nReprovacoes anteriores (failures):')
print(portugues['failures'].value_counts().sort_index())
print('\nEscola e endereco:')
print(pd.crosstab(portugues['school'], portugues['address']))

# As notas dos tres periodos sao muito correlacionadas: G2 quase determina G3
print('\nCorrelacao entre G1, G2 e G3:')
print(portugues[['G1', 'G2', 'G3']].corr().round(2))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
esq.hist(portugues['G3'], bins=range(0, 21), color='#2F648F', align='left')
esq.axvline(9.5, color='#D69A35', linestyle='--')
esq.text(9.3, esq.get_ylim()[1] * 0.9, 'aprovação (10)', ha='right', color='#D69A35')
esq.set_xlabel('Nota final G3 (0–20)')
esq.set_ylabel('Alunos')
esq.set_title('Português: 15% abaixo de 10; um grupo com nota zero')
dir.hist(portugues['absences'], bins=range(0, 34, 2), color='#8794A3')
dir.set_xlabel('Faltas no ano')
dir.set_title('Faltas: metade dos alunos tem 2 ou menos')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '01_notas_e_faltas.png'))
plt.show()

# O que a base NAO tem: motivo das faltas, renda, notas de anos anteriores, o que a escola fez com cada aluno.
# E um retrato de um ano, em duas escolas portuguesas, ha vinte anos. Nao descreve escolas brasileiras.
