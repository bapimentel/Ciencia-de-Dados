# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 09:04:26 2019

@author: Bruno Pimentel
"""

#Operadores matematicos
2 + 3
3.2 + 2.7
6 - 4
7 - 8
7 * 8
2 * 2 * 2
100 / 20
10 / 3
666 // 137
666 / 137
10 % 2
10 % 3
2 ** 10
10 ** 3

# Importando pacotes
import math
raiz = math.sqrt(16)
pi = math.pi

# Comparacoes
2 < 10
2 > 11
10 > 10
10 >= 10
42 == 24
666 != 137
8**2 == 60 + 4
100 != 99 + 3

# Atribuicao
numero = 11
numero
frase = "Me da um copo d'agua"
frase
pi = 3.141592
pi
a, b, c, d = 1, 2, 3, 4
print(a, b, c, d)

# Tipo
x = 1
type(x)
y = 2.3
type(y)
type('Python')
type(True)

# str
nome = 'Silvio Santos'
nome
canto1 = 'vem ai, '
canto2 = 'la '
nome + ' ' + canto1 + canto2 * 6 + '!!'
len('Abracadabra')

# list
lista = [100, 200, 300, 400, 500]
lista[0] #primeiro elemento da lista
lista[-1] #ultimo elemento da lista
lista[-5] #primeiro elemento da lista
lista[2:4] #da posicao 2 ate a 4 (nao inclusa)
lista[:3] #ate a posicao 3 (nao incluso)
lista[2:] #da posicao 2 ate o final
lista = ['duas palavras', 42, True, ['batman', 'robin'], -0.84, 'hipofise']
42 in lista
'domino' in lista
'batman' in lista[3] #note que o elemento com indice 3 tambem eh uma lista
a = [1, 2, 3]
b = [4, 5, 6]
c = a + b
c
[0] * 3
lista = ['a', 'b', 'c']
lista.append('e')
lista
lista_grande = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] #como simplificar?
print(list(range(1, 14)))
print(list(range(10)))

# dict
idades = {"ana": 34, "yudi": 40, "julia": 41}
idades
constantes = dict(pi=3.14, e=2.7, alpha=1/137)
print(constantes)
constantes['e']
numeros_por_extenso = {2: "dois", 1: "um", 3: "tres", 0: "zero"}
numeros_por_extenso[0]
numeros_por_extenso[2]
numeros_por_extenso[2] = 'two'
numeros_por_extenso[2]
meses = {1: "Janeiro", 2: "Fevereiro", 3: "Marco"}
meses[4] = "Abril"
meses
pessoa = {"nome": "Enzo", "RA": 242334, "curso": "fiscomp"}
pessoa.items()
pessoa.values()
valores = list(pessoa.values())
valores
pessoa.keys()
chaves = list(pessoa.keys())
chaves

# Estruturas de controle
True
type(False)
2 < 3
2 == 5
10 > 3 and 2 == 4
10 > 3 or 2 == 4
not not not 1 == 1
not []
a = 7
if a > 3:
    print("estou no if")
else:
    print("cai no else")
# Aqui repetimos o print 3 vezes
for n in range(3):
    print(n)
lista = [1, 2, 3, 4, 10]
for numero in lista:
    print(numero ** 2)
gatos = {"Portugues": "gato", "Ingles": "cat", "Frances": "chat", "Finlandes":"Kissa"}
for chave, valor in gatos.items():
    print(chave, '->', valor)
# Aqui iniciamos o n em 0, e repetimos o print ate que seu valor seja maior ou igual a 3
n = 0
while n < 3:
    print(n)
    n += 1
    
# Funcoes
def soma():
    print(1 + 1)
soma()
def soma2():
    return(1 + 1)
soma2()
def soma_valor(x):
    return 3 + x
soma_valor(5)
z = soma_valor(10)
z
def tabuada_do_n(n):
    for i in range(11):
        print(n * i)
tabuada_do_n(7)

# Arquivos de texto
arq = open('lista.txt', 'w')
texto = '''
Lista de Alunos

- - -

Joao da Silva

Jose Lima

Maria das Dores

'''
arq.write(texto)
arq.close()
arq = open('lista.txt', 'w')
texto = []
texto.append('Lista de Alunos\n')
texto.append('- - -\n')
texto.append('Joao da Silva\n')
texto.append('Jose Lima\n')
texto.append('Maria das Dores')
arq.writelines(texto)
arq.close()
arq = open('lista.txt', 'r')
texto = arq.read()
print(texto)
arq.close()
arq = open('lista.txt', 'r')
texto = arq.readlines()
for linha in texto:
    print(linha)
arq.close()

