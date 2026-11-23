# Um produto de dados em miniatura: uma funcao que aprende com as vendas passadas e devolve,
# para cada dia da semana e hora, uma sugestao de quantos caixas abrir.
# Produto de dados = algo que aprende com dados e entrega valor de forma repetida (nao uma analise unica).
# Dados: dados/supermercado.csv. Os numeros de "clientes por caixa" sao uma suposicao didatica.

import os
import math
import pandas as pd
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
vendas = pd.read_csv(os.path.join(pasta, '..', 'dados', 'supermercado.csv'))
vendas['Data'] = pd.to_datetime(vendas['Date'], format='%m/%d/%Y')
vendas['Hora'] = pd.to_datetime(vendas['Time'], format='%H:%M').dt.hour
vendas['Dia'] = vendas['Data'].dt.day_of_week          # 0 = segunda

CLIENTES_POR_CAIXA_POR_HORA = 1.5    # suposicao: um caixa atende com folga 1,5 cupom por hora nesta base


def treinar(historico):
    # "Treinar" aqui e so calcular a media de cupons por (dia da semana, hora) no historico.
    cupons = historico.groupby(['Dia', 'Hora', 'Data']).size().reset_index(name='cupons')
    return cupons.groupby(['Dia', 'Hora'])['cupons'].mean()


def sugerir_caixas(modelo, dia, hora):
    media = modelo.get((dia, hora), 0)
    return max(1, math.ceil(media / CLIENTES_POR_CAIXA_POR_HORA))


# Treina com janeiro e fevereiro, como se marco ainda nao tivesse acontecido
treino = vendas[vendas['Data'] < '2019-03-01']
teste = vendas[vendas['Data'] >= '2019-03-01']
modelo = treinar(treino)
print('Sugestao para sabado (dia 5) as 19h:', sugerir_caixas(modelo, 5, 19), 'caixa(s)')
print('Sugestao para segunda (dia 0) as 16h:', sugerir_caixas(modelo, 0, 16), 'caixa(s)')

# O produto e util se acerta o que acontece DEPOIS. Comparamos a media prevista com a observada em marco.
observado = teste.groupby(['Dia', 'Hora', 'Data']).size().reset_index(name='cupons').groupby(['Dia', 'Hora'])['cupons'].mean()
comparacao = pd.DataFrame({'previsto (jan-fev)': modelo, 'observado (marco)': observado}).dropna()
erro = (comparacao['previsto (jan-fev)'] - comparacao['observado (marco)']).abs().mean()
print(f'\nErro medio absoluto da media de cupons por (dia, hora): {erro:.2f} cupons')
print(f'Media observada em marco: {comparacao["observado (marco)"].mean():.2f} cupons por (dia, hora)')
# O erro (cerca de 0,6 cupom) e mais de um terco da propria media (cerca de 1,6): com 3 meses e
# pouco mais de 1 cupom por hora, esse produto ainda nao e confiavel. Um produto de dados precisa
# ser AVALIADO antes de ser usado, e reavaliado depois.

# Ciclo de retroalimentacao: ao final de marco, o modelo e treinado de novo com os tres meses.
modelo_atualizado = treinar(vendas)
mapa = modelo_atualizado.unstack(0)
mapa.columns = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={'width_ratios': [1, 1.2]})
esq.scatter(comparacao['previsto (jan-fev)'], comparacao['observado (marco)'], color='#2F648F', alpha=0.7)
limite = max(comparacao.max()) + 0.3
esq.plot([0, limite], [0, limite], color='#8794A3', linestyle='--')
esq.set_xlabel('Média prevista com jan–fev (cupons por hora)')
esq.set_ylabel('Média observada em março')
esq.set_title(f'Avaliação: erro médio de {erro:.2f} cupom por hora')
imagem = dir.imshow(mapa.values, aspect='auto', cmap='Blues', origin='lower')
dir.set_xticks(range(7))
dir.set_xticklabels(mapa.columns)
dir.set_yticks(range(len(mapa.index)))
dir.set_yticklabels([f'{h}h' for h in mapa.index])
dir.set_title('O "produto": média de cupons por dia e hora (jan–mar)')
dir.grid(False)
plt.colorbar(imagem, ax=dir, label='cupons por hora (média)')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'produto_de_dados.png'))
plt.show()
