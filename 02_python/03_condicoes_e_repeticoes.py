# Condicoes (if/else) e repeticoes (for/while).
# Execute linha a linha para ver cada resultado aparecer.

# Valores logicos e operadores and, or, not
print(2 < 3)
print(2 == 5)
print(10 > 3 and 2 == 4)
print(10 > 3 or 2 == 4)
print(not 1 == 1)
print(not [])          # uma lista vazia vale False

# if: executa um bloco so quando a condicao e verdadeira
a = 7
if a > 3:
    print('estou no if')
else:
    print('cai no else')

# for: repete o bloco para cada elemento
for n in range(3):
    print(n)

lista = [1, 2, 3, 4, 10]
for numero in lista:
    print(numero ** 2)

gatos = {'Portugues': 'gato', 'Ingles': 'cat', 'Frances': 'chat', 'Finlandes': 'kissa'}
for chave, valor in gatos.items():
    print(chave, '->', valor)

# while: repete enquanto a condicao for verdadeira
n = 0
while n < 3:
    print(n)
    n += 1       # mesmo que n = n + 1

# Juntando tudo: somar vendas e contar dias acima de uma meta
vendas_por_dia = [120, 98, 143, 87, 160, 131, 75]
meta = 100

total = 0
dias_acima = 0
for venda in vendas_por_dia:
    total = total + venda
    if venda > meta:
        dias_acima = dias_acima + 1

print('Total da semana:', total)
print('Dias acima da meta:', dias_acima, 'de', len(vendas_por_dia))

# Uma condicao com tres saidas
media = total / len(vendas_por_dia)
if media > 130:
    print('Semana forte:', media)
elif media > 100:
    print('Semana normal:', media)
else:
    print('Semana fraca:', media)

# Experimente: mude a meta para 130. O que acontece com dias_acima?
