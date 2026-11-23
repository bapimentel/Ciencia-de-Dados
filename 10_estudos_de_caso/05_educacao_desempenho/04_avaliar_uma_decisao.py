# Aplicacao adicional - Educacao. Etapa 4: que decisao os dados sustentam?
# Decisao candidata: montar, apos o 1o periodo, uma lista de acompanhamento preventivo. Quantos alunos
# entrariam, quantos reprovados seriam alcancados e como medir o efeito, sem rotular ninguem.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
probs = pd.read_csv(os.path.join(pasta, 'dados', 'probabilidades_validacao.csv'))
n = len(probs)
reprovados = probs['risco'].sum()

# Se a escola acompanhar os X% de maior probabilidade, que fracao dos reprovados estaria na lista?
linhas = []
for fracao in [0.10, 0.15, 0.20, 0.25, 0.30, 0.40]:
    k = int(round(fracao * n))
    for momento in ['prob_inicio', 'prob_periodo']:
        lista = probs.nlargest(k, momento)
        linhas.append({'momento': 'início do ano' if momento == 'prob_inicio' else 'após 1º período',
                       'fração acompanhada': f'{fracao:.0%}', 'alunos na lista': k,
                       'reprovados alcançados': int(lista['risco'].sum()),
                       '% dos reprovados': lista['risco'].sum() / reprovados,
                       'alunos acompanhados sem necessidade': int(k - lista['risco'].sum())})
tabela = pd.DataFrame(linhas)
print(tabela.to_string(index=False, float_format=lambda v: f'{v:.0%}'))

# Regra simples para comparar: acompanhar quem tem reprovacao anterior OU G1 < 10
alunos = pd.read_csv(os.path.join(pasta, 'dados', 'student-por.csv'), sep=';')
regra = (alunos['failures'] > 0) | (alunos['G1'] < 10)
print(f'\nRegra simples (reprovou antes ou G1 < 10): {regra.sum()} alunos ({regra.mean():.0%}), '
      f'alcanca {int(((alunos["G3"] < 10) & regra).sum())} de {reprovados} reprovados ({((alunos["G3"] < 10) & regra).sum() / reprovados:.0%})')
# Uma regra transparente alcanca quase o mesmo que o modelo. Para a escola, isso pesa: e explicavel.

fig, eixo = plt.subplots(figsize=(7, 4.2))
for momento, cor in [('início do ano', '#2F648F'), ('após 1º período', '#168A8A')]:
    sub = tabela[tabela['momento'] == momento]
    eixo.plot([float(f.strip('%')) for f in sub['fração acompanhada']], 100 * sub['% dos reprovados'], marker='o', color=cor, label=momento)
eixo.plot([10, 40], [10, 40], linestyle='--', color='#8794A3', label='lista aleatória')
eixo.scatter([100 * regra.mean()], [100 * ((alunos['G3'] < 10) & regra).sum() / reprovados], color='#D69A35', s=80, zorder=5, label='regra simples')
eixo.set_xlabel('% dos alunos na lista de acompanhamento')
eixo.set_ylabel('% dos reprovados alcançados')
eixo.set_title('Após o 1º período, acompanhar 20% dos alunos alcança a maioria dos reprovados')
eixo.legend(loc='lower right')
plt.savefig(os.path.join(pasta, 'figuras', '04_lista_de_acompanhamento.png'))
plt.show()

print('''
Achado: reprovacoes anteriores, intencao de nao seguir para o ensino superior e, apos o 1o periodo, a nota G1
sao as variaveis mais associadas a reprovacao; faltas pesam menos do que se costuma supor nesta base.
Isso sugere que um acompanhamento preventivo pode ser iniciado cedo, com uma lista curta.
Recomendacao (hipotese): apos o 1o periodo, acompanhar os alunos com reprovacao anterior ou G1 < 10
(regra transparente), com contato ativo e reforco; a lista e um convite ao apoio, nao um rotulo. O modelo
estatistico nao supera a regra o bastante para justificar a perda de transparencia.
Evidencia: probabilidades fora da amostra (validacao cruzada); cobertura dos reprovados por tamanho de lista.
Avaliacao (proposta): ao fim do ano seguinte, comparar a taxa de reprovacao dos alunos da lista com a dos
alunos de perfil semelhante em anos anteriores (metrica principal), acompanhando frequencia e evolucao de
G1 para G3 (auxiliares). Sucesso proposto: taxa de reprovacao da lista menor que a historica do mesmo perfil.
Sem grupo de comparacao, uma queda pode ser so o ano mais facil.
Limites eticos e de alcance: duas escolas portuguesas em 2005-2006; nada aqui descreve o Brasil. Nenhum
aluno deve ser tratado de forma diferente pelo modelo sem revisao humana; a lista nao pode ser divulgada
nem usada para selecionar quem fica. Apoio escolar aparece associado a nota baixa porque e dado a quem
precisa: o modelo nao mede efeito de intervencoes.
''')
