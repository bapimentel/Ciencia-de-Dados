# Regressao logistica: quando a resposta e sim/nao, modela-se a PROBABILIDADE com a curva logistica.
# Pergunta: como a chance de reprovar se relaciona com a nota do 1o periodo e com reprovacoes anteriores?
# Dados: dados/alunos_portugues.csv (649 alunos; reprovado = nota final G3 < 10).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
alunos = pd.read_csv(os.path.join(pasta, '..', 'dados', 'alunos_portugues.csv'), sep=';')
alunos['reprovado'] = (alunos['G3'] < 10).astype(int)
print('Alunos:', len(alunos), '| reprovados:', alunos['reprovado'].sum())

# Por que nao uma reta? A reta preve "probabilidades" abaixo de 0 e acima de 1.
reta = LinearRegression().fit(alunos[['G1']], alunos['reprovado'])
print('Reta: "probabilidade" prevista para G1 = 0 e 19:', reta.predict(pd.DataFrame({'G1': [0, 19]})).round(2))

# Logistica: log( p / (1 - p) ) = b0 + b1 * G1   ->   p = 1 / (1 + exp(-(b0 + b1 * G1)))
modelo = sm.Logit(alunos['reprovado'], sm.add_constant(alunos[['G1']])).fit(disp=0)
print(modelo.summary().tables[1])
b0, b1 = modelo.params['const'], modelo.params['G1']
for nota in [6, 8, 10, 12]:
    p = 1 / (1 + np.exp(-(b0 + b1 * nota)))
    print(f'G1 = {nota:2d}: P(reprovar) = {p:.2f} | chance (odds) = p/(1-p) = {p / (1 - p):.2f}')
print(f'Razao de chances por ponto a mais em G1: exp({b1:.2f}) = {np.exp(b1):.2f}  '
      f'-> cada ponto a mais multiplica a chance de reprovar por {np.exp(b1):.2f}')

# Com duas variaveis: G1 e reprovacoes anteriores
modelo2 = sm.Logit(alunos['reprovado'], sm.add_constant(alunos[['G1', 'failures']])).fit(disp=0)
razoes = np.exp(modelo2.params)
ic = np.exp(modelo2.conf_int())
print('\nRazoes de chances (IC 95%) com G1 e reprovacoes anteriores:')
for v in ['G1', 'failures']:
    print(f'  {v:9s}: {razoes[v]:.2f} [{ic.loc[v, 0]:.2f}, {ic.loc[v, 1]:.2f}]')
# Mantida a nota do 1o periodo, cada reprovacao anterior multiplica a chance de reprovar por ~razoes['failures'].

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.4))
gerador = np.random.default_rng(0)
esq.scatter(alunos['G1'] + gerador.uniform(-0.2, 0.2, len(alunos)), alunos['reprovado'] + gerador.uniform(-0.04, 0.04, len(alunos)),
            s=8, alpha=0.3, color='#8794A3')
notas = np.linspace(0, 20, 200)
esq.plot(notas, reta.predict(pd.DataFrame({'G1': notas})), color='#BD5B58', linestyle='--', label='reta (sai de 0–1)')
esq.plot(notas, 1 / (1 + np.exp(-(b0 + b1 * notas))), color='#2F648F', linewidth=2.5, label='logística')
esq.axhline(0, color='#E6EBF0')
esq.axhline(1, color='#E6EBF0')
esq.set_xlabel('Nota do 1º período (G1)')
esq.set_ylabel('Reprovado (1) ou não (0)')
esq.set_title('A curva logística fica entre 0 e 1', fontsize=11)
esq.legend(fontsize=9)
for f, cor in [(0, '#2F648F'), (1, '#D69A35'), (2, '#BD5B58')]:
    linha = modelo2.params['const'] + modelo2.params['G1'] * notas + modelo2.params['failures'] * f
    dir.plot(notas, 1 / (1 + np.exp(-linha)), color=cor, linewidth=2, label=f'{f} reprovação(ões) anterior(es)')
dir.set_xlabel('Nota do 1º período (G1)')
dir.set_ylabel('P(reprovar no fim do ano)')
dir.set_title('Mesma nota, risco maior para quem já reprovou', fontsize=11)
dir.legend(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'regressao_logistica.png'))
plt.show()
