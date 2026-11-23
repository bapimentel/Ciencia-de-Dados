# Como escalas, ordenacao e agregacao mudam a leitura de um grafico sem mudar os dados.
# Dados reais: dados/supermercado.csv.

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

# Avaliacao media por linha de produto: todas entre 6,8 e 7,1
avaliacao = dados.groupby('Product line')['Rating'].mean().sort_values()
print(avaliacao.round(2))

fig, eixos = plt.subplots(2, 2, figsize=(11, 7.5))

# 1. Barras sem base zero: a diferenca de 0,3 ponto parece enorme
eixo = eixos[0, 0]
eixo.bar(range(6), avaliacao.values, color='#BD5B58')
eixo.set_ylim(6.7, 7.15)
eixo.set_xticks(range(6))
eixo.set_xticklabels([p.split()[0] for p in avaliacao.index], rotation=0)
eixo.set_title('Eixo cortado em 6,7: "Food" parece avaliado muito melhor')

# 2. Mesmas barras com base zero: a diferenca real e pequena
eixo = eixos[0, 1]
eixo.bar(range(6), avaliacao.values, color='#2F648F')
eixo.set_ylim(0, 10)
eixo.set_xticks(range(6))
eixo.set_xticklabels([p.split()[0] for p in avaliacao.index])
eixo.set_title('Base zero (escala de 0 a 10): as notas são quase iguais')

# 3. Dois eixos y: qualquer par de series pode parecer "andar junto"
vendas_dia = dados.assign(Data=pd.to_datetime(dados['Date'], format='%m/%d/%Y')).groupby('Data')
total_dia = vendas_dia['Total'].sum()
nota_dia = vendas_dia['Rating'].mean()
eixo = eixos[1, 0]
eixo.plot(total_dia.index, total_dia.values, color='#2F648F', linewidth=1)
eixo.set_ylabel('Faturamento do dia', color='#2F648F')
eixo2 = eixo.twinx()
eixo2.plot(nota_dia.index, nota_dia.values, color='#BD5B58', linewidth=1)
eixo2.set_ylabel('Avaliação média do dia', color='#BD5B58')
eixo2.set_ylim(5, 9)
eixo2.grid(False)
eixo.set_title(f'Dois eixos y sugerem relação; a correlação é {total_dia.corr(nota_dia):.2f}')
eixo.tick_params(axis='x', labelrotation=30)

# 4. Ordenacao: alfabetica obriga a procurar; por valor, a resposta salta
por_produto = dados.groupby('Product line')['Total'].sum()
eixo = eixos[1, 1]
ordenado = por_produto.sort_values()
eixo.barh(range(6), ordenado.values, color=['#8794A3'] * 5 + ['#2F648F'])
eixo.set_yticks(range(6))
eixo.set_yticklabels(ordenado.index)
eixo.set_xlabel('Faturamento total')
eixo.set_title('Ordenar por valor e destacar uma barra responde "qual é a maior?"')

plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'escalas_que_enganam.png'))
plt.show()

# Regras que este script ilustra:
# - barras comecam em zero; cortar o eixo exagera diferencas;
# - dois eixos y permitem "encaixar" qualquer coisa em qualquer coisa; prefira dois paineis ou dispersao;
# - a ordem das categorias deve servir a pergunta, nao ao alfabeto.

# Experimente: refaca o painel 3 como um grafico de dispersao (faturamento x avaliacao por dia).
