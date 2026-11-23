# Variedade: dados estruturados, semiestruturados e nao estruturados descrevendo a mesma coisa.
# Exemplo inventado de um cliente de supermercado, so para comparar os formatos.

import os
import json
import pandas as pd

pasta = os.path.dirname(os.path.abspath(__file__))

# --- Estruturado: tabela com linhas e colunas fixas (CSV, planilha, banco relacional)
tabela = pd.DataFrame({
    'cliente': [101, 101, 102],
    'data': ['2019-01-05', '2019-01-19', '2019-01-06'],
    'produto': ['cafe', 'pao', 'leite'],
    'quantidade': [2, 6, 1],
})
print('Estruturado:')
print(tabela)

# --- Semiestruturado: documentos com campos aninhados e opcionais (JSON, bancos como o MongoDB)
documentos = '''[
  {"cliente": 101, "nome": "Ana", "endereco": {"cidade": "Maceio", "bairro": "Farol"},
   "compras": [{"data": "2019-01-05", "itens": [{"produto": "cafe", "qtd": 2}]},
               {"data": "2019-01-19", "itens": [{"produto": "pao", "qtd": 6}]}]},
  {"cliente": 102, "nome": "Bruno", "compras": [{"data": "2019-01-06", "itens": [{"produto": "leite", "qtd": 1}]}]}
]'''
clientes = json.loads(documentos)
print('\nSemiestruturado: o cliente 102 nao tem endereco, e cada compra tem uma lista de itens.')
print(json.dumps(clientes[1], indent=2, ensure_ascii=False))

# Para analisar, "achatamos" o documento em tabela: uma linha por item comprado
achatado = pd.json_normalize(clientes, record_path=['compras', 'itens'], meta=['cliente', 'nome', ['compras', 'data']])
print('\nDepois de json_normalize:')
print(achatado)
print('Endereco do 102 virou ausente ao achatar as cidades:')
print(pd.json_normalize(clientes)[['cliente', 'endereco.cidade']])

# --- Nao estruturado: texto livre. A informacao existe, mas nao em colunas.
comentarios = [
    'Comprei 2 pacotes de cafe, mas o caixa demorou muito.',
    'Pao fresquinho! Voltarei. Caixa rapido.',
    'Faltou leite de novo. Demorou para achar um atendente.',
]
# Uma primeira estruturacao: contar palavras de interesse
palavras = ['demorou', 'rapido', 'faltou', 'cafe', 'pao', 'leite']
contagem = pd.DataFrame([[c.lower().count(p) for p in palavras] for c in comentarios], columns=palavras)
print('\nNao estruturado -> contagem de palavras (uma tabela que um modelo consegue usar):')
print(contagem)

# Variedade e um desafio porque cada formato exige um tratamento antes de virar tabela, e
# juntar fontes diferentes exige saber que "cliente" em uma e "cust_id" em outra sao a mesma coisa
# (integracao, unidade 06). O "Naive Bayes" da unidade 10 classifica textos a partir de contagens assim.
