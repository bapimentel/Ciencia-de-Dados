# Primeira pergunta respondida com dados, usando so listas e dicionarios.
# Pergunta: em uma semana de vendas, qual produto vendeu mais e em que dia?
# Sem pandas: o objetivo e entender o que uma biblioteca fara por nos depois.

# Cada registro e uma lista: [dia, produto, quantidade]
registros = [
    ['segunda', 'pao', 40], ['segunda', 'leite', 25], ['segunda', 'cafe', 12],
    ['terca', 'pao', 38], ['terca', 'leite', 30], ['terca', 'cafe', 15],
    ['quarta', 'pao', 45], ['quarta', 'leite', 22], ['quarta', 'cafe', 10],
    ['quinta', 'pao', 50], ['quinta', 'leite', 28], ['quinta', 'cafe', 14],
    ['sexta', 'pao', 70], ['sexta', 'leite', 35], ['sexta', 'cafe', 20],
    ['sabado', 'pao', 90], ['sabado', 'leite', 40], ['sabado', 'cafe', 30],
]

print('Quantidade de registros:', len(registros))
print('Primeiro registro:', registros[0])

# Total por produto: um dicionario que acumula as quantidades
total_por_produto = {}
for dia, produto, quantidade in registros:
    if produto not in total_por_produto:
        total_por_produto[produto] = 0
    total_por_produto[produto] = total_por_produto[produto] + quantidade

print('Total por produto:', total_por_produto)

# Qual vendeu mais? max com key escolhe a chave de maior valor
mais_vendido = max(total_por_produto, key=total_por_produto.get)
print('Mais vendido:', mais_vendido)

# Total por dia, do mesmo jeito
total_por_dia = {}
for dia, produto, quantidade in registros:
    total_por_dia[dia] = total_por_dia.get(dia, 0) + quantidade

print('Total por dia:', total_por_dia)
melhor_dia = max(total_por_dia, key=total_por_dia.get)
print('Melhor dia:', melhor_dia)

# Um filtro: so os registros de cafe
so_cafe = []
for registro in registros:
    if registro[1] == 'cafe':
        so_cafe.append(registro)
print('Registros de cafe:', so_cafe)

# Media de cafe por dia
quantidades_cafe = [registro[2] for registro in so_cafe]
print('Media diaria de cafe:', sum(quantidades_cafe) / len(quantidades_cafe))

# Repare: contar, somar por grupo, filtrar e tirar a media exigiram varios lacos.
# Na unidade 02 o pandas faz cada uma dessas operacoes em uma linha,
# mas o raciocinio continua sendo este.

# Experimente: o sabado vendeu mais de tudo. Isso quer dizer que a loja deve
# pedir mais estoque para o proximo sabado? O que mais voce precisaria saber?
