# Antes e depois: o mesmo grafico, os mesmos dados, duas formas de comunicar.
# "Antes" usa escolhas muito comuns (e problematicas): barras verticais, uma cor por barra em paleta
# viridis, rotulos inclinados, titulo generico.
# "Depois" aplica as regras do manual visual (materiais/manual_visual.md).

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

mediana = dados.groupby('Product line')['Rating'].median()
print(mediana)
contagem = dados['Product line'].value_counts()

# ---------- ANTES: estilo padrao do matplotlib, paleta decorativa ----------
plt.style.use('default')
cores_viridis = plt.cm.viridis([i / 5 for i in range(6)])
fig, eixo = plt.subplots(figsize=(8, 4.5))
eixo.bar(mediana.index, mediana.values, color=cores_viridis)
eixo.set_title('Mediana do Rating por Produto')
eixo.set_xlabel('Produto')
eixo.set_ylabel('Mediana do Rating')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'antes_rating_por_produto.png'), dpi=150)
plt.show()

# Problemas: a cor varia sem significado (seis cores para seis barras iguais em natureza);
# os rotulos inclinados exigem virar a cabeca; o titulo repete o eixo em vez de dizer o achado;
# nao ha indicacao de quantas vendas sustentam cada mediana.

# ---------- DEPOIS: estilo do repositorio ----------
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
ordenada = mediana.sort_values()
cores = ['#8794A3'] * len(ordenada)
cores[-1] = '#2F648F'                       # so a maior recebe a cor principal
rotulos = [f'{nome}  (n={contagem[nome]})' for nome in ordenada.index]

fig, eixo = plt.subplots(figsize=(8, 4))
eixo.barh(rotulos, ordenada.values, color=cores)
for i, valor in enumerate(ordenada.values):
    eixo.text(valor + 0.08, i, f'{valor:.1f}', va='center', color='#20324A')
eixo.set_xlim(0, 10)
eixo.set_xlabel('Mediana da avaliação dos clientes (escala de 4 a 10)')
eixo.set_title('Avaliação mediana por linha de produto: de 6,7 a 7,3, uma faixa estreita')
eixo.grid(axis='y', visible=False)
eixo.grid(axis='x', color='#E6EBF0')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'depois_rating_por_produto.png'))
plt.show()

# O que mudou e por que:
# - barras horizontais: nomes longos ficam legiveis sem rotacao;
# - ordenacao por valor: a pergunta "qual e a maior?" se responde no primeiro olhar;
# - uma cor para o destaque, cinza para o contexto (atributo pre-atentivo: cor);
# - titulo afirma o achado (a faixa e estreita) em vez de repetir o nome do eixo;
# - base zero e escala ate 10 mostram que 0,6 ponto e pouco em uma escala de 10;
# - n por grupo informa quantas vendas sustentam cada mediana.
# Os numeros sao exatamente os mesmos nas duas figuras.
