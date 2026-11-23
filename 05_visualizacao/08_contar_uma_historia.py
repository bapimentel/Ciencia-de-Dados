# Contar uma historia com dados: a mesma informacao apresentada em uma sequencia de quatro quadros,
# cada um com uma frase-titulo que afirma um achado, ate chegar a uma recomendacao.
# Dados reais: alugueis por hora de bicicletas, Washington D.C., 2012 (UCI Bike Sharing).
# Estrutura: inicio (por que prestar atencao) -> meio (o que os dados mostram) -> fim (o que fazer).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
horas = pd.read_csv(os.path.join(pasta, '..', '18_estudos_de_caso', '04_mobilidade_bicicletas', 'dados', 'hour.csv'))
horas = horas[horas['yr'] == 1]                     # 2012
util = horas[horas['workingday'] == 1].groupby('hr')['cnt'].mean()
fds = horas[horas['workingday'] == 0].groupby('hr')['cnt'].mean()
pico = (util.loc[[7, 8, 9, 17, 18, 19]].sum()) / util.sum()
print(f'Em dias uteis de 2012, 7-9h e 17-19h concentram {pico:.0%} dos alugueis medios por hora')

# Primeiro, o grafico "de relatorio" que costuma aparecer: barras agrupadas, 48 barras, legenda
fig, eixo = plt.subplots(figsize=(10, 3.6))
eixo.bar(util.index - 0.2, util.values, width=0.4, label='working day')
eixo.bar(fds.index + 0.2, fds.values, width=0.4, label='non working day')
eixo.set_title('Bike rentals per hour (2012)')
eixo.legend()
plt.savefig(os.path.join(pasta, 'figuras', 'historia_antes.png'))
plt.show()

# Agora a historia em quatro quadros
fig, eixos = plt.subplots(2, 2, figsize=(13, 8), sharey=True)

# Quadro 1 - inicio: o contexto, so a curva dos dias uteis em cinza
eixo = eixos[0, 0]
eixo.plot(util.index, util.values, color='#8794A3', linewidth=2)
eixo.set_title('1. Em dias úteis, o uso de bicicletas não é uniforme ao longo do dia', fontsize=11)

# Quadro 2 - meio: destacar os picos
eixo = eixos[0, 1]
eixo.plot(util.index, util.values, color='#8794A3', linewidth=2)
for inicio, fim in [(7, 9), (17, 19)]:
    trecho = util.loc[inicio:fim]
    eixo.plot(trecho.index, trecho.values, color='#2F648F', linewidth=3.5)
eixo.text(8, util.loc[8] + 30, 'ida ao trabalho', ha='center', color='#2F648F')
eixo.text(18, util.loc[17] + 30, 'volta', ha='center', color='#2F648F')
eixo.set_title(f'2. Seis horas concentram {pico:.0%} do uso: os deslocamentos ao trabalho', fontsize=11)

# Quadro 3 - meio: o contraste com os fins de semana
eixo = eixos[1, 0]
eixo.plot(util.index, util.values, color='#E6EBF0', linewidth=2)
eixo.plot(fds.index, fds.values, color='#168A8A', linewidth=2.5)
eixo.text(13, fds.loc[13] + 30, 'fins de semana e feriados', ha='center', color='#168A8A')
eixo.set_title('3. Nos fins de semana, um pico só, à tarde: outro tipo de uso', fontsize=11)

# Quadro 4 - fim: o que fazer com isso
eixo = eixos[1, 1]
eixo.plot(util.index, util.values, color='#2F648F', linewidth=2)
eixo.plot(fds.index, fds.values, color='#168A8A', linewidth=1.5)
eixo.axvspan(0.5, 5.5, color='#D69A35', alpha=0.15)
eixo.text(3, 520, 'manutenção\nprogramada', ha='center', color='#D69A35')
eixo.axvspan(5.5, 6.9, color='#2F648F', alpha=0.10)
eixo.axvspan(15.5, 16.9, color='#2F648F', alpha=0.10)
eixo.text(6.2, 690, 'reposição\nantes do pico', ha='center', color='#2F648F', fontsize=9)
eixo.text(14.2, 690, 'reposição\nantes do pico', ha='center', color='#2F648F', fontsize=9)
eixo.set_title('4. Organizar a operação pelas janelas: manutenção de madrugada,\nreposição antes dos picos', fontsize=11)

for eixo in eixos.ravel():
    eixo.set_ylim(0, 800)
    eixo.set_xticks(range(0, 24, 3))
    eixo.set_xlabel('Hora do dia')
for eixo in eixos[:, 0]:
    eixo.set_ylabel('Aluguéis por hora (média, 2012)')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'historia_quatro_quadros.png'))
plt.show()

# A "grande ideia" em uma frase: o sistema e usado principalmente para ir e voltar do trabalho, e a operacao
# deve seguir esse ritmo. Cada quadro acrescenta UMA informacao; o titulo diz qual.
