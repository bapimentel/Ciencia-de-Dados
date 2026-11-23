# 18 · Estudos de caso

**Pergunta inicial:** depois de descrever, visualizar, testar e modelar, o que você recomendaria, e como saberia se deu certo?

Cada estudo de caso começa com uma decisão que alguém precisa tomar e segue, passo a passo, até uma recomendação. Em todos eles a ordem é a mesma: **primeiro encontrar o resultado, depois recomendar**. Uma recomendação só aparece quando há um achado medido que a sustenta, e esse achado é **verificado em dados que não foram usados para encontrá-lo** (outro período, outra turma, outra semente do algoritmo) antes de virar ação.

## Como cada estudo está organizado

1. **A situação** e as perguntas.
2. **Os dados**: origem, colunas e, principalmente, o que a base **não** tem.
3. **Passos numerados**, cada um com a pergunta do passo, o trecho de código principal, o que saiu (números e figura) e como ler.
4. **Um passo de verificação**: o achado se repete em outro período, outra turma, outra semente, ou contra o acaso?
5. **Recomendação, a partir do que foi encontrado**: achados com números → ação → como acompanhar, com referências **medidas nos próprios dados** → o que não podemos afirmar.
6. **Limites** e **atividades**.

Os scripts de cada estudo são numerados e rodam na ordem; alguns gravam arquivos em `dados/` usados pelos seguintes.

## Os estudos

### Estudos de caso do livro

Correspondem aos capítulos de aplicação de *Ciência de Dados: da teoria à prática*.

| Estudo | Capítulo | Decisão em jogo | O que a verificação mostrou |
|---|---|---|---|
| [01 · Reclamações por perdas (TSA)](01_reclamacoes_tsa/) | 11 | Em que ordem analisar reclamações | Treinado no 1º semestre, o modelo pôs 62% dos casos pagos na 1ª metade da fila do 2º semestre (58% a 70% por mês) |
| [02 · Energia doméstica](02_energia_domestica/) | 12 | Que hábito mudar e como saber se funcionou | O perfil horário se repete entre os anos (correlação 0,91); sem intervenção, o consumo noturno varia até 19%, então só uma redução maior que isso é detectável |
| [03 · Vendas em supermercado](03_vendas_supermercado/) | 13 | Escala por horário, preços | O "pico das 19h" não se repete entre meses (correlação de −0,12 a 0,27): a recomendação é não agir e coletar mais dados |

### Aplicações adicionais — não integram o livro

Usam bases públicas com origem, licença e data de acesso registradas em cada README.

| Estudo | Unidades relacionadas | Decisão em jogo | O que a verificação mostrou |
|---|---|---|---|
| [04 · Bicicletas compartilhadas](04_mobilidade_bicicletas/) | 04, 11, 15 | Janelas de manutenção e de reforço | Horas de pico entre 50% e 55% do uso em todos os 24 meses; previsão melhor que a linha de base em 3 de 4 trimestres |
| [05 · Educação](05_educacao_desempenho/) | 04, 07, 11 | Lista de acompanhamento preventivo | Regra criada com a turma de português alcança 84% dos reprovados na turma de matemática |
| [06 · Varejo on-line](06_varejo_online/) | 05, 06, 08 | O que fazer com os cancelamentos | Os "50 maiores canceladores" de um semestre não se repetem no outro; metade do valor cancelado são dois erros de digitação corrigidos em minutos |
| [07 · Votações na Wikipédia](07_votacoes_wikipedia/) | 17 | Por onde começar uma revisão | O padrão é muito diferente do acaso, mas só 68 de 313 usuários aparecem em todas as sementes do algoritmo |

Repare que, em três estudos (03, 06 e 07), a verificação **mudou** a recomendação que a análise inicial parecia sugerir. Isso não é falha: é exatamente para isso que a verificação serve.

## Como executar

Da pasta principal do repositório, com o ambiente ativado:

```powershell
python 18_estudos_de_caso/01_reclamacoes_tsa/01_conhecer_os_dados.py
```

e assim por diante, na ordem numérica de cada estudo. Para rodar todos sem abrir janelas:

```powershell
python scripts/executar_todos.py 18_estudos_de_caso
```

Os números dos READMEs foram calculados por estes scripts em novembro de 2026, com as versões de `requirements-basico.txt`. Algoritmos com etapa aleatória (florestas, Louvain, k-means) usam semente fixa; com outras versões das bibliotecas, pequenas diferenças podem aparecer.

Próxima etapa: [19 · Projeto final](../19_projeto_final/)
