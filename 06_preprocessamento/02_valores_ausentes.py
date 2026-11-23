# Valores ausentes: descartar, preencher com media ou mediana, e o que isso faz com as conclusoes.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Exemplo 1: preencher Age e Income com a media
clientes = pd.read_csv(os.path.join(pasta, '..', 'dados', 'Data.csv'))
print(clientes.isna().sum())

imputador = SimpleImputer(missing_values=np.nan, strategy='mean')
numericas = clientes[['Age', 'Income']]
preenchido = pd.DataFrame(imputador.fit_transform(numericas), columns=['Age', 'Income'])
print(preenchido.round(1))
print('Medias usadas:', imputador.statistics_.round(1))

# A mediana resiste melhor a valores extremos
imputador_mediana = SimpleImputer(strategy='median')
print('Medianas usadas:', imputador_mediana.fit(numericas).statistics_)

# Seis estrategias para ausentes, da mais simples a mais elaborada:
# 1) ignorar a linha (dropna); 2) preencher a mao (bases pequenas, com especialista);
# 3) valor global ('desconhecido', -1): cria um padrao novo; 4) media ou mediana;
# 5) media ou mediana POR CLASSE; 6) valor mais provavel, estimado por um modelo (regressao, arvore).
# Exemplo da estrategia 5: a renda ausente e preenchida com a mediana do grupo do cliente
por_classe = clientes.copy()
por_classe['Income'] = por_classe.groupby('Online Shopper')['Income'].transform(lambda g: g.fillna(g.median()))
print('\nRenda preenchida pela mediana de cada classe (Online Shopper):')
print(por_classe[clientes['Income'].isna()])
# Cuidado: se a classe for o alvo de um modelo, preencher usando a classe e vazamento (script 10 desta unidade).

# --- Quando a falta nao e aleatoria, qualquer escolha distorce.
# Simulacao com dados reais: nas vendas do supermercado, apagamos 40% dos valores altos
# (como se o sistema falhasse justamente nas compras grandes).
vendas = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
total_real = vendas['Total'].copy()

gerador = np.random.default_rng(3)
grandes = total_real[total_real > total_real.quantile(0.6)].index
apagar = gerador.choice(grandes, size=int(0.4 * len(grandes)), replace=False)
total_com_falta = total_real.copy()
total_com_falta[apagar] = np.nan
print(f'\nAusentes criados: {total_com_falta.isna().sum()} de {len(total_com_falta)}')

media_real = total_real.mean()
media_dropna = total_com_falta.dropna().mean()
preenchido_media = total_com_falta.fillna(total_com_falta.mean())
preenchido_mediana = total_com_falta.fillna(total_com_falta.median())
print(f'Media verdadeira:              {media_real:7.1f}')
print(f'Media ignorando ausentes:      {media_dropna:7.1f}')
print(f'Media apos preencher c/ media: {preenchido_media.mean():7.1f}')
print(f'Media apos preencher c/ mediana:{preenchido_mediana.mean():6.1f}')
print(f'Desvio verdadeiro: {total_real.std():.1f} | apos preencher c/ media: {preenchido_media.std():.1f}')
# Todas as versoes subestimam a media, porque a falta atingiu os valores altos.
# Preencher com a media ainda encolhe o desvio: cria uma pilha artificial no centro.

fig, eixos = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
bins = np.arange(0, 1100, 50)
eixos[0].hist(total_real, bins=bins, color='#2F648F')
eixos[0].set_title(f'Completo: média {media_real:.0f}')
eixos[1].hist(total_com_falta.dropna(), bins=bins, color='#8794A3')
eixos[1].set_title(f'Ausentes descartados: média {media_dropna:.0f}')
eixos[2].hist(preenchido_media, bins=bins, color='#BD5B58')
eixos[2].set_title(f'Preenchido com a média: média {preenchido_media.mean():.0f}')
for eixo in eixos:
    eixo.set_xlabel('Total da venda')
eixos[0].set_ylabel('Vendas')
fig.suptitle('Quando a falta atinge os valores altos, descartar ou preencher distorce', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'ausentes.png'))
plt.show()

# Regra pratica: antes de preencher, pergunte POR QUE falta. Se faltar mais em um grupo,
# registre isso na analise. A quantidade de ausentes por coluna deve aparecer no relatorio.

# Experimente: apague 40% dos valores ao acaso (sem o filtro de valores altos) e repita.
