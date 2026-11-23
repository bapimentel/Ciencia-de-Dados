# Paradoxo de Simpson e o metodo de Mantel-Haenszel: quando a tabela agregada engana.
# Dados reais publicados: comparacao de dois tratamentos para calculo renal (Charig et al., BMJ, 1986):
# A = cirurgia aberta; B = nefrolitotomia percutanea. Sucesso por tamanho do calculo.

import os
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.contingency_tables import StratifiedTable

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# sucessos / total em cada estrato
dados = {
    'cálculos pequenos': {'A': (81, 87), 'B': (234, 270)},
    'cálculos grandes': {'A': (192, 263), 'B': (55, 80)},
}
for estrato, trat in dados.items():
    print(f'{estrato:18s}: A {trat["A"][0]}/{trat["A"][1]} = {trat["A"][0] / trat["A"][1]:.0%} | '
          f'B {trat["B"][0]}/{trat["B"][1]} = {trat["B"][0] / trat["B"][1]:.0%}')
total_a = (81 + 192, 87 + 263)
total_b = (234 + 55, 270 + 80)
print(f'{"total":18s}: A {total_a[0]}/{total_a[1]} = {total_a[0] / total_a[1]:.0%} | B {total_b[0]}/{total_b[1]} = {total_b[0] / total_b[1]:.0%}')
# A vence nos dois estratos, mas B vence no total. Por que? A foi usado sobretudo em calculos grandes
# (casos mais dificeis) e B em pequenos. O tamanho do calculo afeta a escolha do tratamento E o sucesso.

# Razao de chances (odds ratio) em cada estrato: chance de sucesso com A / chance com B
tabelas = []
for estrato, trat in dados.items():
    sa, na = trat['A']
    sb, nb = trat['B']
    tabela = np.array([[sa, na - sa], [sb, nb - sb]])     # linhas: A, B; colunas: sucesso, fracasso
    tabelas.append(tabela)
    rc = (sa * (nb - sb)) / ((na - sa) * sb)
    print(f'Razao de chances ({estrato}): {rc:.2f}')

# Mantel-Haenszel: combina os estratos em uma razao de chances AJUSTADA pelo tamanho do calculo
numerador = sum(t[0, 0] * t[1, 1] / t.sum() for t in tabelas)
denominador = sum(t[0, 1] * t[1, 0] / t.sum() for t in tabelas)
print(f'\nRazao de chances de Mantel-Haenszel (a mao): {numerador / denominador:.2f}')
estratificada = StratifiedTable(tabelas)
baixo, alto = estratificada.oddsratio_pooled_confint()
print(f'statsmodels: {estratificada.oddsratio_pooled:.2f}, IC 95% [{baixo:.2f}, {alto:.2f}]')
print(f'Teste de homogeneidade entre estratos: p = {estratificada.test_equal_odds().pvalue:.3f}')
agregada = np.array([[total_a[0], total_a[1] - total_a[0]], [total_b[0], total_b[1] - total_b[0]]])
print(f'Razao de chances ingenua (tabela somada): {(agregada[0, 0] * agregada[1, 1]) / (agregada[0, 1] * agregada[1, 0]):.2f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4.2))
grupos = ['cálculos pequenos', 'cálculos grandes', 'total']
taxas_a = [81 / 87, 192 / 263, total_a[0] / total_a[1]]
taxas_b = [234 / 270, 55 / 80, total_b[0] / total_b[1]]
x = np.arange(3)
esq.bar(x - 0.2, [100 * t for t in taxas_a], width=0.4, color='#2F648F', label='A (cirurgia aberta)')
esq.bar(x + 0.2, [100 * t for t in taxas_b], width=0.4, color='#168A8A', label='B (percutânea)')
for i in range(3):
    esq.text(i - 0.2, 100 * taxas_a[i] + 1, f'{100 * taxas_a[i]:.0f}%', ha='center', fontsize=9)
    esq.text(i + 0.2, 100 * taxas_b[i] + 1, f'{100 * taxas_b[i]:.0f}%', ha='center', fontsize=9)
esq.set_xticks(x)
esq.set_xticklabels(grupos)
esq.set_ylim(0, 105)
esq.set_ylabel('% de sucesso')
esq.set_title('A vence em cada estrato; B "vence" no total')
esq.legend(loc='lower left', fontsize=9)
dir.bar(['A', 'B'], [87, 270], color='#E6EBF0', label='pequenos')
dir.bar(['A', 'B'], [263, 80], bottom=[87, 270], color='#8794A3', label='grandes')
dir.set_ylabel('Pacientes')
dir.set_title('O porquê: A recebeu sobretudo os casos difíceis')
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'paradoxo_de_simpson.png'))
plt.show()

# Leitura dos numeros: a tabela somada da razao de chances 0,75 (B parece melhor); ajustando pelo tamanho
# do calculo, 1,45 (A parece melhor). O IC 95% ajustado vai de 0,92 a 2,29 e inclui 1: com estes dados,
# a vantagem de A tambem nao e conclusiva. O que e conclusivo e que a tabela somada inverte a direcao.
# Licao: antes de comparar grupos, pergunte o que mais difere entre eles. Estratificar (ou ajustar em um
# modelo) por essa variavel pode inverter a conclusao.
