# Vazamento de dados: quando o modelo "aprende" algo que nao estaria disponivel na hora de prever.
# Dados: dados/supermercado.csv. Modelos simples, so para mostrar o efeito.

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

pasta = os.path.dirname(os.path.abspath(__file__))
vendas = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))

# Tarefa: prever o valor Total de uma venda.
y = vendas['Total']

# --- Vazamento 1: usar uma coluna que e consequencia do alvo
# 'Tax 5%' e 'gross income' sao calculados A PARTIR do total. Na hora de prever, ninguem os teria.
X_vazado = vendas[['Tax 5%', 'gross income']]
X_tr, X_te, y_tr, y_te = train_test_split(X_vazado, y, test_size=0.3, random_state=0)
modelo = LinearRegression().fit(X_tr, y_tr)
print('Com colunas derivadas do alvo: R2 =', round(r2_score(y_te, modelo.predict(X_te)), 4))
# R2 = 1.0 nao e um modelo bom; e um modelo que recebeu a resposta.

# --- Sem vazamento: so o que se conhece antes da venda fechar
X_honesto = pd.get_dummies(vendas[['Unit price', 'Quantity', 'Product line', 'City', 'Customer type']], dtype=int)
X_tr, X_te, y_tr, y_te = train_test_split(X_honesto, y, test_size=0.3, random_state=0)
modelo = LinearRegression().fit(X_tr, y_tr)
print('Com preco e quantidade:        R2 =', round(r2_score(y_te, modelo.predict(X_te)), 4),
      '| MAE =', round(mean_absolute_error(y_te, modelo.predict(X_te)), 1))
# Alto, mas por outro motivo: Total = preco x quantidade x 1,05 e uma formula, nao um padrao de mercado.
# Um modelo linear nao reproduz o produto exatamente; por isso o R2 nao chega a 1.

# Pergunta honesta: da para prever a QUANTIDADE antes da compra, com o que se sabe do cliente?
y2 = vendas['Quantity']
X2 = pd.get_dummies(vendas[['Unit price', 'Product line', 'City', 'Customer type', 'Gender']], dtype=int)
X_tr, X_te, y_tr, y_te = train_test_split(X2, y2, test_size=0.3, random_state=0)
modelo = LinearRegression().fit(X_tr, y_tr)
previsto = modelo.predict(X_te)
print('Prever quantidade:             R2 =', round(r2_score(y_te, previsto), 4),
      '| MAE =', round(mean_absolute_error(y_te, previsto), 2))
print('Linha de base (prever a media):            MAE =', round(mean_absolute_error(y_te, np.full(len(y_te), y_tr.mean())), 2))
# R2 perto de zero e MAE igual ao da media: as variaveis disponiveis nao explicam a quantidade.
# Essa e a resposta real, e ela importa: nao ha como "direcionar" quem vai comprar mais com estes dados.

# --- Vazamento 2: pre-processar antes de separar treino e teste
# Preencher ausentes com a media de TODOS os dados usa informacao do teste.
# Ordem correta: separar -> ajustar (fit) imputador/escala no treino -> aplicar (transform) nos dois.
# O script 04_escala.py mostra a ordem correta com StandardScaler.

# --- Vazamento 3: embaralhar dados que tem tempo
# Se a tarefa e prever o futuro, separe por data (treino = passado, teste = futuro).
# A unidade 08 faz isso; o estudo de caso de energia tambem.

# Experimente: acrescente 'Rating' nas variaveis do modelo de quantidade. A avaliacao e dada
# DEPOIS da compra. Ela ajuda a prever? Ela estaria disponivel na hora de decidir?
