# Barras ou pizza? Que pergunta cada um responde.
# Reescreve os exemplos "Grafico de barras" e "Grafico de pizza" de estatistica.py (2019)
# e aplica o mesmo raciocinio a dados reais (formas de pagamento no supermercado).

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Exemplo original: valores em dinheiro, com formatador no eixo
nomes = ['Bill', 'Fred', 'Mary', 'Sue']
dinheiro = [1.5e5, 2.5e6, 5.5e6, 2.0e7]

def milhoes(x, pos):
    return f'${x * 1e-6:.1f}M'

fig, eixo = plt.subplots(figsize=(6, 3.6))
eixo.bar(nomes, dinheiro, color='#2F648F')
eixo.yaxis.set_major_formatter(FuncFormatter(milhoes))
eixo.set_title('Barras: comparar valores entre categorias')
eixo.set_ylabel('Valor')
plt.savefig(os.path.join(pasta, 'figuras', 'barras_dinheiro.png'))
plt.show()

# --- Exemplo original de pizza, lado a lado com a versao em barras
rotulos = ['Frogs', 'Hogs', 'Dogs', 'Logs']
tamanhos = [15, 30, 45, 10]

fig, (esq, dir) = plt.subplots(1, 2, figsize=(9, 3.8))
esq.pie(tamanhos, labels=rotulos, autopct='%1.0f%%', startangle=90,
        colors=['#2F648F', '#168A8A', '#D69A35', '#8794A3'])
esq.set_title('Pizza: qual fatia é maior, Frogs ou Logs?')
esq.axis('equal')

serie = pd.Series(tamanhos, index=rotulos).sort_values()
dir.barh(serie.index, serie.values, color='#2F648F')
for i, v in enumerate(serie.values):
    dir.text(v + 0.5, i, f'{v}%', va='center')
dir.set_title('Barras ordenadas: a comparação é imediata')
dir.set_xlabel('% do total')
dir.set_xlim(0, 55)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'pizza_vs_barras.png'))
plt.show()

# --- Dados reais: participacao das formas de pagamento
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
pagamentos = dados['Payment'].value_counts()
print(pagamentos)
percentual = (100 * pagamentos / pagamentos.sum()).round(1)
print(percentual)

fig, eixo = plt.subplots(figsize=(6, 3.2))
eixo.barh(percentual.index[::-1], percentual.values[::-1], color='#2F648F')
for i, v in enumerate(percentual.values[::-1]):
    eixo.text(v + 0.5, i, f'{v}%', va='center')
eixo.set_xlim(0, 45)
eixo.set_xlabel('% das 1000 vendas')
eixo.set_title('As três formas de pagamento têm participação parecida')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'pagamentos.png'))
plt.show()

# Com tres fatias de 31% a 35%, uma pizza nao deixaria ver qual e maior.
# Em barras, a diferenca de 3 pontos aparece, e o titulo ja diz que ela e pequena.

# Experimente: faca o mesmo para 'Product line' (6 categorias). Ordene as barras.
