# Velocidade: dados que chegam em fluxo e precisam ser resumidos sem guardar tudo.
# Veracidade: nem todo dado que chega e confiavel; o resumo precisa resistir a erros.
# Fluxo simulado de leituras de um sensor de temperatura (semente fixa).

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
gerador = np.random.default_rng(3)

# Leituras: temperatura que sobe devagar, com ruido, e alguns erros grosseiros do sensor (999)
n = 600
verdadeiro = 25 + 3 * np.sin(np.arange(n) / 80)
leituras = verdadeiro + gerador.normal(0, 0.6, size=n)
erros = gerador.choice(n, size=8, replace=False)
leituras[erros] = 999.0

# --- Velocidade: media "online", atualizada a cada leitura, com memoria constante
# media_nova = media_antiga + (x - media_antiga) / k   (nao precisa guardar as leituras anteriores)
media = 0.0
medias_online = []
for k, x in enumerate(leituras, start=1):
    media = media + (x - media) / k
    medias_online.append(media)
print(f'Media online ao final: {media:.2f} (igual a media de tudo: {leituras.mean():.2f})')

# Media movel exponencial: da mais peso ao recente, tambem com memoria constante
alfa = 0.05
mme = leituras[0]
mmes = []
for x in leituras:
    mme = alfa * x + (1 - alfa) * mme
    mmes.append(mme)

# --- Veracidade: os 8 erros de 999 arrastam as duas medias. Uma regra simples de validacao
# descarta leituras fisicamente impossiveis antes de atualizar o resumo.
mme_validada = leituras[0]
mmes_validadas = []
descartadas = 0
for x in leituras:
    if x < -40 or x > 60:          # faixa plausivel para este sensor
        descartadas += 1
    else:
        mme_validada = alfa * x + (1 - alfa) * mme_validada
    mmes_validadas.append(mme_validada)
print(f'Leituras descartadas pela validacao: {descartadas}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4))
esq.plot(np.clip(leituras, 15, 40), color='#E6EBF0', linewidth=1, label='leituras (999 cortado no gráfico)')
esq.plot(mmes, color='#BD5B58', label='média móvel exponencial, sem validação')
esq.plot(mmes_validadas, color='#2F648F', label='com validação da faixa plausível')
esq.plot(verdadeiro, color='#20324A', linestyle='--', linewidth=1, label='valor real')
esq.set_ylim(15, 40)
esq.set_xlabel('Leitura nº')
esq.set_ylabel('°C')
esq.set_title('Oito erros do sensor bastam para distorcer o resumo')
esq.legend(fontsize=8.5, loc='upper left')
dir.plot(medias_online, color='#BD5B58', label='média online, sem validação')
dir.axhline(verdadeiro.mean(), color='#20324A', linestyle='--', linewidth=1, label='média real')
dir.set_xlabel('Leitura nº')
dir.set_ylabel('°C')
dir.set_title('A média acumulada nunca se recupera dos erros')
dir.legend(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'velocidade_e_veracidade.png'))
plt.show()
