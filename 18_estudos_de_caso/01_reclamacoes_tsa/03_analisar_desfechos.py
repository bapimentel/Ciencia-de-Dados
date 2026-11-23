# Estudo de caso 1 - Reclamacoes por perdas (TSA). Passo 3: em que situacoes as reclamacoes sao negadas?
# Para cada variavel: taxa de negativa por grupo, com intervalo de confianca de 95% (Wilson) e teste qui-quadrado.
# Uma diferenca so e tratada como achado se o intervalo e o teste a sustentam.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
pd.set_option('display.width', 160)
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'))
print(f'Registros: {len(dados)} | negadas: {dados["Negada"].sum()} ({dados["Negada"].mean():.1%})')


def wilson(sucessos, n, z=1.96):
    p = sucessos / n
    centro = (p + z ** 2 / (2 * n)) / (1 + z ** 2 / n)
    meia = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / (1 + z ** 2 / n)
    return centro - meia, centro + meia


def taxa_por_grupo(coluna, minimo=30):
    t = dados.groupby(coluna)['Negada'].agg(n='count', negadas='sum')
    t = t[t['n'] >= minimo].copy()
    t['taxa'] = t['negadas'] / t['n']
    t['ic_inf'], t['ic_sup'] = wilson(t['negadas'], t['n'])
    return t.sort_values('taxa')


# Dias ate registrar em faixas (quartis), para tratar como categoria
dados['Faixa de dias'] = pd.qcut(dados['Dias ate registrar'], 4, labels=['0-9 dias', '10-19 dias', '20-35 dias', '36+ dias'])
resultados = {}
for coluna in ['Claim Site', 'Item Category (agrupada)', 'Airline Name', 'Faixa de dias', 'Claim Type']:
    t = taxa_por_grupo(coluna)
    tabela_cont = pd.crosstab(dados.loc[dados[coluna].isin(t.index), coluna], dados['Negada'])
    qui2, p, gl, _ = chi2_contingency(tabela_cont)
    resultados[coluna] = (t, p)
    print(f'\nTaxa de negativa por {coluna} (grupos com n >= 30) | qui-quadrado = {qui2:.1f}, gl = {gl}, p = {p:.2g}')
    print(t[['n', 'taxa', 'ic_inf', 'ic_sup']].round(3).to_string())

# Estabilidade no tempo: a taxa de negativa muda ao longo do ano?
por_mes = taxa_por_grupo('Mes', minimo=1).sort_index()
print('\nTaxa de negativa por mes de recebimento:')
print(por_mes[['n', 'taxa']].round(3).to_string())

titulos = {'Claim Site': 'Local do incidente', 'Item Category (agrupada)': 'Categoria do item',
           'Airline Name': 'Companhia aérea', 'Faixa de dias': 'Dias entre incidente e registro'}
fig, eixos = plt.subplots(2, 2, figsize=(13, 7.5), gridspec_kw={'height_ratios': [0.55, 1.6]})
media = dados['Negada'].mean()
for eixo, coluna in zip([eixos[0, 0], eixos[0, 1], eixos[1, 0], eixos[1, 1]],
                        ['Claim Site', 'Faixa de dias', 'Item Category (agrupada)', 'Airline Name']):
    t, p = resultados[coluna]
    if coluna == 'Faixa de dias':
        t = t.loc[['0-9 dias', '10-19 dias', '20-35 dias', '36+ dias']]
    rotulos = [f'{str(i)[:28]} (n={n})' for i, n in zip(t.index, t['n'])]
    eixo.errorbar(100 * t['taxa'], range(len(t)), xerr=[100 * (t['taxa'] - t['ic_inf']), 100 * (t['ic_sup'] - t['taxa'])],
                  fmt='o', color='#2F648F', ecolor='#8794A3', capsize=3)
    eixo.axvline(100 * media, color='#D69A35', linestyle='--', linewidth=1)
    eixo.set_yticks(range(len(t)), rotulos, fontsize=9)
    eixo.set_xlim(0, 100)
    eixo.set_xlabel('% negadas (ponto) e intervalo de 95%')
    eixo.set_title(f'{titulos[coluna]} (qui-quadrado: p = {p:.1g})', fontsize=11)
plt.suptitle(f'Taxa de negativa por grupo; linha âmbar = média geral ({media:.0%})', fontsize=11, y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '03_taxa_negativa_por_grupo.png'), bbox_inches='tight')
plt.show()

fig, eixo = plt.subplots(figsize=(8, 3.6))
eixo.fill_between(por_mes.index, 100 * por_mes['ic_inf'], 100 * por_mes['ic_sup'], color='#2F648F', alpha=0.15)
eixo.plot(por_mes.index, 100 * por_mes['taxa'], marker='o', color='#2F648F')
eixo.set_xticks(range(1, 13), ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'])
eixo.set_ylim(30, 80)
eixo.set_ylabel('% negadas')
eixo.set_title('A taxa de negativa oscila entre 50% e 58% ao longo do ano, sem tendência clara')
plt.savefig(os.path.join(pasta, 'figuras', '03_negativa_por_mes.png'))
plt.show()
