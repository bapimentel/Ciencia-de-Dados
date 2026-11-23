# Volume: o que muda quando os dados crescem?
# Geramos tabelas de vendas sinteticas (semente fixa) de tamanhos crescentes e medimos
# (1) memoria ocupada, (2) tempo de uma agregacao, (3) o efeito de escolher bem os tipos de dados.
# Dados sinteticos: o objetivo e observar o comportamento do computador, nao tirar conclusoes de negocio.

import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
gerador = np.random.default_rng(0)
produtos = np.array(['pao', 'leite', 'cafe', 'arroz', 'feijao', 'sabao', 'fruta', 'carne'])


def gerar_vendas(n):
    return pd.DataFrame({
        'loja': gerador.integers(1, 51, size=n),                  # 50 lojas
        'produto': gerador.choice(produtos, size=n),
        'quantidade': gerador.integers(1, 11, size=n),
        'preco': gerador.uniform(1, 50, size=n).round(2),
    })


tamanhos = [10_000, 100_000, 1_000_000, 3_000_000]
memoria_mb = []
tempo_s = []
for n in tamanhos:
    tabela = gerar_vendas(n)
    memoria_mb.append(tabela.memory_usage(deep=True).sum() / 1e6)
    inicio = time.perf_counter()
    tabela.groupby(['loja', 'produto'])['quantidade'].sum()
    tempo_s.append(time.perf_counter() - inicio)
    print(f'{n:>9,} linhas: {memoria_mb[-1]:7.1f} MB, agregacao em {tempo_s[-1]:.3f} s')

# A memoria cresce na proporcao das linhas. Em algum ponto a tabela nao cabe mais na memoria
# de um computador: e ai que entram processamento em blocos (script 05) e sistemas distribuidos.

# Tipos de dados importam: a mesma tabela com tipos menores
grande = gerar_vendas(1_000_000)
antes = grande.memory_usage(deep=True)
enxuta = grande.astype({'loja': 'int8', 'produto': 'category', 'quantidade': 'int8', 'preco': 'float32'})
depois = enxuta.memory_usage(deep=True)
comparacao = pd.DataFrame({'tipos padrão (MB)': antes / 1e6, 'tipos escolhidos (MB)': depois / 1e6}).drop('Index')
print('\nMemoria por coluna, 1 milhao de linhas:')
print(comparacao.round(1))
print(f'Total: {antes.sum() / 1e6:.1f} MB -> {depois.sum() / 1e6:.1f} MB')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 4))
esq.plot(tamanhos, memoria_mb, marker='o', color='#2F648F')
esq.set_xscale('log')
esq.set_yscale('log')
esq.set_xlabel('Linhas (escala log)')
esq.set_ylabel('Memória (MB, escala log)')
esq.set_title('Memória cresce na mesma proporção que as linhas')
x = np.arange(len(comparacao))
esq_largura = 0.38
dir.bar(x - esq_largura / 2, comparacao['tipos padrão (MB)'], width=esq_largura, color='#8794A3', label='tipos padrão')
dir.bar(x + esq_largura / 2, comparacao['tipos escolhidos (MB)'], width=esq_largura, color='#2F648F', label='tipos escolhidos')
dir.set_xticks(x)
dir.set_xticklabels(comparacao.index)
dir.set_ylabel('MB (1 milhão de linhas)')
dir.set_title('Texto repetido vira "category" e cai muito')
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'volume.png'))
plt.show()
