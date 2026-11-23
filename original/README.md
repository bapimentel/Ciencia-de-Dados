# Material original preservado

Nada aqui foi editado. São as fontes da reestruturação, mantidas para rastreabilidade e comparação.

## `repositorio_2019/`

Cópia do repositório [github.com/bapimentel/Ciencia-de-Dados](https://github.com/bapimentel/Ciencia-de-Dados) tal como estava em novembro de 2026 (arquivos de 2019): `introducao.py`, `estatistica.py`, `preprocessamento.py`, `series_temporais.py`, `lista.txt`, `Dados/` (`Data.csv`, `Drugs.csv`, `SPCS20RPSNSA.csv`) e `Figuras/` (dez PNGs). O arquivo `Thumbs.db` do Windows foi omitido.

| Original | Onde foi parar |
|---|---|
| `introducao.py` | [01_python](../01_python/), scripts 01 a 05 (mesma progressão, com `print` onde o resultado precisa aparecer) |
| `estatistica.py` (medidas, distribuições, testes) | [03_estatistica](../03_estatistica/), scripts 01, 03, 05 |
| `estatistica.py` (barras, pizza, histograma, linha, dispersão) | [04_visualizacao](../04_visualizacao/), scripts 01 a 04 |
| `preprocessamento.py` | [05_preprocessamento/07_preprocessamento_revisado.py](../05_preprocessamento/07_preprocessamento_revisado.py) (API atual, ordem corrigida) |
| `series_temporais.py` | [08_series_temporais/04_arima_revisado.py](../08_series_temporais/04_arima_revisado.py) (API atual do statsmodels) |
| `Dados/Data.csv`, `Drugs.csv`, `SPCS20RPSNSA.csv` | copiados para [dados/](../dados/) com os mesmos nomes |
| `lista.txt` | o script [01_python/05_arquivos.py](../01_python/05_arquivos.py) o recria em UTF-8 na própria pasta |
| `Figuras/*.png` | substituídas pelas figuras geradas pelos novos scripts; as originais ficam aqui |

## `aplicacao_zip/`

Conteúdo integral de `Aplicacao.zip`, material do autor para o livro *Ciência de Dados: da teoria à prática*:

| Pasta | Conteúdo | Onde foi parar |
|---|---|---|
| `TSA/` | `leitura.py`, `dados/claims-data-2015-as-of-feb-9-2016.xlsx`, 42 figuras | [10_estudos_de_caso/01_reclamacoes_tsa](../10_estudos_de_caso/01_reclamacoes_tsa/) (capítulo 11) |
| `Series Temporais/` | `analise.py`, `dados/D202.csv`, `dados/D202.xlsx`, 18 figuras | [10_estudos_de_caso/02_energia_domestica](../10_estudos_de_caso/02_energia_domestica/) (capítulo 12); só o CSV foi copiado |
| `Vendas/` | `analise.py`, `dados/supermarket_sales - Sheet1.csv`, `estatisticas_produtos.txt`, 14 figuras e 2 CSVs de previsões | [10_estudos_de_caso/03_vendas_supermercado](../10_estudos_de_caso/03_vendas_supermercado/) (capítulo 13); a base também está em [dados/supermercado.csv](../dados/supermercado.csv) para as unidades iniciais |
| `Capitulos/Redes sociais/` | `grafoMatriz.py`, `metricasLocais.py`, `clique.py`, `comunidades_karate.py`, `dados/Wiki-Vote.txt`, 13 figuras | aula [09_redes_sociais](../09_redes_sociais/) (capítulo 9) e caso [07_votacoes_wikipedia](../10_estudos_de_caso/07_votacoes_wikipedia/) |

Os scripts originais dependem de bibliotecas que não estão no ambiente básico (`seaborn`, `shap`, `pmdarima`, `python-louvain`, `node2vec`) e de caminhos relativos à pasta em que são executados. Eles não são executados pelo `scripts/executar_todos.py`.
