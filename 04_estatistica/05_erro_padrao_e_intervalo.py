# Desvio-padrao x erro-padrao x intervalo de confianca: tres coisas que costumam ser confundidas.
# Usamos as 1000 vendas do supermercado como se fossem a POPULACAO e sorteamos amostras dela.
# Assim conhecemos a "verdade" e podemos ver o que cada medida faz.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
populacao = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))['Total'].values
media_verdadeira = populacao.mean()
print(f'"Populacao": {len(populacao)} vendas | media verdadeira = {media_verdadeira:.1f} | desvio = {populacao.std():.1f}')

gerador = np.random.default_rng(10)

# 1) Desvio-padrao: variabilidade dos DADOS. Nao diminui com o tamanho da amostra.
# 2) Erro-padrao: variabilidade da MEDIA AMOSTRAL de uma amostra para outra. Diminui com raiz(n).
for n in [10, 40, 160]:
    medias = [gerador.choice(populacao, size=n, replace=False).mean() for _ in range(2000)]
    print(f'n={n:4d}: desvio dos dados ~ {populacao.std():.0f} | desvio das 2000 medias amostrais = {np.std(medias):.1f} '
          f'| teoria (desvio / raiz(n)) = {populacao.std() / np.sqrt(n):.1f}')

# 3) Intervalo de confianca de 95%: faixa construida a partir de UMA amostra. Se repetirmos o
# procedimento muitas vezes, cerca de 95% dos intervalos contem a media verdadeira.
n = 40
intervalos = []
for _ in range(50):
    amostra = gerador.choice(populacao, size=n, replace=False)
    margem = stats.t.ppf(0.975, n - 1) * amostra.std(ddof=1) / np.sqrt(n)
    intervalos.append((amostra.mean() - margem, amostra.mean(), amostra.mean() + margem))
cobertura = np.mean([baixo <= media_verdadeira <= alto for baixo, _, alto in intervalos])
print(f'\n50 intervalos de 95% com n={n}: {cobertura:.0%} contem a media verdadeira')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.6))
for n, cor in [(10, '#8794A3'), (40, '#168A8A'), (160, '#2F648F')]:
    medias = [gerador.choice(populacao, size=n, replace=False).mean() for _ in range(2000)]
    esq.hist(medias, bins=40, alpha=0.6, color=cor, density=True, label=f'n = {n}')
esq.axvline(media_verdadeira, color='#D69A35', linewidth=2, label='média verdadeira')
esq.set_xlabel('Média de uma amostra')
esq.set_ylabel('densidade')
esq.set_title('Médias de amostras maiores variam menos (erro-padrão)')
esq.legend()
for i, (baixo, centro, alto) in enumerate(intervalos):
    contem = baixo <= media_verdadeira <= alto
    cor = '#2F648F' if contem else '#BD5B58'
    dir.plot([baixo, alto], [i, i], color=cor, linewidth=2)
    dir.plot(centro, i, 'o', color=cor, markersize=3)
dir.axvline(media_verdadeira, color='#D69A35', linewidth=2)
dir.set_xlabel('Total da venda')
dir.set_yticks([])
dir.set_title(f'50 intervalos de 95% (n = 40): {int(cobertura * 50)} contêm a média (vermelho: erraram)')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'erro_padrao_e_intervalos.png'))
plt.show()

# Resumo:
# desvio-padrao -> descreve os dados ("as vendas variam cerca de 246 em torno da media");
# erro-padrao   -> descreve a incerteza da estimativa ("a media de 40 vendas erra cerca de 39");
# IC 95%        -> faixa de valores plausiveis para o parametro, dada a amostra.
