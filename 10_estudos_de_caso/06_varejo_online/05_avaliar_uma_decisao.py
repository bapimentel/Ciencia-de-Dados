# Aplicacao adicional - E-commerce. Etapa 5: que decisao os dados sustentam?
# Decisao candidata: tratar cancelamentos como processo operacional concentrado em poucos clientes e produtos,
# em vez de "problema de abandono de carrinho" (que a base nao mede).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

faturas = pd.read_csv(os.path.join(pasta, 'dados', 'faturas.csv'), parse_dates=['data'])
clientes = pd.read_csv(os.path.join(pasta, 'dados', 'clientes.csv'))
segmentos = pd.read_csv(os.path.join(pasta, 'dados', 'segmentos.csv'))
clientes = clientes.merge(segmentos, on='cliente')

vendido = faturas.loc[~faturas['cancelamento'], 'valor'].sum()
cancelado = -faturas.loc[faturas['cancelamento'], 'valor'].sum()
print(f'Valor vendido: {vendido:,.0f} | cancelado: {cancelado:,.0f} ({cancelado / vendido:.1%})')

# Quanto do valor cancelado vem de cada segmento?
por_segmento = clientes.groupby('nome do segmento').agg(clientes=('cliente', 'size'), valor_total=('valor_total', 'sum'),
                                                        valor_cancelado=('valor_cancelado', 'sum'))
por_segmento['cancelado/vendido'] = por_segmento['valor_cancelado'] / por_segmento['valor_total']
por_segmento['parte do cancelado'] = por_segmento['valor_cancelado'] / por_segmento['valor_cancelado'].sum()
print('\nCancelamentos por segmento:')
print(por_segmento.round(3).to_string())

# Os 50 clientes com maior valor cancelado
top = clientes.sort_values('valor_cancelado', ascending=False).head(50)
print(f'\n50 clientes com maior valor cancelado: {top["valor_cancelado"].sum() / clientes["valor_cancelado"].sum():.0%} do valor cancelado '
      f'e {top["valor_total"].sum() / clientes["valor_total"].sum():.0%} do valor vendido')
print('Segmentos desses 50:', top['nome do segmento'].value_counts().to_dict())
# Sao grandes compradores que tambem estornam muito: o cancelamento e parte da relacao comercial (trocas,
# ajustes de pedidos atacadistas), nao desistencia.

# Cenario: se uma conferencia de pedido reduzisse em 20% o valor cancelado desses 50 clientes
reducao = 0.2 * top['valor_cancelado'].sum()
print(f'\nCenario (nao previsao): reduzir em 20% os estornos desses 50 clientes = {reducao:,.0f} libras no ano ({reducao / vendido:.2%} do vendido)')

fig, eixo = plt.subplots(figsize=(8, 4))
ordem = por_segmento.sort_values('parte do cancelado', ascending=True)
eixo.barh(ordem.index, 100 * ordem['parte do cancelado'], color=['#8794A3'] * (len(ordem) - 1) + ['#2F648F'])
for i, (nome, linha) in enumerate(ordem.iterrows()):
    eixo.text(100 * linha['parte do cancelado'] + 1, i, f'{linha["parte do cancelado"]:.0%}  (taxa {linha["cancelado/vendido"]:.1%})', va='center')
eixo.set_xlim(0, 100)
eixo.set_xlabel('% do valor cancelado (clientes identificados)')
eixo.set_title('O valor cancelado vem de quem mais compra; a taxa por segmento varia pouco')
eixo.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '05_cancelado_por_segmento.png'))
plt.show()

print('''
Achado: cerca de 15% das faturas sao cancelamentos, mas eles levam so 4,7% do valor (faturas pequenas,
estornos de um item, mediana de 15 libras); a taxa e estavel ao longo dos meses; 50 clientes (1,2%), em geral
atacadistas recorrentes de alto valor, concentram 80% do valor cancelado.
Isso sugere que o cancelamento e parte da operacao com grandes compradores (ajustes e trocas), e nao um
sinal de desistencia na compra. A base nao registra carrinhos, frete ou motivo; nenhuma conclusao sobre
"abandono" ou "custo de entrega" e possivel.
Recomendacao (hipotese operacional): para os 50 clientes com maior valor estornado, introduzir uma etapa
de confirmacao do pedido antes do faturamento (quantidades e variantes), em vez de campanhas gerais.
Evidencia: concentracao do valor cancelado por cliente e por segmento; tamanho mediano dos cancelamentos.
Avaliacao (proposta): apos 90 dias, comparar a razao valor cancelado / valor vendido desses clientes com os
90 dias anteriores e com os demais clientes recorrentes (metrica principal), acompanhando o tempo entre
pedido e faturamento e a frequencia de compra (auxiliares, para ver se a conferencia atrasa ou afasta).
Sucesso proposto: queda da razao no grupo tratado maior que a variacao observada no grupo de comparacao,
sem queda da frequencia de compra.
Limites: um ano de um varejista; 25% das linhas sem cliente ficam fora da analise por cliente; nao ha
custo nem margem, entao "valor" e receita bruta, nao lucro.
''')
