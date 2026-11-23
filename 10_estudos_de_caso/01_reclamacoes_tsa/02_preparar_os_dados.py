# Estudo de caso 1 - Reclamacoes por perdas (TSA). Etapa 2: preparar os dados (livro, secao 11.2).
# Reproduz as decisoes de leitura.py (material original): remover registros com '-' em Close Amount,
# Claim Type, Claim Site e Airline Name e manter as cinco companhias com mais reclamacoes.
# Cada decisao esta registrada com o numero de linhas que ela remove.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

reclamacoes = pd.read_excel(os.path.join(pasta, 'dados', 'claims-data-2015-as-of-feb-9-2016.xlsx'))
print('Inicio:', len(reclamacoes), 'registros')

# 1) '-' significa ausente: tratar como NaN em toda a tabela
reclamacoes = reclamacoes.replace('-', np.nan)
ausentes_antes = reclamacoes.isna().sum()
print('\nAusentes por coluna:')
print(ausentes_antes[ausentes_antes > 0])

# 2) Nomes de companhia tem espacos sobrando no fim ("Southwest Airlines  ")
reclamacoes['Airline Name'] = reclamacoes['Airline Name'].str.strip()

# 3) Close Amount vira numero
reclamacoes['Close Amount'] = pd.to_numeric(reclamacoes['Close Amount'])

# 4) Sem desfecho (e portanto sem valor) nao da para analisar desfecho nem valor
com_desfecho = reclamacoes.dropna(subset=['Close Amount', 'Disposition'])
print(f'\nSem desfecho registrado: removidos {len(reclamacoes) - len(com_desfecho)}, restam {len(com_desfecho)}')

# 5) Sem tipo, local ou companhia: removidos, como no original
completas = com_desfecho.dropna(subset=['Claim Type', 'Claim Site', 'Airline Name'])
print(f'Sem tipo/local/companhia: removidos {len(com_desfecho) - len(completas)}, restam {len(completas)}')

# 6) Cinco companhias com mais reclamacoes (as mesmas do original)
contagem = completas['Airline Name'].value_counts()
print('\nCompanhias com mais reclamacoes:')
print(contagem.head(8))
cinco = ['Southwest Airlines', 'Delta Air Lines', 'American Airlines', 'UAL', 'USAir']
preparadas = completas[completas['Airline Name'].isin(cinco)].copy()
print(f'\nMantendo as cinco maiores: restam {len(preparadas)} ({100 * len(preparadas) / len(reclamacoes):.0f}% da base)')
# Essa escolha simplifica a comparacao entre companhias, mas limita o alcance das conclusoes
# a essas cinco empresas, que concentram cerca de 2/3 das reclamacoes com informacao completa.

# 7) Variaveis derivadas
preparadas['Dias ate registrar'] = (preparadas['Date Received'] - preparadas['Incident D']).dt.days
preparadas['Negada'] = (preparadas['Disposition'] == 'Deny').astype(int)
preparadas['Mes'] = preparadas['Date Received'].dt.month
print('\nDias entre o incidente e o registro:')
print(preparadas['Dias ate registrar'].describe().round(0))
print('Registros com dias negativos (registro antes do incidente?):', (preparadas['Dias ate registrar'] < 0).sum())

# 8) Categorias de item: 567 valores distintos, muitos combinados com ';'. Agrupamos as raras em 'Outros'.
principais = preparadas['Item Category'].value_counts().head(12).index
preparadas['Item Category (agrupada)'] = preparadas['Item Category'].where(preparadas['Item Category'].isin(principais), 'Outros')
print('\nCategorias de item apos agrupar:')
print(preparadas['Item Category (agrupada)'].value_counts())

preparadas.to_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'), index=False)
print('\nSalvo em dados/reclamacoes_preparadas.csv:', preparadas.shape)

# Figura: quantas linhas cada decisao removeu
etapas = ['base original', 'com desfecho\ne valor', 'com tipo, local\ne companhia', 'cinco maiores\ncompanhias']
tamanhos = [len(reclamacoes), len(com_desfecho), len(completas), len(preparadas)]
fig, eixo = plt.subplots(figsize=(8, 3.6))
eixo.bar(etapas, tamanhos, color=['#8794A3', '#8794A3', '#8794A3', '#2F648F'])
for i, v in enumerate(tamanhos):
    eixo.text(i, v + 80, str(v), ha='center')
eixo.set_ylabel('Registros')
eixo.set_title('Cada filtro remove registros; a análise vale para o que sobra')
plt.savefig(os.path.join(pasta, 'figuras', '02_filtros_aplicados.png'))
plt.show()
