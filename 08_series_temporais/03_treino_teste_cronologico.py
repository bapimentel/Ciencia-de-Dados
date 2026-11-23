# Separar treino e teste no tempo e comparar previsoes simples (linhas de base).
# Em series, o teste e o FUTURO: nada de embaralhar.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

serie = pd.read_csv(os.path.join(pasta, '..', 'dados', 'SPCS20RPSNSA.csv'), index_col=0, parse_dates=True)
serie.columns = ['vendas']
serie = serie.asfreq('MS')['vendas']

# Ultimos 24 meses para teste; tudo antes e treino
horizonte = 24
treino = serie[:-horizonte]
teste = serie[-horizonte:]
print('Treino:', treino.index.min().date(), 'a', treino.index.max().date(), f'({len(treino)} meses)')
print('Teste: ', teste.index.min().date(), 'a', teste.index.max().date(), f'({len(teste)} meses)')

# Tres previsoes ingenuas, que todo modelo precisa superar
previsao_media = pd.Series(treino.mean(), index=teste.index)                 # media historica
previsao_ultimo = pd.Series(treino.iloc[-1], index=teste.index)             # repete o ultimo valor
previsao_sazonal = pd.Series(treino.iloc[-12:].values.tolist() * 2, index=teste.index)   # repete os 12 ultimos meses

def mae(real, previsto):
    return np.mean(np.abs(real - previsto))

def mape(real, previsto):
    return 100 * np.mean(np.abs((real - previsto) / real))

for nome, prev in [('media historica', previsao_media), ('ultimo valor', previsao_ultimo), ('sazonal ingenua', previsao_sazonal)]:
    print(f'{nome:16s} MAE = {mae(teste, prev):8.0f}   MAPE = {mape(teste, prev):5.1f}%')
# A sazonal ingenua (mesmo mes do ano anterior) costuma ser dificil de bater em series com sazonalidade forte.

fig, eixo = plt.subplots(figsize=(9, 4.2))
eixo.plot(treino.index[-60:], treino.iloc[-60:], color='#2F648F', label='treino (últimos 5 anos)')
eixo.plot(teste.index, teste, color='#20324A', linewidth=2.2, label='teste (real)')
eixo.plot(teste.index, previsao_sazonal, color='#168A8A', linestyle='--', label='sazonal ingênua')
eixo.plot(teste.index, previsao_ultimo, color='#D69A35', linestyle=':', label='último valor')
eixo.axvline(teste.index[0], color='#8794A3', linewidth=1)
eixo.text(teste.index[0], eixo.get_ylim()[1] * 0.97, ' início do teste', color='#8794A3', va='top')
eixo.set_ylabel('Pares de vendas no mês')
eixo.set_title('Repetir o ano anterior já acompanha o desenho da série; repetir o último valor não')
eixo.legend(loc='lower left')
plt.savefig(os.path.join(pasta, 'figuras', 'treino_teste_linhas_de_base.png'))
plt.show()

# Por que nao embaralhar? Se meses futuros entrassem no treino, o modelo "veria" o que vem depois.
# A separacao cronologica imita o uso real: so o passado esta disponivel na hora de prever.

# Experimente: use horizonte = 12 e horizonte = 36. Os erros mudam muito? Qual linha de base resiste melhor?
