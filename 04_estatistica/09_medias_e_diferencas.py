# Duas medidas emparelhadas (o mesmo aluno medido duas vezes): grafico de medias e diferencas
# (Tukey / Bland-Altman). Pergunta: as notas do 2o periodo sao sistematicamente diferentes das do 1o?
# Dados: dados/alunos_portugues.csv.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
alunos = pd.read_csv(os.path.join(pasta, '..', 'dados', 'alunos_portugues.csv'), sep=';')

# Excluimos quem tem nota zero em algum periodo (zero indica ausencia na prova, nao desempenho)
pares = alunos[(alunos['G1'] > 0) & (alunos['G2'] > 0)][['G1', 'G2']]
print('Alunos com as duas notas:', len(pares))

media_par = (pares['G1'] + pares['G2']) / 2
diferenca = pares['G2'] - pares['G1']
vies = diferenca.mean()
limites = (vies - 1.96 * diferenca.std(ddof=1), vies + 1.96 * diferenca.std(ddof=1))
print(f'Diferenca media (G2 - G1) = {vies:.2f} ponto')
print(f'Limites de concordancia (95% das diferencas): {limites[0]:.2f} a {limites[1]:.2f}')

# Teste t pareado: a diferenca media e zero?
t, p = stats.ttest_rel(pares['G2'], pares['G1'])
print(f'Teste t pareado: t = {t:.2f}, p = {p:.4f}')
# Wilcoxon pareado (nao exige normalidade das diferencas)
w, p_w = stats.wilcoxon(pares['G2'], pares['G1'])
print(f'Wilcoxon pareado: p = {p_w:.4f}')

# A diferenca depende do nivel do aluno? Correlacao entre media do par e diferenca
r = np.corrcoef(media_par, diferenca)[0, 1]
print(f'Correlacao entre nivel (media do par) e diferenca: r = {r:.2f}')

gerador = np.random.default_rng(0)
fig, eixo = plt.subplots(figsize=(8, 4.6))
# pequeno "tremor" so no desenho, porque as notas sao inteiras e os pontos se sobreporiam
eixo.scatter(media_par + gerador.uniform(-0.15, 0.15, len(pares)), diferenca + gerador.uniform(-0.15, 0.15, len(pares)),
             s=10, alpha=0.4, color='#2F648F')
eixo.axhline(0, color='#8794A3', linewidth=1)
eixo.axhline(vies, color='#D69A35', linewidth=2, label=f'diferença média = {vies:+.2f}')
for limite in limites:
    eixo.axhline(limite, color='#D69A35', linestyle='--', linewidth=1)
eixo.text(19.5, limites[1] + 0.2, f'+1,96 dp = {limites[1]:.1f}', ha='right', color='#D69A35', fontsize=9)
eixo.text(19.5, limites[0] - 0.6, f'−1,96 dp = {limites[0]:.1f}', ha='right', color='#D69A35', fontsize=9)
eixo.set_xlabel('Média das duas notas (G1 + G2) / 2')
eixo.set_ylabel('Diferença G2 − G1')
eixo.set_title('Do 1º para o 2º período, as notas mudam pouco em média, mas variam de aluno para aluno')
eixo.legend(loc='upper left')
plt.savefig(os.path.join(pasta, 'figuras', 'medias_e_diferencas.png'))
plt.show()

# Leitura: a diferenca media e pequena (fracao de ponto) e o teste diz se ela e distinguivel de zero;
# os limites mostram que um aluno individual pode subir ou cair 2-3 pontos. Para decidir sobre um aluno,
# o que importa sao os limites, nao a media.
