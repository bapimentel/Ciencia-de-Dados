# Atributos pre-atentivos (cor, tamanho, posicao) e eliminacao de saturacao, passo a passo.
# Parte 1: quantos digitos 3 ha na tabela? (com e sem destaque)
# Parte 2: o mesmo grafico de linhas em quatro etapas de limpeza, com dados reais
# (aluguel mensal de bicicletas por assinantes e avulsos, Washington D.C., 2011-2012).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Parte 1: o olho encontra o destaque antes de "ler"
gerador = np.random.default_rng(5)
digitos = gerador.integers(0, 10, size=(4, 14))
fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 3.2))
for eixo, destacar, titulo in [(esq, False, 'Quantos números 3? (procure)'), (dir, True, 'Quantos números 3? (o destaque responde)')]:
    eixo.axis('off')
    eixo.set_xlim(-0.5, 13.5)
    eixo.set_ylim(-0.5, 3.5)
    for i in range(4):
        for j in range(14):
            d = digitos[i, j]
            cor = '#20324A' if (destacar and d == 3) else ('#8794A3' if destacar else '#20324A')
            peso = 'bold' if (destacar and d == 3) else 'normal'
            eixo.text(j, 3 - i, str(d), ha='center', va='center', fontsize=20, color=cor, fontweight=peso)
    eixo.set_title(titulo)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'pre_atentivo_digitos.png'))
plt.show()
print('Quantidade de 3:', int((digitos == 3).sum()))

# --- Parte 2: do grafico saturado ao grafico limpo, com os MESMOS dados
dias = pd.read_csv(os.path.join(pasta, '..', 'dados', 'bicicletas_dia.csv'), parse_dates=['dteday'])
mensal = dias.groupby(dias['dteday'].dt.to_period('M'))[['registered', 'casual']].sum() / 1000
meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
rotulos = [f'{meses[p.month - 1]}/{p.year % 100:02d}' for p in mensal.index]
x = np.arange(len(mensal))

fig, eixos = plt.subplots(2, 2, figsize=(13, 8))

# Etapa 1: tudo o que os programas fazem por padrao: moldura, grade densa, marcadores, legenda em caixa, rotulos inclinados
eixo = eixos[0, 0]
eixo.plot(x, mensal['registered'], marker='s', color='tab:blue', label='Registered users (thousands)')
eixo.plot(x, mensal['casual'], marker='D', color='tab:red', label='Casual users (thousands)')
eixo.grid(True, which='both', axis='both', color='#BBBBBB')
for lado in ['top', 'right']:
    eixo.spines[lado].set_visible(True)
eixo.set_xticks(x)
eixo.set_xticklabels(rotulos, rotation=60, fontsize=7)
eixo.legend(frameon=True, fontsize=8, loc='upper left')
eixo.set_title('1. Padrão: moldura, grade densa, marcadores, legenda', fontsize=11)

# Etapa 2: tirar moldura, grade vertical e marcadores; rotulos de mes legiveis
eixo = eixos[0, 1]
eixo.plot(x, mensal['registered'], color='#2F648F')
eixo.plot(x, mensal['casual'], color='#BD5B58')
eixo.set_xticks(x[::3])
eixo.set_xticklabels(rotulos[::3])
eixo.set_title('2. Menos elementos competindo pela atenção', fontsize=11)

# Etapa 3: rotulo direto no fim de cada linha, no lugar da legenda; unidade no eixo
eixo = eixos[1, 0]
eixo.plot(x, mensal['registered'], color='#2F648F')
eixo.plot(x, mensal['casual'], color='#8794A3')
eixo.text(x[-1] + 0.3, mensal['registered'].iloc[-1], 'assinantes', color='#2F648F', va='center')
eixo.text(x[-1] + 0.3, mensal['casual'].iloc[-1], 'avulsos', color='#8794A3', va='center')
eixo.set_xticks(x[::3])
eixo.set_xticklabels(rotulos[::3])
eixo.set_xlim(-0.5, len(x) + 2.5)
eixo.set_ylabel('Aluguéis no mês (mil)')
eixo.set_title('3. Rótulos diretos; uma cor para o que importa', fontsize=11)

# Etapa 4: titulo que afirma o achado e anotacao do ponto que importa
eixo = eixos[1, 1]
eixo.plot(x, mensal['registered'], color='#2F648F', linewidth=2.4)
eixo.plot(x, mensal['casual'], color='#8794A3')
eixo.text(x[-1] + 0.3, mensal['registered'].iloc[-1], 'assinantes', color='#2F648F', va='center', fontweight='bold')
eixo.text(x[-1] + 0.3, mensal['casual'].iloc[-1], 'avulsos', color='#8794A3', va='center')
pico = int(np.argmax(mensal['registered'].values))
eixo.plot(x[pico], mensal['registered'].iloc[pico], 'o', color='#D69A35')
eixo.annotate(f'{mensal["registered"].iloc[pico]:.0f} mil em {rotulos[pico]}', xy=(x[pico], mensal['registered'].iloc[pico]),
              xytext=(-140, -5), textcoords='offset points', color='#D69A35', arrowprops=dict(arrowstyle='-', color='#D69A35'))
eixo.set_xticks(x[::3])
eixo.set_xticklabels(rotulos[::3])
eixo.set_xlim(-0.5, len(x) + 2.5)
eixo.set_ylabel('Aluguéis no mês (mil)')
eixo.set_title('4. Assinantes sustentam o crescimento de 2012', fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'saturacao_passo_a_passo.png'))
plt.show()
print('Pico de assinantes:', rotulos[pico], round(mensal['registered'].iloc[pico], 1), 'mil')
