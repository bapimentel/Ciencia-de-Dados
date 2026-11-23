# Da regra escrita a mao ao modelo aprendido, e os tipos de aprendizado.
# Parte 1 (dados simulados, semente fixa): um diagnostico com uma variavel (temperatura), depois com duas
# (temperatura e batimentos), depois com um padrao que nenhuma regra simples descreve.
# Parte 2: a mesma nuvem de pontos vista como classificacao, regressao e agrupamento.

import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.cluster import KMeans

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
gerador = np.random.default_rng(2)
cores = np.array(['#2F648F', '#BD5B58'])

# --- Parte 1. Pacientes simulados: saudaveis e doentes
n = 120
saudavel = np.column_stack([gerador.normal(36.6, 0.35, n), gerador.normal(72, 8, n)])
doente = np.column_stack([gerador.normal(37.6, 0.45, n), gerador.normal(92, 10, n)])
X = np.vstack([saudavel, doente])
y = np.array([0] * n + [1] * n)

# Regra 1, escrita a mao: "se temperatura > c, entao doente". Testamos varios c e ficamos com o melhor.
cortes = np.arange(36.0, 38.5, 0.05)
acertos = [((X[:, 0] > c).astype(int) == y).mean() for c in cortes]
melhor_c = cortes[int(np.argmax(acertos))]
print(f'Regra de uma variavel: temperatura > {melhor_c:.2f} -> acerto {max(acertos):.1%}')

# Regra 2, aprendida: "se a*temperatura + b*batimentos + c > 0, entao doente" (uma reta no plano)
modelo = LogisticRegression().fit(X, y)
print(f'Reta aprendida com duas variaveis -> acerto {modelo.score(X, y):.1%}')

# Padrao 3: doentes com febre OU com batimentos muito altos, mas nao os dois (nenhuma reta separa)
gerador2 = np.random.default_rng(9)
Z = np.column_stack([gerador2.normal(37, 0.7, 300), gerador2.normal(82, 14, 300)])
febre = Z[:, 0] > 37.2
taquicardia = Z[:, 1] > 88
rotulo_xor = (febre ^ taquicardia).astype(int)
print(f'Padrao "ou exclusivo": uma reta acerta so {LogisticRegression().fit(Z, rotulo_xor).score(Z, rotulo_xor):.1%}'
      ' -> e preciso um modelo mais flexivel (arvores, unidade 12; redes neurais, unidade 13)')

fig, eixos = plt.subplots(1, 3, figsize=(14, 4.2))
eixos[0].scatter(X[:, 0], np.zeros(len(X)) + gerador.uniform(-0.3, 0.3, len(X)), c=cores[y], s=10, alpha=0.6)
eixos[0].axvline(melhor_c, color='#D69A35', linewidth=2)
eixos[0].set_yticks([])
eixos[0].set_xlabel('Temperatura (°C)')
eixos[0].set_title(f'1. Uma variável: "se T > {melhor_c:.1f}"\nacerta {max(acertos):.0%}', fontsize=11)
eixos[1].scatter(X[:, 0], X[:, 1], c=cores[y], s=10, alpha=0.6)
xs = np.linspace(X[:, 0].min(), X[:, 0].max(), 50)
w, b = modelo.coef_[0], modelo.intercept_[0]
eixos[1].plot(xs, -(w[0] * xs + b) / w[1], color='#D69A35', linewidth=2)
eixos[1].set_ylim(X[:, 1].min() - 5, X[:, 1].max() + 5)
eixos[1].set_xlabel('Temperatura (°C)')
eixos[1].set_ylabel('Batimentos por minuto')
eixos[1].set_title(f'2. Duas variáveis: uma reta aprendida\nacerta {modelo.score(X, y):.0%}', fontsize=11)
eixos[2].scatter(Z[:, 0], Z[:, 1], c=cores[rotulo_xor], s=10, alpha=0.6)
eixos[2].axvline(37.2, color='#8794A3', linestyle='--', linewidth=1)
eixos[2].axhline(88, color='#8794A3', linestyle='--', linewidth=1)
eixos[2].set_xlabel('Temperatura (°C)')
eixos[2].set_title('3. Padrão que nenhuma reta separa:\nprecisa de um modelo mais flexível', fontsize=11)
eixos[0].text(0.02, 0.92, '● saudável', color='#2F648F', transform=eixos[0].transAxes)
eixos[0].text(0.02, 0.84, '● doente', color='#BD5B58', transform=eixos[0].transAxes)
fig.suptitle('Dados simulados: da regra escrita à mão ao modelo aprendido', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'da_regra_ao_modelo.png'))
plt.show()

# --- Parte 2. Tipos de aprendizado com os mesmos pacientes
fig, eixos = plt.subplots(1, 3, figsize=(14, 4.2))
eixos[0].scatter(X[:, 0], X[:, 1], c=cores[y], s=10, alpha=0.6)
eixos[0].set_title('Supervisionado, classificação:\ncada ponto tem um rótulo (doente ou não)', fontsize=11)
reg = LinearRegression().fit(X[:, [0]], X[:, 1])
eixos[1].scatter(X[:, 0], X[:, 1], color='#2F648F', s=10, alpha=0.5)
eixos[1].plot(xs, reg.predict(xs.reshape(-1, 1)), color='#D69A35', linewidth=2)
eixos[1].set_title('Supervisionado, regressão:\nprever um número (batimentos) a partir de outro', fontsize=11)
grupos = KMeans(n_clusters=2, n_init=10, random_state=0).fit_predict(X / X.std(axis=0))
eixos[2].scatter(X[:, 0], X[:, 1], c=np.array(['#168A8A', '#D69A35'])[grupos], s=10, alpha=0.6)
eixos[2].set_title('Não supervisionado, agrupamento:\nsem rótulos, o algoritmo propõe grupos', fontsize=11)
for eixo in eixos:
    eixo.set_xlabel('Temperatura (°C)')
eixos[0].set_ylabel('Batimentos por minuto')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'tipos_de_aprendizado.png'))
plt.show()
