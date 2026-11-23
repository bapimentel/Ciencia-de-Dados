# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 12:49:10 2022

@author: Bruno Pimentel
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# from statsmodels.tsa.seasonal import MSTL
from statsmodels.tsa.seasonal import seasonal_decompose as sm
# from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima.arima import auto_arima
from pmdarima import model_selection
from sklearn.ensemble import RandomForestRegressor


def ler_arquivo():
    df = pd.read_excel('dados/D202.xlsx') 
    df = df.drop(['TYPE', 'UNITS', 'NOTES'], axis=1)
    # data = {}
    # df_novo = pd.DataFrame(data, columns=['Data', 'Tempo', 'Uso', 'Custo'])
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['START TIME'] = pd.to_timedelta(df['START TIME'].astype(str))
    df['DATE'] = df['START TIME']+df['DATE']
    df = df.drop(['START TIME', 'END TIME'], axis=1)
    df = df.rename(columns={'DATE': 'Data', 'USAGE': 'Uso', 'COST':'Custo'})
    df['Valor'] = df['Uso']*df['Custo']
    # print(df.describe())
    return df

def plot(df):
    sns.set_theme(style="white")
    plt.rcParams['axes.facecolor'] = '#EDECEC'  # Cor do fundo do retângulo de plotagem
    plt.rcParams['figure.facecolor'] = '#FFFFFF'  # Cor da área fora do retângulo (branca)   
    
    
    paleta_customizada = sns.light_palette("#3155A4", as_cmap=True)
    sns_plot = sns.scatterplot(data=df, x='Data', y='Custo', hue="Uso", palette=paleta_customizada, edgecolor="#393A3A", linewidth=0.1)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.savefig('figuras/scatter_custo_uso.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
    # sns_plot = sns.lineplot(data=df, x='Data', y='Custo', linewidth = 0.2)
    # plt.setp(sns_plot.get_xticklabels(), rotation=90)
    # plt.savefig('figuras/line_custo.png', dpi=200, bbox_inches = "tight")
    # plt.close()
    
    # sns_plot = sns.lineplot(data=df, x='Data', y='Uso', linewidth = 0.2)
    # plt.setp(sns_plot.get_xticklabels(), rotation=90)
    # plt.savefig('figuras/line_uso.png', dpi=200, bbox_inches = "tight")
    # plt.close()
     
    sns_plot = sns.lineplot(data=df, x='Data', y='Uso', color='#3155A4', label='Uso', linewidth=0.3)
    sns.lineplot(data=df, x='Data', y='Custo', label='Custo', color='#FFB511', linewidth=0.3)    
    plt.setp(sns_plot.get_xticklabels(), rotation=90)    
    sns_plot.set_ylabel("Uso / Custo") 
    plt.savefig('figuras/line_uso_custo.png', dpi=200, bbox_inches="tight")
    plt.close()
    
def agrupar_uso_por_hora(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby([df['Data'].dt.hour]).Uso.sum()
    
    sns_plot = sns.lineplot(data=df, markers=True)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Hora')
    plt.savefig('figuras/line_uso_hora.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def agrupar_custo_por_hora(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby([df['Data'].dt.hour]).Custo.sum()
    
    sns_plot = sns.lineplot(data=df, markers=True)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Hora')
    plt.savefig('figuras/line_custo_hora.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def agrupar_uso_por_dia(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby([df['Data'].dt.day]).Uso.sum()
    
    sns_plot = sns.lineplot(data=df, markers=True, err_style='band')
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Dia')
    plt.savefig('figuras/line_uso_dia.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def agrupar_custo_por_dia(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby([df['Data'].dt.day]).Custo.sum()
    
    sns_plot = sns.lineplot(data=df, markers=True)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Dia')
    plt.savefig('figuras/line_custo_dia.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def agrupar_uso_por_mes(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby([df['Data'].dt.month]).Uso.sum()
    
    sns_plot = sns.lineplot(data=df, markers=True)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Mês')
    plt.savefig('figuras/line_uso_mes.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def agrupar_custo_por_mes(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby([df['Data'].dt.month]).Custo.sum()
    
    sns_plot = sns.lineplot(data=df, markers=True)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Mês')
    plt.savefig('figuras/line_custo_mes.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def agrupar_uso_meses_historico(df):
    # Resample to daily precip sum and save as new dataframe
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby(pd.Grouper(key="Data", freq="1M")).sum()
    df = df.drop(['Custo', 'Valor'], axis=1)
    
    sns_plot = sns.lineplot(data=df, markers=False)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Mês')
    plt.ylabel('Uso')
    plt.savefig('figuras/line_uso_meses_historico.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def agrupar_uso_horas_historico(df):
    # Resample to daily precip sum and save as new dataframe
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby(pd.Grouper(key="Data", freq="1H")).sum()
    df = df.drop(['Custo', 'Valor'], axis=1)
    
    sns_plot = sns.lineplot(data=df, markers=False)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Hora')
    plt.ylabel('Uso')
    plt.savefig('figuras/line_uso_hora_historico.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def agrupar_uso_dias_historico(df):
    # Resample to daily precip sum and save as new dataframe
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby(pd.Grouper(key="Data", freq="1D")).sum()
    df = df.drop(['Custo', 'Valor'], axis=1)
    
    sns_plot = sns.lineplot(data=df, markers=False)
    plt.setp(sns_plot.get_xticklabels(), rotation=90)
    plt.xlabel('Dia')
    plt.ylabel('Uso')
    plt.savefig('figuras/line_uso_dias_historico.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
def decompor_serie_uso_dias_historico(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby(pd.Grouper(key="Data", freq="1D")).sum()
    df = df.drop(['Custo', 'Valor'], axis=1)
    
    ts_dicomposition = sm(x=df['Uso'], model='additive')
    trend_estimate = ts_dicomposition.trend
    seasonal_estimate = ts_dicomposition.seasonal
    residual_estimate = ts_dicomposition.resid
    
    print(seasonal_estimate)
    
    # Plotting the time series and it's components together
    fig, axes = plt.subplots(4, 1, sharex=True, sharey=False)
    fig.set_figheight(10)
    fig.set_figwidth(20)
    # First plot to the Original time series
    axes[0].plot(df, label='Original') 
    axes[0].legend(loc='upper left')
    # second plot to be for trend
    axes[1].plot(trend_estimate, label='Tendência')
    axes[1].legend(loc='upper left')
    # third plot to be Seasonality component
    axes[2].plot(seasonal_estimate, label='Sazonalidade')
    axes[2].legend(loc='upper left')
    # last last plot to be Residual component
    axes[3].plot(residual_estimate, label='Resíduos')
    axes[3].legend(loc='upper left')
    
    plt.savefig('figuras/decomposicao_uso_dias.png', dpi=200, bbox_inches = "tight")
    
def predicao_serie(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby(pd.Grouper(key="Data", freq="1D")).sum()
    df = df.drop(['Custo', 'Valor'], axis=1)
    
    train = df[0:513]
    test = df[513:]
    plt.plot(train, color = "black", label="Treino")
    plt.plot(test, color = "red", label="Teste")
    plt.ylabel('Uso')
    plt.xlabel('Data')
    plt.xticks(rotation=90)
    plt.savefig('figuras/treino_teste_uso_dias.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
    train, test = model_selection.train_test_split(df, train_size=0.7)
    modl  = auto_arima(train, start_p=0, start_q=0,
                           start_P=0, start_Q=0,
                           max_order=100,
                           seasonal=True,
                           max_P=3, max_D=3, max_Q=3,
                           d=3, D=3, trace=False,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True,
                           method='bfgs')     
    
    preds, conf_int = modl.predict(n_periods=len(test), return_conf_int=True)
    
    print(modl.get_params())
    
    resposta = test
    resposta.index = test.index
    resposta.value = preds
    
    plt.plot(resposta, color='Blue', linewidth = 1, label="Predição")
    plt.ylabel('Uso')
    plt.xlabel('Data')
    plt.xticks(rotation=90)
    plt.legend()
    plt.savefig('figuras/predicao_uso_dias.png', dpi=200, bbox_inches = "tight")
    plt.close()
    

def MAE(Y_actual,Y_Predicted):
    mae = 0
    for i in range(len(Y_Predicted)):
        mae = mae + np.abs(Y_actual[i] - Y_Predicted[i])/len(Y_Predicted)
    return mae
    
    
def predicao_RF(df):
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.groupby(pd.Grouper(key="Data", freq="1D")).sum()
    
    clf = RandomForestRegressor(n_estimators=1000)
    train, test = model_selection.train_test_split(df, train_size=0.7) 
    print('train.index', train.index)
    print('test.index', test.index)
    print(len(train), len(test))
    x_train = train[['Uso', 'Custo']]
    y_train = train['Valor']
    x_test = test[['Uso', 'Custo']]
    y_test = test['Valor']
    clf.fit(x_train, y_train)
    preds = clf.predict(x_test)
    print(MAE(y_test, preds))
    print('Soma valor teste =', np.sum(y_test))
    print('Soma valor predito =', np.sum(preds))
    print('--------------------------------')
    soma_antes = np.sum(preds)
    plt.plot(y_train, 'k-', label="Treino")
    plt.plot(y_test, 'r-', linewidth = 1.5, label="Teste")
    plt.ylabel('Valor')
    plt.xlabel('Data')
    plt.xticks(rotation=90)
    plt.legend()
    plt.savefig('figuras/treino_teste_uso_dias.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
    resposta = test['Valor']
    resposta.index = test.index
    resposta.value = preds  
    plt.plot(y_test, 'rs-', label="Valor Real")
    plt.plot(resposta, 'bo-', linewidth = 1.5, label="Valor Predito")
    plt.ylabel('Valor')
    plt.xlabel('Data')
    plt.xticks(rotation=90)
    plt.legend()
    plt.savefig('figuras/predicao_uso_dias_RF.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
    reducao_uso = np.arange(0,100,10)
    reducao_valor = []
    for i in reducao_uso:
        x_test['Uso'] = x_test['Uso']*(1-i/100.0)
        preds = clf.predict(x_test)
        print(MAE(y_test, preds))
        print('Soma valor teste =', np.sum(y_test))
        print('Soma valor predito =', np.sum(preds))
        soma_depois = np.sum(preds)
        print((soma_antes-soma_depois)/soma_antes)
        reducao_valor.append(100*(soma_antes-soma_depois)/soma_antes)
    # plt.plot(reducao_uso, 'bs-', label="Redução Uso")
    # plt.plot(reducao_valor, 'ro-', linewidth = 1.5, label="Redução Valor")
    # plt.ylabel('Redução (%)')
    # plt.xlabel('Redução de uso (%)')
    # plt.xticks(range(0,10), ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90'])
    # plt.xticks(rotation=90)
    # plt.legend()
    plt.plot(reducao_valor, 'bo-', linewidth = 1.5)
    plt.ylabel('Redução do Valor (%)')
    plt.xlabel('Redução de Uso (%)')
    plt.xticks(range(0,10), ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90'])
    plt.savefig('figuras/reducao_uso_RF.png', dpi=200, bbox_inches = "tight")
    plt.close()
    
    


df = ler_arquivo()
plot(df)
# agrupar_uso_por_hora(df)
# agrupar_custo_por_hora(df)
# agrupar_uso_por_dia(df)
# agrupar_custo_por_dia(df)
# agrupar_uso_por_mes(df)
# agrupar_custo_por_mes(df)

# agrupar_uso_meses_historico(df)
# agrupar_uso_horas_historico(df)

# agrupar_uso_dias_historico(df)
# decompor_serie_uso_dias_historico(df)

# predicao_serie(df)
# predicao_RF(df)
