# Tipos de variaveis: a natureza da variavel decide como resumir, visualizar e modelar.
# Dados: dados/alunos_portugues.csv (649 alunos de duas escolas portuguesas, 2005-2006; UCI Student Performance).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
alunos = pd.read_csv(os.path.join(pasta, '..', 'dados', 'alunos_portugues.csv'), sep=';')
print('Alunos:', len(alunos), '| colunas:', alunos.shape[1])

# Quatro tipos, um exemplo de cada nesta base:
# qualitativa nominal  -> 'school' (GP ou MS): categorias sem ordem
# qualitativa ordinal  -> 'studytime' (1: <2h, 2: 2-5h, 3: 5-10h, 4: >10h por semana): categorias COM ordem
# quantitativa discreta -> 'absences' (numero de faltas): contagem
# quantitativa continua -> nesta base as notas G1-G3 (0 a 20) sao inteiras, mas medem algo continuo

# Nominal: tabela de frequencias absolutas e relativas
frequencias = alunos['school'].value_counts()
print('\nNominal (escola): frequencia e %')
print(pd.DataFrame({'f': frequencias, '%': (100 * frequencias / len(alunos)).round(1)}))

# Ordinal: a ordem importa; faz sentido falar em mediana, nao em media
estudo = alunos['studytime'].value_counts().sort_index()
rotulos_estudo = {1: '< 2h', 2: '2–5h', 3: '5–10h', 4: '> 10h'}
print('\nOrdinal (tempo de estudo semanal):')
print(pd.DataFrame({'categoria': estudo.index.map(rotulos_estudo), 'f': estudo.values}))
print('Mediana da categoria:', rotulos_estudo[int(alunos['studytime'].median())])

# Discreta: contagens; histograma com uma barra por valor
print('\nDiscreta (faltas):')
print(alunos['absences'].describe().round(2))

# Continua: histograma com intervalos; media, mediana, quantis
print('\nNota final G3:')
print(alunos['G3'].describe().round(2))

# Transformacao: uma variavel muito assimetrica pode ficar mais legivel em escala logaritmica
faltas_log = np.log1p(alunos['absences'])     # log(1 + x), para lidar com zeros
print(f'\nAssimetria das faltas: {alunos["absences"].skew():.2f} | apos log(1+x): {faltas_log.skew():.2f}')

fig, eixos = plt.subplots(1, 4, figsize=(15, 3.6))
eixos[0].bar(frequencias.index, frequencias.values, color='#2F648F')
eixos[0].set_title('Nominal: escola\n(barras; a ordem não importa)', fontsize=11)
eixos[1].bar([rotulos_estudo[i] for i in estudo.index], estudo.values, color='#2F648F')
eixos[1].set_title('Ordinal: horas de estudo\n(barras na ordem natural)', fontsize=11)
contagem_faltas = alunos['absences'].value_counts().sort_index()
eixos[2].bar(contagem_faltas.index, contagem_faltas.values, color='#2F648F', width=0.8)
eixos[2].set_title('Discreta: faltas\n(uma barra por valor)', fontsize=11)
eixos[3].hist(faltas_log, bins=15, color='#168A8A')
eixos[3].set_title('Faltas em log(1+x)\n(assimetria reduzida)', fontsize=11)
for eixo in eixos:
    eixo.set_ylabel('alunos')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'tipos_de_variaveis.png'))
plt.show()

# Regra pratica:
# nominal  -> frequencias, proporcoes, barras (moda)
# ordinal  -> frequencias na ordem, barras ordenadas, mediana e quantis
# discreta/continua -> media, mediana, quantis, desvio; histograma, boxplot
# Transformar (log, raiz) nao e "maquiar" os dados: e escolher uma escala mais adequada ao fenomeno.
