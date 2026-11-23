import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.signal import find_peaks
from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
# import shap
from sklearn.model_selection import train_test_split
# from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from scipy.stats import wilcoxon




# Leitura do arquivo CSV na pasta 'dados'
df = pd.read_csv('dados/supermarket_sales - Sheet1.csv', encoding='utf-8')

# Renomeando as colunas relevantes
df.rename(columns={
    'Product line': 'Product',
    'Unit price': 'Price',
    'Quantity': 'Quantity',
    'Date': 'Data',
    'Rating': 'Rating'  # Incluindo o Rating
}, inplace=True)

# Convertendo a coluna 'Data' para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'])

# Função para gerar as estatísticas descritivas globais e por produto para Preço, Quantidade e Rating
def estatisticas_globais_produtos(arquivo_saida):
    """
    Função que calcula e exibe as estatísticas descritivas globais e por produto para Preço, Quantidade e Rating,
    salvando tudo em um arquivo de texto.
    
    Args:
    arquivo_saida: Nome do arquivo de saída para salvar as estatísticas.
    """
    colunas = ['Price', 'Quantity', 'Rating']
    nomes_colunas = ['Price', 'Quantity', 'Rating']

    with open(arquivo_saida, 'a') as f:  # Abrindo o arquivo em modo de adição ('append')
        for i, coluna in enumerate(colunas):
            nome_coluna = nomes_colunas[i]
            # Estatísticas Globais
            f.write(f"=== Estatísticas Globais de {nome_coluna} ===\n")
            media_global = df[coluna].mean()
            mediana_global = df[coluna].median()
            desvio_padrao_global = df[coluna].std()
            moda_global = df[coluna].mode()[0]

            f.write(f"Média: {media_global}\n")
            f.write(f"Mediana: {mediana_global}\n")
            f.write(f"Desvio Padrão: {desvio_padrao_global}\n")
            f.write(f"Moda: {moda_global}\n\n")

            # Estatísticas por Produto
            produtos = df['Product'].unique()
            for produto in produtos:
                df_produto = df[df['Product'] == produto]
                media = df_produto[coluna].mean()
                mediana = df_produto[coluna].median()
                desvio_padrao = df_produto[coluna].std()
                moda = df_produto[coluna].mode()[0]

                f.write(f"=== Estatísticas de {nome_coluna} para o Produto: {produto} ===\n")
                f.write(f"Média: {media}\n")
                f.write(f"Mediana: {mediana}\n")
                f.write(f"Desvio Padrão: {desvio_padrao}\n")
                f.write(f"Moda: {moda}\n\n")

# Função para análise da série temporal e decomposição
def analise_serie_temporal():
    """
    Função que realiza a análise de série temporal da quantidade vendida ao longo do tempo e sua decomposição.
    """
    # Gráfico de linha para a média da quantidade vendida ao longo do tempo
    # Agrupando a quantidade vendida por data
    media_por_data = df.groupby('Data')['Quantity'].mean().reset_index()

    # Criando o gráfico de linha
    plt.figure(figsize=(12, 6))
    plt.plot(media_por_data['Data'], media_por_data['Quantity'], marker='o', linestyle='-', color='b')

    plt.title('', fontsize=14)
    plt.xlabel('Data', fontsize=14)
    plt.ylabel('Média da Quantidade Vendida', fontsize=14)
    plt.xticks(rotation=45)

    # Ajustando o layout
    plt.tight_layout()

    # Salvando o gráfico
    plt.savefig('figuras/media_quantidade_vendida_ao_longo_do_tempo.png', dpi=300)
    plt.show()

    # Decomposição da série temporal
    # Configurando o índice do DataFrame para a data
    media_por_data.set_index('Data', inplace=True)

    # Decompondo a série temporal
    decomposicao = seasonal_decompose(media_por_data['Quantity'], model='additive')

    # Criando gráficos de decomposição
    plt.figure(figsize=(12, 10))

    # Ajustando os tamanhos das fontes
    decomposicao.plot()
    plt.suptitle('Decomposição da Série Temporal', fontsize=14)
    plt.tight_layout()

    # Ajustando o tamanho das fontes dos eixos
    for ax in plt.gcf().axes:
        for label in ax.get_xticklabels():
            label.set_fontsize(8)
        for label in ax.get_yticklabels():
            label.set_fontsize(8)

    # Salvando o gráfico de decomposição
    plt.savefig('figuras/decomposicao_serie_temporal.png', dpi=300)
    plt.show()

    # Identificando picos na componente sazonal
    sazonalidade = decomposicao.seasonal
    picos, _ = find_peaks(sazonalidade)

    # Extraindo os dias correspondentes aos picos
    dias_picos = media_por_data.index[picos]

    # Mostrando os picos e os dias correspondentes
    print("Picos na Sazonalidade:")
    for dia in dias_picos:
        print(dia.strftime('%Y-%m-%d'), sazonalidade[dia])

    # Plotando a sazonalidade e os picos
    plt.figure(figsize=(12, 6))
    plt.plot(sazonalidade, label='Sazonalidade', color='b')
    plt.scatter(dias_picos, sazonalidade[picos], color='red', label='Picos', zorder=5)
    plt.title('', fontsize=14)
    plt.xlabel('Data', fontsize=14)
    plt.ylabel('Sazonalidade', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('figuras/sazonalidade_com_picos.png', dpi=300)
    plt.show()

# Função para gerar gráfico da mediana do Rating por Produto
def grafico_mediana_rating():
    """
    Função que gera um gráfico de barras da mediana de rating por produto.
    """
    mediana_rating_por_produto = df.groupby('Product')['Rating'].median().reset_index()

    # Criando o gráfico de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(data=mediana_rating_por_produto, x='Product', y='Rating', palette='viridis')

    # Adicionando título e rótulos aos eixos
    plt.title('Mediana do Rating por Produto')
    plt.xlabel('Produto')
    plt.ylabel('Mediana do Rating')

    # Rotacionando os rótulos do eixo x para melhor visualização
    plt.xticks(rotation=45)

    # Ajustando o layout
    plt.tight_layout()

    # Salvando o gráfico
    plt.savefig('figuras/mediana_rating_por_produto.png', dpi=300)

    # Exibindo o gráfico
    plt.show()
    
    
    
def biplot_3d(pca, df_pca, df, clusters, output_path):
    """
    Função para criar um biplot 3D com os componentes principais do PCA e salvar o gráfico.

    Args:
    pca (PCA): O modelo PCA ajustado.
    df_pca (DataFrame): DataFrame contendo os componentes principais.
    df (DataFrame): DataFrame original com as variáveis.
    clusters (array): Array com os clusters atribuídos aos dados.
    output_path (str): Caminho para salvar o gráfico.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plotando os clusters nos componentes principais primeiro
    scatter = ax.scatter(df_pca[:, 0], df_pca[:, 1], df_pca[:, 2], c=clusters, cmap='Set2', s=60, alpha=0.2)

    # Adicionando as setas das variáveis
    for i in range(3):  # Alterado para apenas as 4 variáveis mais importantes
        feature = df.columns[i]
        ax.quiver(0, 0, 0, pca.components_[0, i] * 2.5, pca.components_[1, i] * 2.5, pca.components_[2, i] * 2.5, color='r', alpha=0.9)

        # Deslocando o nome da variável para não ficar sobreposto à seta
        ax.text(
            pca.components_[0, i] * 2.5 * 1.1,  # Multiplica por 1.1 para deslocar o texto
            pca.components_[1, i] * 2.5 * 1.1,
            pca.components_[2, i] * 2.5 * 1.1,
            feature,
            color='black',
            fontsize=10
        )

    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    plt.title('Biplot 3D - PCA com Clusters')
    plt.colorbar(scatter)

    # Salvando o gráfico
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.show()
    
    
    
    
def analisar_clusterizacao(df, num_clusters=2, output_dir='figuras'):
    """
    Função para analisar a clusterização usando agrupamento hierárquico e visualização com Biplot 3D.

    Args:
    df (DataFrame): O DataFrame com os dados já carregados.
    num_clusters (int): O número de clusters a serem utilizados.
    output_dir (str): Diretório onde os gráficos serão salvos.
    """

    # Criação do diretório, caso não exista
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Renomeando as colunas relevantes
    df.rename(columns={
        'Product line': 'Product',
        'Unit price': 'Price',
        'Quantity': 'Quantity',
        'gross income': 'GrossIncome',
        'Total': 'Total',
        'Rating': 'Rating'
    }, inplace=True)

    # Convertendo colunas categóricas para numéricas
    label_cols = ['Branch', 'City', 'Customer type', 'Gender', 'Product', 'Payment']
    original_values_dict = {}
    
    for col in label_cols:
        le = LabelEncoder()
        original_values = df[col].unique()
        df[col] = le.fit_transform(df[col])
        # Armazenando valores originais e suas conversões
        original_values_dict[col] = {
            'Original': original_values,
            'Converted': df[col].unique()  # Valores convertidos (números)
        }
    print(original_values_dict)

    # Selecionando as colunas para clusterização
    colunas_cluster = ['Branch', 'City', 'Customer type', 'Gender', 'Product', 'Price', 'Quantity', 'Total', 'GrossIncome', 'Rating']

    # Padronizando os dados
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df[colunas_cluster])

    # Aplicando o agrupamento hierárquico
    linked = linkage(df_scaled, method='ward')
    df['Cluster'] = fcluster(linked, num_clusters, criterion='maxclust')

    # Plotando o dendrograma
    plt.figure(figsize=(12, 8))
    dendrogram(linked, color_threshold=0.9 * np.max(linked[:, 2]))  # Ajuste o threshold de cor
    plt.title('', fontsize=14)
    plt.xlabel('')  # Removendo o rótulo do eixo x
    plt.ylabel('Distância', fontsize=14)
    plt.tight_layout()

    # Salvando o dendrograma
    dendro_path = os.path.join(output_dir, 'dendrograma.png')
    plt.savefig(dendro_path, dpi=300)
    plt.show()

    # Aplicando PCA para análise de importância das variáveis
    # pca = PCA(n_components=3)  # Usando 3 componentes principais para o biplot 3D
    # df_pca = pca.fit_transform(df_scaled)

    # Criando e salvando o biplot 3D
    # biplot_path = os.path.join(output_dir, 'biplot_3d_clusters.png')
    # biplot_3d(pca, df_pca, df[colunas_cluster], df['Cluster'], biplot_path)

    # Cálculo de estatísticas dos elementos centrais dos grupos
    for cluster_id in range(1, num_clusters + 1):
        cluster_data = df[df['Cluster'] == cluster_id]
        
        print(f"\nEstatísticas do Cluster {cluster_id}:")
        print(f"Tamanho do Cluster: {len(cluster_data)}")  # Tamanho do grupo
        # Calcular e imprimir estatísticas e proporções
        for col in colunas_cluster:
            if col in cluster_data.columns:
                media = cluster_data[col].mean()
                mediana = cluster_data[col].median()
                desvio_padrao = cluster_data[col].std()
                moda = cluster_data[col].mode()[0] if not cluster_data[col].mode().empty else np.nan
                
                print(f"{col} - Média: {media:.2f}, Mediana: {mediana:.2f}, Desvio Padrão: {desvio_padrao:.2f}, Moda: {moda}")
                
                # Proporções dos valores categóricos
                if col in label_cols:
                    proporcoes = cluster_data[col].value_counts(normalize=True) * 100  # Proporções em porcentagem
                    print(f"Proporções de {col} no Cluster {cluster_id}:")
                    for value, prop in proporcoes.items():
                        print(f"  Valor: {value}, Proporção: {prop:.2f}%")

    # Treinando o modelo de regressão para cada cluster
    colunas_previsoras = ['Branch', 'City', 'Customer type', 'Gender', 'Product', 'Rating', 'Price']
    treinar_modelo_regressao_por_cluster(df, colunas_previsoras, target='Total', output_dir=output_dir)

    


def treinar_modelo_regressao_por_cluster(df, colunas_previsoras, target='Total', output_dir='figuras', ajuste_percentual=10):
    """
    Função para treinar um modelo de regressão para cada cluster e avaliar o desempenho,
    além de realizar predições com preços ajustados e testar a significância da diferença.

    Args:
    df (DataFrame): O DataFrame com os dados e os clusters já definidos.
    colunas_previsoras (list): Lista de colunas previsoras usadas no treinamento do modelo.
    target (str): Nome da coluna alvo para a regressão (por padrão, 'Total').
    output_dir (str): Diretório onde salvar gráficos ou relatórios.
    ajuste_percentual (float): Percentual de ajuste no preço (por padrão, 10%).
    """
    
    # Garantindo que o diretório de saída exista
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop sobre cada cluster
    clusters = df['Cluster'].unique()
    
    for cluster_id in clusters:
        # Filtrando os dados do cluster atual
        df_cluster = df[df['Cluster'] == cluster_id]

        # Definindo X e y para o modelo
        X = df_cluster[colunas_previsoras].copy()
        y = df_cluster[target]
        
        # Dividindo os dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Treinando o modelo de regressão Random Forest
        modelo = RandomForestRegressor(n_estimators=200, random_state=42)
        modelo.fit(X_train, y_train)

        # Fazendo previsões no conjunto de teste com os preços originais
        y_pred_original = modelo.predict(X_test)

        # Avaliando o desempenho do modelo com os preços originais
        mse_original = mean_squared_error(y_test, y_pred_original)
        mape_original = mean_absolute_percentage_error(y_test, y_pred_original)
        r2_original = r2_score(y_test, y_pred_original)
        
        print(f"Cluster {cluster_id} - Métricas do modelo (preço original):")
        print(f"  MSE: {mse_original:.2f}")
        print(f"  MAPE: {mape_original:.2%}")
        print(f"  R2: {r2_original:.2f}")
        
        # Importância das Features
        importancias = modelo.feature_importances_
        indices = np.argsort(importancias)[::-1]
        
        # Gerando um gráfico de Importância das Features
        plt.figure(figsize=(10, 6))
        plt.title('', fontsize=14)
        plt.bar(range(X_train.shape[1]), importancias[indices], align='center', color='b')
        plt.xticks(range(X_train.shape[1]), np.array(colunas_previsoras)[indices], rotation=90)
        plt.xlabel('Variáveis', fontsize=14)
        plt.ylabel('Importância', fontsize=14)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/importancia_features_cluster_{cluster_id}_original.png', dpi=300)
        plt.show()

        # Calculando a mediana dos valores preditos para diferentes percentuais de ajuste
        percentuais = np.arange(0, 151, 1)  # Percentuais de ajuste de 0% a 150%
        medianas_ajustadas = []

        for p in percentuais:
            # Ajustando os preços com o percentual atual
            X_test_ajustado = X_test.copy()
            if 'Price' in colunas_previsoras:
                X_test_ajustado['Price'] *= (1 + p / 100)
            
            # Fazendo previsões com os preços ajustados
            y_pred_ajustado = modelo.predict(X_test_ajustado)

            # Calculando a mediana dos valores preditos ajustados
            mediana_ajustada = np.median(y_pred_ajustado)
            medianas_ajustadas.append(mediana_ajustada)
        
        # Plotando o gráfico de variação da mediana com diferentes percentuais de ajuste
        plt.figure(figsize=(10, 6))
        plt.plot(percentuais, medianas_ajustadas, marker='o', linestyle='-', color='b')
        plt.axvline(x=10, color='r', linestyle='--', label='Ajuste de 10%')
        plt.xlabel('Percentual de Ajuste', fontsize=14)
        plt.ylabel('Mediana dos Valores Preditos', fontsize=14)
        plt.title('', fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'{output_dir}/variacao_mediana_ajuste_cluster_{cluster_id}.png', dpi=300)
        plt.show()

        # Teste de hipótese e cálculo de medianas para ajuste de 10%
        X_test_ajustado_10 = X_test.copy()
        if 'Price' in colunas_previsoras:
            X_test_ajustado_10['Price'] *= (1 + 10 / 100)
        
        y_pred_ajustado_10 = modelo.predict(X_test_ajustado_10)
        
        # Teste de Hipótese não paramétrico (Wilcoxon) para comparar se há diferença significativa
        stat, p_value = wilcoxon(y_pred_original, y_pred_ajustado_10)
        
        if p_value < 0.05:
            resultado = "significativa"
        else:
            resultado = "não significativa"

        print(f"  Teste de Hipótese (Wilcoxon para ajuste de 10%): p-value = {p_value:.4f} (Diferença {resultado})")

        # Calculando as medianas dos valores preditos antes e depois do ajuste de 10%
        mediana_original = np.median(y_pred_original)
        mediana_ajustada_10 = np.median(y_pred_ajustado_10)

        print(f"  Mediana dos valores preditos (original): {mediana_original:.2f}")
        print(f"  Mediana dos valores preditos (ajustado em 10%): {mediana_ajustada_10:.2f}")




# Execução das funções
if __name__ == "__main__":
    # Nome do arquivo para salvar as estatísticas
    arquivo_saida = 'estatisticas_produtos.txt'

    # Apaga o arquivo se já existir para começar do zero
    if os.path.exists(arquivo_saida):
        os.remove(arquivo_saida)

    # Análise de estatísticas globais e por produto para Preço, Quantidade e Rating
    estatisticas_globais_produtos(arquivo_saida)

    # Realizando a análise de série temporal
    analise_serie_temporal()

    # Gerando gráfico da mediana do rating por produto
    grafico_mediana_rating()
    
    cluster_data = analisar_clusterizacao(df)
    
