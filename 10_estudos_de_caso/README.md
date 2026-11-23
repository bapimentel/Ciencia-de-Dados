# 10 · Estudos de caso

**Pergunta inicial:** depois de descrever, visualizar, testar e modelar, o que você recomendaria, e como saberia se deu certo?

Cada estudo começa com uma decisão que alguém precisa tomar e termina com o que os dados sustentam, inclusive quando sustentam pouco. Todos seguem a mesma sequência: situação e pergunta; dados e alcance (e o que a base não mede); primeira inspeção; investigação visual e estatística; modelagem só quando ajuda; resposta e recomendação com indicador, prazo e critério de sucesso; atividades. Os scripts são curtos, numerados e rodam na ordem; alguns gravam arquivos em `dados/` usados pelos seguintes.

Pré-requisitos: unidades [02](../02_primeiros_dados/) a [08](../08_series_temporais/); para o caso 7, também a [09](../09_redes_sociais/).

## Os casos do livro

Reproduzem a Parte II de *Ciência de Dados: da teoria à prática*, com os scripts e dados originais preservados em [original/aplicacao_zip/](../original/aplicacao_zip/) e refeitos aqui em etapas.

| Caso | Capítulo do livro | Decisão em jogo | Técnicas |
|---|---|---|---|
| [01 · Reclamações por perdas (TSA)](01_reclamacoes_tsa/) | 11 (11.1–11.4) | Ordenar a fila de análise de reclamações | descrição, preparação, classificação, regressão, custo do erro |
| [02 · Energia doméstica](02_energia_domestica/) | 12 (12.1–12.4) | Que hábito mudar para gastar menos, e como testar | séries temporais, perfis horários, linhas de base, cenários |
| [03 · Vendas em supermercado](03_vendas_supermercado/) | 13 (13.1–13.4) | Organizar a operação por horário; **não** mexer em preços com estes dados | descrição, decomposição semanal, agrupamento hierárquico, crítica a um experimento |

## Aplicações adicionais (não integram o livro)

Usam bases públicas com origem, data de acesso e licença registradas em cada README. Relacionam-se aos capítulos teóricos indicados, mas não aparecem como estudos de caso na obra.

| Caso | Capítulos teóricos | Decisão em jogo | Técnicas |
|---|---|---|---|
| [04 · Mobilidade: bicicletas compartilhadas](04_mobilidade_bicicletas/) | 3, 4, 8 | Janelas de capacidade operacional | perfis horários, clima, previsão com separação cronológica |
| [05 · Educação: desempenho e acompanhamento](05_educacao_desempenho/) | 3, 5, 6 | Lista de acompanhamento preventivo | comparação de grupos com tamanho de efeito, risco com validação cruzada, regra transparente |
| [06 · Varejo on-line: cancelamentos](06_varejo_online/) | 3, 4, 7 | Conferência de pedidos para poucos grandes clientes | preparação em escala, concentração, segmentos RFM |
| [07 · Votações na Wikipédia](07_votacoes_wikipedia/) | 9 | Nenhuma sobre pessoas; só por onde começar uma revisão e o que coletar | grafo dirigido, centralidades, comunidades, limites da inferência |

A tabela completa de correspondência entre casos, origem dos dados, seções do livro e conceitos está em [materiais/mapa_capitulos_aplicacoes.md](../materiais/mapa_capitulos_aplicacoes.md).

## Como executar

Da pasta principal do repositório, com o ambiente ativado:

```
python 10_estudos_de_caso/01_reclamacoes_tsa/01_conhecer_os_dados.py
```

e assim por diante, na ordem numérica de cada caso. Para rodar todos sem abrir janelas: `python scripts/executar_todos.py 10_estudos_de_caso`.

## O que esperar

Os números dos READMEs foram calculados pelos scripts deste repositório em novembro de 2026, com as versões listadas em `requirements-basico.txt`. Pequenas diferenças podem aparecer com outras versões (florestas aleatórias, Louvain), nunca na direção das conclusões. Onde a evidência é fraca, o texto diz; as metas de avaliação são propostas, não resultados.

## Próxima etapa

[11 · Projeto final](../11_projeto_final/)
