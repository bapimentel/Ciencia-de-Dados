# Estudo de caso 3 - Vendas em supermercado. Etapa 5: que decisao os dados sustentam?
# Decisao candidata: concentrar equipe e reposicao no horario e nos dias de maior movimento, e testar
# uma acao comercial no horario fraco. Avaliamos o tamanho da concentracao e como medir o efeito.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour
dias = vendas['Data'].nunique()

# Concentracao por hora: participacao de cada hora no faturamento, por filial
por_hora_filial = vendas.pivot_table(index='Hora', columns='Branch', values='Total', aggfunc='sum')
participacao = por_hora_filial / por_hora_filial.sum()
print('Participacao de cada hora no faturamento da filial (%):')
print((100 * participacao).round(1))
hora_pico = participacao.mean(axis=1).idxmax()
hora_fraca = participacao.mean(axis=1).idxmin()
print(f'\nHora de pico (media das filiais): {hora_pico}h ({participacao.mean(axis=1).max():.1%}); '
      f'hora mais fraca: {hora_fraca}h ({participacao.mean(axis=1).min():.1%})')

# Incerteza: com cerca de 90 cupons por hora em 3 meses, a participacao de uma hora oscila bastante.
# Reamostragem simples (bootstrap) para dar uma faixa a participacao do pico.
gerador = np.random.default_rng(0)
amostras = []
for _ in range(500):
    reamostra = vendas.sample(len(vendas), replace=True, random_state=gerador.integers(1e9))
    p = reamostra.groupby('Hora')['Total'].sum()
    amostras.append(p.get(hora_pico, 0) / p.sum())
faixa = np.percentile(amostras, [2.5, 97.5])
print(f'Participacao das {hora_pico}h: {participacao.mean(axis=1).max():.1%}, faixa de 95% por bootstrap: {faixa[0]:.1%} a {faixa[1]:.1%}')
# A faixa e larga: o pico das 19h existe, mas seu tamanho exato e incerto com 3 meses de dados.

fig, eixo = plt.subplots(figsize=(9, 4))
largura = 0.27
for i, (filial, cor) in enumerate(zip(['A', 'B', 'C'], ['#2F648F', '#168A8A', '#8794A3'])):
    eixo.bar(participacao.index + (i - 1) * largura, 100 * participacao[filial], width=largura, color=cor, label=f'filial {filial}')
eixo.set_xticks(participacao.index)
eixo.set_xlabel('Hora')
eixo.set_ylabel('% do faturamento da filial')
eixo.set_title('As três filiais concentram faturamento às 19h; 17h e 20h são as horas mais fracas')
eixo.legend()
plt.savefig(os.path.join(pasta, 'figuras', '05_participacao_por_hora_filial.png'))
plt.show()

print(f'''
Achado: nas tres filiais, as {hora_pico}h concentram a maior fatia do faturamento e as {hora_fraca}h a menor;
sabado tem mais cupons por dia. Linhas de produto, avaliacoes e tipos de cliente sao parecidos entre si.
Isso sugere que o horario importa mais que o mix de produtos para organizar a operacao.
Recomendacao proporcional: (1) escalar caixas e reposicao para o fim da tarde e a noite, sobretudo aos
sabados; (2) testar uma acao comercial nas horas fracas (por exemplo, {hora_fraca}h as {hora_fraca + 1}h) em UMA
filial, mantendo as outras duas como comparacao.
Evidencia: participacao por hora com faixa de incerteza; cupons por dia da semana.
Avaliacao: apos 8 semanas, comparar o faturamento por hora na faixa testada da filial com acao contra as
outras filiais e contra as 8 semanas anteriores (metrica principal); acompanhar o ticket medio e a
avaliacao dos clientes (auxiliares). Sucesso proposto: aumento do faturamento na faixa testada superior a
variacao observada entre semanas nas filiais sem acao.
O que NAO se pode recomendar com esta base: mudanca de precos (script 04), compras de estoque (nao ha
estoque nem ruptura registrados) ou acoes por "perfil de cliente" (a base identifica cupons, nao clientes).
''')
