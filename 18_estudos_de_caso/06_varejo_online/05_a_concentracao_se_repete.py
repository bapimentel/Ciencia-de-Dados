# Aplicacao adicional - E-commerce. Passo 5: os clientes que mais cancelam continuam sendo os que mais cancelam?
# No passo 3, poucos clientes concentram o valor cancelado no ano. Uma acao dirigida a eles so faz sentido se a
# concentracao se repetir no futuro. Teste: identificar os 50 clientes com maior valor cancelado no 1o semestre
# (dez/2010 a mai/2011) e ver quanto eles cancelam no 2o semestre (jun a dez/2011).

import os
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
faturas = pd.read_csv(os.path.join(pasta, 'dados', 'faturas.csv'), parse_dates=['data']).dropna(subset=['cliente'])
faturas['cliente'] = faturas['cliente'].astype(int)
corte = pd.Timestamp('2011-06-01')


def por_cliente(tabela):
    vendido = tabela[~tabela['cancelamento']].groupby('cliente')['valor'].sum()
    cancelado = -tabela[tabela['cancelamento']].groupby('cliente')['valor'].sum()
    return pd.DataFrame({'vendido': vendido, 'cancelado': cancelado}).fillna(0)


s1 = por_cliente(faturas[faturas['data'] < corte])
s2 = por_cliente(faturas[faturas['data'] >= corte])
for nome, s in [('1o semestre', s1), ('2o semestre', s2)]:
    print(f'{nome}: vendido {s["vendido"].sum():,.0f} | cancelado {s["cancelado"].sum():,.0f} '
          f'({s["cancelado"].sum() / s["vendido"].sum():.1%}) | maior cancelamento de um so cliente: '
          f'{s["cancelado"].max():,.0f} ({s["cancelado"].max() / s["cancelado"].sum():.0%} do semestre)')

top_s1 = s1['cancelado'].nlargest(50).index
top_s2 = s2['cancelado'].nlargest(50).index
s2_top = s2.reindex(top_s1).fillna(0)
print(f'\nOs 50 maiores do 1o semestre respondem por {s1.loc[top_s1, "cancelado"].sum() / s1["cancelado"].sum():.0%} do cancelado no 1o semestre')
print(f'No 2o semestre, os MESMOS 50 respondem por {s2_top["cancelado"].sum() / s2["cancelado"].sum():.1%} do cancelado '
      f'e {s2_top["vendido"].sum() / s2["vendido"].sum():.1%} do vendido')
print(f'Quantos dos 50 maiores do 1o semestre tambem estao entre os 50 maiores do 2o: {len(set(top_s1) & set(top_s2))}')
outros = s2.drop(index=top_s1, errors='ignore')
print(f'Razao cancelado/vendido no 2o semestre: os 50 = {s2_top["cancelado"].sum() / s2_top["vendido"].sum():.1%} | '
      f'demais clientes = {outros["cancelado"].sum() / outros["vendido"].sum():.1%}')

# De onde vem, entao, o valor cancelado? As maiores faturas canceladas
maiores = faturas[faturas['cancelamento']].nsmallest(5, 'valor')[['InvoiceNo', 'cliente', 'data', 'itens', 'unidades', 'valor']]
print('\nAs cinco maiores faturas canceladas:')
print(maiores.to_string(index=False))

fig, eixo = plt.subplots(figsize=(8.5, 4))
rotulos = ['% do cancelado\nno 1º semestre', '% do cancelado\nno 2º semestre', '% do vendido\nno 2º semestre']
valores = [100 * s1.loc[top_s1, 'cancelado'].sum() / s1['cancelado'].sum(),
           100 * s2_top['cancelado'].sum() / s2['cancelado'].sum(),
           100 * s2_top['vendido'].sum() / s2['vendido'].sum()]
eixo.bar(rotulos, valores, color=['#2F648F', '#BD5B58', '#8794A3'])
for i, v in enumerate(valores):
    eixo.text(i, v + 1.5, f'{v:.0f}%', ha='center')
eixo.set_ylim(0, 100)
eixo.set_title('Os 50 clientes que mais cancelaram no 1º semestre, vistos no 2º', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '05_a_concentracao_se_repete.png'))
plt.show()
