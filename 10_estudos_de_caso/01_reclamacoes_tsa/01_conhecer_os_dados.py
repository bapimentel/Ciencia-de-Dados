# Estudo de caso 1 - Reclamacoes por perdas (TSA). Etapa 1: conhecer os dados (livro, secao 11.1).
# Base: reclamacoes registradas na Transportation Security Administration (EUA) em 2015,
# arquivo claims-data-2015-as-of-feb-9-2016.xlsx (dados.gov / TSA), o mesmo usado no livro.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

reclamacoes = pd.read_excel(os.path.join(pasta, 'dados', 'claims-data-2015-as-of-feb-9-2016.xlsx'))
print('Registros:', len(reclamacoes), '| colunas:', reclamacoes.shape[1])
print(reclamacoes.dtypes)
print(reclamacoes.head(3).to_string())

# Cada linha e uma reclamacao: quando foi recebida, quando ocorreu o incidente, aeroporto,
# companhia aerea, tipo, local (bagagem despachada, inspecao...), categoria do item,
# valor pago (Close Amount) e desfecho (Disposition).

# Valores unicos por coluna: separa identificadores, categorias e numeros
print('\nValores distintos por coluna:')
print(reclamacoes.nunique())

# As categorias principais
for coluna in ['Disposition', 'Claim Type', 'Claim Site']:
    print(f'\n{coluna}:')
    print(reclamacoes[coluna].value_counts(dropna=False))

# Um detalhe importante: o traco '-' e usado como "sem informacao" em varias colunas
print('\nRegistros com "-" por coluna:')
print((reclamacoes == '-').sum()[lambda s: s > 0])

# Close Amount veio como texto por causa dos tracos
print('\nTipo de Close Amount:', reclamacoes['Close Amount'].dtype)
print(reclamacoes['Close Amount'].value_counts().head(6))

# Periodo coberto
print('\nRecebidas de', reclamacoes['Date Received'].min().date(), 'a', reclamacoes['Date Received'].max().date())
print('Incidentes de', reclamacoes['Incident D'].min().date(), 'a', reclamacoes['Incident D'].max().date())

# Figura 1: desfechos e locais, em barras ordenadas
fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
desfechos = reclamacoes['Disposition'].replace('-', 'sem desfecho registrado').value_counts().sort_values()
esq.barh(desfechos.index, desfechos.values, color=['#8794A3', '#8794A3', '#8794A3', '#2F648F'])
for i, v in enumerate(desfechos.values):
    esq.text(v + 40, i, str(v), va='center')
esq.set_title('Entre as reclamações com desfecho, 54% foram negadas')
esq.set_xlabel('Reclamações (2015)')
esq.grid(axis='y', visible=False)
locais = reclamacoes['Claim Site'].replace('-', 'sem informação').value_counts().sort_values()
dir.barh(locais.index, locais.values, color='#8794A3')
dir.set_title('A maioria ocorre na bagagem despachada')
dir.set_xlabel('Reclamações (2015)')
dir.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '01_desfechos_e_locais.png'))
plt.show()

# Figura 2: reclamacoes recebidas por mes
por_mes = reclamacoes.groupby(reclamacoes['Date Received'].dt.to_period('M')).size()
fig, eixo = plt.subplots(figsize=(8, 3.6))
eixo.bar(por_mes.index.astype(str), por_mes.values, color='#2F648F')
eixo.set_title('Reclamações recebidas por mês em 2015 (última atualização: fev/2016)')
eixo.set_ylabel('Reclamações')
eixo.tick_params(axis='x', labelrotation=45)
plt.savefig(os.path.join(pasta, 'figuras', '01_reclamacoes_por_mes.png'))
plt.show()

# Perguntas que ficam para as proximas etapas:
# - os desfechos variam com o tipo, o local e a companhia?
# - quanto se paga quando se paga? O valor depende do tipo de item?
# - um modelo ajudaria a priorizar a revisao humana de casos?
