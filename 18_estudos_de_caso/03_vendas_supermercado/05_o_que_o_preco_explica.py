# Estudo de caso 3 - Vendas em supermercado. Passo 5: aumentar o preco aumentaria o faturamento?
# Um experimento comum: treinar, para cada perfil, uma floresta que preve o Total a partir de filial, cidade,
# tipo de cliente, genero, produto, avaliacao e preco; depois aumentar o preco em p% e observar a mediana
# dos totais previstos subir. Reproduzimos o experimento e mostramos por que ele nao responde a pergunta
# "aumentar o preco aumenta o faturamento?": como Total = preco x quantidade x 1,05, o modelo so pode
# repetir essa conta, e a base nao informa como a quantidade reagiria a um preco diferente.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from scipy.stats import wilcoxon

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

vendas = pd.read_csv(os.path.join(pasta, 'dados', 'supermarket_sales - Sheet1.csv'))
perfis = pd.read_csv(os.path.join(pasta, 'dados', 'perfis.csv'))
vendas = vendas.merge(perfis, on='Invoice ID')

# --- 1. O experimento, por perfil
variaveis = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Rating', 'Unit price']
for perfil in sorted(vendas['Perfil'].unique()):
    grupo = vendas[vendas['Perfil'] == perfil]
    X = pd.get_dummies(grupo[variaveis], dtype=int)
    y = grupo['Total']
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)
    modelo = RandomForestRegressor(n_estimators=200, random_state=42).fit(X_tr, y_tr)
    previsto = modelo.predict(X_te)
    print(f'\nPerfil {perfil} ({len(grupo)} cupons): MAE {mean_absolute_error(y_te, previsto):.1f} | R2 {r2_score(y_te, previsto):.2f}')
    X_mais10 = X_te.copy()
    X_mais10['Unit price'] = X_mais10['Unit price'] * 1.10
    previsto_mais10 = modelo.predict(X_mais10)
    _, p = wilcoxon(previsto, previsto_mais10)
    print(f'  mediana prevista: {np.median(previsto):.1f} -> {np.median(previsto_mais10):.1f} com preco +10% (Wilcoxon p={p:.4f})')
# As medianas sobem e o teste da p pequeno. Mas o que foi testado? Que o modelo, ao ver um preco 10% maior
# com a MESMA quantidade implicita, preve um total maior. Isso e a formula do total, nao o comportamento do cliente.

# --- 2. O que a base diz sobre a reacao da quantidade ao preco
r = vendas['Unit price'].corr(vendas['Quantity'])
print(f'\nCorrelacao preco unitario x quantidade: {r:.3f}')
faixas = pd.qcut(vendas['Unit price'], 5)
print(vendas.groupby(faixas, observed=True)['Quantity'].agg(['count', 'mean']).round(2))
# A quantidade media e a mesma em todas as faixas de preco. Nesta base, cada cupom e um produto
# diferente com um preco diferente: nao ha o mesmo produto vendido a precos diferentes ao longo do tempo,
# que e o que permitiria estimar elasticidade.

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
esq.scatter(vendas['Unit price'], vendas['Quantity'], s=10, alpha=0.4, color='#2F648F')
esq.set_xlabel('Preço unitário')
esq.set_ylabel('Quantidade no cupom')
esq.set_title(f'Preço e quantidade não se relacionam (r = {r:.2f})')
medias = vendas.groupby(faixas, observed=True)['Quantity'].mean()
dir.bar(range(5), medias.values, color='#8794A3')
dir.set_xticks(range(5))
dir.set_xticklabels([f'{int(i.left)}–{int(i.right)}' for i in medias.index])
dir.set_xlabel('Faixa de preço unitário')
dir.set_ylabel('Quantidade média')
dir.set_ylim(0, 8)
dir.set_title('Quantidade média por faixa de preço: plana')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '05_preco_x_quantidade.png'))
plt.show()

print('''
Conclusao deste passo: a base nao permite afirmar que aumentar precos aumenta o faturamento. O modelo
reproduz a identidade Total = preco x quantidade x 1,05; a quantidade nao varia com o preco porque cada
cupom e um item diferente. Para responder a pergunta seria preciso um experimento de precos (o mesmo
produto, precos diferentes, periodos ou lojas comparaveis) ou um historico de precos do mesmo item.
O que a base sustenta esta nos passos 3 e 6.
''')
