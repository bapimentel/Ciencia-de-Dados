# Figura didatica: uma lista em Python vira tabela e depois grafico de barras.
# Saida: figuras/geradas/lista_para_grafico.png. Dados inventados para o exemplo.

import os
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'estilo.mplstyle'))

dias = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb']
vendas = [40, 38, 45, 50, 70, 90]

fig, eixos = plt.subplots(1, 3, figsize=(12, 3.8), gridspec_kw={'width_ratios': [1.1, 0.8, 1.3]})

# Painel 1: o codigo
eixo = eixos[0]
eixo.axis('off')
codigo = ("dias = ['seg', 'ter', 'qua',\n        'qui', 'sex', 'sáb']\n"
          "vendas = [40, 38, 45, 50, 70, 90]\n\n"
          "for dia, v in zip(dias, vendas):\n    print(dia, v)")
eixo.text(0.02, 0.95, codigo, family='monospace', fontsize=10.5, va='top', color='#20324A',
          bbox=dict(boxstyle='round,pad=0.6', facecolor='#F6F8FA', edgecolor='#E6EBF0'))
eixo.set_title('1. Duas listas em Python')

# Painel 2: a tabela
eixo = eixos[1]
eixo.axis('off')
tabela = eixo.table(cellText=[[d, str(v)] for d, v in zip(dias, vendas)], colLabels=['dia', 'vendas'],
                    loc='center', cellLoc='center', colWidths=[0.4, 0.4])
tabela.auto_set_font_size(False)
tabela.set_fontsize(10.5)
tabela.scale(1, 1.35)
for (linha, coluna), celula in tabela.get_celld().items():
    celula.set_edgecolor('#E6EBF0')
    if linha == 0:
        celula.set_facecolor('#2F648F')
        celula.set_text_props(color='white', fontweight='bold')
eixo.set_title('2. Como tabela')

# Painel 3: o grafico
eixo = eixos[2]
cores = ['#8794A3'] * 5 + ['#2F648F']
eixo.bar(dias, vendas, color=cores)
for i, v in enumerate(vendas):
    eixo.text(i, v + 1.5, str(v), ha='center', color='#20324A')
eixo.set_ylabel('Pães vendidos')
eixo.set_ylim(0, 100)
eixo.set_title('3. Como gráfico: sábado vende mais que o dobro da terça')

plt.tight_layout()
plt.savefig(os.path.join(pasta, '..', 'geradas', 'lista_para_grafico.png'))
print('Figura salva em figuras/geradas/lista_para_grafico.png')
