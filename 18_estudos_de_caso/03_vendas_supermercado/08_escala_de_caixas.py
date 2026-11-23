# Estudo de caso 3 - Vendas em supermercado. Passo 8: distribuir os caixas pelo perfil horario ou por igual?
# Teste fora da amostra: montamos duas escalas com o que se sabia em janeiro e fevereiro e as aplicamos a marco.
#   - escala por perfil: horas de caixa proporcionais a participacao de cada hora nos cupons de jan-fev;
#   - escala uniforme: as mesmas horas de caixa divididas igualmente entre as 11 horas de funcionamento.
# Total de horas igual nas duas. Medida: cupons de marco que chegaram acima da capacidade da hora (fila) e
# capacidade ociosa, somados sobre todos os dias e horas, para tres folgas de capacidade.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour
horas = list(range(10, 21))
treino = vendas[vendas['Data'] < '2019-03-01']
teste = vendas[vendas['Data'] >= '2019-03-01']
perfil = treino.groupby('Hora').size().reindex(horas, fill_value=0)
perfil = perfil / perfil.sum()
uniforme = pd.Series(1 / len(horas), index=horas)
demanda = teste.groupby(['Data', 'Hora']).size().unstack(fill_value=0).reindex(columns=horas, fill_value=0)
print(f'Marco: {len(demanda)} dias, {int(demanda.values.sum())} cupons')
print('Participacao de cada hora em jan-fev (%):', (100 * perfil).round(1).to_dict())

linhas = []
for folga in [1.0, 1.2, 1.5]:
    total_dia = demanda.sum(axis=1).mean() * folga
    for nome, escala in [('por perfil (jan-fev)', perfil), ('uniforme', uniforme)]:
        capacidade = pd.DataFrame(np.outer(np.full(len(demanda), total_dia), escala.values), index=demanda.index, columns=horas)
        acima = (demanda - capacidade).clip(lower=0).values.sum()
        ociosa = (capacidade - demanda).clip(lower=0).values.sum()
        linhas.append({'folga': folga, 'escala': nome, 'cupons acima da capacidade': acima, 'capacidade ociosa': ociosa})
tabela = pd.DataFrame(linhas)
print(tabela.round(1).to_string(index=False))

fig, eixo = plt.subplots(figsize=(8.5, 4.2))
x = np.arange(3)
for k, (nome, cor) in enumerate([('por perfil (jan-fev)', '#8794A3'), ('uniforme', '#2F648F')]):
    t = tabela[tabela['escala'] == nome]
    eixo.bar(x + (k - 0.5) * 0.4, t['cupons acima da capacidade'], width=0.4, color=cor, label=f'escala {nome}')
eixo.set_xticks(x, ['capacidade = demanda média', '+20% de folga', '+50% de folga'])
eixo.set_ylabel('Cupons de março acima da capacidade')
eixo.set_title('Em março, as duas escalas deixam praticamente a mesma fila', fontsize=11)
eixo.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '08_escala_de_caixas.png'))
plt.show()
