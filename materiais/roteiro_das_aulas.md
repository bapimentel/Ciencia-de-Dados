# Roteiro das aulas

Correspondência entre as unidades deste repositório, as aulas do [site da disciplina](https://sites.google.com/ic.ufal.br/ciencia-de-dados/documentos?authuser=0) e os capítulos teóricos (Parte I, capítulos 1 a 10) do livro *Ciência de Dados: da teoria à prática*. Os títulos das aulas foram lidos nos 18 PDFs publicados no site (`Ciencias_de_Dados_1.pdf` e `Ciencia_de_Dados_2.pdf` a `Ciencia_de_Dados_18.pdf`, versão de novembro de 2026); os sumários dos capítulos vêm da [página do livro](https://bapimentel.github.io/livro/).

## Aulas do site (títulos e sumários lidos)

| PDF | Título | Sumário |
|---|---|---|
| Ciencias_de_Dados_1 | Apresentação da disciplina | Informações gerais; o que é Ciência de Dados; por que estudar; plano do curso |
| Ciencia_de_Dados_2 | Conceitos de Ciência de Dados | O que é Ciência de Dados; cientista de dados; produto de dados; aplicações |
| Ciencia_de_Dados_3 | Conceitos de Big Data | Geração de dados; conceito; ferramentas; perspectivas |
| Ciencia_de_Dados_4 | Introdução a Python | Por que Python; operações básicas; tipos de objetos; estruturas de controle; funções; arquivos |
| Ciencia_de_Dados_5 | Estatística | O que é Estatística; Estatística, Ciência de Dados e megadados; preparação dos dados; análise de uma, duas e várias variáveis; regressão; sobrevivência |
| Ciencia_de_Dados_6 | Pré-processamento de dados | Visão geral; limpeza; integração; redução; transformação; exemplo em Python |
| Ciencia_de_Dados_7 | Aprendizagem de Máquina | Visão geral; algoritmos; aprendizagem supervisionada; avaliação de modelos; métodos de avaliação; vazamento de dados |
| Ciencia_de_Dados_8 | Aprendizado não supervisionado | Introdução; agrupamento hierárquico; agrupamento particional |
| Ciencia_de_Dados_9 | K-vizinhos mais próximos | Motivação; aprendizagem baseada em instâncias; K-NN; variações; aplicações |
| Ciencia_de_Dados_10 | Classificador Naive Bayes | Teorema de Bayes; Naive Bayes; limitações; aplicações |
| Ciencia_de_Dados_11 | Regressão | Simples; múltipla; logística; aplicação |
| Ciencia_de_Dados_12 | Métodos baseados em árvores e regras | Introdução; árvore de decisão; ganho de informação; overfitting |
| Ciencia_de_Dados_13 | Redes perceptron de múltiplas camadas | Revisão; perceptron de camada única; múltiplas camadas |
| Ciencia_de_Dados_14 | Máquinas de vetores de suporte | Introdução; modelo linear; não linear; margem soft |
| Ciencia_de_Dados_15 | Séries temporais | Introdução; fenômenos típicos; modelos; análise |
| Ciencia_de_Dados_16 | Recomendação de modelos | Introdução; estudos recentes; recomendação de modelos; aplicações |
| Ciencia_de_Dados_17 | Visualização de dados | Motivação; contexto; visual eficaz; saturação; foco da atenção; pensar como designer; contar uma história |
| Ciencia_de_Dados_18 | Análise de redes sociais | Motivação; conceitos básicos; análise estrutural; detecção de comunidades |

A seção *Projeto* do site contém `Projeto (2026-1).pdf` (lido integralmente; resumido em [11_projeto_final](../11_projeto_final/README.md)) e `Aula_cd_projeto.pdf` (não lido nesta reestruturação).

## Unidades do repositório

| Unidade | Conhecimentos prévios | Scripts | Aulas do site | Capítulos teóricos do livro |
|---|---|---|---|---|
| [00 · Como começar](../00_como_comecar/) | nenhum | `primeiro_programa.py` | 1 (apresentação), 4 (início) | 1 |
| [01 · Python do zero](../01_python/) | 00 | `01_operadores_e_variaveis.py` … `06_primeira_pergunta_com_dados.py` | 4 | 1 (contexto), 2 (dados em volume, só como leitura) |
| [02 · Primeiros dados](../02_primeiros_dados/) | 01 | `01_ler_uma_tabela.py` … `04_tipos_datas_e_ausencias.py` | 4, 5 (preparação dos dados) | 3.2 |
| [03 · Estatística](../03_estatistica/) | 02 | `01_medidas.py` … `05_teste_de_hipoteses.py` | 5 | 3 (3.2 descritiva, 3.3 probabilidade, 3.4 inferência) |
| [04 · Visualização](../04_visualizacao/) | 03 | `01_barras_ou_pizza.py` … `06_antes_e_depois.py` | 17 | figuras dos capítulos 11 a 13 como exemplos |
| [05 · Pré-processamento](../05_preprocessamento/) | 02, 03 | `01_inspecionar_e_duplicatas.py` … `07_preprocessamento_revisado.py` | 6, 7 (vazamento) | 4 (4.1 a 4.4) |
| [06 · Classificação e avaliação](../06_classificacao_e_avaliacao/) | 05 | `01_descricao_x_predicao.py` … `06_desbalanceamento_e_validacao.py` | 7, 9, 10, 11 (logística), 12, 13, 14 | 5 (5.1 a 5.5), 6 (6.1, 6.2) |
| [07 · Agrupamento](../07_agrupamento/) | 05, 06 | `01_kmeans_passo_a_passo.py` … `05_segmentar_vendas.py` | 8 | 7 (7.2.1, 7.2.2) |
| [08 · Séries temporais](../08_series_temporais/) | 03, 04 | `01_ler_e_visualizar.py` … `05_janelas_de_validacao.py` | 15 | 8 (8.1 a 8.3) |
| [09 · Redes sociais](../09_redes_sociais/) | 01, 07 | `01_grafo_manual.py` … `06_comunidades.py` | 18 | 9 (9.1, 9.2.1, 9.2.2, 9.3.1 a 9.3.3) |
| [10 · Estudos de caso](../10_estudos_de_caso/) | 02 a 09 | ver cada caso | 5, 6, 7, 8, 15, 18 conforme o caso | 11, 12, 13 (casos do livro); 3 a 9 (adicionais) |
| [11 · Projeto final](../11_projeto_final/) | tudo | — | Projeto (2026-1).pdf | 14 (considerações finais) |

## O que não tem unidade própria

- **Big Data** (aula 3, capítulo 2) e **meta-aprendizagem** (aula 16, capítulo 10): conteúdo conceitual, sem script neste repositório.
- **K-NN, Naive Bayes, MLP e SVM** (aulas 9, 10, 13, 14; seções 5.1, 5.2, 5.4, 5.5): a unidade 06 ensina a avaliar classificadores com regressão logística, árvore e floresta; os demais entram trocando uma linha (`KNeighborsClassifier`, `GaussianNB`, `MLPClassifier`, `SVC`), com a mesma sequência de separação, linha de base e métricas. A figura [fronteira_de_decisao.png](../figuras/geradas/fronteira_de_decisao.png) compara logística, árvore e K-NN.
- **Regras de associação e mapas de Kohonen** (7.1, 7.3) e **análise de sobrevivência** (aula 5): sem script.
- **Regressão linear** (aula 11, 8.2.3): aparece como ferramenta nas unidades 05 (vazamento) e no caso 04 (bicicletas), sem unidade dedicada.
