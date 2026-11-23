# Estudo de caso 1 - Reclamacoes por perdas em aeroportos (TSA). Passo 1: conhecer os dados.
# Base publica da Transportation Security Administration (EUA): reclamacoes recebidas em 2015,
# na atualizacao de 9 de fevereiro de 2016 (arquivo dados/claims-data-2015-as-of-feb-9-2016.xlsx).
# Objetivo deste passo: entender o que cada linha e cada coluna registram ANTES de qualquer filtro.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
os.makedirs(os.path.join(pasta, 'figuras'), exist_ok=True)

reclamacoes = pd.read_excel(os.path.join(pasta, 'dados', 'claims-data-2015-as-of-feb-9-2016.xlsx'))
print('Registros:', len(reclamacoes), '| colunas:', reclamacoes.shape[1])
print(reclamacoes.dtypes)
print(reclamacoes.head(3).to_string())
# Cada linha e uma reclamacao: quando foi recebida (Date Received), quando ocorreu o incidente (Incident D),
# aeroporto, companhia aerea, tipo, local (bagagem despachada, inspecao...), categoria do item,
# valor pago (Close Amount) e desfecho (Disposition).

# 1) Quantos valores distintos cada coluna tem? Separa identificadores, categorias e numeros.
print('\nValores distintos por coluna:')
print(reclamacoes.nunique())

# 2) As categorias principais
for coluna in ['Disposition', 'Claim Type', 'Claim Site']:
    print(f'\n{coluna}:')
    print(reclamacoes[coluna].value_counts(dropna=False))

# 3) O traco '-' e usado como "sem informacao" em varias colunas (nao aparece como NaN!)
tracos = (reclamacoes == '-').sum()
print('\nRegistros com "-" por coluna:')
print(tracos[tracos > 0])

# 4) Close Amount veio como texto justamente por causa dos tracos
print('\nTipo de Close Amount:', reclamacoes['Close Amount'].dtype)
print(reclamacoes['Close Amount'].value_counts().head(6))

# 5) Periodo coberto
print('\nRecebidas de', reclamacoes['Date Received'].min().date(), 'a', reclamacoes['Date Received'].max().date())
print('Incidentes de', reclamacoes['Incident D'].min().date(), 'a', reclamacoes['Incident D'].max().date())

# 6) Reclamacoes sem desfecho por mes de recebimento: as mais recentes ainda estavam em analise em fev/2016?
sem_desfecho = reclamacoes['Disposition'].eq('-').groupby(reclamacoes['Date Received'].dt.month).mean()
print('\nFracao sem desfecho por mes de recebimento:')
print(sem_desfecho.round(2).to_string())

fig, eixos = plt.subplots(1, 3, figsize=(15, 3.9))
desfechos = reclamacoes['Disposition'].replace('-', 'sem desfecho').value_counts().sort_values()
eixos[0].barh(desfechos.index, desfechos.values, color=['#2F648F' if d == 'Deny' else '#8794A3' for d in desfechos.index])
for i, v in enumerate(desfechos.values):
    eixos[0].text(v + 40, i, str(v), va='center')
eixos[0].set_title('Desfechos registrados', fontsize=11)
eixos[0].set_xlabel('Reclamações')
eixos[0].grid(axis='y', visible=False)
eixos[1].barh(tracos[tracos > 0].sort_values().index, tracos[tracos > 0].sort_values().values, color='#BD5B58')
eixos[1].set_title('Campos marcados com "-" (sem informação)', fontsize=11)
eixos[1].set_xlabel('Reclamações')
eixos[1].grid(axis='y', visible=False)
eixos[2].bar(range(1, 13), 100 * sem_desfecho.values, color=['#BD5B58' if v > 0.4 else '#8794A3' for v in sem_desfecho.values])
eixos[2].set_xticks(range(1, 13), ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'])
eixos[2].set_ylabel('% sem desfecho')
eixos[2].set_title('Os pedidos do fim do ano ainda estavam em análise', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '01_visao_geral.png'))
plt.show()

por_mes = reclamacoes.groupby(reclamacoes['Date Received'].dt.to_period('M')).size()
fig, eixo = plt.subplots(figsize=(8, 3.6))
eixo.bar(por_mes.index.astype(str), por_mes.values, color='#2F648F')
eixo.set_title('Reclamações recebidas por mês em 2015')
eixo.set_ylabel('Reclamações')
eixo.tick_params(axis='x', labelrotation=45)
plt.savefig(os.path.join(pasta, 'figuras', '01_reclamacoes_por_mes.png'))
plt.show()
