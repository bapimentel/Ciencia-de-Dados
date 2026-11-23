# Ler e escrever arquivos de texto.
# Baseado em introducao.py (2019). O arquivo lista.txt e criado na pasta deste script.

import os
pasta = os.path.dirname(os.path.abspath(__file__))   # pasta onde este script esta
caminho = os.path.join(pasta, 'lista.txt')

# Escrever um texto inteiro ('w' = write, apaga o conteudo anterior)
arq = open(caminho, 'w', encoding='utf-8')
texto = '''Lista de Alunos
- - -
Joao da Silva
Jose Lima
Maria das Dores
'''
arq.write(texto)
arq.close()

# Escrever linha por linha a partir de uma lista
arq = open(caminho, 'w', encoding='utf-8')
linhas = []
linhas.append('Lista de Alunos\n')
linhas.append('- - -\n')
linhas.append('Joao da Silva\n')
linhas.append('Jose Lima\n')
linhas.append('Maria das Dores\n')
arq.writelines(linhas)
arq.close()

# Ler tudo de uma vez ('r' = read)
arq = open(caminho, 'r', encoding='utf-8')
conteudo = arq.read()
print(conteudo)
arq.close()

# Ler como lista de linhas
arq = open(caminho, 'r', encoding='utf-8')
linhas = arq.readlines()
for linha in linhas:
    print(linha.strip())      # strip remove a quebra de linha do final
arq.close()

# A forma mais comum em Python: with fecha o arquivo sozinho
with open(caminho, 'r', encoding='utf-8') as arq:
    for linha in arq:
        print(len(linha.strip()), 'caracteres:', linha.strip())

# Experimente: acrescente seu nome na lista usando o modo 'a' (append)
# e leia o arquivo de novo.
