# Aplicacao adicional - Educacao. Passo 2: comparar grupos.
# Pergunta: que caracteristicas observaveis antes do fim do ano aparecem associadas a nota final?
# Comparacoes com teste, tamanho do efeito e intervalo, sem transformar associacao em causa.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
alunos = pd.read_csv(os.path.join(pasta, 'dados', 'student-por.csv'), sep=';')

# Tamanho do efeito para comparar dois grupos sem assumir normalidade: delta de Cliff
# (probabilidade de um valor do grupo A ser maior que um de B, menos a probabilidade contraria; -1 a 1)
def delta_cliff(a, b):
    a, b = np.asarray(a), np.asarray(b)
    maior = (a[:, None] > b[None, :]).mean()
    menor = (a[:, None] < b[None, :]).mean()
    return maior - menor

def comparar(coluna, grupo_a, grupo_b, rotulo_a, rotulo_b):
    a = alunos.loc[grupo_a, coluna]
    b = alunos.loc[grupo_b, coluna]
    u, p = stats.mannwhitneyu(a, b)
    print(f'{coluna} | {rotulo_a}: n={len(a)}, mediana={a.median():.1f}, media={a.mean():.2f} | '
          f'{rotulo_b}: n={len(b)}, mediana={b.median():.1f}, media={b.mean():.2f} | '
          f'Mann-Whitney p={p:.4f} | delta de Cliff={delta_cliff(a, b):+.2f}')

print('Nota final G3 por grupo:')
comparar('G3', alunos['failures'] == 0, alunos['failures'] > 0, 'sem reprovacao anterior', 'com reprovacao')
comparar('G3', alunos['higher'] == 'yes', alunos['higher'] == 'no', 'quer ensino superior', 'nao quer')
comparar('G3', alunos['studytime'] >= 3, alunos['studytime'] <= 2, 'estuda 5h+ por semana', 'estuda menos de 5h')
comparar('G3', alunos['absences'] <= 5, alunos['absences'] > 5, 'ate 5 faltas', 'mais de 5 faltas')
comparar('G3', alunos['schoolsup'] == 'yes', alunos['schoolsup'] == 'no', 'com apoio escolar', 'sem apoio escolar')
comparar('G3', alunos['address'] == 'U', alunos['address'] == 'R', 'urbano', 'rural')
# Repare no apoio escolar: quem recebe apoio tem nota MENOR. Nao e que o apoio prejudique: o apoio e dado a
# quem ja tem dificuldade. E o exemplo classico de associacao que nao e efeito.

# Faltas x nota: correlacao de Spearman e taxa de reprovacao por faixa de faltas
rho, p = stats.spearmanr(alunos['absences'], alunos['G3'])
print(f'\nSpearman faltas x G3: rho={rho:.3f}, p={p:.4f}')
faixas = pd.cut(alunos['absences'], bins=[-1, 0, 2, 5, 10, 100], labels=['0', '1–2', '3–5', '6–10', '>10'])
tabela = alunos.groupby(faixas, observed=True).agg(alunos=('G3', 'size'), nota_media=('G3', 'mean'), reprovacao=('G3', lambda g: (g < 10).mean()))
print('\nPor faixa de faltas:')
print(tabela.round(3))
# Intervalo de confianca para a taxa de reprovacao em cada faixa (Wilson)
def intervalo_wilson(k, n, z=1.96):
    p = k / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    meio = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centro - meio, centro + meio
print('IC 95% da taxa de reprovacao por faixa:')
for faixa, linha in tabela.iterrows():
    k = int(round(linha['reprovacao'] * linha['alunos']))
    baixo, alto = intervalo_wilson(k, int(linha['alunos']))
    print(f'  {faixa:>5s}: {linha["reprovacao"]:.1%}  [{baixo:.1%}, {alto:.1%}]  (n={int(linha["alunos"])})')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
grupos = [alunos.loc[alunos['failures'] == f, 'G3'] for f in range(4)]
esq.boxplot(grupos, tick_labels=[f'{f}\n(n={len(g)})' for f, g in zip(range(4), grupos)], medianprops=dict(color='#D69A35', linewidth=2))
esq.set_xlabel('Reprovações anteriores')
esq.set_ylabel('Nota final G3')
esq.set_title('Quem já reprovou tem notas bem menores (delta de Cliff = 0,71)')
dir.bar(range(len(tabela)), 100 * tabela['reprovacao'], color='#2F648F')
for i, (faixa, linha) in enumerate(tabela.iterrows()):
    k = int(round(linha['reprovacao'] * linha['alunos']))
    baixo, alto = intervalo_wilson(k, int(linha['alunos']))
    dir.plot([i, i], [100 * baixo, 100 * alto], color='#20324A', linewidth=1.5)
dir.set_xticks(range(len(tabela)))
dir.set_xticklabels([f'{f}\n(n={int(n)})' for f, n in zip(tabela.index, tabela['alunos'])])
dir.set_xlabel('Faltas no ano')
dir.set_ylabel('% reprovados (G3 < 10), IC 95%')
dir.set_title('Mais de 10 faltas: reprovação maior, mas o intervalo é largo')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '02_grupos.png'))
plt.show()

# A diferenca mais forte e com reprovacoes anteriores, nao com faltas. Nenhuma delas e causa demonstrada:
# faltar e reprovar podem ter uma origem comum (saude, trabalho, familia) que a base nao registra.
