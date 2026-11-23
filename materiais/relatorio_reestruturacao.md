# Relatório da reestruturação (prestação de contas)

Data: 23 de novembro de 2026. Trabalho feito em uma pasta temporária, a partir de um único prompt de reestruturação, sem alterar o repositório original publicado. Este documento lista o que foi lido, o que foi criado, o que foi testado e o que ficou pendente.

## 1. Fontes consultadas

| Fonte | Situação |
|---|---|
| Repositório original (github.com/bapimentel/Ciencia-de-Dados) | Baixado (branch `master`) e lido por inteiro: `introducao.py`, `estatistica.py`, `preprocessamento.py`, `series_temporais.py`, `lista.txt`, `Dados/`, `Figuras/`. Cópia em `original/repositorio_2019/`. |
| `Aplicacao.zip` | Lido por inteiro: TSA, Series Temporais, Vendas e Capitulos/Redes sociais (scripts, dados e figuras). Cópia em `original/aplicacao_zip/`. |
| `Aulas.zip` (18 PDFs do site) | Texto extraído de todos; títulos e sumários registrados em `materiais/roteiro_das_aulas.md`. A pasta `Antigo/` do ZIP (versões anteriores e um vídeo de 208 MB) não foi usada. |
| `Ciencia_de_Dados_17.pdf` (visualização) | Lido integralmente: texto das 104 páginas e imagens das páginas com figuras. Princípios, páginas e regras em `materiais/manual_visual.md`. |
| `Projeto (2026-1).pdf` | Lido integralmente (11 páginas) no visualizador do site da disciplina; resumido em `11_projeto_final/README.md`. |
| `Aula_cd_projeto.pdf` | **Não lido.** |
| Página do livro (bapimentel.github.io/livro) e repositório da landing page | Sumário completo verificado; editora e ano (UICLAP, 2025) confirmados pela bibliografia do site da disciplina; ISBN não exibido. Nenhuma licença declarada. |
| Site da disciplina (página inicial e Documentos) | Lido; a seção "Estudos de Caso" não exibe arquivos. |
| Bases da UCI (ids 275, 320, 352) | Baixadas em 23/11/2026, licença CC BY 4.0 verificada nas páginas da UCI. |
| Wiki-Vote (SNAP) | Usado o arquivo que veio no ZIP; contagens conferem com o cabeçalho do SNAP (7 115 nós, 103 689 arcos). |
| Guia da Wikipédia sobre texto gerado por IA | Consultado como critério de estilo, não como detector. |

## 2. Árvore final

```
Ciencia-de-Dados/
├── README.md
├── requirements-basico.txt          requirements-aplicacoes.txt
├── 00_como_comecar/                 README + primeiro_programa.py
├── 01_python/                       README + 6 scripts + exercicios.md
├── 02_primeiros_dados/              README + 4 scripts + figuras/
├── 03_estatistica/                  README + 5 scripts + figuras/
├── 04_visualizacao/                 README + 6 scripts + figuras/ (inclui antes/depois)
├── 05_preprocessamento/             README + 7 scripts + figuras/
├── 06_classificacao_e_avaliacao/    README + 6 scripts + figuras/
├── 07_agrupamento/                  README + 5 scripts + figuras/
├── 08_series_temporais/             README + 5 scripts + figuras/
├── 09_redes_sociais/                README + 6 scripts + figuras/   (aula do capítulo 9)
├── 10_estudos_de_caso/              README de índice
│   ├── 01_reclamacoes_tsa/          cap. 11 · 5 scripts + 1 opcional (SHAP) + dados/ + figuras/
│   ├── 02_energia_domestica/        cap. 12 · 5 scripts
│   ├── 03_vendas_supermercado/      cap. 13 · 5 scripts
│   ├── 04_mobilidade_bicicletas/    adicional · 4 scripts (UCI 275)
│   ├── 05_educacao_desempenho/      adicional · 4 scripts (UCI 320)
│   ├── 06_varejo_online/            adicional · 5 scripts (UCI 352)
│   └── 07_votacoes_wikipedia/       adicional · 4 scripts (SNAP)
├── 11_projeto_final/                README (roteiro baseado no PDF do projeto)
├── materiais/                       roteiro_das_aulas.md, mapa_capitulos_aplicacoes.md, manual_visual.md, este relatório
├── figuras/                         estilo.mplstyle, README, fontes/ (5 geradores), geradas/ (5 PNG)
├── animacoes/                       fontes/ (7 geradores), geradas/ (7 GIF + 7 PNG)
├── dados/                           README + Data.csv, Drugs.csv, SPCS20RPSNSA.csv, supermercado.csv
├── original/                        README + repositorio_2019/ + aplicacao_zip/ (sem alterações)
└── scripts/                         executar_todos.py, verificar_links.py, relatorio_execucao.txt
```

Totais fora de `original/`: 98 scripts Python, 27 arquivos Markdown, 102 PNG e 7 GIF gerados por código, 29 MB (dos quais 7,5 MB é `online_retail.csv.gz`). Com `original/`: 387 arquivos, 47 MB.

## 3. Origem de cada arquivo novo

| Arquivo original | Arquivos novos |
|---|---|
| `introducao.py` | `01_python/01` a `05` (mesma progressão; `print` acrescentado); `06_primeira_pergunta_com_dados.py` é novo |
| `estatistica.py` | `03_estatistica/01`, `03`, `05` (medidas, distribuições, testes); `04_visualizacao/01` a `04` (gráficos) |
| `preprocessamento.py` | `05_preprocessamento/07_preprocessamento_revisado.py` (API atual, `fit` só no treino); `02`, `03`, `04` decompõem os conceitos |
| `series_temporais.py` | `08_series_temporais/04_arima_revisado.py` (API atual, linha de base); `01`, `02`, `03`, `05` novos |
| `Aplicacao/TSA/leitura.py` | `10_estudos_de_caso/01_reclamacoes_tsa/01` a `05` + `06_shap_opcional.py` |
| `Aplicacao/Series Temporais/analise.py` | `10_estudos_de_caso/02_energia_domestica/01` a `05` |
| `Aplicacao/Vendas/analise.py` | `10_estudos_de_caso/03_vendas_supermercado/01` a `05` |
| `Redes sociais/grafoMatriz.py` | `09_redes_sociais/01_grafo_manual.py`, `02_matriz_de_adjacencia.py`, `animacoes/fontes/matriz_adjacencia_construcao.py` |
| `Redes sociais/metricasLocais.py` | `09_redes_sociais/03_metricas_locais.py` (`04_metricas_globais.py` é novo) |
| `Redes sociais/clique.py` | `09_redes_sociais/05_cliques.py` |
| `Redes sociais/comunidades_karate.py` | `09_redes_sociais/06_comunidades.py` |
| `Redes sociais/dados/Wiki-Vote.txt` | `10_estudos_de_caso/07_votacoes_wikipedia/` |
| — | `02_primeiros_dados/*`, `06_classificacao_e_avaliacao/*`, `07_agrupamento/*`, casos 04 a 06, `figuras/fontes/*`, `animacoes/fontes/*`, `materiais/*`, `scripts/*`: novos |

## 4. Correções de API e de conteúdo

- `OneHotEncoder(categorical_features=...)` → `OneHotEncoder(sparse_output=False, handle_unknown='ignore')`.
- `statsmodels.tsa.arima_model.ARIMA` e `plot_predict` → `statsmodels.tsa.arima.model.ARIMA` e `get_forecast`.
- `vert=False` (depreciado no Matplotlib 3.11) → `orientation='horizontal'`; `dayofweek` (depreciado no pandas 3) → `day_of_week`.
- `comunidades_karate.py` dependia de `python-louvain` e `node2vec`; a aula usa `nx.community.louvain_communities` e dispensa o K-means sobre *embeddings*.
- `grafoMatriz.py`: título dizia "6 nós e 8 arestas" para 7 nós e 12 arestas; corrigido e arestas fixadas. Layouts e sorteios sem semente nos scripts de redes receberam semente.
- `analise.py` (energia) criava `Valor = Uso × Custo` (kWh × dólares); a coluna não tem significado e não foi mantida. A tarifa implícita é constante (US$ 0,202/kWh), o que é mostrado.
- `analise.py` (vendas): o experimento de +10% no preço é reproduzido e explicado como artefato da identidade `Total = preço × quantidade × 1,05`; a codificação de categorias como inteiros antes do agrupamento é comparada com a versão só numérica.
- `leitura.py` (TSA): separação estratificada com semente, linha de base e métricas por classe acrescentadas; SHAP isolado em script opcional.

## 5. Testes executados

- `python scripts/executar_todos.py` (ambiente virtual limpo, Python 3.13.15, pandas 3.1.1, numpy 2.5.5, matplotlib 3.11.2, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, networkx 3.7, Pillow 13.0.0, openpyxl 3.1.5): **95 de 95 scripts executaram sem erro**, com `MPLBACKEND=Agg`, cada um a partir da própria pasta. Tempo total abaixo de 2 minutos. Registro em `scripts/relatorio_execucao.txt`.
- `python -m compileall` em todas as pastas de código: sem erros.
- `python scripts/verificar_links.py`: 295 links e imagens relativos conferidos nos 27 Markdown, nenhum quebrado.
- Figuras conferidas visualmente por amostragem (cerca de 30 das 102) para sobreposição de títulos, legendas e legibilidade; as que apresentavam problema foram ajustadas e regeneradas.
- Os números citados nos READMEs foram copiados da saída dos scripts nesta execução.

## 6. Não verificado ou não feito

- `06_shap_opcional.py` não foi executado (o `shap` não está no ambiente básico); o runner o ignora pelo nome.
- `requirements-aplicacoes.txt` não foi instalado em ambiente separado; só o básico foi testado.
- Os scripts originais em `original/` não foram executados (dependências ausentes e caminhos relativos ao diretório de execução).
- Não foi testado em Linux ou macOS nem com Python 3.11/3.12; os comandos da unidade 00 para esses sistemas seguem a documentação oficial.
- `Aula_cd_projeto.pdf` não foi lido; o cronograma do site não foi consultado.
- A licença do código não foi definida: o repositório original não tinha arquivo de licença e nenhum foi criado. A origem primária de `supermarket_sales - Sheet1.csv` e de `D202.csv` não consta no material e não foi presumida.
- Os PDFs das aulas 2 a 16 e 18 foram lidos pelo texto extraído, apenas para títulos e sumários; o conteúdo interno não foi incorporado além disso.
- Não há notebooks `.ipynb`; a trilha é só em scripts, como o prompt permitia.

## 7. Decisões que dependem do autor

1. Licença do código e confirmação da redistribuição das bases do livro (ver `dados/README.md`).
2. Manter ou não `online_retail.csv.gz` (7,5 MB) no repositório; a alternativa é só o script de conversão e a instrução de download.
3. Publicar `original/` inteiro (18 MB, com 87 figuras antigas) ou apenas um ponto do histórico do Git.
4. Nome do repositório e da branch de publicação; os links dos READMEs são relativos e funcionam em qualquer um.
5. Conferir, no livro impresso, as páginas das seções 11.1 a 13.4 citadas nas tabelas dos casos (as tabelas citam seções, não páginas).

## 8. Como aplicar

A pasta temporária contém o repositório completo. Para publicar: copiar o conteúdo para um clone do repositório, revisar os itens da seção 7, e fazer o commit. O `original/repositorio_2019/` reproduz o que já está no histórico; se preferir não duplicar, basta apontar o `original/README.md` para o commit correspondente.

## 9. Verificação final específica do prompt

- [x] Um único prompt orientou todo o trabalho; o README final é o resultado.
- [x] `09_redes_sociais/` é aula do capítulo 9, com os scripts do ZIP reorganizados (grafo → matriz → métricas locais → globais → cliques → comunidades).
- [x] Redes sociais só entram em `10_estudos_de_caso/` com dados observacionais reais (Wiki-Vote), significado das arestas explicado e pergunta aplicada com limites declarados.
- [x] TSA, energia e supermercado identificam os capítulos 11, 12 e 13, as subseções e a origem no ZIP, com tabela verificável em cada README.
- [x] Casos 04 a 07 declaram "Aplicação adicional — não corresponde a um capítulo de aplicação do livro" e os capítulos teóricos de apoio.
- [x] `materiais/mapa_capitulos_aplicacoes.md` existe, com links conferidos.
- [x] O PDF de visualização foi lido, com nome e páginas registrados em `materiais/manual_visual.md`.
- [x] `materiais/manual_visual.md` tem paleta única, tipografia, eixos, acessibilidade e convenção semântica de cores.
- [x] Gráficos antigos foram refeitos (antes/depois documentado); os novos usam o mesmo estilo e têm código gerador.
- [x] Sete animações didáticas, leves (37 a 270 KB), com semente e quadro estático.
- [x] Todas as aplicações têm pergunta, evidência calculada, limites, recomendação proporcional, indicador, prazo e critério proposto; onde a evidência não sustenta a ação, isso está escrito.
- [x] README principal sem publicidade, com os capítulos corretos e sem exigir o livro.
- [x] Scripts curtos (20 a 110 linhas), lineares, sem classes ou `main()`.
