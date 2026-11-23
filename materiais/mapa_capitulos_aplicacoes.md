# Mapa entre estudos de caso, origem dos dados e capítulos do livro

Sumário do livro *Ciência de Dados: da teoria à prática* (Bruno Pimentel, UICLAP, 2025) conferido em novembro de 2026 na [página do livro](https://bapimentel.github.io/livro/). Parte I — Teoria: 1 Conceitos; 2 Big Data; 3 Estatística; 4 Pré-processamento; 5 Classificação; 6 Avaliação de Classificadores; 7 Aprendizagem Não-Supervisionada; 8 Séries Temporais; 9 Análise de Redes Sociais; 10 Meta-Aprendizagem. Parte II — Prática: 11 Aplicação 1: Reclamações por Perdas; 12 Aplicação 2: Energia Doméstica; 13 Aplicação 3: Vendas em Supermercado; 14 Considerações Finais.

## Casos que reproduzem a Parte II do livro

| Caso (pasta) | Origem dos dados e scripts | Capítulo e subseções | Conceitos anteriores (unidades) | Perguntas do caso |
|---|---|---|---|---|
| [01 · Reclamações por perdas (TSA)](../10_estudos_de_caso/01_reclamacoes_tsa/) | `Aplicacao/TSA/leitura.py` e `dados/claims-data-2015-as-of-feb-9-2016.xlsx` do material do autor ([original/aplicacao_zip/TSA](../original/aplicacao_zip/TSA/)); dados públicos da TSA (EUA), 2015 | **Capítulo 11 — Aplicação 1: Reclamações por Perdas**: 11.1 Análise Descritiva (`01_conhecer_os_dados.py`), 11.2 Pré-processamento (`02_preparar_os_dados.py`), 11.3 Análise das Reclamações (`03_analisar_desfechos.py`), 11.4 Análise dos Valores Recebidos (`04_analisar_valores_recebidos.py`); síntese em `05_avaliar_uma_decisao.py` | 02, 03, 04, 05, 06 | Os desfechos variam com tipo, local, companhia e item? Quanto se paga quando se paga? Um modelo apoia a análise humana sem substituí-la? |
| [02 · Energia doméstica](../10_estudos_de_caso/02_energia_domestica/) | `Aplicacao/Series Temporais/analise.py`, `dados/D202.csv` e `D202.xlsx` ([original/aplicacao_zip/Series Temporais](../original/aplicacao_zip/Series%20Temporais/)); leituras de 15 min de uma residência, 2016–2018 | **Capítulo 12 — Aplicação 2: Energia Doméstica**: 12.1 Análise Descritiva (`01`), 12.2 Pré-processamento (`02`), 12.3 Análise do Uso de Energia (`03`, `04`), 12.4 Recomendação de Uso (`05`) | 02, 03, 04, 05, 08 | Quando o consumo se concentra? O custo é proporcional? O histórico prevê melhor que repetir a semana? Que teste honesto mediria uma mudança de hábito? |
| [03 · Vendas em supermercado](../10_estudos_de_caso/03_vendas_supermercado/) | `Aplicacao/Vendas/analise.py`, `dados/supermarket_sales - Sheet1.csv`, `estatisticas_produtos.txt` ([original/aplicacao_zip/Vendas](../original/aplicacao_zip/Vendas/)); 1 000 cupons, 3 filiais, jan–mar 2019 | **Capítulo 13 — Aplicação 3: Vendas em Supermercado**: 13.1 Análise Descritiva (`01`), 13.2 Análise Temporal de Vendas (`02`), 13.3 Perfis de Vendas (`03`), 13.4 Maximização das Vendas (`04`); síntese em `05` | 02, 03, 04, 07, 08 | Linhas e filiais diferem? Há padrão semanal ou horário? Os cupons formam perfis? O que o experimento de +10% no preço mede de fato? |

## Aplicações adicionais — não integram o livro

Cada uma declara em seu README: "Aplicação adicional — não corresponde a um capítulo de aplicação do livro. Fundamentação teórica: capítulos X, Y, Z."

| Caso (pasta) | Origem dos dados (fonte, licença, acesso) | Capítulos teóricos de apoio | Conceitos anteriores (unidades) | Perguntas do caso |
|---|---|---|---|---|
| [04 · Mobilidade: bicicletas compartilhadas](../10_estudos_de_caso/04_mobilidade_bicicletas/) | *Bike Sharing Dataset*, UCI id 275, CC BY 4.0, acesso 23/11/2026; `day.csv` e `hour.csv`, Washington D.C., 2011–2012 | 3 (Estatística), 4 (Pré-processamento), 8 (Séries Temporais); 5 (floresta, como ferramenta) | 02, 03, 04, 05, 08 | Quando a demanda é maior? Quanto pesa o clima? Modelos superam a linha de base no último trimestre? Que janelas operacionais os dados mostram? |
| [05 · Educação: desempenho e acompanhamento](../10_estudos_de_caso/05_educacao_desempenho/) | *Student Performance*, UCI id 320, CC BY 4.0, acesso 23/11/2026; `student-por.csv` e `student-mat.csv`, duas escolas portuguesas, 2005–2006 | 3 (Estatística: comparação de grupos, inferência), 5 (Classificação), 6 (Avaliação) | 03, 05, 06 | Que características se associam à nota final? Faltas importam tanto quanto se supõe? Uma lista curta de acompanhamento com boa cobertura é possível sem rotular alunos? |
| [06 · Varejo on-line: cancelamentos](../10_estudos_de_caso/06_varejo_online/) | *Online Retail*, UCI id 352, CC BY 4.0, acesso 23/11/2026; `online_retail.csv.gz` (conversão sem alteração do `.xlsx` original), Reino Unido, dez/2010–dez/2011 | 3 (Estatística), 4 (Pré-processamento), 7 (Agrupamento particional) | 02, 05, 07 | Quanto os cancelamentos valem e onde se concentram? Que segmentos existem? A pergunta sobre "abandono de carrinho" é respondível? |
| [07 · Votações na Wikipédia](../10_estudos_de_caso/07_votacoes_wikipedia/) | *Wikipedia vote network*, Stanford SNAP; `Wiki-Vote.txt` veio com o material do autor ([original/aplicacao_zip/Capitulos/Redes sociais/dados](../original/aplicacao_zip/Capitulos/Redes%20sociais/dados/)) e confere com o SNAP (7 115 nós, 103 689 arcos) | 9 (Redes Sociais: 9.1, 9.2, 9.3) | 07, 09 | Que padrões estruturais a rede tem? Centralidades concordam? Há comunidades? O que a estrutura não autoriza concluir sobre comportamento? |

## A aula de redes sociais não é um estudo de caso

Os scripts `grafoMatriz.py`, `metricasLocais.py`, `clique.py` e `comunidades_karate.py` do material do autor ([original/aplicacao_zip/Capitulos/Redes sociais](../original/aplicacao_zip/Capitulos/Redes%20sociais/)) fundamentam a **aula** [09 · Redes sociais](../09_redes_sociais/), baseada no **capítulo 9** (9.1 Rede Social e Grafo; 9.2 Análise Estrutural, com 9.2.1 Métricas Locais e 9.2.2 Métricas Globais; 9.3 Detecção de Comunidades, com 9.3.1 Girvan-Newman, 9.3.2 Louvain e 9.3.3 Espectral). Eles usam grafos construídos à mão, aleatórios com semente e o clube de karatê: servem para ver o que cada métrica calcula, não para sustentar recomendações. O caso 07 é a aplicação separada, com dados observacionais reais e limitações próprias.

## Mapa inverso: capítulo teórico → onde aparece

| Capítulo | Unidades | Casos |
|---|---|---|
| 3 Estatística | 03 | 01, 02, 03, 04, 05, 06 |
| 4 Pré-processamento | 05 | 01, 02, 04, 06 |
| 5 Classificação | 06 | 01, 05 (e 04 como regressão) |
| 6 Avaliação de Classificadores | 06 | 01, 05 |
| 7 Aprendizagem Não-Supervisionada | 07 | 03, 06 |
| 8 Séries Temporais | 08 | 02, 03 (decomposição), 04 |
| 9 Análise de Redes Sociais | 09 | 07 |
| 11, 12, 13 (Parte II) | — | 01, 02, 03 |
