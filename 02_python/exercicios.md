# Exercícios de revisão · 01 Python do zero

Resolva no console ou em um arquivo novo. Antes de executar, escreva em um comentário qual resultado você espera.

1. **Operadores.** Sem rodar, diga o resultado de `7 // 2`, `7 % 2`, `7 / 2` e `2 ** 3 ** 2`. Depois confira.

2. **Variáveis.** Uma lanchonete vende 18 sanduíches a R$ 14,00 e 25 sucos a R$ 7,50 em um dia. Calcule o faturamento em uma variável `faturamento` e imprima com `print`.

3. **Listas.** Dada `temperaturas = [31, 29, 33, 35, 30, 28, 32]`, imprima: a primeira temperatura, a última, as três do meio (`[33, 35, 30]`) e a quantidade de dias com temperatura acima de 30.

4. **Dicionários.** Crie um dicionário `estoque` com três produtos e suas quantidades. Acrescente um quarto produto, reduza a quantidade de um deles em 2 e imprima o dicionário final.

5. **Repetição e condição.** Com a lista `notas = [7.5, 4.0, 9.2, 6.8, 5.5]`, conte quantas notas são maiores ou iguais a 7 e calcule a média das notas abaixo de 7.

6. **Função.** Escreva `def desvio_medio(valores)` que devolve a média das distâncias de cada valor até a média da lista. Teste com `[10, 10, 10]` (deve dar 0) e `[0, 10, 20]`.

7. **Arquivos.** Escreva um arquivo `compras.txt` com uma compra por linha no formato `produto,quantidade`. Depois leia o arquivo, separe cada linha com `.split(',')` e some as quantidades.

8. **Pergunta com dados.** Reaproveite `06_primeira_pergunta_com_dados.py` e responda: qual produto tem a maior variação entre o melhor e o pior dia? O que isso sugere sobre o planejamento de compras desse produto?

Sugestão de verificação: para os itens 5 e 6, confira seus resultados na unidade 04 (Estatística), quando as mesmas medidas aparecerem calculadas com `statistics` e `numpy`.
