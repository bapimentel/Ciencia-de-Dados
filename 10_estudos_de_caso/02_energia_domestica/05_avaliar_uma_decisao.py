# Estudo de caso 2 - Energia domestica. Etapa 5: recomendacao de uso (livro, secao 12.4).
# O analise.py original estimava a reducao do "valor" para reducoes de 0 a 90% do uso com um RandomForest.
# Como a tarifa e praticamente constante (script 02), essa relacao e aritmetica: reduzir x% do kWh reduz
# x% do custo. O que vale a pena calcular e ONDE o consumo esta (faixa horaria) e quanto uma mudanca
# de habito nessa faixa representaria, como CENARIO, e como se testaria isso de verdade.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))

horario = pd.read_csv(os.path.join(pasta, 'dados', 'energia_por_hora.csv'), index_col=0, parse_dates=True)
dias = (horario.index.max() - horario.index.min()).days + 1
tarifa = horario['Custo'].sum() / horario['Consumo_kWh'].sum()
print(f'Periodo: {dias} dias | tarifa media US$ {tarifa:.3f}/kWh')

# Onde esta o consumo: faixa da noite (18-23h)
horario['Hora'] = horario.index.hour
noite = horario[horario['Hora'].between(18, 23)]
parte_noite = noite['Consumo_kWh'].sum() / horario['Consumo_kWh'].sum()
kwh_ano = horario['Consumo_kWh'].sum() / dias * 365
custo_ano = kwh_ano * tarifa
print(f'Consumo anualizado: {kwh_ano:.0f} kWh (US$ {custo_ano:.0f}); a noite (18-23h) responde por {parte_noite:.0%}')

# Cenarios (nao previsoes): reduzir a faixa da noite em 10%, 20% e 30%
print('\nCenarios aritmeticos de reducao do consumo noturno:')
linhas = []
for reducao in [0.10, 0.20, 0.30]:
    kwh_economizado = kwh_ano * parte_noite * reducao
    linhas.append({'redução na noite': f'{reducao:.0%}', 'kWh/ano economizados': round(kwh_economizado),
                   'US$/ano': round(kwh_economizado * tarifa), '% da conta': f'{kwh_economizado / kwh_ano:.1%}'})
print(pd.DataFrame(linhas).to_string(index=False))

# Como seria um teste honesto da mudanca de habito
# Semanas sao a unidade natural (o padrao semanal e forte). Comparamos a variabilidade entre semanas
# do mesmo mes para saber que tamanho de efeito seria detectavel.
semanal = horario['Consumo_kWh'].resample('W').sum()
semanal = semanal[(semanal.index > semanal.index.min()) & (semanal.index < semanal.index.max())]   # semanas completas
variacao = semanal.groupby(semanal.index.month).std().mean()
media_semana = semanal.mean()
print(f'\nConsumo semanal medio: {media_semana:.0f} kWh; variacao tipica entre semanas do mesmo mes: {variacao:.0f} kWh ({variacao / media_semana:.0%})')
# Uma reducao de 10% na noite equivale a cerca de 3-4% da semana: menor que a variacao natural entre
# semanas. Para detecta-la, seria preciso comparar varias semanas antes e depois, na mesma estacao,
# e de preferencia registrar a temperatura externa, que a base nao tem.

fig, (esq, dir) = plt.subplots(1, 2, figsize=(11, 3.8))
faixas = pd.cut(horario['Hora'], bins=[-1, 5, 11, 17, 23], labels=['madrugada', 'manhã', 'tarde', 'noite'])
participacao = horario.groupby(faixas, observed=True)['Consumo_kWh'].sum() / horario['Consumo_kWh'].sum()
cores = ['#8794A3', '#8794A3', '#8794A3', '#2F648F']
esq.bar(participacao.index.astype(str), 100 * participacao.values, color=cores)
for i, v in enumerate(participacao.values):
    esq.text(i, 100 * v + 1, f'{v:.0%}', ha='center')
esq.set_ylabel('% do consumo total')
esq.set_title(f'A noite (18–23h) concentra {parte_noite:.0%} do consumo')
esq.set_ylim(0, 50)
dir.plot(semanal.index, semanal.values, color='#2F648F', linewidth=1)
dir.axhline(media_semana, color='#8794A3', linestyle='--')
dir.fill_between(semanal.index, media_semana - variacao, media_semana + variacao, color='#E6EBF0')
dir.set_ylabel('kWh por semana')
dir.set_title('Variação natural entre semanas (faixa cinza): a meta tem de ser maior que ela')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '05_cenarios_e_variacao.png'))
plt.show()

print('''
Achado: o consumo se concentra a noite (18-23h) todos os dias da semana e sobe no inverno; a tarifa e
constante, entao custo e consumo andam juntos.
Isso sugere que uma mudanca de habito concentrada na noite (deslocar lavanderia e cozimento, revisar
aquecimento) e onde ha mais a ganhar. A base nao diz quais aparelhos causam o pico.
Recomendacao (hipotese a testar): escolher uma mudanca especifica e aplica-la por 8 semanas.
Evidencia usada: perfil horario de 2 anos, participacao da noite, tarifa implicita.
Avaliacao: apos 8 semanas, comparar o consumo medio semanal na faixa 18-23h com as 8 semanas
anteriores e com o mesmo periodo do ano anterior (metrica principal), acompanhando o consumo total
diario (metrica auxiliar, para ver se o consumo so mudou de horario).
Criterio proposto: queda de pelo menos 10% na faixa noturna, sem aumento equivalente nas demais faixas.
Limite: sem temperatura e sem ocupacao, uma queda pode ser clima ou viagem, nao habito; por isso a
comparacao com o mesmo periodo do ano anterior.
''')
