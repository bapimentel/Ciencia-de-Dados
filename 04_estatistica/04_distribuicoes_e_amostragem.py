# Distribuicoes de probabilidade, amostragem e teste de normalidade.

import os
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro
from statsmodels.graphics.gofplots import qqplot

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# A densidade da normal, escrita como formula
def normal_pdf(x, mu=0, sigma=1):
    return math.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma)

xs = [a / 10.0 for a in range(-50, 50)]
plt.figure()
plt.plot(xs, [normal_pdf(a, sigma=1) for a in xs], '-', label='mu=0, sigma=1')
plt.plot(xs, [normal_pdf(a, sigma=2) for a in xs], '--', label='mu=0, sigma=2')
plt.plot(xs, [normal_pdf(a, sigma=0.5) for a in xs], ':', label='mu=0, sigma=0.5')
plt.plot(xs, [normal_pdf(a, mu=-1) for a in xs], '-.', label='mu=-1, sigma=1')
plt.legend()
plt.title('Densidade normal: a média desloca, o desvio alarga')
plt.xlabel('x')
plt.ylabel('densidade')
plt.savefig(os.path.join(pasta, 'figuras', 'densidades_normais.png'))
plt.show()

# Amostrar: sortear valores de uma distribuicao. Semente fixa = resultado reproduzivel
gerador = np.random.default_rng(0)

# Uma amostra pequena nao mostra a forma; uma grande, sim
fig, eixos = plt.subplots(1, 3, figsize=(10, 3.4), sharey=False)
for eixo, n in zip(eixos, [20, 200, 5000]):
    amostra = gerador.normal(loc=50, scale=5, size=n)
    eixo.hist(amostra, bins=25, density=True, color='#2F648F')
    eixo.plot(np.linspace(30, 70, 200), [normal_pdf(v, 50, 5) for v in np.linspace(30, 70, 200)],
              color='#D69A35', linewidth=2)
    eixo.set_title(f'n = {n}')
    eixo.set_xlabel('valor')
eixos[0].set_ylabel('densidade')
fig.suptitle('O histograma só revela a distribuição quando a amostra cresce', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'amostra_crescendo.png'))
plt.show()

# Teste de normalidade (Shapiro-Wilk): hipotese nula = os dados vem de uma normal
gauss = gerador.normal(loc=50, scale=5, size=100)
uniforme = gerador.uniform(low=-2, high=2, size=100)
for nome, amostra in [('normal', gauss), ('uniforme', uniforme)]:
    estatistica, valor_p = shapiro(amostra)
    print(f'{nome:9s} media={amostra.mean():.2f} desvio={amostra.std():.2f} '
          f'Shapiro W={estatistica:.3f} p={valor_p:.4f}')
# p pequeno (ex.: < 0.05) = evidencia contra a normalidade. p grande nao PROVA normalidade.

# QQ-plot: pontos sobre a reta = compatível com a normal
fig, eixos = plt.subplots(1, 2, figsize=(9, 3.8))
qqplot(gauss, line='s', ax=eixos[0], markerfacecolor='#2F648F', markeredgecolor='#2F648F', alpha=0.7)
eixos[0].set_title('Amostra normal: pontos sobre a reta')
qqplot(uniforme, line='s', ax=eixos[1], markerfacecolor='#BD5B58', markeredgecolor='#BD5B58', alpha=0.7)
eixos[1].set_title('Amostra uniforme: caudas fogem da reta')
for eixo in eixos:
    eixo.get_lines()[1].set_color('#8794A3')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'qqplot.png'))
plt.show()

# Experimente: troque size=100 por size=15 no teste de Shapiro.
# Com amostras pequenas, o teste raramente rejeita, mesmo para dados nao normais.
