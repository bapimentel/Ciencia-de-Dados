# Duas variaveis qualitativas: tabela de contingencia, teste qui-quadrado e concordancia (kappa de Cohen).
# Dados: dados/alunos_portugues.csv (649 alunos; aprovado = nota >= 10).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from sklearn.metrics import cohen_kappa_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
alunos = pd.read_csv(os.path.join(pasta, '..', 'dados', 'alunos_portugues.csv'), sep=';')
alunos['situacao final'] = np.where(alunos['G3'] >= 10, 'aprovado', 'reprovado')

# --- 1. Associacao: a situacao final muda conforme a escola?
tabela = pd.crosstab(alunos['school'], alunos['situacao final'], margins=True)
print('Tabela de contingencia (contagens):')
print(tabela)
proporcoes = pd.crosstab(alunos['school'], alunos['situacao final'], normalize='index')
print('\nProporcoes por linha (cada escola soma 100%):')
print((100 * proporcoes).round(1))

# Qui-quadrado: compara as contagens observadas com as esperadas se NAO houvesse associacao
observado = pd.crosstab(alunos['school'], alunos['situacao final'])
qui2, valor_p, graus, esperado = chi2_contingency(observado)
print('\nContagens esperadas sem associacao:')
print(pd.DataFrame(esperado, index=observado.index, columns=observado.columns).round(1))
print(f'Qui-quadrado = {qui2:.2f}, graus de liberdade = {graus}, p = {valor_p:.2e}')
# A escola MS tem 30% de reprovacao contra 8% na GP; p muito pequeno: a diferenca dificilmente e acaso.
# Mas associacao nao e causa: as escolas recebem alunos de perfis diferentes (endereco, escolaridade dos pais).

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4))
esq.barh(proporcoes.index, 100 * proporcoes['aprovado'], color='#2F648F', label='aprovado')
esq.barh(proporcoes.index, 100 * proporcoes['reprovado'], left=100 * proporcoes['aprovado'], color='#BD5B58', label='reprovado')
for i, escola in enumerate(proporcoes.index):
    esq.text(100 * proporcoes.loc[escola, 'aprovado'] / 2, i, f'{100 * proporcoes.loc[escola, "aprovado"]:.0f}%', color='white', ha='center', va='center', fontweight='bold')
    esq.text(100 * proporcoes.loc[escola, 'aprovado'] + 100 * proporcoes.loc[escola, 'reprovado'] / 2, i,
             f'{100 * proporcoes.loc[escola, "reprovado"]:.0f}%', color='white', ha='center', va='center', fontweight='bold')
esq.set_xlim(0, 100)
esq.set_xlabel('% dos alunos da escola')
esq.set_title(f'Reprovação: 8% na GP, 30% na MS (qui² p = {valor_p:.0e})')
esq.legend(loc='lower right', fontsize=9)
esq.grid(axis='y', visible=False)

# --- 2. Concordancia: a classificacao pela nota do 1o periodo concorda com a do 2o periodo?
# Como dois "avaliadores" classificando os mesmos alunos em: baixo (<10), medio (10-13), alto (>=14)
faixas = [-1, 9, 13, 20]
nomes = ['baixo', 'médio', 'alto']
periodo1 = pd.cut(alunos['G1'], bins=faixas, labels=nomes)
periodo2 = pd.cut(alunos['G2'], bins=faixas, labels=nomes)
concordancia = pd.crosstab(periodo1, periodo2, rownames=['1º período'], colnames=['2º período'])
print('\nClassificacao no 1o x 2o periodo:')
print(concordancia)

# Kappa de Cohen: concordancia observada corrigida pela concordancia esperada por acaso
n = concordancia.values.sum()
p_observada = np.trace(concordancia.values) / n
p_acaso = (concordancia.sum(axis=1).values * concordancia.sum(axis=0).values).sum() / n ** 2
kappa_a_mao = (p_observada - p_acaso) / (1 - p_acaso)
print(f'Concordancia observada = {p_observada:.3f} | esperada por acaso = {p_acaso:.3f} | kappa = {kappa_a_mao:.3f}')
print(f'Conferencia com scikit-learn: {cohen_kappa_score(periodo1, periodo2):.3f}')
# kappa = 1: concordancia perfeita; ~0: igual ao acaso; negativo: discordancia sistematica.

imagem = dir.imshow(concordancia.values, cmap='Blues')
for i in range(3):
    for j in range(3):
        valor = concordancia.values[i, j]
        dir.text(j, i, str(valor), ha='center', va='center', color='white' if valor > 150 else '#20324A', fontsize=12)
dir.set_xticks(range(3))
dir.set_xticklabels(nomes)
dir.set_yticks(range(3))
dir.set_yticklabels(nomes)
dir.set_xlabel('2º período')
dir.set_ylabel('1º período')
dir.set_title(f'A diagonal concentra os acordos: κ = {kappa_a_mao:.2f}')
dir.grid(False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'duas_qualitativas.png'))
plt.show()
