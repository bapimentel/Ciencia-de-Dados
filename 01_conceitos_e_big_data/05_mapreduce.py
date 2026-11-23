# MapReduce em miniatura: a ideia que permite processar dados que nao cabem em um computador.
# 1) Dividir os dados em blocos; 2) MAP: cada bloco produz resultados parciais, de forma independente;
# 3) REDUCE: juntar os parciais. Aqui os "blocos" sao arquivos lidos aos pedacos, em um so computador,
# mas cada MAP poderia rodar em uma maquina diferente (e o que o Hadoop e o Spark fazem).
# Dados: um arquivo CSV sintetico de 2 milhoes de vendas, gravado na pasta deste script e apagado no fim.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
arquivo = os.path.join(pasta, 'vendas_grandes_temporario.csv')

# Gera o arquivo "grande" (semente fixa)
gerador = np.random.default_rng(1)
n = 2_000_000
pd.DataFrame({
    'loja': gerador.integers(1, 51, size=n),
    'produto': gerador.choice(['pao', 'leite', 'cafe', 'arroz', 'feijao'], size=n),
    'quantidade': gerador.integers(1, 11, size=n),
}).to_csv(arquivo, index=False)
print(f'Arquivo gerado: {os.path.getsize(arquivo) / 1e6:.0f} MB, {n:,} linhas')

# --- MAP: ler em blocos de 250 mil linhas; cada bloco devolve a soma parcial por produto
parciais = []
for numero, bloco in enumerate(pd.read_csv(arquivo, chunksize=250_000)):
    parcial = bloco.groupby('produto')['quantidade'].sum()
    parciais.append(parcial)
    print(f'bloco {numero}: {len(bloco):,} linhas -> parcial {parcial.to_dict()}')

# --- REDUCE: somar os parciais
total_mapreduce = pd.concat(parciais).groupby(level=0).sum()
print('\nResultado MapReduce:')
print(total_mapreduce)

# Conferencia: o mesmo calculo lendo tudo de uma vez (so possivel porque o arquivo ainda cabe na memoria)
total_direto = pd.read_csv(arquivo).groupby('produto')['quantidade'].sum()
print('Igual ao calculo direto?', bool((total_mapreduce == total_direto).all()))

# Nem toda conta "se divide" assim. A soma sim; a media precisa levar a soma E a contagem de cada bloco;
# a mediana nao se obtem a partir de medianas parciais.
medias_parciais = [b['quantidade'].mean() for b in pd.read_csv(arquivo, chunksize=300_000)]
print(f'\nMedia das medias dos blocos (ERRADO se os blocos tem tamanhos diferentes): {np.mean(medias_parciais):.5f}')
somas = 0
contagens = 0
for bloco in pd.read_csv(arquivo, chunksize=300_000):
    somas += bloco['quantidade'].sum()
    contagens += len(bloco)
print(f'Soma total / contagem total (CERTO): {somas / contagens:.5f}')

os.remove(arquivo)

fig, eixo = plt.subplots(figsize=(10, 3.8))
eixo.axis('off')
eixo.set_xlim(0, 10)
eixo.set_ylim(0, 4)
for i in range(4):
    y = 3.2 - i * 0.85
    eixo.text(0.9, y, f'bloco {i + 1}', ha='center', va='center', color='white', fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.4', facecolor='#8794A3', edgecolor='none'))
    eixo.annotate('', xy=(3.0, y), xytext=(1.6, y), arrowprops=dict(arrowstyle='->', color='#20324A'))
    eixo.text(4.1, y, 'MAP: soma\nparcial', ha='center', va='center', color='white', fontsize=9, fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.4', facecolor='#2F648F', edgecolor='none'))
    eixo.annotate('', xy=(6.6, 2.0), xytext=(5.2, y), arrowprops=dict(arrowstyle='->', color='#20324A'))
eixo.text(7.5, 2.0, 'REDUCE:\nsoma dos\nparciais', ha='center', va='center', color='white', fontweight='bold',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#168A8A', edgecolor='none'))
eixo.text(9.4, 2.0, 'total por\nproduto', ha='center', va='center', color='#20324A')
eixo.annotate('', xy=(8.9, 2.0), xytext=(8.4, 2.0), arrowprops=dict(arrowstyle='->', color='#20324A'))
eixo.set_title('MapReduce: cada bloco é resumido sozinho; depois os resumos são combinados')
plt.savefig(os.path.join(pasta, 'figuras', 'mapreduce.png'))
plt.show()
