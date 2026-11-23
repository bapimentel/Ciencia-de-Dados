# Aplicacao adicional - E-commerce. Passo 7: quem cancela vai embora? E a quem a equipe comercial deve ligar?
# (a) Clientes com algum cancelamento deixam de comprar mais ou menos que os outros?
# (b) Lista de retencao: a equipe liga, a cada trimestre, para uma fracao dos clientes. Qual criterio coloca na
#     lista a maior parte da receita dos clientes que vao parar de comprar?
#     Perda esperada = probabilidade de parar de comprar (modelo) x receita dos ultimos 90 dias.
# Construcao no tempo, sem olhar o futuro:
#   treino: o que se sabia em 01/06/2011; alvo = nao comprar de junho a agosto;
#   teste:  o que se sabia em 01/09/2011; alvo = nao comprar de setembro a novembro (periodo que o modelo nao viu).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
faturas = pd.read_csv(os.path.join(pasta, 'dados', 'faturas.csv'), parse_dates=['data']).dropna(subset=['cliente'])
faturas['cliente'] = faturas['cliente'].astype(int)


def montar(referencia, meses=3):
    passado = faturas[faturas['data'] < referencia]
    futuro = faturas[(faturas['data'] >= referencia) & (faturas['data'] < referencia + pd.DateOffset(months=meses))]
    vendas = passado[~passado['cancelamento']]
    t = vendas.groupby('cliente').agg(ultima=('data', 'max'), primeira=('data', 'min'), compras=('InvoiceNo', 'nunique'), valor=('valor', 'sum'))
    t['recencia'] = (referencia - t['ultima']).dt.days
    t['antiguidade'] = (referencia - t['primeira']).dt.days
    t['log_compras'] = np.log1p(t['compras'])
    t['log_valor'] = np.log1p(t['valor'])
    t['receita_90d'] = vendas[vendas['data'] >= referencia - pd.Timedelta(days=90)].groupby('cliente')['valor'].sum().reindex(t.index, fill_value=0)
    t['log_receita_90d'] = np.log1p(t['receita_90d'])
    t['cancelou'] = t.index.isin(passado.loc[passado['cancelamento'], 'cliente']).astype(int)
    t['parou'] = (~t.index.isin(futuro.loc[~futuro['cancelamento'], 'cliente'])).astype(int)
    return t


variaveis = ['recencia', 'antiguidade', 'log_compras', 'log_valor', 'log_receita_90d', 'cancelou']
treino = montar(pd.Timestamp('2011-06-01'))
teste = montar(pd.Timestamp('2011-09-01'))
print(f'Treino: {len(treino)} clientes, {treino["parou"].mean():.0%} pararam | Teste: {len(teste)} clientes, {teste["parou"].mean():.0%} pararam')

# (a) Cancelamento x parar de comprar, nos dois periodos
for nome, t in [('treino (jun-ago)', treino), ('teste (set-nov)', teste)]:
    taxa = t.groupby('cancelou')['parou'].mean()
    print(f'{nome}: pararam {taxa[1]:.0%} dos que cancelaram algo x {taxa[0]:.0%} dos que nunca cancelaram')

# (b) Modelo e listas
modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000)).fit(treino[variaveis], treino['parou'])
prob = modelo.predict_proba(teste[variaveis])[:, 1]
print(f'AUC no periodo de teste: {roc_auc_score(teste["parou"], prob):.3f}')
coef = pd.Series(modelo[-1].coef_[0], index=variaveis).round(2)
print('Coeficientes (variaveis padronizadas):', coef.to_dict())

em_risco = teste.loc[teste['parou'] == 1, 'receita_90d'].sum()
print(f'Receita dos ultimos 90 dias dos clientes que pararam no teste: {em_risco:,.0f} libras ({(teste["parou"] == 1).sum()} clientes)')
gerador = np.random.default_rng(0)
criterios = {'perda esperada (modelo × receita)': prob * teste['receita_90d'].values,
             'maior receita recente': teste['receita_90d'].values,
             'maior probabilidade de parar': prob}
linhas = []
for fracao in [0.05, 0.10, 0.20]:
    k = int(round(fracao * len(teste)))
    for nome, escore in criterios.items():
        lista = teste.iloc[np.argsort(-escore)[:k]]
        coberta = lista.loc[lista['parou'] == 1, 'receita_90d'].sum()
        linhas.append({'lista': f'{fracao:.0%} ({k} clientes)', 'critério': nome, 'clientes que pararam na lista': int(lista['parou'].sum()),
                       'receita em risco coberta': coberta, '% da receita em risco': coberta / em_risco})
    sorteio = [teste.iloc[gerador.choice(len(teste), k, replace=False)] for _ in range(500)]
    cob = np.mean([s.loc[s['parou'] == 1, 'receita_90d'].sum() for s in sorteio])
    linhas.append({'lista': f'{fracao:.0%} ({k} clientes)', 'critério': 'sorteio (média de 500)',
                   'clientes que pararam na lista': np.mean([s['parou'].sum() for s in sorteio]),
                   'receita em risco coberta': cob, '% da receita em risco': cob / em_risco})
tabela = pd.DataFrame(linhas)
pd.set_option('display.width', 200)
print(tabela.round(2).to_string(index=False))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.4))
taxas = pd.DataFrame({'treino (jun–ago)': treino.groupby('cancelou')['parou'].mean(), 'teste (set–nov)': teste.groupby('cancelou')['parou'].mean()})
x = np.arange(2)
esq.bar(x - 0.2, 100 * taxas.loc[0], width=0.4, color='#8794A3', label='nunca cancelaram')
esq.bar(x + 0.2, 100 * taxas.loc[1], width=0.4, color='#2F648F', label='cancelaram algo')
esq.set_xticks(x, taxas.columns)
esq.set_ylabel('% que pararam de comprar no trimestre')
esq.set_title('Quem cancela para de comprar MENOS', fontsize=11)
esq.legend()
cores = {'perda esperada (modelo × receita)': '#2F648F', 'maior receita recente': '#168A8A',
         'maior probabilidade de parar': '#D69A35', 'sorteio (média de 500)': '#8794A3'}
fracoes = tabela['lista'].unique()
for nome, cor in cores.items():
    t = tabela[tabela['critério'] == nome]
    dir.plot(range(len(fracoes)), 100 * t['% da receita em risco'], marker='o', color=cor, label=nome)
dir.set_xticks(range(len(fracoes)), fracoes)
dir.set_xlabel('Tamanho da lista de retenção')
dir.set_ylabel('% da receita em risco coberta')
dir.set_title('Set–nov de 2011 (período que o modelo não viu)', fontsize=11)
dir.legend(fontsize=8.5)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '07_lista_de_retencao.png'))
plt.show()
