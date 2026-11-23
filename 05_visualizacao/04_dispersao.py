# Dispersao: para relacoes entre duas variaveis numericas.

import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# Base iris: 150 flores de 3 especies, 4 medidas em cm (dados reais, incluidos no scikit-learn)
iris = load_iris()
medidas = pd.DataFrame(iris.data, columns=iris.feature_names)
medidas['especie'] = [iris.target_names[t] for t in iris.target]
print(medidas.head())
print(medidas['especie'].value_counts())

# Uma cor por especie e rotulo direto no grafico, em vez de legenda ou barra de cores
cores = {'setosa': '#2F648F', 'versicolor': '#168A8A', 'virginica': '#D69A35'}
fig, eixo = plt.subplots(figsize=(6.5, 4.2))
for especie, grupo in medidas.groupby('especie'):
    eixo.scatter(grupo['sepal length (cm)'], grupo['sepal width (cm)'], s=28, color=cores[especie], alpha=0.8)
    eixo.text(grupo['sepal length (cm)'].mean(), grupo['sepal width (cm)'].max() + 0.12, especie,
              color=cores[especie], ha='center', fontweight='bold')
eixo.set_xlabel('Comprimento da sépala (cm)')
eixo.set_ylabel('Largura da sépala (cm)')
eixo.set_title('Setosa se separa pelas sépalas; versicolor e virginica se misturam')
plt.savefig(os.path.join(pasta, 'figuras', 'dispersao_iris.png'))
plt.show()

# Quando ha muitos pontos, use transparencia e tamanho pequeno
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
fig, (esq, dir) = plt.subplots(1, 2, figsize=(10, 3.8))
esq.scatter(dados['Unit price'], dados['Total'], s=40, color='#2F648F')
esq.set_title('Pontos grandes e opacos: sobreposição esconde')
dir.scatter(dados['Unit price'], dados['Total'], s=10, alpha=0.4, color='#2F648F')
dir.set_title('Pontos pequenos e translúcidos: a densidade aparece')
for eixo in (esq, dir):
    eixo.set_xlabel('Preço unitário')
    eixo.set_ylabel('Total da venda')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'dispersao_sobreposicao.png'))
plt.show()

# Os "leques" no grafico da direita sao as quantidades de 1 a 10: Total = preco x quantidade x 1,05.
# Um grafico de dispersao pode revelar a regra que gerou os dados.

# Experimente: use 'petal length (cm)' e 'petal width (cm)' no grafico da iris.
# As especies se separam melhor ou pior?
