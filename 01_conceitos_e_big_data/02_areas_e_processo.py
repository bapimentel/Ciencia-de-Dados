# Duas figuras de referencia para o curso:
# (1) Ciencia de Dados como integracao de areas; (2) o processo, da pergunta a avaliacao da decisao.
# Saidas: figuras/areas_da_ciencia_de_dados.png e figuras/processo.png

import os
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- 1. Tres areas que se sobrepoem
fig, eixo = plt.subplots(figsize=(7, 6))
eixo.set_xlim(0, 10)
eixo.set_ylim(0, 9.5)
eixo.axis('off')
eixo.set_aspect('equal')
circulos = [((3.6, 5.6), '#2F648F', 'Estatística', (1.6, 7.6),
             'inferência, incerteza,\nmodelagem, avaliação'),
            ((6.4, 5.6), '#168A8A', 'Computação', (8.4, 7.6),
             'algoritmos, bancos de dados,\nprocessamento em escala'),
            ((5.0, 3.2), '#D69A35', 'Domínio do problema', (5.0, 0.4),
             'o que medir, como interpretar,\nque decisão tomar')]
for centro, cor, nome, pos_texto, detalhe in circulos:
    eixo.add_patch(Circle(centro, 2.6, facecolor=cor, alpha=0.22, edgecolor=cor, linewidth=2))
    eixo.text(*pos_texto, nome, ha='center', va='center', fontsize=13, fontweight='bold', color=cor)
    deslocamento = -0.75 if nome != 'Domínio do problema' else 0.55
    eixo.text(pos_texto[0], pos_texto[1] + deslocamento, detalhe, ha='center', va='center', fontsize=9, color='#20324A')
eixo.text(5.0, 4.85, 'Ciência\nde Dados', ha='center', va='center', fontsize=13, fontweight='bold', color='#20324A')
eixo.text(2.75, 3.4, 'análise\ntradicional', ha='center', fontsize=8.5, color='#20324A')
eixo.text(7.25, 3.4, 'software sem\nrigor estatístico', ha='center', fontsize=8.5, color='#20324A')
eixo.text(5.0, 7.2, 'aprendizagem\nde máquina', ha='center', fontsize=8.5, color='#20324A')
eixo.set_title('Ciência de Dados está onde as três áreas se encontram')
plt.savefig(os.path.join(pasta, 'figuras', 'areas_da_ciencia_de_dados.png'))
plt.show()

# --- 2. O processo: etapas em sequencia e a volta da avaliacao para a pergunta
etapas = ['Pergunta e\ndecisão', 'Dados e\nalcance', 'Preparação', 'Exploração e\nestatística',
          'Modelagem\n(se ajudar)', 'Recomen-\ndação', 'Avaliação\ndepois']
unidades = ['unidades 01, 19', 'unidade 03', 'unidade 06', 'unidades 04, 05', 'unidades 07 a 17', 'unidades 18, 19', 'unidades 18, 19']
fig, eixo = plt.subplots(figsize=(12, 3.6))
eixo.set_xlim(0, 14)
eixo.set_ylim(0.3, 4.3)
eixo.axis('off')
for i, (etapa, unidade) in enumerate(zip(etapas, unidades)):
    x = 0.2 + i * 1.95
    cor = '#D69A35' if i in (0, 6) else '#2F648F'
    eixo.add_patch(FancyBboxPatch((x, 1.6), 1.6, 1.3, boxstyle='round,pad=0.05', facecolor=cor, edgecolor='none'))
    eixo.text(x + 0.8, 2.25, etapa, ha='center', va='center', color='white', fontsize=9.5, fontweight='bold')
    eixo.text(x + 0.8, 1.3, unidade, ha='center', va='center', color='#8794A3', fontsize=8)
    if i < len(etapas) - 1:
        eixo.annotate('', xy=(x + 1.92, 2.25), xytext=(x + 1.65, 2.25), arrowprops=dict(arrowstyle='->', color='#20324A'))
eixo.annotate('', xy=(1.0, 3.0), xytext=(12.9, 3.0),
              arrowprops=dict(arrowstyle='->', color='#D69A35', connectionstyle='arc3,rad=0.12', linewidth=1.8))
eixo.text(7.0, 0.65, 'A seta âmbar: o resultado da avaliação gera a próxima pergunta.', ha='center', color='#D69A35', fontsize=10)
eixo.set_title('O processo de Ciência de Dados não termina no modelo: termina na decisão avaliada')
plt.savefig(os.path.join(pasta, 'figuras', 'processo.png'))
plt.show()
