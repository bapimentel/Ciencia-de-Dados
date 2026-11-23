# Estudo de caso 3 - Vendas em supermercado. Passo 6: quanto historico seria preciso para confiar num
# perfil por hora? Medimos, nos proprios dados, como a concordancia entre duas amostras independentes de dias
# cresce com o numero de dias em cada amostra. Depois, a formula de Spearman-Brown estima o numero de dias
# necessario para uma concordancia de 0,8, a partir da concordancia observada.
#   Spearman-Brown: r_m = m r / (1 + (m - 1) r), em que m = quantas vezes mais dados.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour
dias = vendas['Data'].unique()
por_dia_hora = vendas.pivot_table(index='Data', columns='Hora', values='Total', aggfunc='sum', fill_value=0)
gerador = np.random.default_rng(0)


def concordancia(n_dias, repeticoes=500):
    valores = []
    for _ in range(repeticoes):
        sorteio = gerador.permutation(len(por_dia_hora))
        a = por_dia_hora.iloc[sorteio[:n_dias]].sum()
        b = por_dia_hora.iloc[sorteio[n_dias:2 * n_dias]].sum()
        valores.append(np.corrcoef(a, b)[0, 1])
    return np.median(valores)


tamanhos = [5, 10, 15, 20, 30, 44]
medido = {n: concordancia(n) for n in tamanhos}
print('Dias em cada amostra | correlacao mediana entre os perfis horarios das duas amostras')
for n, r in medido.items():
    print(f'{n:20d} | {r:.2f}')

r44 = medido[44]
alvo = 0.8
m = alvo * (1 - r44) / (r44 * (1 - alvo)) if r44 > 0 else np.inf
print(f'\nCom 44 dias por amostra, r = {r44:.2f}. Pela formula de Spearman-Brown, para r = {alvo} seriam necessarios '
      f'cerca de {m:.0f} vezes mais dias: ~{44 * m:.0f} dias por amostra (~{44 * m / 30:.0f} meses).')

projecao = np.arange(5, 1500, 5)
r_proj = (projecao / 44) * r44 / (1 + (projecao / 44 - 1) * r44)
fig, eixo = plt.subplots(figsize=(8.5, 4.2))
eixo.plot(projecao, r_proj, color='#8794A3', linestyle='--', label='projeção (Spearman-Brown, a partir de 44 dias)')
eixo.plot(list(medido), list(medido.values()), marker='o', color='#2F648F', linewidth=2, label='medido nos dados')
eixo.axhline(alvo, color='#D69A35', linestyle=':')
eixo.text(1490, alvo + 0.02, f'concordância {alvo}', color='#D69A35', ha='right')
eixo.set_xscale('log')
eixo.set_xlabel('Dias em cada amostra (escala log)')
eixo.set_ylabel('Correlação entre os perfis horários')
eixo.set_ylim(-0.2, 1)
eixo.set_title('Quanto histórico seria preciso para o perfil por hora se repetir', fontsize=11)
eixo.legend(loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '06_quanto_dado_seria_preciso.png'))
plt.show()
# Cuidado: a projecao supoe que o padrao "verdadeiro" e estavel e que os dias sao independentes.
# Ela da uma ordem de grandeza para planejar a coleta, nao um numero exato.
