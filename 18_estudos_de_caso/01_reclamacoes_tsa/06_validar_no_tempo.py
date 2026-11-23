# Estudo de caso 1 - Reclamacoes por perdas (TSA). Passo 6: o achado se sustenta em meses que o modelo nao viu?
# Antes de recomendar qualquer uso do modelo, simulamos o uso real: treinar com as reclamacoes recebidas
# de janeiro a junho e aplicar nas recebidas de julho a dezembro.
# Uso avaliado: ORDENAR a fila de revisao (casos com maior probabilidade de pagamento primeiro).
# Medida: que fracao dos casos que terminam pagos aparece na primeira metade da fila (ao acaso: 50%).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'))
variaveis = ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)', 'Dias ate registrar']
X = pd.get_dummies(dados[variaveis], dtype=int)
paga = 1 - dados['Negada']
treino = dados['Mes'] <= 6
teste = ~treino
print(f'Treino (jan-jun): {treino.sum()} casos, {paga[treino].mean():.1%} pagos | '
      f'Teste (jul-dez): {teste.sum()} casos, {paga[teste].mean():.1%} pagos')

modelos = {'floresta': RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=0),
           'regressão logística': LogisticRegression(max_iter=3000)}
probs = {}
for nome, modelo in modelos.items():
    modelo.fit(X[treino], paga[treino])
    probs[nome] = modelo.predict_proba(X[teste])[:, 1]
    print(f'{nome}: AUC nos meses futuros = {roc_auc_score(paga[teste], probs[nome]):.3f}')


def fracao_encontrada(y, prob, fracao):
    ordem = np.argsort(-prob)
    k = int(round(fracao * len(y)))
    return y[ordem][:k].sum() / y.sum()


y_teste = paga[teste].values
fracoes = np.linspace(0.1, 1, 10)
curva = {nome: [fracao_encontrada(y_teste, p, f) for f in fracoes] for nome, p in probs.items()}
print('\n% da fila revisada | % dos pagos encontrados (floresta) | (logistica) | ao acaso')
for f, a, b in zip(fracoes, curva['floresta'], curva['regressão logística']):
    print(f'{f:17.0%} | {a:33.0%} | {b:11.0%} | {f:.0%}')

# Variacao mes a mes: o indicador que seria acompanhado na pratica
print('\nMes de teste | casos | pagos | % dos pagos na 1a metade da fila (floresta)')
mensal = []
meses_teste = dados.loc[teste, 'Mes'].values
for mes in range(7, 13):
    sel = meses_teste == mes
    valor = fracao_encontrada(y_teste[sel], probs['floresta'][sel], 0.5)
    mensal.append(valor)
    print(f'{mes:12d} | {sel.sum():5d} | {y_teste[sel].sum():5d} | {valor:.0%}')

# Reamostragem do periodo de teste para um intervalo de confianca da medida principal
gerador = np.random.default_rng(0)
reamostras = []
for _ in range(2000):
    idx = gerador.integers(0, len(y_teste), len(y_teste))
    reamostras.append(fracao_encontrada(y_teste[idx], probs['floresta'][idx], 0.5))
ic = np.percentile(reamostras, [2.5, 97.5])
metade = fracao_encontrada(y_teste, probs['floresta'], 0.5)
print(f'\nPrimeira metade da fila (floresta): {metade:.1%} dos pagos (IC 95% bootstrap {ic[0]:.1%} a {ic[1]:.1%}); ao acaso, 50%')

# Quem fica para o fim da fila? Composicao dos 25% de menor probabilidade
fim = probs['floresta'] <= np.quantile(probs['floresta'], 0.25)
print('\nCategoria do item: participacao no fim da fila (25% menores probabilidades) x no total do teste')
comp = pd.DataFrame({'fim da fila': dados.loc[teste, 'Item Category (agrupada)'][fim].value_counts(normalize=True),
                     'total': dados.loc[teste, 'Item Category (agrupada)'].value_counts(normalize=True)}).fillna(0)
comp['razao'] = comp['fim da fila'] / comp['total']
print(comp.sort_values('razao', ascending=False).round(2).to_string())
# Quem tem menor chance prevista de pagamento esperaria mais. Isso precisa ser vigiado (ver README).

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.4))
esq.plot(100 * fracoes, 100 * np.array(curva['floresta']), marker='o', color='#2F648F', label='floresta')
esq.plot(100 * fracoes, 100 * np.array(curva['regressão logística']), marker='o', color='#168A8A', label='regressão logística')
esq.plot(100 * fracoes, 100 * fracoes, linestyle='--', color='#8794A3', label='ordem de chegada (ao acaso)')
esq.set_xlabel('% da fila revisada primeiro')
esq.set_ylabel('% dos casos pagos já encontrados')
esq.set_title('Meses futuros (jul-dez): ordenar pelo modelo antecipa os pagos', fontsize=11)
esq.legend(loc='lower right')
dir.bar(['jul', 'ago', 'set', 'out', 'nov', 'dez'], 100 * np.array(mensal), color='#2F648F')
dir.axhline(50, color='#8794A3', linestyle='--')
dir.text(-0.45, 46, 'ao acaso', color='#8794A3', ha='left', va='top')
for i, v in enumerate(mensal):
    dir.text(i, 100 * v + 1, f'{100 * v:.0f}%', ha='center')
dir.set_ylim(0, 100)
dir.set_ylabel('% dos pagos na 1ª metade da fila')
dir.set_title('O ganho se repete em cada mês do período de teste', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '06_validacao_no_tempo.png'))
plt.show()
