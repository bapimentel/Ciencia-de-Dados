# Estudo de caso 1 - Reclamacoes por perdas (TSA). Passo 7: qual o efeito de ordenar a fila pelo modelo?
# O passo 6 mostrou que o modelo coloca mais casos pagos no inicio da fila. Aqui medimos a CONSEQUENCIA disso
# em dias de espera, simulando a fila de analise de julho a outubro de 2015 (meses que o modelo nao viu):
#   - cada reclamacao entra na fila no dia em que foi recebida;
#   - a equipe analisa C reclamacoes por dia;
#   - politica atual: ordem de chegada; politica proposta: maior probabilidade de pagamento primeiro,
#     com um teto: quem espera 30 dias passa a frente de todos.
# Novembro e dezembro ficam de fora: muitos casos desses meses ainda nao tinham desfecho na base (passo 1).
# A ordem de analise nao muda o desfecho de cada caso (quem tem direito recebe de qualquer forma); muda QUANDO.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
dados = pd.read_csv(os.path.join(pasta, 'dados', 'reclamacoes_preparadas.csv'), parse_dates=['Date Received'])
variaveis = ['Claim Type', 'Claim Site', 'Airline Name', 'Item Category (agrupada)', 'Dias ate registrar']
X = pd.get_dummies(dados[variaveis], dtype=int)
paga = 1 - dados['Negada']
treino = dados['Mes'] <= 6
teste = dados['Mes'].between(7, 10)
modelo = RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=0).fit(X[treino], paga[treino])

fila = dados[teste].copy()
fila['prob'] = modelo.predict_proba(X[teste])[:, 1]
fila['paga'] = paga[teste].values
fila['dia'] = (fila['Date Received'] - fila['Date Received'].min()).dt.days
print(f'Reclamacoes de julho a outubro: {len(fila)} | chegadas por dia: {len(fila) / (fila["dia"].max() + 1):.1f}')


def simular(capacidade, politica, teto=30):
    chegadas = fila.groupby('dia').groups
    espera, aguardando, dia = {}, [], 0
    while len(espera) < len(fila):
        aguardando.extend(chegadas.get(dia, []))
        if politica == 'ordem de chegada':
            aguardando.sort(key=lambda i: (fila.at[i, 'dia'], i))
        else:
            aguardando.sort(key=lambda i: (dia - fila.at[i, 'dia'] < teto, -fila.at[i, 'prob']))
        atendidos, aguardando = aguardando[:capacidade], aguardando[capacidade:]
        for i in atendidos:
            espera[i] = dia - fila.at[i, 'dia']
        dia += 1
    return pd.Series(espera).reindex(fila.index)


def resumo(espera):
    pg = fila['paga'] == 1
    valor = fila.loc[pg, 'Close Amount']
    return {'espera media, pagas': espera[pg].mean(), 'espera media, negadas': espera[~pg].mean(),
            'espera ponderada pelo valor pago': (espera[pg] * valor).sum() / valor.sum(), 'maior espera': espera.max()}


linhas = []
for capacidade in [12, 13, 14, 15]:
    atual = resumo(simular(capacidade, 'ordem de chegada'))
    proposta = resumo(simular(capacidade, 'modelo'))
    linhas.append({'capacidade/dia': capacidade, **{f'{k} (atual)': v for k, v in atual.items()},
                   **{f'{k} (modelo)': v for k, v in proposta.items()}})
tabela = pd.DataFrame(linhas).set_index('capacidade/dia')
for k in ['espera media, pagas', 'espera media, negadas', 'espera ponderada pelo valor pago']:
    tabela[f'{k}: variacao'] = tabela[f'{k} (modelo)'] / tabela[f'{k} (atual)'] - 1
pd.set_option('display.width', 200)
print(tabela.round(2).T.to_string())

# Cenario principal: 13 analises por dia
c = 13
e_atual, e_modelo = simular(c, 'ordem de chegada'), simular(c, 'modelo')
pg = fila['paga'] == 1
dolar_dia_atual = (e_atual[pg] * fila.loc[pg, 'Close Amount']).sum()
dolar_dia_modelo = (e_modelo[pg] * fila.loc[pg, 'Close Amount']).sum()
print(f'\nCenario principal ({c}/dia): {pg.sum()} casos pagos, US$ {fila.loc[pg, "Close Amount"].sum():,.0f} pagos')
print(f'  espera media dos casos pagos: {e_atual[pg].mean():.1f} -> {e_modelo[pg].mean():.1f} dias')
print(f'  dinheiro x dias de espera ate o pagamento: {dolar_dia_atual:,.0f} -> {dolar_dia_modelo:,.0f} US$.dia '
      f'({dolar_dia_modelo / dolar_dia_atual - 1:+.0%})')
print(f'  espera media dos casos negados: {e_atual[~pg].mean():.1f} -> {e_modelo[~pg].mean():.1f} dias; '
      f'maior espera: {e_atual.max():.0f} -> {e_modelo.max():.0f} dias (teto de 30)')
sem_teto = simular(c, 'modelo', teto=10 ** 6)
print(f'  sem o teto, a maior espera seria {sem_teto.max():.0f} dias')
print('\nEscolha do teto (capacidade 13/dia): teto | espera das pagas | espera das negadas | maior espera')
for teto in [14, 20, 30]:
    e = simular(c, 'modelo', teto)
    print(f'  {teto:4d} | {e[pg].mean() / e_atual[pg].mean() - 1:+.0%} | {e[~pg].mean() / e_atual[~pg].mean() - 1:+.0%} | {e.max():.0f} dias')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.4))
cap = tabela.index.astype(str)
x = np.arange(len(cap))
esq.bar(x - 0.2, tabela['espera media, pagas (atual)'], width=0.4, color='#8794A3', label='ordem de chegada')
esq.bar(x + 0.2, tabela['espera media, pagas (modelo)'], width=0.4, color='#2F648F', label='ordenada pelo modelo (teto 30 dias)')
for i, v in enumerate(tabela['espera media, pagas: variacao']):
    esq.text(i + 0.2, tabela['espera media, pagas (modelo)'].iloc[i] + 0.3, f'{v:+.0%}', ha='center', fontsize=9)
esq.set_xticks(x, [f'{c}/dia' for c in cap])
esq.set_xlabel('Capacidade de análise da equipe')
esq.set_ylabel('Dias de espera (média)')
esq.set_title('Casos que terminam pagos esperam menos em qualquer capacidade', fontsize=11)
esq.legend()
bins = np.arange(0, 32, 2)
dir.hist(e_atual[pg], bins=bins, color='#8794A3', alpha=0.7, label='pagas, ordem de chegada')
dir.hist(e_modelo[pg], bins=bins, color='#2F648F', alpha=0.7, label='pagas, ordenada pelo modelo')
dir.set_xlabel('Dias de espera')
dir.set_ylabel('Reclamações pagas')
dir.set_title(f'Capacidade de {c}/dia: distribuição da espera dos casos pagos', fontsize=11)
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '07_simulacao_da_fila.png'))
plt.show()
