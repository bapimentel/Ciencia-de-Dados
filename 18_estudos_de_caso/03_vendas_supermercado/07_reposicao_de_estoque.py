# Estudo de caso 3 - Vendas em supermercado. Passo 7: com quanto estoque cada linha de produto deve comecar a semana?
# Os passos 1 a 3 mostraram que as vendas nao tem tendencia nem padrao semanal ou horario estavel: a demanda
# semanal de cada linha oscila em torno de uma media. Para demanda assim, a teoria de estoques (modelo do
# "jornaleiro", newsvendor) diz: estoque-alvo = media + z x desvio-padrao das semanas anteriores, com z escolhido
# pelo nivel de servico (z = 1,28 -> 90% das semanas sem falta).
# Avaliacao por origem movel: para cada semana a partir da 5a, a politica so ve as semanas anteriores e e
# comparada com a demanda real daquela semana. Sao 7 semanas x 6 linhas = 42 linhas-semana de teste.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
semanal = vendas.groupby([vendas['Data'].dt.to_period('W'), 'Product line'])['Quantity'].sum().unstack()
semanal = semanal.iloc[1:-1]                                     # descarta as semanas incompletas das pontas
print(f'{len(semanal)} semanas completas ({semanal.index[0]} a {semanal.index[-1]}); unidades por linha-semana:')
print(semanal.describe().loc[['mean', 'std', 'min', 'max']].round(1).to_string())

politicas = {
    'repor o que vendeu na semana anterior': lambda h: h.iloc[-1],
    'média das semanas anteriores': lambda h: h.mean(),
    'média + 0,67 dp (75% de serviço)': lambda h: h.mean() + 0.674 * h.std(),
    'média + 1,28 dp (90% de serviço)': lambda h: h.mean() + 1.282 * h.std(),
}
linhas, por_semana = [], {}
for nome, regra in politicas.items():
    falta = sobra = rupturas = estoque = n = 0
    serie = []
    for i in range(4, len(semanal)):
        alvo = regra(semanal.iloc[:i])
        demanda = semanal.iloc[i]
        rupturas += int((demanda > alvo).sum())
        falta += (demanda - alvo).clip(lower=0).sum()
        sobra += (alvo - demanda).clip(lower=0).sum()
        estoque += alvo.sum()
        n += len(demanda)
        serie.append((demanda > alvo).mean())
    por_semana[nome] = serie
    linhas.append({'política': nome, 'linhas-semana com falta': f'{rupturas}/{n}', '% com falta': rupturas / n,
                   'unidades em falta': falta, 'unidades que sobraram': sobra, 'estoque médio por linha': estoque / n})
tabela = pd.DataFrame(linhas).set_index('política')
print('\n' + tabela.round(2).to_string())
base, nova = tabela.loc['repor o que vendeu na semana anterior'], tabela.loc['média + 1,28 dp (90% de serviço)']
print(f'\nEfeito de trocar "repor a semana anterior" por "media + 1,28 dp": linhas-semana com falta '
      f'{base["% com falta"]:.0%} -> {nova["% com falta"]:.0%}; unidades em falta {base["unidades em falta"]:.0f} -> '
      f'{nova["unidades em falta"]:.0f} ({nova["unidades em falta"] / base["unidades em falta"] - 1:+.0%}); '
      f'estoque medio {base["estoque médio por linha"]:.1f} -> {nova["estoque médio por linha"]:.1f} '
      f'({nova["estoque médio por linha"] / base["estoque médio por linha"] - 1:+.0%})')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.4))
cores = ['#8794A3', '#7A9CC6', '#168A8A', '#2F648F']
for (nome, linha), cor in zip(tabela.iterrows(), cores):
    esq.scatter(linha['estoque médio por linha'], linha['unidades em falta'], s=120, color=cor, zorder=3)
    esq.annotate(nome, (linha['estoque médio por linha'], linha['unidades em falta']), textcoords='offset points',
                 xytext=(6, 6), fontsize=8.5)
esq.set_xlabel('Estoque médio no início da semana (unidades por linha)')
esq.set_ylabel('Unidades em falta (soma das 42 linhas-semana)')
esq.set_title('Cada política: quanto estoque usa e quanto deixa faltar', fontsize=11)
esq.set_xlim(70, 120)
x = np.arange(len(tabela))
dir.bar(x, 100 * tabela['% com falta'], color=cores)
for i, v in enumerate(tabela['% com falta']):
    dir.text(i, 100 * v + 1, f'{v:.0%}', ha='center')
dir.set_xticks(x, ['semana\nanterior', 'média', 'média +\n0,67 dp', 'média +\n1,28 dp'])
dir.set_ylabel('% das linhas-semana com falta de produto')
dir.set_ylim(0, 60)
dir.set_title('Semanas que o modelo não viu (origem móvel)', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '07_reposicao_de_estoque.png'))
plt.show()
