# Figura de referencia: a paleta unica do repositorio e o papel de cada cor.
# Saida: figuras/geradas/paleta.png. Usada em materiais/manual_visual.md.

import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'estilo.mplstyle'))

cores = [
    ('#2F648F', 'Azul', 'série principal, valores observados, grupo em destaque'),
    ('#168A8A', 'Verde-petróleo', 'comparação, alternativa, previsão'),
    ('#D69A35', 'Âmbar', 'destaque de pergunta, ponto crítico, limiar escolhido'),
    ('#BD5B58', 'Vermelho queimado', 'risco, erro, versão que distorce (nunca decorativo)'),
    ('#8794A3', 'Cinza médio', 'contexto, elementos neutros, demais categorias'),
    ('#E6EBF0', 'Cinza muito claro', 'grade, divisórias, séries ao fundo'),
    ('#20324A', 'Azul-marinho escuro', 'títulos, números e texto'),
]

fig, eixo = plt.subplots(figsize=(9, 4.2))
eixo.set_xlim(0, 10)
eixo.set_ylim(0, len(cores))
eixo.axis('off')
for i, (hexa, nome, papel) in enumerate(cores):
    y = len(cores) - 1 - i
    eixo.add_patch(Rectangle((0.2, y + 0.15), 1.4, 0.7, facecolor=hexa, edgecolor='#8794A3', linewidth=0.5))
    eixo.text(1.8, y + 0.5, f'{nome}  {hexa}', va='center', fontsize=11, fontweight='bold', color='#20324A')
    eixo.text(5.0, y + 0.5, papel, va='center', fontsize=10.5, color='#20324A')
eixo.set_title('Paleta única do repositório: a mesma informação recebe sempre a mesma cor')
plt.savefig(os.path.join(pasta, '..', 'geradas', 'paleta.png'))
print('Figura salva em figuras/geradas/paleta.png')
