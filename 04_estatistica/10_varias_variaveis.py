# Varias variaveis ao mesmo tempo: matriz de dispersao, dispersao simbolica, perfis medios,
# interacao entre fatores e ANOVA de dois fatores com comparacoes de Tukey.
# Dados: dados/bicicletas_dia.csv (alugueis diarios de bicicletas em Washington D.C., 2011-2012; UCI Bike Sharing).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
dias = pd.read_csv(os.path.join(pasta, '..', 'dados', 'bicicletas_dia.csv'))
# Colunas vem normalizadas; voltamos para unidades legiveis (descricao no README do estudo de caso 04)
dias['temperatura'] = dias['temp'] * 47 - 8           # graus C
dias['umidade'] = dias['hum'] * 100                    # %
dias['vento'] = dias['windspeed'] * 67                 # km/h
dias['alugueis'] = dias['cnt']
dias['estacao'] = dias['season'].map({1: 'inverno', 2: 'primavera', 3: 'verão', 4: 'outono'})
dias['tipo de dia'] = np.where(dias['workingday'] == 1, 'útil', 'fim de semana/feriado')

# --- 1. Vetor de medias e matriz de correlacoes: o resumo numerico de varias variaveis
variaveis = ['temperatura', 'umidade', 'vento', 'alugueis']
print('Vetor de medias:')
print(dias[variaveis].mean().round(1))
print('\nMatriz de correlacoes:')
print(dias[variaveis].corr().round(2))

# --- 2. Matriz de dispersao ("grafico do desenhista"): diagonal = histogramas, abaixo = dispersao, acima = r
n = len(variaveis)
fig, eixos = plt.subplots(n, n, figsize=(9, 9))
for i, linha in enumerate(variaveis):
    for j, coluna in enumerate(variaveis):
        eixo = eixos[i, j]
        if i == j:
            eixo.hist(dias[linha], bins=20, color='#8794A3')
            eixo.set_title(linha, fontsize=10)
        elif i > j:
            eixo.scatter(dias[coluna], dias[linha], s=4, alpha=0.4, color='#2F648F')
        else:
            r = dias[linha].corr(dias[coluna])
            eixo.text(0.5, 0.5, f'r = {r:.2f}', ha='center', va='center', fontsize=14,
                      color='#2F648F' if abs(r) > 0.3 else '#8794A3', transform=eixo.transAxes)
            eixo.set_xticks([])
            eixo.set_yticks([])
            eixo.grid(False)
        if j > 0 and i != j:
            eixo.set_yticklabels([])
        eixo.tick_params(labelsize=7)
fig.suptitle('Matriz de dispersão: temperatura é a variável mais associada aos aluguéis', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'matriz_de_dispersao.png'))
plt.show()

# --- 3. Dispersao simbolica: uma terceira variavel no tamanho/cor do ponto
fig, eixo = plt.subplots(figsize=(8, 4.6))
pontos = eixo.scatter(dias['temperatura'], dias['alugueis'], c=dias['umidade'], s=12, cmap='Blues', edgecolors='#8794A3', linewidths=0.2)
plt.colorbar(pontos, ax=eixo, label='umidade (%)')
eixo.set_xlabel('Temperatura média do dia (°C)')
eixo.set_ylabel('Aluguéis no dia')
eixo.set_title('Terceira variável na cor: os dias de umidade alta (escuros) ficam embaixo')
plt.savefig(os.path.join(pasta, 'figuras', 'dispersao_simbolica.png'))
plt.show()

# --- 4. Perfis medios: dois fatores qualitativos explicando uma variavel quantitativa
perfis = dias.groupby(['estacao', 'tipo de dia'])['alugueis'].agg(['mean', 'sem', 'count'])
print('\nMedia de alugueis por estacao e tipo de dia:')
print(perfis.round(0))
ordem = ['inverno', 'primavera', 'verão', 'outono']
fig, eixo = plt.subplots(figsize=(8, 4.4))
for tipo, cor in [('útil', '#2F648F'), ('fim de semana/feriado', '#168A8A')]:
    medias = [perfis.loc[(e, tipo), 'mean'] for e in ordem]
    erros = [1.96 * perfis.loc[(e, tipo), 'sem'] for e in ordem]
    eixo.errorbar(range(4), medias, yerr=erros, marker='o', capsize=5, color=cor, label=tipo)
eixo.set_xticks(range(4))
eixo.set_xticklabels(ordem)
eixo.set_ylabel('Aluguéis por dia (média, IC 95%)')
eixo.set_title('Perfis quase paralelos: a estação pesa muito, o tipo de dia pouco')
eixo.legend()
plt.savefig(os.path.join(pasta, 'figuras', 'perfis_medios.png'))
plt.show()

# --- 5. ANOVA de dois fatores: formaliza o que os perfis sugerem
modelo = smf.ols('alugueis ~ C(estacao) * C(Q("tipo de dia"))', data=dias).fit()
tabela = anova_lm(modelo, typ=2)
print('\nANOVA de dois fatores (com interacao):')
print(tabela.round(4))
# Leitura: efeito da estacao com p muito pequeno; tipo de dia e interacao com p grandes ->
# os perfis paralelos do grafico sao compativeis com "sem interacao".

# --- 6. Comparacoes multiplas de Tukey: QUAIS estacoes diferem?
tukey = pairwise_tukeyhsd(dias['alugueis'], dias['estacao'])
print('\nComparacoes de Tukey entre estacoes:')
print(tukey.summary())
