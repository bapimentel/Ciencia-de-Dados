# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 13:25:55 2019

@author: Bruno Pimentel
"""

import numpy as np
import matplotlib.pyplot as plt

# Grafico de barras
from matplotlib.ticker import FuncFormatter
x = np.arange(4)
money = [1.5e5, 2.5e6, 5.5e6, 2.0e7]
def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fM' % (x * 1e-6)

formatter = FuncFormatter(millions)

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(formatter)
plt.bar(x, money)
plt.xticks(x, ('Bill', 'Fred', 'Mary', 'Sue'))
plt.show()



# Grafico de pizza
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()



# Histograma
mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)
n, bins, patches = plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)
plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.xlim(40, 160)
plt.ylim(0, 0.03)
plt.grid(True)
plt.show()



# Grafico de linha
t = np.arange(0.0, 2.0, 0.05)
s = 1 + np.sin(2 * np.pi * t)
fig, ax = plt.subplots()
ax.plot(t, s, '-o')
ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='Line gragh')
ax.grid()
plt.show()



# Grafico de dispersao
from sklearn.datasets import load_iris
iris = load_iris()
x_index = 0
y_index = 1
# this formatter will label the colorbar with the correct target names
formatter = plt.FuncFormatter(lambda i, *args: iris.target_names[int(i)])
plt.figure(figsize=(5, 4))
plt.scatter(iris.data[:, x_index], iris.data[:, y_index], c=iris.target)
plt.colorbar(ticks=[0, 1, 2], format=formatter)
plt.xlabel(iris.feature_names[x_index])
plt.ylabel(iris.feature_names[y_index])
plt.tight_layout()
plt.show()


# Medidas
import statistics
from scipy import stats as st
media = statistics.mean(x)
media2 = sum(x)/len(x)
mediana = statistics.median(x)
amplitude = max(x) - min(x)
variancia = statistics.variance(x)
desvio_padrao = statistics.stdev(x)
coeficente_variacao = st.variation(x)



# Quartil
q1 = np.quantile(x, 0.25)
q2 = np.quantile(x, 0.50)
q3 = np.quantile(x, 0.75)



# Boxplot
plt.title('Boxplot')
plt.boxplot(x, vert=False)
plt.show()



# Distribuicao Normal
import math
SQRT_TWO_PI = math.sqrt(2 * math.pi)
def normal_pdf(x, mu=0, sigma=1):
    return (math.exp(-(x-mu) ** 2 / 2 / sigma ** 2) / (SQRT_TWO_PI * sigma))

xs = [a / 10.0 for a in range(-50, 50)]
plt.plot(xs,[normal_pdf(a,sigma=1) for a in xs],'-',label='mu=0,sigma=1')
plt.plot(xs,[normal_pdf(a,sigma=2) for a in xs],'--',label='mu=0,sigma=2')
plt.plot(xs,[normal_pdf(a,sigma=0.5) for a in xs],':',label='mu=0,sigma=0.5')
plt.plot(xs,[normal_pdf(a,mu=-1)   for a in xs],'-.',label='mu=-1,sigma=1')
plt.legend()
plt.title("Various Normal pdfs")
plt.show()

# Exemplo
from scipy.stats import ttest_ind
metodo1 = [0.70, 0.75, 0.69, 0.76, 0.81, 0.85]
metodo2 = [0.73, 0.70, 0.63, 0.61, 0.52, 0.70]
stat, pvalue = ttest_ind(metodo1,metodo2)

# Teste de normalidade
import numpy as np
# Generacao de amostra de uma normal (media=50, desvio=5)
gauss_data = 5 * np.random.randn(100) + 50
print('media=%.3f desvio=%.3f' % (np.mean(gauss_data), np.std(gauss_data)))
# Histograma
plt.hist(gauss_data)
# QQ-plot
from statsmodels.graphics.gofplots import qqplot
qqplot_data = qqplot(gauss_data, line='s').gca().lines
# Teste Shapiro-Wilk
from scipy.stats import shapiro
stat, pvalue = shapiro(gauss_data)

# Generacao de amostra de uma uniforme
uniform = np.random.uniform(low=-2, high=2, size=100)
# Histograma
plt.hist(uniform)
# QQ-plot
qqplot_data = qqplot(uniform, line='s').gca().lines
# Teste Shapiro-Wilk
stat, pvalue = shapiro(uniform)

