# Figura didatica: duas variaveis correlacionadas por uma causa comum.
# Saida: figuras/geradas/correlacao_nao_causalidade.png. Dados simulados com semente fixa.

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'estilo.mplstyle'))

gerador = np.random.default_rng(7)
n = 120
temperatura = gerador.uniform(18, 38, size=n)
sorvetes = 20 + 6 * temperatura + gerador.normal(0, 15, size=n)
afogamentos = 0.5 + 0.08 * temperatura + gerador.normal(0, 0.6, size=n)
afogamentos = np.clip(afogamentos, 0, None)

r_sa = np.corrcoef(sorvetes, afogamentos)[0, 1]
r_ts = np.corrcoef(temperatura, sorvetes)[0, 1]
r_ta = np.corrcoef(temperatura, afogamentos)[0, 1]

fig, eixos = plt.subplots(1, 3, figsize=(12, 3.8))
eixos[0].scatter(sorvetes, afogamentos, s=16, color='#BD5B58', alpha=0.7)
eixos[0].set_xlabel('Sorvetes vendidos no dia')
eixos[0].set_ylabel('Afogamentos no dia')
eixos[0].set_title(f'Sorvetes × afogamentos: r = {r_sa:.2f}')
eixos[1].scatter(temperatura, sorvetes, s=16, color='#2F648F', alpha=0.7)
eixos[1].set_xlabel('Temperatura (°C)')
eixos[1].set_ylabel('Sorvetes vendidos')
eixos[1].set_title(f'Temperatura × sorvetes: r = {r_ts:.2f}')
eixos[2].scatter(temperatura, afogamentos, s=16, color='#2F648F', alpha=0.7)
eixos[2].set_xlabel('Temperatura (°C)')
eixos[2].set_ylabel('Afogamentos')
eixos[2].set_title(f'Temperatura × afogamentos: r = {r_ta:.2f}')
fig.suptitle('Proibir sorvete não reduz afogamentos: a causa comum é o calor (dados simulados)', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, '..', 'geradas', 'correlacao_nao_causalidade.png'))
print('Figura salva em figuras/geradas/correlacao_nao_causalidade.png')
