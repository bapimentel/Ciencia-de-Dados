# Teste de hipoteses, intervalo de confianca e tamanho do efeito.
# Baseado nos trechos "Exemplo" (ttest_ind) e "Intervalo de confianca" de estatistica.py (2019).

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

# --- Exemplo original: acuracia de dois metodos em 6 execucoes
metodo1 = [0.70, 0.75, 0.69, 0.76, 0.81, 0.85]
metodo2 = [0.73, 0.70, 0.63, 0.61, 0.52, 0.70]
estatistica, valor_p = stats.ttest_ind(metodo1, metodo2)
print(f'Teste t (metodos): t={estatistica:.3f}, p={valor_p:.4f}')
print('Medias:', np.mean(metodo1), round(np.mean(metodo2), 3))
# Se p < 0.05, costuma-se dizer que a diferenca de medias e "estatisticamente significativa".
# Isso NAO diz se a diferenca e grande o bastante para importar na pratica.

# Tamanho do efeito (d de Cohen): diferenca de medias em unidades de desvio-padrao
def d_cohen(a, b):
    a, b = np.asarray(a), np.asarray(b)
    desvio_comum = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return (a.mean() - b.mean()) / desvio_comum

print('d de Cohen (metodos):', round(d_cohen(metodo1, metodo2), 2))

# --- Dados reais: clientes com cartao de fidelidade (Member) gastam mais que os outros (Normal)?
dados = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
membro = dados.loc[dados['Customer type'] == 'Member', 'Total']
normal = dados.loc[dados['Customer type'] == 'Normal', 'Total']
print(f'\nMember: n={len(membro)} media={membro.mean():.2f}   Normal: n={len(normal)} media={normal.mean():.2f}')

# Teste t de Welch (nao assume variancias iguais)
t, p = stats.ttest_ind(membro, normal, equal_var=False)
print(f'Teste t de Welch: t={t:.3f}, p={p:.3f}')

# Mann-Whitney: alternativa que nao depende de normalidade (os totais sao assimetricos)
u, p_mw = stats.mannwhitneyu(membro, normal)
print(f'Mann-Whitney: U={u:.0f}, p={p_mw:.3f}')
print('d de Cohen:', round(d_cohen(membro, normal), 3))
# Diferenca de ~7 unidades em medias de ~320, p ~0.6: nada aqui sustenta afirmar que membros gastam mais.

# --- Intervalo de confianca para a media (t de Student)
def intervalo_confianca(valores, confianca=0.95):
    valores = np.asarray(valores)
    erro_padrao = stats.sem(valores)
    margem = erro_padrao * stats.t.ppf((1 + confianca) / 2, len(valores) - 1)
    return valores.mean() - margem, valores.mean() + margem

print('\nIC 95% da media (Member):', [round(float(v), 1) for v in intervalo_confianca(membro)])
print('IC 95% da media (Normal):', [round(float(v), 1) for v in intervalo_confianca(normal)])
# Os intervalos se sobrepoem bastante: coerente com o teste.

# --- Exemplo original dos materiais: medias com barras de erro
aluminio = np.array([6.4, 3.01, 2.36, 3.0, 7.0, 4.5, 3.8, 4.2, 2.62, 3.6])
cobre = np.array([4.5, 1.97, 1.6, 1.97, 4.0, 2.4, 1.9, 2.41, 1.85, 3.3])
aco = np.array([3.3, 1.2, 0.9, 1.2, 1.3, 1.6, 1.4, 1.58, 1.32, 2.1])
materiais = ['Alumínio', 'Cobre', 'Aço']
medias = [aluminio.mean(), cobre.mean(), aco.mean()]
# A versao de 2019 usava o desvio-padrao como barra de erro. Aqui usamos a metade do IC 95% da media,
# que e o que interessa para comparar medias.
margens = [(intervalo_confianca(m)[1] - intervalo_confianca(m)[0]) / 2 for m in [aluminio, cobre, aco]]

fig, eixo = plt.subplots(figsize=(6, 3.8))
eixo.bar(materiais, medias, yerr=margens, capsize=8, color='#2F648F', ecolor='#20324A')
eixo.set_ylabel('Coeficiente de expansão térmica')
eixo.set_title('Médias de 10 medições com intervalo de confiança de 95%')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'intervalos_materiais.png'))
plt.show()

# Experimente: compare o Rating entre Gender == 'Female' e 'Male'.
# Antes de rodar, escreva qual resultado voce espera e por que.
