# Transformacao de dados: discretizar (numero -> faixa), gerar hierarquias (dia -> mes -> trimestre)
# e agregar (muitas linhas -> um resumo por grupo).
# Dados: dados/bicicletas_dia.csv.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
dias = pd.read_csv(os.path.join(pasta, '..', 'dados', 'bicicletas_dia.csv'), parse_dates=['dteday'])
dias['temperatura'] = dias['temp'] * 47 - 8

# --- Discretizacao: tres jeitos de cortar a temperatura em 4 faixas
# (a) larguras iguais: cada faixa cobre o mesmo intervalo de graus
largura = pd.cut(dias['temperatura'], bins=4)
# (b) frequencias iguais: cada faixa tem o mesmo numero de dias (quantis)
frequencia = pd.qcut(dias['temperatura'], q=4)
# (c) cortes com significado no dominio, escolhidos por quem conhece o problema
dominio = pd.cut(dias['temperatura'], bins=[-20, 5, 15, 25, 40], labels=['frio', 'ameno', 'agradável', 'quente'])
for nome, faixas in [('larguras iguais', largura), ('frequencias iguais', frequencia), ('dominio', dominio)]:
    print(f'\n{nome}:')
    print(dias.groupby(faixas, observed=True)['cnt'].agg(dias='size', media='mean').round(0))
# Larguras iguais deixam faixas quase vazias nas pontas; frequencias iguais garantem amostra em cada faixa;
# cortes de dominio sao os mais faceis de comunicar.

# --- Hierarquia de conceitos: dia -> mes -> trimestre -> ano. Subir na hierarquia = agregar.
dias['mes'] = dias['dteday'].dt.to_period('M')
dias['trimestre'] = dias['dteday'].dt.to_period('Q')
dias['ano'] = dias['dteday'].dt.year
for nivel in ['mes', 'trimestre', 'ano']:
    agregado = dias.groupby(nivel)['cnt'].sum()
    print(f'\nAgregado por {nivel}: {len(agregado)} linhas; primeiras: {agregado.head(3).to_dict()}')

# --- Construcao de atributos: combinar colunas em uma nova com significado
dias['dia agradavel'] = (dias['temperatura'].between(15, 28)) & (dias['weathersit'] == 1) & (dias['hum'] < 0.7)
print('\nMedia de alugueis em dias "agradaveis" x demais:')
print(dias.groupby('dia agradavel')['cnt'].agg(['size', 'mean']).round(0))

fig, eixos = plt.subplots(1, 3, figsize=(14, 3.8))
for eixo, (titulo, faixas) in zip(eixos, [('Larguras iguais', largura), ('Frequências iguais', frequencia), ('Cortes do domínio', dominio)]):
    contagem = faixas.value_counts().sort_index()
    rotulos = [str(c) if titulo == 'Cortes do domínio' else f'{c.left:.0f} a {c.right:.0f}' for c in contagem.index]
    eixo.bar(rotulos, contagem.values, color='#2F648F')
    eixo.set_title(f'{titulo}: dias por faixa', fontsize=11)
    eixo.tick_params(axis='x', labelsize=9)
eixos[0].set_ylabel('Dias')
fig.suptitle('Três maneiras de discretizar a mesma temperatura (°C)', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'discretizacao.png'))
plt.show()
