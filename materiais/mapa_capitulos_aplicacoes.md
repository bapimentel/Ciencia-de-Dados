# Mapa entre unidades, estudos de caso e capítulos do livro

O livro *Ciência de Dados: da teoria à prática* (Bruno Pimentel, UICLAP, 2025) tem duas partes. Parte I — Teoria: 1 Conceitos; 2 Big Data; 3 Estatística; 4 Pré-processamento; 5 Classificação; 6 Avaliação de Classificadores; 7 Aprendizagem Não-Supervisionada; 8 Séries Temporais; 9 Análise de Redes Sociais; 10 Meta-Aprendizagem. Parte II — Prática: 11 Aplicação 1: Reclamações por Perdas; 12 Aplicação 2: Energia Doméstica; 13 Aplicação 3: Vendas em Supermercado; 14 Considerações Finais.

## Capítulo teórico → unidade do repositório

| Capítulo | Unidades |
|---|---|
| 1 Conceitos | [01](../01_conceitos_e_big_data/) |
| 2 Big Data | [01](../01_conceitos_e_big_data/) |
| 3 Estatística | [04](../04_estatistica/) |
| 4 Pré-processamento | [06](../06_preprocessamento/) |
| 5 Classificação | [09](../09_knn/) (k-NN), [10](../10_naive_bayes/) (Naive Bayes), [11](../11_regressao/) (logística), [12](../12_arvores_de_decisao/) (árvores), [13](../13_redes_neurais/) (redes neurais), [14](../14_svm/) (SVM) |
| 6 Avaliação de Classificadores | [07](../07_aprendizagem_de_maquina/) |
| 7 Aprendizagem Não-Supervisionada | [08](../08_agrupamento/) |
| 8 Séries Temporais | [15](../15_series_temporais/) |
| 9 Análise de Redes Sociais | [17](../17_redes_sociais/) |
| 10 Meta-Aprendizagem | [16](../16_recomendacao_de_modelos/) |

## Estudos de caso do livro (Parte II)

| Estudo de caso | Capítulo | Dados | Unidades de apoio |
|---|---|---|---|
| [01 · Reclamações por perdas (TSA)](../18_estudos_de_caso/01_reclamacoes_tsa/) | 11 | reclamações recebidas pela TSA (EUA) em 2015 | 04, 06, 07, 11, 12 |
| [02 · Energia doméstica](../18_estudos_de_caso/02_energia_domestica/) | 12 | leituras de 15 minutos de uma residência, 2016–2018 | 04, 06, 15 |
| [03 · Vendas em supermercado](../18_estudos_de_caso/03_vendas_supermercado/) | 13 | 1 000 cupons de três filiais, jan–mar/2019 | 04, 05, 08, 15 |

## Aplicações adicionais — não integram o livro

| Estudo de caso | Capítulos teóricos relacionados | Dados (fonte e licença) | Unidades de apoio |
|---|---|---|---|
| [04 · Bicicletas compartilhadas](../18_estudos_de_caso/04_mobilidade_bicicletas/) | 3, 4, 8 | *Bike Sharing Dataset*, UCI id 275, CC BY 4.0 | 04, 06, 11, 15 |
| [05 · Educação](../18_estudos_de_caso/05_educacao_desempenho/) | 3, 5, 6 | *Student Performance*, UCI id 320, CC BY 4.0 | 04, 07, 11 |
| [06 · Varejo on-line](../18_estudos_de_caso/06_varejo_online/) | 3, 4, 7 | *Online Retail*, UCI id 352, CC BY 4.0 | 05, 06, 08 |
| [07 · Votações na Wikipédia](../18_estudos_de_caso/07_votacoes_wikipedia/) | 9 | *Wikipedia vote network*, Stanford SNAP | 17 |

## A unidade de redes sociais não é um estudo de caso

A unidade [17 · Redes sociais](../17_redes_sociais/) usa grafos construídos à mão, redes aleatórias com semente e o clube de karatê de Zachary: servem para ver o que cada métrica calcula, não para sustentar recomendações. O estudo de caso 07 é a aplicação com dados reais, com limitações próprias.
