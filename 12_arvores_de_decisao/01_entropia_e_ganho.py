# Entropia e ganho de informacao: como a arvore escolhe a pergunta de cada no.
# Tabela ilustrativa de 10 dias: ir a praia ou nao, conforme temperatura, vento, nebulosidade e feriado.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

dias = pd.DataFrame({
    'temperatura': ['frio', 'frio', 'frio', 'frio', 'frio', 'quente', 'quente', 'quente', 'quente', 'quente'],
    'vento':       ['forte', 'forte', 'forte', 'forte', 'forte', 'forte', 'fraco', 'fraco', 'fraco', 'forte'],
    'nublado':     ['pouco', 'muito', 'muito', 'muito', 'muito', 'pouco', 'pouco', 'pouco', 'pouco', 'pouco'],
    'feriado':     ['nao', 'nao', 'nao', 'nao', 'nao', 'sim', 'nao', 'sim', 'sim', 'nao'],
    'praia':       ['sim', 'nao', 'nao', 'nao', 'nao', 'nao', 'sim', 'sim', 'sim', 'sim'],
})

# Entropia mede a impureza de um conjunto: 0 se todos tem a mesma classe, 1 (com 2 classes) se metade/metade.
# Entropia(S) = - p+ log2(p+) - p- log2(p-)
def entropia(classes):
    proporcoes = pd.Series(classes).value_counts(normalize=True)
    return float(-(proporcoes * np.log2(proporcoes)).sum())

print('Exemplos de entropia:')
for positivos, negativos in [(5, 5), (2, 1), (3, 4), (4, 0)]:
    print(f'  [{positivos}+; {negativos}-] -> {entropia(["+"] * positivos + ["-"] * negativos):.4f}')

# Ganho(S, A) = Entropia(S) - soma sobre os valores v de A de |S_v|/|S| * Entropia(S_v)
def ganho(tabela, atributo, alvo='praia'):
    total = entropia(tabela[alvo])
    restante = 0.0
    for valor, grupo in tabela.groupby(atributo):
        restante += len(grupo) / len(tabela) * entropia(grupo[alvo])
    return total - restante

print(f'\nEntropia do conjunto inteiro: {entropia(dias["praia"]):.4f}')
ganhos = {}
for atributo in ['temperatura', 'vento', 'nublado', 'feriado']:
    ganhos[atributo] = ganho(dias, atributo)
    partes = ', '.join(f'{v}: {list(g["praia"])}' for v, g in dias.groupby(atributo))
    print(f'Ganho({atributo:11s}) = {ganhos[atributo]:.4f}   [{partes}]')
melhor = max(ganhos, key=ganhos.get)
print(f'Melhor atributo para a raiz: {melhor}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
p = np.linspace(0.001, 0.999, 300)
esq.plot(p, -p * np.log2(p) - (1 - p) * np.log2(1 - p), color='#2F648F', linewidth=2)
for positivos, total, rotulo in [(5, 10, '[5+;5−]'), (2, 3, '[2+;1−]'), (4, 5, '[4+;1−]')]:
    pp = positivos / total
    e = -pp * np.log2(pp) - (1 - pp) * np.log2(1 - pp)
    esq.scatter(pp, e, color='#D69A35', zorder=3)
    esq.text(pp - 0.03, e - 0.02, f'{rotulo} = {e:.2f}', fontsize=9, color='#20324A', ha='right', va='top')
esq.set_xlabel('Proporção de positivos no conjunto')
esq.set_ylabel('Entropia (bits)')
esq.set_title('Entropia: máxima com metade de cada classe', fontsize=11)
serie = pd.Series(ganhos).sort_values()
dir.barh(serie.index, serie.values, color=['#8794A3'] * 3 + ['#2F648F'])
for i, v in enumerate(serie.values):
    dir.text(v + 0.01, i, f'{v:.3f}', va='center')
dir.set_xlabel('Ganho de informação')
dir.set_title(f'"{melhor}" separa melhor: vira a raiz da árvore', fontsize=11)
dir.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'entropia_e_ganho.png'))
plt.show()
