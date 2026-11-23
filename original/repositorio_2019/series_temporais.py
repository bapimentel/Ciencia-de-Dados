# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:23:03 2019

@author: Bruno Pimentel
"""


import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA

# https://fred.stlouisfed.org/series/SPCS20RPSNSA
data = pd.read_csv("Dados/SPCS20RPSNSA.csv",index_col=0)
data.head()

data.index = pd.to_datetime(data.index)

data.columns = ['SP&C']
#data = data[800:970]

plt.plot(data)
plt.title("S&P/Case-Shiller 20-City Home Price Sales Pair Counts")
plt.show()

decomp = seasonal_decompose(data, model="additive")
tendencia = decomp.trend
sazonalidade = decomp.seasonal
residuo = decomp.resid

plt.subplot(411)
plt.plot(data, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(tendencia, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(sazonalidade,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residuo, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()

model = ARIMA(data, order=(1,1,2))
model_fit = model.fit(disp=0)
print(model_fit.summary())

# Plot residual errors
residuals = pd.DataFrame(model_fit.resid)
residuals.plot(title="Residuals")
residuals.plot(kind='kde', title='Density')
plt.show()

# Actual vs Fitted
model_fit.plot_predict(dynamic=False)
plt.show()




