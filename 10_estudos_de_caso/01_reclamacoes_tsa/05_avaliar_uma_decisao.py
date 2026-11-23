# Estudo de caso 1 - Reclamacoes por perdas (TSA). Etapa 5: que decisao os dados sustentam?
# Candidata: usar o modelo para ORDENAR a fila de revisao humana (casos com maior chance de pagamento
# primeiro), e nao para decidir pedidos. Avaliamos o que isso renderia e como medir depois.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'))

variaveis = ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)', 'Dias ate registrar', 'Mes']
X = pd.get_dummies(dados[variaveis], dtype=int)
y_paga = (dados['Negada'] == 0).astype(int)             # 1 = teve pagamento (aprovada ou acordo)
X_tr, X_te, y_tr, y_te = train_test_split(X, y_paga, test_size=0.3, random_state=0, stratify=y_paga)
modelo = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, random_state=0).fit(X_tr, y_tr)
prob = modelo.predict_proba(X_te)[:, 1]

# Se a equipe revisar primeiro os X% com maior probabilidade de pagamento, que fracao dos pagamentos encontra?
ordem = np.argsort(-prob)
y_ordenado = y_te.values[ordem]
fracoes = np.arange(0.1, 1.01, 0.1)
linhas = []
for f in fracoes:
    k = int(f * len(y_ordenado))
    encontrados = y_ordenado[:k].sum()
    linhas.append({'fila revisada': f'{f:.0%}', 'casos': k, 'pagamentos encontrados': int(encontrados),
                   'fracao dos pagamentos': encontrados / y_ordenado.sum(), 'ao acaso': f})
tabela = pd.DataFrame(linhas)
print(tabela.to_string(index=False, float_format=lambda v: f'{v:.2f}'))

fig, eixo = plt.subplots(figsize=(6.5, 4.2))
eixo.plot(100 * fracoes, 100 * tabela['fracao dos pagamentos'], marker='o', color='#2F648F', label='ordenando pelo modelo')
eixo.plot(100 * fracoes, 100 * fracoes, linestyle='--', color='#8794A3', label='ordem aleatória')
eixo.set_xlabel('% da fila revisada primeiro')
eixo.set_ylabel('% dos casos com pagamento já encontrados')
eixo.set_title('Revisar 50% da fila pelo modelo encontra ~60% dos pagamentos')
eixo.legend(loc='lower right')
plt.savefig(os.path.join(pasta, 'figuras', '05_ganho_na_fila.png'))
plt.show()

metade = tabela.iloc[4]
print(f'\nCom 50% da fila: {metade["fracao dos pagamentos"]:.0%} dos pagamentos, contra 50% ao acaso.')

# O que os dados sustentam e o que nao sustentam:
print('''
Achado: a taxa de negativa varia com o local (inspecao x bagagem despachada), a categoria do item e o
tempo entre o incidente e o registro. Um modelo com essas variaveis supera a linha de base, mas pouco:
boa parte do desfecho depende de informacoes que a base nao traz.

Decisao candidata: ordenar a fila de revisao humana pela probabilidade de pagamento, para que os casos
com mais chance de ressarcimento sejam analisados antes. Ninguem e negado pelo modelo.

Evidencia: no teste, revisar metade da fila na ordem do modelo alcanca cerca de 60% dos pagamentos,
contra 50% ao acaso. O ganho e modesto; a decisao so vale se o custo de reordenar for baixo.

Como avaliar (proposta, nao resultado): apos 3 meses, comparar o tempo mediano ate o pagamento dos
casos pagos (metrica principal) com o trimestre anterior, acompanhando a taxa de negativa e o tempo
mediano dos casos negados (metricas auxiliares, para verificar que ninguem ficou para tras). Criterio
proposto de sucesso: queda do tempo mediano ate o pagamento sem aumento do tempo dos demais casos.

Limites: a base cobre 2015, cinco companhias e so casos com desfecho; nao ha valor pedido nem evidencias;
"dias ate registrar" pode refletir regras de prazo. Correlacoes aqui nao dizem por que um caso e negado.
''')
