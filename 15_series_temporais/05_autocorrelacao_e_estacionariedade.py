# Autocorrelacao: a correlacao de uma serie com ela mesma deslocada h passos (defasagem, ou lag, h).
#   rho(h) = cor(X_t, X_{t+h})
# O correlograma mostra rho(h) para varias defasagens e ajuda a reconhecer ruido, tendencia e sazonalidade.
# Estacionariedade: media e variancia constantes, e rho(h) dependendo so de h (nao de quando).
# Diferenciar (x_t - x_{t-1}) costuma remover a tendencia; a diferenca sazonal (x_t - x_{t-12}) remove o ciclo anual.

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, adfuller

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

serie = pd.read_csv(os.path.join(pasta, '..', 'dados', 'SPCS20RPSNSA.csv'), index_col=0, parse_dates=True)
x = serie.iloc[:, 0].asfreq('MS')


# Autocorrelacao calculada a mao para uma defasagem, e conferida com statsmodels
def autocorrelacao(v, h):
    v = np.asarray(v, dtype=float)
    media = v.mean()
    return np.sum((v[:-h] - media) * (v[h:] - media)) / np.sum((v - media) ** 2)


print(f'rho(1) a mao = {autocorrelacao(x, 1):.4f} | statsmodels = {acf(x, nlags=1)[1]:.4f}')

gerador = np.random.default_rng(0)
candidatas = {
    'Ruído i.i.d. (simulado)': pd.Series(gerador.normal(0, 1, len(x))),
    'Vendas de imóveis': x,
    'Diferença de 1 mês': x.diff().dropna(),
    'Diferença de 1 e de 12 meses': x.diff().diff(12).dropna(),
}
limite = 1.96 / np.sqrt(len(x))     # faixa aproximada em que rho(h) de um ruido costuma cair
print(f'Faixa de 95% para um ruido: +-{limite:.3f}')
print('\nSerie                           rho(1)  rho(12)  teste ADF (p)')
for nome, v in candidatas.items():
    r = acf(v, nlags=24)
    with warnings.catch_warnings():               # aviso sobre o formato futuro do resultado; nao muda o p
        warnings.simplefilter('ignore', FutureWarning)
        p = adfuller(v)[1]
    print(f'{nome:30s}  {r[1]:+.2f}   {r[12]:+.2f}    {p:.3f}')
# Teste ADF (Dickey-Fuller aumentado): hipotese nula = a serie NAO e estacionaria (tem "raiz unitaria").
# p pequeno (< 0,05) e evidencia de estacionariedade.

fig, eixos = plt.subplots(4, 2, figsize=(12, 10), gridspec_kw={'width_ratios': [1.6, 1]})
for linha, (nome, v) in enumerate(candidatas.items()):
    eixos[linha, 0].plot(np.arange(len(v)), v.values, color='#2F648F' if linha else '#8794A3', linewidth=1)
    eixos[linha, 0].set_title(nome, fontsize=11)
    r = acf(v, nlags=24)
    eixos[linha, 1].bar(range(1, 25), r[1:], color=['#D69A35' if h % 12 == 0 else '#2F648F' for h in range(1, 25)])
    eixos[linha, 1].axhspan(-limite, limite, color='#E6EBF0', zorder=0)
    eixos[linha, 1].set_ylim(-1, 1)
    eixos[linha, 1].set_title('Correlograma (defasagens 1 a 24)', fontsize=10)
eixos[3, 0].set_xlabel('mês')
eixos[3, 1].set_xlabel('defasagem h (âmbar: 12 e 24)')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'correlogramas.png'))
plt.show()
