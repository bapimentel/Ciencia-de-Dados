# Animacao: uma serie temporal montada em etapas (tendencia, + sazonalidade, + ruido)
# e, no fim, as janelas de treino e teste deslizando sobre ela.
# Saidas: animacoes/geradas/serie_componentes.gif e .png. Serie simulada com semente fixa.

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
saida = os.path.join(pasta, '..', 'geradas')

gerador = np.random.default_rng(1)
meses = np.arange(72)                                        # 6 anos mensais
tendencia = 100 + 0.8 * meses
sazonalidade = 15 * np.sin(2 * np.pi * meses / 12)
ruido = gerador.normal(0, 6, size=len(meses))
serie = tendencia + sazonalidade + ruido

fig, eixo = plt.subplots(figsize=(8, 4.5))
eixo.set_xlim(0, 71)
eixo.set_ylim(60, 190)
eixo.set_xlabel('mês')
eixo.set_ylabel('valor')
eixo.set_xticks(range(0, 72, 12))
eixo.set_xticklabels([f'ano {a + 1}' for a in range(6)])
l_tend, = eixo.plot([], [], color='#8794A3', linewidth=2, label='tendência')
l_saz, = eixo.plot([], [], color='#168A8A', linewidth=2, label='tendência + sazonalidade')
l_serie, = eixo.plot([], [], color='#2F648F', linewidth=1.6, label='série observada (+ ruído)')
faixa_treino = eixo.axvspan(0, 0, color='#2F648F', alpha=0.08)
faixa_teste = eixo.axvspan(0, 0, color='#D69A35', alpha=0.25)
texto_janela = eixo.text(0, 0, '', fontsize=9, color='#20324A')
eixo.legend(loc='upper left')
titulo = eixo.set_title('')

cortes = [36, 42, 48, 54, 60]      # inicio de cada janela de teste (12 meses)

def quadro(i):
    if i == 0:
        l_tend.set_data(meses, tendencia)
        titulo.set_text('1. Tendência: o nível sobe devagar')
    elif i == 1:
        l_saz.set_data(meses, tendencia + sazonalidade)
        titulo.set_text('2. + Sazonalidade: o mesmo desenho a cada 12 meses')
    elif i == 2:
        l_serie.set_data(meses, serie)
        titulo.set_text('3. + Ruído: o que de fato se observa')
    else:
        j = i - 3
        corte = cortes[j]
        faixa_treino.set_x(0)
        faixa_treino.set_width(corte)
        faixa_teste.set_x(corte)
        faixa_teste.set_width(12)
        texto_janela.set_position((corte + 0.5, 66))
        texto_janela.set_text('teste')
        titulo.set_text(f'4. Validação: treino até o mês {corte}, teste nos 12 seguintes (janela {j + 1} de {len(cortes)})')
    return [l_tend, l_saz, l_serie, faixa_treino, faixa_teste, titulo]

quadros = [0, 0, 1, 1, 2, 2, 2] + [3 + j for j in range(len(cortes)) for _ in range(2)] + [2 + len(cortes)] * 3
animacao = FuncAnimation(fig, quadro, frames=quadros, interval=900, blit=False)
animacao.save(os.path.join(saida, 'serie_componentes.gif'), writer=PillowWriter(fps=1.2), dpi=80)
plt.savefig(os.path.join(saida, 'serie_componentes.png'))
print('Salvo: animacoes/geradas/serie_componentes.gif e .png')
