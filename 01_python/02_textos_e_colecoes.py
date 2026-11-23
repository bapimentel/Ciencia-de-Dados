# Textos (str), listas (list) e dicionarios (dict).
# Baseado em introducao.py (2019).

# str: texto entre aspas
nome = 'Silvio Santos'
canto1 = 'vem ai, '
canto2 = 'la '
print(nome + ' ' + canto1 + canto2 * 6 + '!!')   # + junta, * repete
print(len('Abracadabra'))                        # len conta os caracteres

# list: sequencia ordenada de valores
lista = [100, 200, 300, 400, 500]
print(lista[0])      # primeiro elemento (a contagem comeca em 0)
print(lista[-1])     # ultimo elemento
print(lista[2:4])    # da posicao 2 ate a 4 (nao inclusa)
print(lista[:3])     # ate a posicao 3 (nao inclusa)
print(lista[2:])     # da posicao 2 ate o final

# Uma lista pode misturar tipos, inclusive outra lista
lista = ['duas palavras', 42, True, ['batman', 'robin'], -0.84, 'hipofise']
print(42 in lista)
print('domino' in lista)
print('batman' in lista[3])   # o elemento de indice 3 tambem e uma lista

# Juntar, repetir e acrescentar
a = [1, 2, 3]
b = [4, 5, 6]
print(a + b)
print([0] * 3)
lista = ['a', 'b', 'c']
lista.append('e')
print(lista)

# range gera sequencias de numeros sem digitar um por um
print(list(range(1, 14)))
print(list(range(10)))

# dict: pares chave -> valor
idades = {'ana': 34, 'yudi': 40, 'julia': 41}
print(idades['ana'])
constantes = dict(pi=3.14, e=2.7, alpha=1/137)
print(constantes['e'])

# Chaves podem ser numeros; valores podem ser trocados ou acrescentados
numeros_por_extenso = {2: 'dois', 1: 'um', 3: 'tres', 0: 'zero'}
print(numeros_por_extenso[2])
numeros_por_extenso[2] = 'two'
print(numeros_por_extenso[2])
meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Marco'}
meses[4] = 'Abril'
print(meses)

# Percorrendo as partes de um dicionario
pessoa = {'nome': 'Enzo', 'RA': 242334, 'curso': 'fiscomp'}
print(pessoa.keys())
print(pessoa.values())
print(pessoa.items())
chaves = list(pessoa.keys())
print(chaves)

# Uma pergunta pequena: quantas unidades de cada produto foram vendidas hoje?
vendas = ['pao', 'leite', 'pao', 'cafe', 'pao', 'leite']
print(vendas.count('pao'))
print(vendas.count('leite'))
print(len(vendas))

# Experimente: acrescente 'cafe' duas vezes na lista e veja como a contagem muda.
