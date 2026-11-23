# Estudo de caso 1 - Reclamacoes por perdas (TSA). Passo 2: preparar os dados.
# Cada decisao de limpeza e registrada com o numero de linhas que ela remove, para que o leitor saiba
# a que recorte as conclusoes se aplicam. Saida: dados/reclamacoes_preparadas.csv.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

reclamacoes = pd.read_excel(os.path.join(pasta, 'dados', 'claims-data-2015-as-of-feb-9-2016.xlsx'))
inicio = len(reclamacoes)
print('Inicio:', inicio, 'registros')

# 1) '-' significa ausente: tratar como NaN em toda a tabela
reclamacoes = reclamacoes.replace('-', np.nan)

# 2) Nomes de companhia tem espacos sobrando no fim ("Southwest Airlines  ")
reclamacoes['Airline Name'] = reclamacoes['Airline Name'].str.strip()

# 3) Close Amount vira numero
reclamacoes['Close Amount'] = pd.to_numeric(reclamacoes['Close Amount'])

# 4) Sem desfecho nao da para estudar desfecho nem valor
com_desfecho = reclamacoes.dropna(subset=['Close Amount', 'Disposition'])
print(f'Sem desfecho registrado: removidos {inicio - len(com_desfecho)}, restam {len(com_desfecho)}')

# 5) Sem tipo, local ou companhia: nao entram nas comparacoes por grupo
completas = com_desfecho.dropna(subset=['Claim Type', 'Claim Site', 'Airline Name'])
print(f'Sem tipo/local/companhia: removidos {len(com_desfecho) - len(completas)}, restam {len(completas)}')

# 6) Companhias: ha dezenas, a maioria com poucas reclamacoes. Para comparar companhias com amostras
#    grandes, ficamos com as cinco maiores e registramos quanto elas representam.
contagem = completas['Airline Name'].value_counts()
print('\nCompanhias com mais reclamacoes (casos completos):')
print(contagem.head(8).to_string())
cinco = contagem.head(5).index.tolist()
preparadas = completas[completas['Airline Name'].isin(cinco)].copy()
print(f'As cinco maiores ({", ".join(cinco)}) somam {len(preparadas)} casos: '
      f'{len(preparadas) / len(completas):.0%} dos completos e {len(preparadas) / inicio:.0%} da base')

# 7) Variaveis derivadas, todas conhecidas no momento do registro (exceto o desfecho e o valor)
preparadas['Dias ate registrar'] = (preparadas['Date Received'] - preparadas['Incident D']).dt.days
preparadas['Negada'] = (preparadas['Disposition'] == 'Deny').astype(int)
preparadas['Mes'] = preparadas['Date Received'].dt.month
print('\nDias entre o incidente e o registro:')
print(preparadas['Dias ate registrar'].describe().round(0).to_string())
print('Registros com dias negativos:', (preparadas['Dias ate registrar'] < 0).sum())

# 8) Categoria do item: centenas de valores, muitos combinados com ';'. As 12 mais comuns ficam; o resto vira 'Outros'.
print('\nCategorias de item distintas:', preparadas['Item Category'].nunique())
principais = preparadas['Item Category'].value_counts().head(12).index
preparadas['Item Category (agrupada)'] = preparadas['Item Category'].where(preparadas['Item Category'].isin(principais), 'Outros')
print(preparadas['Item Category (agrupada)'].value_counts().to_string())

preparadas.to_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'), index=False)
print('\nSalvo em dados/reclamacoes_preparadas.csv:', preparadas.shape)

etapas = ['base inteira', 'com desfecho\ne valor', 'com tipo, local\ne companhia', 'cinco maiores\ncompanhias']
tamanhos = [inicio, len(com_desfecho), len(completas), len(preparadas)]
fig, eixo = plt.subplots(figsize=(8, 3.6))
eixo.bar(etapas, tamanhos, color=['#8794A3', '#8794A3', '#8794A3', '#2F648F'])
for i, v in enumerate(tamanhos):
    eixo.text(i, v + 80, f'{v} ({v / inicio:.0%})', ha='center')
eixo.set_ylabel('Registros')
eixo.set_title('Cada filtro remove registros; as conclusões valem para o que sobra')
plt.savefig(os.path.join(pasta, 'figuras', '02_filtros_aplicados.png'))
plt.show()
