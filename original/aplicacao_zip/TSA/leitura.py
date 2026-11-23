# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 09:00:44 2022

@author: Bruno Pimentel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
# from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
# from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import shap
import sys


def descrever_valor(valores, nome_arq):
    valor = [float(i) for i in valores]
    media = np.mean(valor)
    p25 = np.quantile(valor, 0.25)
    p50 = np.quantile(valor, 0.5)
    p75 = np.quantile(valor, 0.75)
    print(media, p25, p50, p75)
    histograma(valor, nome_arq)
    box_plot(valor, nome_arq)
    
def histograma(valores, nome_arq):
    plt.hist(valores, bins=100, color='g')
    plt.xlabel(nome_arq)
    plt.ylabel('Frequência')
    plt.savefig('figuras/'+nome_arq+'_hist.png', dpi=200)
    plt.close()
    
def box_plot(valores, nome_arq, nomes=None):
    # sns.violinplot(data = valores, linewidth = 2)
    # valor = [float(i) for i in valores]
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    plt.boxplot(valores)
    plt.xlabel(nome_arq)
    if nomes != None:
        ax.set_xticklabels(nomes)
    plt.ylabel('Close Amount')
    plt.savefig('figuras/'+nome_arq+'_box.png', dpi=200)
    plt.close()
    
def contar_valores(df):
    variaveis = df.columns
    for i in variaveis:
        print(df[i].value_counts())
        print('-----------------')
        
# def predizer_Disposition(df):
#     data = df.drop(['Claim Number', 'Date Received', 'Incident D', 'Airport Code', 'Close Amount'], axis=1)
#     X = data.drop(['Disposition'], axis=1)
#     y = data['Disposition']
#     clf = tree.DecisionTreeClassifier()
#     one_hot_data = pd.get_dummies(X)
#     scores = cross_val_score(clf, one_hot_data, y, cv=10)
#     print("%0.4f (%0.4f)" % (scores.mean(), scores.std()))
    
#     # clf = clf.fit(one_hot_data, y)
#     # fig = plt.figure(figsize=(50,50))
#     # tree.plot_tree(clf, filled=True, class_names='Disposition')
#     # fig.savefig("tree.png")
#     return X, y, data

# Predizer Deny ou Not-deny usando classificadores
def predizer_Disposition_clf(df, tipo):
    data = df.drop(['Claim Number', 'Date Received', 'Incident D', 'Airport Code', 'Close Amount', 'Item Category', 'Airport Name'], axis=1)
    data['Disposition'].replace({"Settle": "Not-deny", "Approve in Full": "Not-deny"}, inplace=True)
    print(data.columns)
    # sys.exit()
    contar_valores(data)
    X = data.drop(['Disposition'], axis=1)
    y = pd.DataFrame(data['Disposition'])
    X = pd.get_dummies(X)
    y=y['Disposition'].replace({'Deny':-1, 'Not-deny':1})
    # one_hot_data = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    if tipo == 'LR': #regressao logistica
        clf = LogisticRegression(max_iter=200)  
    elif tipo == 'DT':
        clf = tree.DecisionTreeClassifier()
    elif tipo == 'RF':
        clf = RandomForestClassifier(n_estimators=10)
        
    clf.fit(X_train, y_train)
    predicao = clf.predict(X_test)
    print(classification_report(y_test, predicao))
    # sys.exit()
    matriz_confusao(y_test, predicao, tipo)
    
    if tipo == 'LR': #regressao logistica
        importance = clf.coef_.flatten()
    elif tipo == 'DT' or tipo == 'RF':
        importance = clf.feature_importances_
        
    pyplot.barh(X.columns, importance, color='g')
    pyplot.xlabel('Importância')
    pyplot.savefig('figuras/clf_feature_importance_'+tipo, dpi=200, bbox_inches = "tight")
    pyplot.show()
    
    # Fits the explainer
    import warnings
    warnings.filterwarnings('ignore')
    explainer = shap.Explainer(clf.predict, X_test)
    # Calculates the SHAP values - It takes some time
    shap_values = explainer(X_test)
    # Evaluate SHAP values
    # shap_values = explainer.shap_values(X_test)
    # shap.summary_plot(shap_values)
    # fig, ax = plt.subplots(figsize=(10, 5))
    shap.plots.bar(shap_values,show=False)
    plt.savefig('figuras/clf_shap_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
    shap.plots.bar(shap_values[0],show=False)
    plt.savefig('figuras/clf_shap_0_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
    shap.plots.bar(shap_values[1],show=False)
    plt.savefig('figuras/clf_shap_1_'+tipo, dpi=200, bbox_inches = "tight")
    shap.plots.beeswarm(shap_values,show=False)
    plt.savefig('figuras/clf_shap_beeswarm_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
        
    return X, y, data

def matriz_confusao(y_test, y_pred, tipo):
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(cm)
    ax.grid(False)
    ax.set_xlabel('Predição', fontsize=18, color='black')
    ax.set_ylabel('Real', fontsize=18, color='black')
    ax.xaxis.set(ticks=range(2))
    ax.yaxis.set(ticks=range(2))
    ax.xaxis.set_ticklabels(['Deny', 'Not-deny'], fontsize=15)
    ax.yaxis.set_ticklabels(['Deny', 'Not-deny'], fontsize=15)
    # ax.set_ylim(9.5, -0.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha='center', va='center', color='black', fontsize=15)
    plt.savefig('figuras/matriz_confusao_'+tipo, dpi=200, bbox_inches = "tight")
    plt.show()
    
    
def predizer_CloseAmount(df, tipo):
    data = df.drop(['Claim Number', 'Date Received', 'Incident D', 'Airport Code', 'Disposition', 'Item Category', 'Airport Name'], axis=1)
    data = data[data['Close Amount'] != 0]
    data = data[data['Close Amount'] < 300]
    # descrever_valor(data['Close Amount'], 'boxplot_300')
    contar_valores(data)
    X = data.drop(['Close Amount'], axis=1)
    y = pd.DataFrame(data['Close Amount'])
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    if tipo == 'RF':
        clf = RandomForestRegressor(n_estimators=10)
        
    clf.fit(X_train, y_train)
    
    if tipo == 'RF':
        importance = clf.feature_importances_
        
    pyplot.barh(X.columns, importance, color='g')
    pyplot.xlabel('Importância')
    pyplot.savefig('figuras/close_feature_importance_'+tipo, dpi=200, bbox_inches = "tight")
    pyplot.show()
    plt.close()
    
    # Fits the explainer
    import warnings
    warnings.filterwarnings('ignore')
    explainer = shap.Explainer(clf.predict, X_test)
    shap_values = explainer(X_test)
    shap.plots.bar(shap_values,show=False)
    plt.savefig('figuras/close_shap_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
    print(np.array(y_test)[0][0])
    shap.plots.bar(shap_values[0],show=False)
    plt.savefig('figuras/close_shap_0_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
    print(np.array(y_test)[1][0])
    shap.plots.bar(shap_values[1],show=False)
    plt.savefig('figuras/close_shap_1_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
    print(np.array(y_test)[2][0])
    shap.plots.bar(shap_values[2],show=False)
    plt.savefig('figuras/close_shap_2_'+tipo, dpi=200, bbox_inches = "tight")
    print(np.array(y_test)[3][0])
    shap.plots.bar(shap_values[3],show=False)
    plt.savefig('figuras/close_shap_3_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
    print(np.array(y_test)[4][0])
    shap.plots.bar(shap_values[4],show=False)
    plt.savefig('figuras/close_shap_4_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
    shap.plots.beeswarm(shap_values,show=False)
    plt.savefig('figuras/close_shap_beeswarm_'+tipo, dpi=200, bbox_inches = "tight")
    plt.close()
        
    return X, y, data
    

# def predizer_CloseAmount(df):
#     data = df.drop(['Claim Number', 'Date Received', 'Incident D', 'Airport Code', 'Disposition', 'Item Category', 'Airline Name', 'Airport Name'], axis=1)
#     data = data[data['Close Amount'] != 0]
#     X = data.drop(['Close Amount'], axis=1)
#     y = data['Close Amount']
#     clf = tree.DecisionTreeRegressor()
#     # clf = RandomForestRegressor(n_estimators=50)
#     one_hot_data = pd.get_dummies(X)
#     clf = clf.fit(one_hot_data, y)
#     print(clf.score(one_hot_data, y))
#     kf = KFold(n_splits=10)
#     kf.get_n_splits(one_hot_data)
#     KFold(n_splits=10, random_state=None, shuffle=False)
#     X = np.array(one_hot_data)
#     y = np.array(y)
#     lista_r2 = []
#     for train_index, test_index in kf.split(X):
#         # print(len(train_index))
#         X_train, X_test = X[train_index], X[test_index]
#         y_train, y_test = y[train_index], y[test_index]
#         clf = clf.fit(X_train, y_train)
#         r2 = clf.score(X_test, y_test)
#         lista_r2.append(r2)
#         print(r2)
#     print("%0.4f (%0.4f)" % (np.mean(lista_r2), np.std(lista_r2)))
    
#     # clf = clf.fit(one_hot_data, y)
#     # fig = plt.figure(figsize=(50,50))
#     # tree.plot_tree(clf, filled=True, class_names='Disposition')
#     # fig.savefig("tree.png")
#     return X, y, data

def descrever_todos(df):
    print('Todos os valores')
    valor_todos = df['Close Amount']
    valor_todos = [float(i) for i in valor_todos]
    descrever_valor(valor_todos, 'Avaliando todos os valores')

    print('Todos os valores, exceto os negados')
    valor_negados = df[df['Disposition'] != 'Deny']['Close Amount']
    valor_negados = [float(i) for i in valor_negados]
    descrever_valor(valor_negados, "Todos os valores, exceto \'Deny\'")

    print('Valores Approve in Full')
    valor_full = df[df['Disposition'] == 'Approve in Full']['Close Amount']
    valor_full = [float(i) for i in valor_full]
    descrever_valor(valor_full, "Valores \'Approve in Full\'")

    print('Valores Settle')
    valor_settle = df[df['Disposition'] == 'Settle']['Close Amount']
    valor_settle = [float(i) for i in valor_settle]
    descrever_valor(valor_settle, "Valores \'Approve in Settle\'")

    box_plot([valor_todos, valor_negados, valor_full, valor_settle], 'boxblot_todos', ['Todos', 'Execeto Deny', 'Full', 'Settle'])


def descrever_filtro(df):
    print('Todos os valores')
    valor_todos = df[df['Close Amount']<300]['Close Amount']
    valor_todos = [float(i) for i in valor_todos]
    descrever_valor(valor_todos, 'Avaliando todos os valores (300)')

    print('Todos os valores, exceto os negados')
    valor_negados = df[df['Close Amount'] < 300]
    valor_negados = valor_negados[valor_negados['Disposition'] != 'Deny']['Close Amount']
    valor_negados = [float(i) for i in valor_negados]
    descrever_valor(valor_negados, "Todos os valores, exceto (300) \'Deny\'")

    print('Valores Approve in Full')
    valor_full = df[df['Close Amount'] < 300]
    valor_full = valor_full[valor_full['Disposition'] == 'Approve in Full']['Close Amount']
    valor_full = [float(i) for i in valor_full]
    descrever_valor(valor_full, "Valores \'Approve in Full\' (300)")

    print('Valores Settle')
    valor_settle = df[df['Close Amount'] < 300]
    valor_settle = valor_settle[valor_settle['Disposition'] == 'Settle']['Close Amount']
    valor_settle = [float(i) for i in valor_settle]
    descrever_valor(valor_settle, "Valores \'Approve in Settle\' (300) ")

    box_plot([valor_todos, valor_negados, valor_full, valor_settle], 'boxblot_300', ['Todos', 'Execeto Deny', 'Full', 'Settle'])



# https://www.reddit.com/r/datasets/comments/5pn2re/tsa_claims_data_a_list_of_everything_lost_in/
# https://www.dhs.gov/tsa-claims-data
df = pd.read_excel('dados/claims-data-2015-as-of-feb-9-2016.xlsx') 
print('Descricao antes do pre-processamento----------')
contar_valores(df)
#Remover 
df = df[df['Close Amount'] != '-']
df = df[df['Claim Type'] != '-']
df = df[df['Claim Site'] != '-']
df = df[df['Airline Name'] != '-']
print(len(df))
df_sa = df[df['Airline Name']=='Southwest Airlines  ']
df_da = df[df['Airline Name']=='Delta Air Lines  ']
df_aa = df[df['Airline Name']=='American Airlines  ']
df_ual = df[df['Airline Name']=='UAL  ']
df_usa = df[df['Airline Name']=='USAir  ']
# contar_valores(df)
df = pd.concat([df_sa, df_da, df_aa, df_ual, df_usa]) 
print(len(df))
# print('\n\n----------------Descricao depois do pre-processamento----------')   
# contar_valores(df)

# descrever_todos(df)
# descrever_filtro(df)
# clf = ['LR', 'DT', 'RF']
# for c in clf:
    # X, y, data = predizer_Disposition_clf(df, c)
X, y, data = predizer_CloseAmount(df, 'RF')



