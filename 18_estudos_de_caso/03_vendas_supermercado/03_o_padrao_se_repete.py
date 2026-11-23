# Estudo de caso 3 - Vendas em supermercado. Passo 3: o padrao por hora se repete?
# No passo 2, as 19h aparecem como a hora de maior faturamento. Antes de reorganizar a operacao em torno
# disso, verificamos se o padrao aparece em CADA mes e em CADA filial, e nao so no total.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour
vendas['Mes'] = vendas['Data'].dt.month

# 1) Participacao de cada hora no faturamento, mes a mes
por_mes = vendas.pivot_table(index='Hora', columns='Mes', values='Total', aggfunc='sum')
part_mes = por_mes / por_mes.sum()
print('Participacao de cada hora no faturamento do mes (%):')
print((100 * part_mes).round(1).to_string())
print('Hora de maior faturamento em cada mes:', {m: f'{h}h' for m, h in part_mes.idxmax().items()})
print('Correlacao entre os perfis horarios dos meses:')
print(part_mes.corr().round(2).to_string())

# 2) O mesmo, filial a filial
por_filial = vendas.pivot_table(index='Hora', columns='Branch', values='Total', aggfunc='sum')
part_filial = por_filial / por_filial.sum()
print('\nHora de maior faturamento em cada filial:', {f: f'{h}h' for f, h in part_filial.idxmax().items()})
print('Correlacao entre os perfis horarios das filiais:')
print(part_filial.corr().round(2).to_string())

# 3) Quanto do "pico das 19h" vem de cada mes?
cupons_19 = vendas[vendas['Hora'] == 19].groupby('Mes').size()
print('\nCupons as 19h por mes:', cupons_19.to_dict())

# 4) Testes: (a) os cupons se distribuem igualmente pelas horas? (b) a distribuicao por hora muda entre meses?
cupons_hora = vendas.groupby('Hora').size()
teste_uniforme = stats.chisquare(cupons_hora)
tabela = pd.crosstab(vendas['Hora'], vendas['Mes'])
teste_meses = stats.chi2_contingency(tabela)
print(f'\nCupons por hora: de {cupons_hora.min()} a {cupons_hora.max()}; qui-quadrado contra "todas iguais": p = {teste_uniforme.pvalue:.3f}')
print(f'Distribuicao por hora x mes: qui-quadrado p = {teste_meses.pvalue:.2f}')
print(f'Valor por cupom entre as horas (Kruskal-Wallis): p = {stats.kruskal(*[g["Total"] for _, g in vendas.groupby("Hora")]).pvalue:.2f}')

# 5) Metade dos dias contra a outra metade: o perfil de uma metade preve o da outra?
dias = vendas['Data'].unique()
gerador = np.random.default_rng(0)
correlacoes = []
for _ in range(1000):
    sorteio = gerador.permutation(dias)
    a = vendas[vendas['Data'].isin(sorteio[:len(dias) // 2])].groupby('Hora')['Total'].sum()
    b = vendas[vendas['Data'].isin(sorteio[len(dias) // 2:])].groupby('Hora')['Total'].sum()
    correlacoes.append(np.corrcoef(a / a.sum(), b / b.sum())[0, 1])
correlacoes = np.array(correlacoes)
print(f'\nDividindo os 89 dias em duas metades sorteadas (1000 vezes): correlacao entre os perfis horarios '
      f'mediana {np.median(correlacoes):.2f} (90% entre {np.percentile(correlacoes, 5):.2f} e {np.percentile(correlacoes, 95):.2f})')

# 6) O mesmo teste para o dia da semana: cupons por dia, mes a mes
cupons_dia = vendas.groupby('Data').size().asfreq('D').fillna(0)
semana_mes = cupons_dia.groupby([cupons_dia.index.month, cupons_dia.index.day_of_week]).mean().unstack()
semana_mes.columns = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
print('\nCupons por dia, por dia da semana, mes a mes:')
print(semana_mes.round(1).to_string())

fig, eixos = plt.subplots(1, 3, figsize=(16, 4.4), gridspec_kw={'width_ratios': [1.2, 1.2, 1]})
for eixo, tabela_part, titulo, nomes in [(eixos[0], part_mes, 'Mês a mês', {1: 'jan', 2: 'fev', 3: 'mar'}),
                                         (eixos[1], part_filial, 'Filial a filial', {'A': 'filial A', 'B': 'filial B', 'C': 'filial C'})]:
    for (coluna, cor) in zip(tabela_part.columns, ['#2F648F', '#168A8A', '#D69A35']):
        eixo.plot(tabela_part.index, 100 * tabela_part[coluna], marker='o', markersize=4, color=cor, label=nomes[coluna])
    eixo.set_xticks(tabela_part.index)
    eixo.set_xlabel('Hora')
    eixo.set_ylabel('% do faturamento')
    eixo.set_title(f'{titulo}: a hora de pico muda', fontsize=11)
    eixo.legend()
eixos[2].hist(correlacoes, bins=30, color='#8794A3')
eixos[2].axvline(np.median(correlacoes), color='#BD5B58', linestyle='--')
eixos[2].set_xlabel('Correlação entre os perfis das duas metades')
eixos[2].set_ylabel('Sorteios')
eixos[2].set_title(f'Metade × metade dos dias: mediana {np.median(correlacoes):.2f}', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_o_padrao_se_repete.png'))
plt.show()
