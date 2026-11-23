# Analise de sobrevivencia: tempo ate um evento, com censura.
# Parte 1: 8 equipamentos (dados ilustrativos) e a curva de Kaplan-Meier calculada a mao.
# Parte 2: dois grupos simulados com semente fixa e o teste log-rank.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.duration.survfunc import SurvfuncRight, survdiff

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Parte 1. Tempo (meses) e status: 1 = falhou, 0 = censurado (o estudo acabou antes da falha)
equipamentos = pd.DataFrame({'tempo': [2, 3, 4, 6, 7, 8, 10, 11], 'falhou': [1, 0, 1, 1, 0, 1, 1, 0]})
print(equipamentos)

# Erro comum 1: ignorar os censurados -> so 5 equipamentos, todos "falharam" (pessimista)
# Erro comum 2: tratar censura como falha -> 8 falhas (mais pessimista ainda)
print('Media ingenua do tempo ate falha, so com quem falhou:', equipamentos.loc[equipamentos['falhou'] == 1, 'tempo'].mean())

# Kaplan-Meier: em cada tempo de falha, S(t) = S(anterior) x (1 - falhas / em risco)
sobrevivencia = 1.0
em_risco = len(equipamentos)
linhas = []
for _, linha in equipamentos.sort_values('tempo').iterrows():
    if linha['falhou'] == 1:
        sobrevivencia = sobrevivencia * (1 - 1 / em_risco)
        linhas.append({'tempo': linha['tempo'], 'em risco': em_risco, 'falhas': 1, 'S(t)': round(sobrevivencia, 3)})
    em_risco -= 1          # quem falhou ou foi censurado sai do grupo em risco
print('\nKaplan-Meier calculado a mao:')
print(pd.DataFrame(linhas))

km = SurvfuncRight(equipamentos['tempo'], equipamentos['falhou'])
print('\nConferencia com statsmodels:')
print(km.summary())

# --- Parte 2. Dois tratamentos (simulados): tempos exponenciais com riscos diferentes, censura ao fim de 12 meses
gerador = np.random.default_rng(4)
n = 60
tempo_a = gerador.exponential(18, size=n)          # risco menor
tempo_b = gerador.exponential(9, size=n)           # risco maior
fim_do_estudo = 12
grupos = pd.DataFrame({
    'tempo': np.concatenate([np.minimum(tempo_a, fim_do_estudo), np.minimum(tempo_b, fim_do_estudo)]),
    'evento': np.concatenate([(tempo_a <= fim_do_estudo).astype(int), (tempo_b <= fim_do_estudo).astype(int)]),
    'grupo': ['A'] * n + ['B'] * n,
})
print('\nEventos observados por grupo:')
print(grupos.groupby('grupo')['evento'].agg(['sum', 'count']))
estatistica, p = survdiff(grupos['tempo'], grupos['evento'], grupos['grupo'])
print(f'Teste log-rank: qui2 = {estatistica:.2f}, p = {p:.4f}')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2))
tempos = [0] + [l['tempo'] for l in linhas]
valores = [1] + [l['S(t)'] for l in linhas]
esq.step(tempos + [11], valores + [valores[-1]], where='post', color='#2F648F', linewidth=2)
censurados = equipamentos[equipamentos['falhou'] == 0]
for t in censurados['tempo']:
    s = valores[max(i for i, tt in enumerate(tempos) if tt <= t)]
    esq.plot(t, s, marker='+', markersize=14, color='#D69A35', markeredgewidth=2)
esq.set_ylim(0, 1.05)
esq.set_xlabel('Meses')
esq.set_ylabel('Probabilidade de ainda não ter falhado')
esq.set_title('Kaplan–Meier: degraus nas falhas, + nas censuras')
for nome, cor in [('A', '#2F648F'), ('B', '#168A8A')]:
    sub = grupos[grupos['grupo'] == nome]
    curva = SurvfuncRight(sub['tempo'], sub['evento'])
    dir.step(np.concatenate([[0], curva.surv_times]), np.concatenate([[1], curva.surv_prob]), where='post', color=cor, linewidth=2,
             label=f'tratamento {nome}')
dir.set_ylim(0, 1.05)
dir.set_xlabel('Meses')
dir.set_ylabel('Probabilidade de sobrevivência')
dir.set_title('Dois grupos simulados: log-rank p < 0,001' if p < 0.001 else f'Dois grupos simulados: log-rank p = {p:.3f}')
dir.legend()
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'sobrevivencia.png'))
plt.show()

# Onde isso aparece na pratica: tempo ate o cliente cancelar (churn), ate a maquina falhar, ate o aluno
# evadir, ate o emprestimo ficar inadimplente. Em todos, quem ainda nao teve o evento e censurado, nao ignorado.
