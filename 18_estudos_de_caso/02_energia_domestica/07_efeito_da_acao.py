# Estudo de caso 2 - Energia domestica. Passo 7: quanto vale cortar a carga extra da madrugada?
# Entre 0h e 5h, a casa normalmente so tem a carga que nunca desliga (geladeira, aparelhos em espera). Quando o
# consumo da madrugada passa muito desse nivel, ha algo ligado sem ninguem usar (aquecimento, aparelho esquecido).
# Modelo do consumo "sem carga extra": as madrugadas do verao mais recente (jun-ago de 2018), quando nao ha
# aquecimento. Referencia = percentil 90 dessas madrugadas (conservador: so conta como extra o que passa dele).
# Efeito da acao "programar o desligamento das cargas extras de madrugada" = consumo acima da referencia,
# medido madrugada a madrugada no ano mais recente (22/10/2017 a 21/10/2018), convertido pela tarifa desse ano.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', '..', 'figuras', 'estilo.mplstyle'))
horario = pd.read_csv(os.path.join(pasta, 'dados', 'energia_por_hora.csv'), index_col=0, parse_dates=True)
madrugada = horario[horario.index.hour <= 5].resample('D').sum()
diario = horario.resample('D').sum()

# 1) O nivel de referencia: madrugadas de verao
for ano in [2017, 2018]:
    v = madrugada.loc[f'{ano}-06-01':f'{ano}-08-31', 'Consumo_kWh']
    print(f'Verao {ano}: {len(v)} madrugadas | mediana {v.median():.2f} kWh | percentil 90 {v.quantile(0.9):.2f} kWh')
referencia = madrugada.loc['2018-06-01':'2018-08-31', 'Consumo_kWh'].quantile(0.9)
print(f'Referencia: percentil 90 das madrugadas do verao de 2018 = {referencia:.2f} kWh por madrugada '
      f'({referencia / 6:.2f} kWh por hora)')

# 2) Ano mais recente: madrugadas acima da referencia e consumo acima dela
periodo = slice('2017-10-22', '2018-10-21')
ano = madrugada.loc[periodo, 'Consumo_kWh']
tarifa = horario.loc[periodo, 'Custo'].sum() / horario.loc[periodo, 'Consumo_kWh'].sum()
conta = diario.loc[periodo, 'Custo'].sum()
excesso = (ano - referencia).clip(lower=0)
print(f'\nAno mais recente: {len(ano)} madrugadas; {int((excesso > 0).sum())} acima da referencia')
print(f'Consumo acima da referencia: {excesso.sum():.0f} kWh = US$ {excesso.sum() * tarifa:.0f} '
      f'({excesso.sum() * tarifa / conta:.1%} da conta do ano, US$ {conta:.0f}; tarifa US$ {tarifa:.3f}/kWh)')
por_mes = excesso.groupby(excesso.index.to_period('M')).sum()
print('Por mes (kWh):', {str(m): round(v, 1) for m, v in por_mes.items()})
print(f'Novembro a marco: {por_mes[[p for p in por_mes.index if p.month in (11, 12, 1, 2, 3)]].sum() / excesso.sum():.0%} do excesso')
maiores = excesso.sort_values(ascending=False)
print(f'As 10 piores madrugadas respondem por {maiores.head(10).sum() / excesso.sum():.0%} do excesso')

# 3) A acao e factivel nesta casa? No inverno, quantas madrugadas ja ficaram no nivel de verao?
inverno = ano[ano.index.month.isin([12, 1, 2])]
print(f'\nInverno 2017-18: {(inverno <= referencia).mean():.0%} das madrugadas ja ficaram no nivel de verao '
      f'({int((inverno <= referencia).sum())} de {len(inverno)})')

# 4) O mesmo calculo no ano anterior (22/10/2016 a 21/10/2017), com a mesma referencia
ano1 = madrugada.loc['2016-10-22':'2017-10-21', 'Consumo_kWh']
excesso1 = (ano1 - referencia).clip(lower=0)
print(f'Ano anterior: {int((excesso1 > 0).sum())} madrugadas acima; {excesso1.sum():.0f} kWh acima da referencia')

fig, (esq, dir) = plt.subplots(1, 2, figsize=(13, 4.3))
esq.plot(ano.index, ano.values, color='#8794A3', linewidth=0.8, label='consumo da madrugada (0h–5h)')
esq.fill_between(ano.index, referencia, ano.values, where=ano.values > referencia, color='#BD5B58', alpha=0.6,
                 label=f'acima da referência: {excesso.sum():.0f} kWh')
esq.axhline(referencia, color='#2F648F', linestyle='--', label=f'referência de verão ({referencia:.2f} kWh)')
esq.set_ylabel('kWh por madrugada')
esq.set_title('Ano mais recente: madrugadas com carga extra', fontsize=11)
esq.legend(fontsize=9)
dir.bar([str(m)[2:] for m in por_mes.index], por_mes.values * tarifa, color='#BD5B58')
dir.set_ylabel('US$ consumidos acima da referência')
dir.set_title(f'Carga extra de madrugada: US$ {excesso.sum() * tarifa:.0f} no ano', fontsize=11)
dir.tick_params(axis='x', labelrotation=45)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', '07_efeito_da_acao.png'))
plt.show()
