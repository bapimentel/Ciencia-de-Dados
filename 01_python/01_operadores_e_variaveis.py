# Operadores, comparacoes, variaveis e tipos.
# Baseado em introducao.py (2019). Execute linha a linha no console ou com
# python 01_python/01_operadores_e_variaveis.py

# Operadores matematicos
print(2 + 3)
print(3.2 + 2.7)
print(7 - 8)
print(7 * 8)
print(100 / 20)
print(10 / 3)        # divisao comum: resultado com casas decimais
print(666 // 137)    # divisao inteira: descarta a parte decimal
print(666 / 137)
print(10 % 3)        # resto da divisao
print(2 ** 10)       # potencia

# Funcoes matematicas vem do modulo math
import math
raiz = math.sqrt(16)
print(raiz)
print(math.pi)

# Comparacoes produzem True ou False
print(2 < 10)
print(10 > 10)
print(10 >= 10)
print(42 == 24)      # igual?
print(666 != 137)    # diferente?
print(8 ** 2 == 60 + 4)

# Atribuicao: o nome a esquerda passa a guardar o valor a direita
numero = 11
frase = "Me da um copo d'agua"
pi = 3.141592
print(numero, frase, pi)

# Varias atribuicoes de uma vez
a, b, c, d = 1, 2, 3, 4
print(a, b, c, d)

# Tipos: todo valor tem um tipo
x = 1
y = 2.3
print(type(x))
print(type(y))
print(type('Python'))
print(type(True))

# Uma pergunta pequena para responder com variaveis:
# se a loja vendeu 37 unidades a 12.50 cada e deu 10% de desconto, quanto arrecadou?
quantidade = 37
preco = 12.50
desconto = 0.10
arrecadado = quantidade * preco * (1 - desconto)
print('Arrecadado:', arrecadado)

# Experimente: troque o desconto por 0.25 e preveja o resultado antes de rodar.
