# Tres conjuntos com a MESMA media e historias diferentes.
# Dados sinteticos, gerados aqui com semente fixa, so para ensinar o conceito.

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

gerador = np.random.default_rng(42)   # semente fixa: os mesmos numeros a cada execucao

# Loja A: vendas diarias estaveis em torno de 100
loja_a = gerador.normal(loc=100, scale=5, size=60)

# Loja B: vendas muito variaveis, mas com a mesma media
loja_b = gerador.normal(loc=100, scale=30, size=60)

# Loja C: quase sempre vende pouco, com alguns dias excepcionais
loja_c = np.concatenate([gerador.normal(loc=80, scale=5, size=54), gerador.normal(loc=280, scale=10, size=6)])

# Ajuste fino para que as tres medias fiquem exatamente iguais a 100
loja_a = loja_a - loja_a.mean() + 100
loja_b = loja_b - loja_b.mean() + 100
loja_c = loja_c - loja_c.mean() + 100

for nome, loja in [('A', loja_a), ('B', loja_b), ('C', loja_c)]:
    print(f'Loja {nome}: media={loja.mean():.1f}  mediana={np.median(loja):.1f}  '
          f'desvio={loja.std(ddof=1):.1f}  min={loja.min():.1f}  max={loja.max():.1f}')

# A media nao distingue as lojas. O desvio-padrao e a mediana, sim.

fig, eixos = plt.subplots(1, 3, figsize=(10, 3.6), sharex=True, sharey=True)
for eixo, nome, loja in zip(eixos, ['A', 'B', 'C'], [loja_a, loja_b, loja_c]):
    eixo.hist(loja, bins=np.arange(40, 320, 10), color='#2F648F')
    eixo.axvline(loja.mean(), color='#D69A35', linewidth=2, label='média')
    eixo.axvline(np.median(loja), color='#168A8A', linewidth=2, linestyle='--', label='mediana')
    eixo.set_title(f'Loja {nome}: média 100, desvio {loja.std(ddof=1):.0f}')
    eixo.set_xlabel('Vendas por dia')
eixos[0].set_ylabel('Dias')
eixos[0].legend()
fig.suptitle('A mesma média esconde três situações diferentes (60 dias simulados)', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'mesma_media.png'))
plt.show()

# O boxplot resume as tres de uma vez: caixa = Q1 a Q3, linha = mediana, pontos = atipicos
plt.figure(figsize=(7, 3.6))
plt.boxplot([loja_a, loja_b, loja_c], tick_labels=['Loja A', 'Loja B', 'Loja C'], orientation='horizontal')
plt.xlabel('Vendas por dia')
plt.title('Boxplot: a caixa mostra onde está a metade central dos dias')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'mesma_media_boxplot.png'))
plt.show()

# Pergunta de decisao: qual loja precisa de um estoque de seguranca maior?
# A media nao responde. O desvio e os quantis respondem.

# Experimente: aumente o scale da loja B para 50 e veja como o boxplot muda.
