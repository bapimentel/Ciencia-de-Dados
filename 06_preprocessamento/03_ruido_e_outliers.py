# Dados ruidosos e valores atipicos: suavizar por faixas (binning), suavizar por regressao e detectar
# outliers por IQR e por z-score.
# Dados: dados/bicicletas_dia.csv (alugueis diarios, Washington D.C., 2011-2012).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
dias = pd.read_csv(os.path.join(pasta, '..', 'dados', 'bicicletas_dia.csv'), parse_dates=['dteday'])
dias['temperatura'] = dias['temp'] * 47 - 8

# --- 1. Binning: ordenar, dividir em faixas e trocar cada valor pela media da faixa.
# Exemplo pequeno, para ver a conta: 12 precos ordenados em 3 faixas de 4 valores (mesma frequencia)
precos = np.array([4, 8, 9, 15, 21, 21, 24, 25, 26, 28, 29, 34])
faixas = precos.reshape(3, 4)
print('Faixas:', faixas.tolist())
print('Suavizado pela media da faixa:', np.repeat(faixas.mean(axis=1), 4).round(1).tolist())
# Suavizar pelas bordas: cada valor vira a borda (menor ou maior valor da faixa) mais proxima
pelas_bordas = []
for faixa in faixas:
    menor, maior = faixa[0], faixa[-1]
    for valor in faixa:
        pelas_bordas.append(int(menor) if valor - menor <= maior - valor else int(maior))
print('Suavizado pelas bordas da faixa:', pelas_bordas)

# Nos dados reais: alugueis em funcao da temperatura, suavizados por faixas de temperatura
dias['faixa de temperatura'] = pd.qcut(dias['temperatura'], q=10)
media_faixa = dias.groupby('faixa de temperatura', observed=True)['cnt'].transform('mean')

# --- 2. Regressao: ajustar uma curva e usar o valor ajustado como versao "sem ruido"
coeficientes = np.polyfit(dias['temperatura'], dias['cnt'], deg=2)
ajustado = np.polyval(coeficientes, dias['temperatura'])

# --- 3. Outliers por IQR: abaixo de Q1 - 1,5 IQR ou acima de Q3 + 1,5 IQR
# Olhamos o RESIDUO (aluguel real - esperado para a temperatura): um dia frio com poucos alugueis e normal;
# um dia quente com quase nenhum aluguel e atipico.
dias['residuo'] = dias['cnt'] - ajustado
q1, q3 = dias['residuo'].quantile([0.25, 0.75])
iqr = q3 - q1
atipicos_iqr = dias[(dias['residuo'] < q1 - 1.5 * iqr) | (dias['residuo'] > q3 + 1.5 * iqr)]
print(f'\nResiduo: Q1 = {q1:.0f}, Q3 = {q3:.0f}, IQR = {iqr:.0f}')
print('Dias atipicos pelo criterio do IQR:')
print(atipicos_iqr[['dteday', 'temperatura', 'cnt', 'residuo', 'weathersit']].round({'temperatura': 1, 'residuo': 0}).to_string(index=False))

# --- 4. Outliers por z-score: |valor - media| / desvio > 3
z = (dias['residuo'] - dias['residuo'].mean()) / dias['residuo'].std()
print(f'\nDias com |z| > 3: {int((z.abs() > 3).sum())}')
# O que fazer com eles? Antes de apagar, investigar: os dois dias atipicos sao 27/08/2011 (furacao Irene)
# e 29/10/2012 (furacao Sandy). Sao dados VERDADEIROS e informativos; apaga-los esconderia a realidade.
# O que se decide depende da pergunta: para estudar o efeito da temperatura, faz sentido excluir esses dias
# (e dizer isso); para planejar a operacao, eles sao exatamente o tipo de dia que importa prever.

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
ordem = np.argsort(dias['temperatura'].values)
esq.scatter(dias['temperatura'], dias['cnt'], s=8, alpha=0.35, color='#8794A3', label='dias')
esq.plot(dias['temperatura'].values[ordem], media_faixa.values[ordem], color='#168A8A', drawstyle='steps-mid', label='média por faixa (binning)')
esq.plot(dias['temperatura'].values[ordem], ajustado[ordem], color='#2F648F', linewidth=2, label='regressão quadrática')
esq.set_xlabel('Temperatura média do dia (°C)')
esq.set_ylabel('Aluguéis no dia')
esq.set_title('Duas formas de suavizar o ruído')
esq.legend(fontsize=9)
dir.scatter(dias['dteday'], dias['residuo'], s=8, alpha=0.5, color='#8794A3')
dir.scatter(atipicos_iqr['dteday'], atipicos_iqr['residuo'], s=30, color='#BD5B58', label='atípicos (IQR)')
dir.axhline(q1 - 1.5 * iqr, color='#D69A35', linestyle='--', linewidth=1)
dir.axhline(q3 + 1.5 * iqr, color='#D69A35', linestyle='--', linewidth=1)
sandy = dias[dias['dteday'] == '2012-10-29']
dir.annotate('furacão Sandy', xy=(sandy['dteday'].iloc[0], sandy['residuo'].iloc[0]), xytext=(-120, 10), textcoords='offset points',
             color='#BD5B58', arrowprops=dict(arrowstyle='-', color='#BD5B58'))
dir.set_ylabel('Aluguéis reais − esperados pela temperatura')
dir.set_title('Os dois atípicos são dias de furacão (Irene, Sandy), não erros')
dir.legend(loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'ruido_e_outliers.png'))
plt.show()
