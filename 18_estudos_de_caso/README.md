# 18 · Estudos de caso

**Pergunta inicial:** depois de descrever, visualizar, testar e modelar, que decisão você tomaria, e qual é o efeito dela, em números?

Cada estudo de caso começa com uma decisão que alguém precisa tomar e termina com uma recomendação no formato:

> **Observamos** [achado medido] → **portanto decidimos** [ação concreta] → **porque**, medido em dados que não foram usados para construir a decisão, **ela produz** [efeito, com número e unidade].

O efeito nunca é uma expectativa ("deve reduzir…"). Ele é medido: por um modelo avaliado em outro período, por uma simulação que usa os desfechos reais, por validação em outra turma, ou em observações escondidas do método. Cada estudo também mede o **custo** da decisão (quem espera mais, quanto estoque a mais, quantas vagas a mais) e diz como acompanhar o efeito depois de implantada.

## Como cada estudo está organizado

1. **A situação** e as perguntas.
2. **Os dados**: origem, colunas e o que a base **não** tem.
3. **Passos numerados**, cada um com a pergunta do passo, o trecho de código principal, o que saiu (números e figura) e como ler.
4. **Verificação** do achado em dados que não foram usados para encontrá-lo (outro período, outra turma, outra semente, contra o acaso).
5. **Medição do efeito da decisão**, com o modelo ou a simulação que a mede.
6. **Recomendação**: achados → decisão → efeito medido → como acompanhar, com referências medidas nos próprios dados.
7. **Limites** e **atividades**.

Os scripts de cada estudo são numerados e rodam na ordem; alguns gravam arquivos em `dados/` usados pelos seguintes.

## Os estudos

### Estudos de caso do livro

Correspondem aos capítulos de aplicação de *Ciência de Dados: da teoria à prática*.

| Estudo | Capítulo | Decisão | Efeito medido |
|---|---|---|---|
| [01 · Reclamações por perdas (TSA)](01_reclamacoes_tsa/) | 11 | Ordenar a fila de análise pela probabilidade de pagamento, com teto de 20 dias de espera | Simulação da fila com os desfechos reais de jul–out/2015: espera até o pagamento **−25%** (8,6 → 6,5 dias); casos negados esperam +20% |
| [02 · Energia doméstica](02_energia_domestica/) | 12 | Desligar as cargas extras da madrugada (0h–5h) e avisar quando a madrugada passar do nível de verão | Consumo acima da referência de verão no ano mais recente: **229 kWh = US$ 48 = 5,3% da conta** |
| [03 · Vendas em supermercado](03_vendas_supermercado/) | 13 | Repor cada linha de produto até média + 1,28 desvio-padrão das semanas anteriores | 42 linhas-semana não vistas: semanas com falta **48% → 7%**, unidades em falta **−97%**, com +38% de estoque |

### Aplicações adicionais — não integram o livro

Usam bases públicas com origem, licença e data de acesso registradas em cada README.

| Estudo | Unidades relacionadas | Decisão | Efeito medido |
|---|---|---|---|
| [04 · Bicicletas compartilhadas](04_mobilidade_bicicletas/) | 04, 11, 15 | Manutenção às 3h–5h; equipe diária dimensionada pela previsão | Manutenção afeta **0,8%** dos aluguéis de 2012; dias com equipe insuficiente **32 → 17 (−47%)** |
| [05 · Educação](05_educacao_desempenho/) | 04, 07, 11 | Acompanhar quem já reprovou ou teve G1 < 10 | Na turma de validação, **109 de 130** alunos que reprovariam recebem apoio, contra 56 com uma lista sorteada do mesmo tamanho |
| [06 · Varejo on-line](06_varejo_online/) | 05, 06, 08 | Lista trimestral de retenção pela perda esperada; bloqueio de linhas de 5 000 unidades ou mais | A lista de 10% dos clientes contém **55% da receita em risco** do trimestre seguinte (sorteio: 10%); o bloqueio teria evitado 55% do valor cancelado do 2º semestre, sem alarme falso |
| [07 · Votações na Wikipédia](07_votacoes_wikipedia/) | 17 | Sugerir a cada usuário 10 eleições por eleitores parecidos, com 3 vagas de fora da sua comunidade | Em votos escondidos, as sugestões acertam **15,4%** contra 5,9% da página por popularidade, sem efeito bolha (60,7% na própria comunidade, contra 67,1% dos votos reais) |

Em três estudos (03, 06 e 07), a verificação derrubou a ação que a análise inicial parecia sugerir (escala por horário, foco nos "clientes que mais cancelam", suspeita sobre usuários). A decisão final veio do que a verificação mostrou.

## Como executar

Da pasta principal do repositório, com o ambiente ativado:

```powershell
python 18_estudos_de_caso/01_reclamacoes_tsa/01_conhecer_os_dados.py
```

e assim por diante, na ordem numérica de cada estudo. Para rodar todos sem abrir janelas:

```powershell
python scripts/executar_todos.py 18_estudos_de_caso
```

Os números dos READMEs foram calculados por estes scripts em novembro de 2026, com as versões de `requirements-basico.txt`. Algoritmos com etapa aleatória (florestas, Louvain, k-means, sorteios) usam semente fixa; com outras versões das bibliotecas, pequenas diferenças podem aparecer.

Próxima etapa: [19 · Projeto final](../19_projeto_final/)
