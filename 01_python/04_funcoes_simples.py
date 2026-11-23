# Funcoes: dar nome a um trecho de codigo para reutiliza-lo.
# Baseado em introducao.py (2019).

# Uma funcao que so imprime
def soma():
    print(1 + 1)

soma()

# Uma funcao que devolve um valor com return
def soma2():
    return 1 + 1

resultado = soma2()
print(resultado)

# Funcao com parametro
def soma_valor(x):
    return 3 + x

print(soma_valor(5))
z = soma_valor(10)
print(z)

# Funcao com repeticao dentro
def tabuada_do_n(n):
    for i in range(11):
        print(n * i)

tabuada_do_n(7)

# Funcoes evitam repetir a mesma conta varias vezes.
# Exemplo: a media de uma lista.
def media(valores):
    return sum(valores) / len(valores)

vendas_loja_a = [120, 98, 143, 87, 160, 131, 75]
vendas_loja_b = [90, 95, 101, 99, 97, 102, 94]
print('Media A:', media(vendas_loja_a))
print('Media B:', media(vendas_loja_b))

# As medias sao parecidas. As lojas se comportam igual?
# A amplitude (maior - menor) ja mostra uma diferenca.
def amplitude(valores):
    return max(valores) - min(valores)

print('Amplitude A:', amplitude(vendas_loja_a))
print('Amplitude B:', amplitude(vendas_loja_b))

# Experimente: escreva uma funcao mediana(valores) que ordena a lista
# (use sorted) e devolve o valor do meio. Teste nas duas lojas.
