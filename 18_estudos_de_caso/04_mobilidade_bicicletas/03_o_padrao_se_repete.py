# Aplicacao adicional - Bicicletas compartilhadas. Passo 3: o padrao por hora se repete?
# Antes de organizar a operacao em torno das janelas de pico e de vale, verificamos se elas aparecem
# nos dois anos e em todos os meses, e nao so na media geral.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
horas = pd.read_csv(os.path.join(pasta, 'dados', 'hour.csv'), parse_dates=['dteday'])
horas['mes'] = horas['dteday'].dt.to_period('M')
pico = [7, 8, 9, 17, 18, 19]
madrugada = [1, 2, 3, 4, 5]

# 1) Perfil horario (participacao de cada hora no total) em 2011 e em 2012
for tipo, nome in [(1, 'dias uteis'), (0, 'fins de semana e feriados')]:
    sel = horas[horas['workingday'] == tipo]
    perfis = sel.groupby(['yr', 'hr'])['cnt'].sum().unstack(0)
    perfis = perfis / perfis.sum()
    print(f'{nome}: correlacao entre os perfis horarios de 2011 e 2012 = {perfis[0].corr(perfis[1]):.3f}; '
          f'hora de pico 2011 = {perfis[0].idxmax()}h, 2012 = {perfis[1].idxmax()}h')

# 2) Mes a mes (dias uteis): participacao das horas de pico e da madrugada, e a hora de maior uso
uteis = horas[horas['workingday'] == 1]
mensal = uteis.groupby('mes').apply(lambda g: pd.Series({
    'pico (7-9h e 17-19h)': g.loc[g['hr'].isin(pico), 'cnt'].sum() / g['cnt'].sum(),
    'madrugada (1-5h)': g.loc[g['hr'].isin(madrugada), 'cnt'].sum() / g['cnt'].sum(),
    'hora de maior uso': g.groupby('hr')['cnt'].mean().idxmax()}), include_groups=False)
print('\nDias uteis, mes a mes:')
print(f'  participacao das horas de pico: de {mensal["pico (7-9h e 17-19h)"].min():.0%} a {mensal["pico (7-9h e 17-19h)"].max():.0%}')
print(f'  participacao da madrugada (1-5h): de {mensal["madrugada (1-5h)"].min():.1%} a {mensal["madrugada (1-5h)"].max():.1%}')
print(f'  hora de maior uso: {mensal["hora de maior uso"].astype(int).value_counts().to_dict()} (hora: numero de meses)')

# 3) Mes a mes (fins de semana): a hora de maior uso
fds = horas[horas['workingday'] == 0]
hora_fds = fds.groupby('mes').apply(lambda g: g.groupby('hr')['cnt'].mean().idxmax(), include_groups=False)
print(f'Fins de semana, hora de maior uso por mes: {hora_fds.value_counts().sort_index().to_dict()}')

# 4) Metade x metade dos dias uteis (sorteio): o perfil de uma metade preve o da outra?
datas = uteis['dteday'].unique()
gerador = np.random.default_rng(0)
correlacoes = []
por_dia_hora = uteis.pivot_table(index='dteday', columns='hr', values='cnt', aggfunc='sum', fill_value=0)
for _ in range(500):
    s = gerador.permutation(len(por_dia_hora))
    a, b = por_dia_hora.iloc[s[:len(s) // 2]].sum(), por_dia_hora.iloc[s[len(s) // 2:]].sum()
    correlacoes.append(np.corrcoef(a, b)[0, 1])
print(f'Metade x metade dos dias uteis: correlacao minima em 500 sorteios = {min(correlacoes):.4f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.3))
perfis = uteis.groupby(['yr', 'hr'])['cnt'].sum().unstack(0)
perfis = perfis / perfis.sum()
esq.plot(perfis.index, 100 * perfis[0], color='#8794A3', marker='o', markersize=3, label='2011')
esq.plot(perfis.index, 100 * perfis[1], color='#2F648F', marker='o', markersize=3, label='2012')
esq.set_xticks(range(0, 24, 2))
esq.set_xlabel('Hora do dia')
esq.set_ylabel('% dos aluguéis do ano (dias úteis)')
esq.set_title(f'Dias úteis: o mesmo desenho nos dois anos (correlação {perfis[0].corr(perfis[1]):.3f})', fontsize=11)
esq.legend()
x = mensal.index.to_timestamp()
dir.plot(x, 100 * mensal['pico (7-9h e 17-19h)'], marker='o', color='#2F648F', label='horas de pico (7–9h, 17–19h)')
dir.plot(x, 100 * mensal['madrugada (1-5h)'], marker='o', color='#D69A35', label='madrugada (1–5h)')
dir.set_ylim(0, 70)
dir.set_ylabel('% dos aluguéis do mês (dias úteis)')
dir.set_title('Em todos os 24 meses: pico entre 50% e 55%, madrugada abaixo de 2%', fontsize=11)
dir.legend(loc='center right')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_o_padrao_se_repete.png'))
plt.show()
