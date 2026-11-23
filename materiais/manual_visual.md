# Manual visual

Regras para todas as figuras e animações deste repositório, a origem de cada regra e a figura que a exemplifica. O arquivo de estilo que as aplica no Matplotlib é [figuras/estilo.mplstyle](../figuras/estilo.mplstyle); os scripts o carregam com `plt.style.use(...)`. As figuras ficam em `figuras/geradas/`, `animacoes/geradas/` e nas pastas `figuras/` de cada unidade e caso, sempre com o script gerador ao lado ou em `figuras/fontes/` e `animacoes/fontes/`.

## 1. Fonte curricular: a aula de visualização

Arquivo lido: **`Ciencia_de_Dados_17.pdf`** (Visualização de Dados, Bruno Pimentel), 104 páginas no PDF com numeração interna de 1 a 96 (slides com pausas repetem o número interno). Lido integralmente em novembro de 2026: texto de todas as páginas e imagens das páginas com figuras. A aula se declara baseada em Knaflic, C. N., *Storytelling com Dados* (Alta Books, 2019), citado na página 102 do PDF (94 interna). As páginas abaixo são as do arquivo PDF; entre parênteses, a numeração interna do slide.

| Princípio encontrado na aula | Página(s) do PDF | Regra adotada neste repositório | Figura que o exemplifica |
|---|---|---|---|
| Visualização existe para comunicar o significado dos dados e apoiar uma decisão; "insights certos não significam nada se você não sabe como comunicar" | 4 (4), 14 (12) | Toda figura responde a uma pergunta escrita antes dela; figuras decorativas não entram | todos os READMEs trazem a pergunta antes da figura |
| Entender o contexto: quem é o público, o que ele deve fazer, como os dados defendem a ideia; análise exploratória ≠ explanatória | 16–24 (14–19) | Figuras de aula mostram o mecanismo (exploratória); figuras de caso mostram o achado para quem decide (explanatória), com legenda que diz o limite | [04_visualizacao/figuras/depois_rating_por_produto.png](../04_visualizacao/figuras/depois_rating_por_produto.png) |
| Texto simples quando há 1 ou 2 números | 27–29 (22) | Números isolados vão no texto ou no título, não em gráfico de duas barras | caso 02, README: "US$ 0,202 por kWh" no texto |
| Tabelas com bordas leves; heatmap em vez de tabela densa | 30–31 (23–24) | Tabelas em Markdown sem decoração; mapa de calor para hora × dia da semana | [02_energia_domestica/figuras/03_perfil_horario.png](../10_estudos_de_caso/02_energia_domestica/figuras/03_perfil_horario.png) |
| Gráficos mais eficientes: pontos, linhas e barras | 32–40 (25–33) | Repertório padrão: barras para categorias, linhas para tempo, dispersão para relações, histograma e boxplot para distribuições | [04_visualizacao](../04_visualizacao/README.md), scripts 01 a 04 |
| Barras horizontais e com rótulo de valor quando os nomes são longos; barras empilhadas só comparam bem a primeira série | 37–40 (30–33) | Nomes longos → barras horizontais ordenadas; empilhadas evitadas | [03_vendas_supermercado/figuras/01_mediana_avaliacao.png](../10_estudos_de_caso/03_vendas_supermercado/figuras/01_mediana_avaliacao.png) |
| Ética: barras começam em zero ("bar charts must have a zero baseline"); exemplo do eixo cortado em 34% | 41–42 (34–35) | Base zero obrigatória em barras; cortes de eixo em linhas só quando explícitos no título | [04_visualizacao/figuras/escalas_que_enganam.png](../04_visualizacao/figuras/escalas_que_enganam.png) |
| Evite gráfico de pizza; fatias de 26% e 31% parecem iguais; barras ordenadas resolvem | 43–44 (36) | Pizza só aparece como contraexemplo | [04_visualizacao/figuras/pizza_vs_barras.png](../04_visualizacao/figuras/pizza_vs_barras.png) |
| Saturação: alinhamento, cores, imagens, fontes, bordas e espaços competem pela atenção; princípios de Gestalt (proximidade, similaridade, cercamento, continuidade, conexão) | 46–47 (38–39) | Sem moldura superior e direita, grade só horizontal e clara, poucas cores, legenda sem caixa, espaço em branco | `estilo.mplstyle` (spines, grid, legend) |
| Exemplo 1: seis marcadores diferentes → barras com a série de interesse em azul e as demais em cinza | 48–49 (40–41) | "Nossa" série em azul, contexto em cinza | [06_classificacao_e_avaliacao/figuras/importancia_floresta.png](../06_classificacao_e_avaliacao/figuras/importancia_floresta.png) |
| Exemplo 2 passo a passo: tirar borda, grade e marcadores; limpar rótulos; rótulo direto no fim da linha em vez de legenda | 50–57 (42–49) | Rótulo direto quando há poucas séries; legenda só quando necessária | [08_series_temporais/figuras/grafico_sazonal.png](../08_series_temporais/figuras/grafico_sazonal.png) |
| Atributos pré-atentivos: tamanho, cor e posição dirigem a atenção; destaque seletivo (só três itens em vermelho, o resto cinza; texto explicativo ao lado) | 59–66 (51–58) | Uma cor de destaque por figura; cinza para o resto; anotação curta no ponto que importa | [04_visualizacao/figuras/linha_drugs.png](../04_visualizacao/figuras/linha_drugs.png) |
| Tabela com cores arco-íris → escala ordenada de azuis | 67 (59) | Escalas sequenciais em azuis (`Blues`); nada de arco-íris ou viridis decorativo | [09_redes_sociais/figuras/metricas_locais.png](../09_redes_sociais/figuras/metricas_locais.png) |
| Exemplo revisitado: tudo cinza → uma série em azul → rótulos só nos pontos relevantes | 68–72 (60–64) | Séries de comparação em cinza claro; rótulos numéricos só onde há algo a ler | [08_series_temporais/figuras/treino_teste_linhas_de_base.png](../08_series_temporais/figuras/treino_teste_linhas_de_base.png) |
| Design: a forma segue a função; realce o importante; elimine distrações; o texto é seu amigo (anotações explicam picos) | 74–81 (66–73) | Títulos afirmam o achado; anotações em picos e eventos | [04_mobilidade_bicicletas/figuras/01_serie_diaria.png](../10_estudos_de_caso/04_mobilidade_bicicletas/figuras/01_serie_diaria.png) (furacão Sandy) |
| Título em forma de pedido ou achado ("Please approve the hire of 2 FTEs"), eixo com unidade ("Number of tickets") | 82–84 (74–76) | Unidade em todo eixo; título com frase, não com nome de variável | [05_preprocessamento/figuras/ausentes.png](../05_preprocessamento/figuras/ausentes.png) |
| Contar uma história: início (por que prestar atenção), meio (como os dados resolvem), fim (o que fazer); repetição, lógica vertical, storyboarding reverso | 86–90 (78–82) | READMEs dos casos: situação → dados → achados → recomendação → limites; a mesma ordem em todos | [10_estudos_de_caso/README.md](../10_estudos_de_caso/README.md) |
| "Reunindo tudo": barras agrupadas ilegíveis → sequência de linhas, cada uma com uma frase-título, destaque progressivo e faixa da recomendação | 91–101 (83–93) | Antes/depois com os mesmos dados; recomendações marcadas no gráfico (faixa, linha tracejada) | [04_visualizacao/figuras/antes_rating_por_produto.png](../04_visualizacao/figuras/antes_rating_por_produto.png) → [depois](../04_visualizacao/figuras/depois_rating_por_produto.png); [06_classificacao_e_avaliacao/figuras/limiar_e_custo.png](../06_classificacao_e_avaliacao/figuras/limiar_e_custo.png) |

O que a aula **não** trata e que foi decidido de forma independente: a paleta concreta (cores e códigos hexadecimais), a tipografia, as proporções de exportação, a convenção semântica de cores entre figuras e as regras de acessibilidade. Essas decisões estão nas seções seguintes e não devem ser atribuídas à aula.

## 2. Paleta única e convenção semântica

![Paleta do repositório com o papel de cada cor](../figuras/geradas/paleta.png)

| Papel visual | Cor | Hex | Onde |
|---|---|---|---|
| Fundo e área de trabalho | Branco | `#FFFFFF` | `figure.facecolor`, `axes.facecolor` |
| Títulos, números e texto | Azul-marinho escuro | `#20324A` | `text.color`, eixos |
| Série principal, valores observados, grupo em destaque | Azul | `#2F648F` | 1ª cor do ciclo |
| Comparação, alternativa, previsão | Verde-petróleo | `#168A8A` | 2ª cor |
| Destaque de pergunta, ponto crítico, limiar escolhido | Âmbar | `#D69A35` | 3ª cor; linhas de corte tracejadas |
| Risco, erro, versão que distorce | Vermelho queimado | `#BD5B58` | 4ª cor; nunca decorativo |
| Elementos neutros, demais categorias | Cinza médio | `#8794A3` | 5ª cor |
| Grade, divisórias, séries ao fundo | Cinza muito claro | `#E6EBF0` | `grid.color` |
| Cor extra, só quando há mais de cinco grupos | Azul claro | `#7A9CC6` | cliques, comunidades |

Regras: a mesma informação tem a mesma cor em todas as figuras (observado = azul; previsão ou alternativa = verde-petróleo; limiar = âmbar; erro = vermelho). Vermelho só aparece quando há sentido de alerta: a versão que distorce em `escalas_que_enganam.png`, falsos negativos, cancelamentos. Escalas sequenciais usam `Blues`. Com mais grupos do que cores semânticas (comunidades, cliques), usa-se a lista categórica acima, sempre na mesma ordem.

## 3. Tipografia, eixos e formato

- Fonte sem serifa (DejaVu Sans, a padrão do Matplotlib, presente em qualquer instalação); corpo 11 pt, títulos 13 pt em negrito, alinhados à esquerda.
- Título com uma frase que afirma o achado ou a pergunta; subtítulo ou legenda em Markdown diz o limite ("dados simulados", "n = 49").
- Unidade em todo eixo; período e tamanho da amostra no título ou no rótulo quando mudam a leitura.
- Barras começam em zero. Eixo cortado em linhas só com aviso. Painéis lado a lado compartilham escala (`sharey`) quando se comparam. Sem dois eixos y, exceto como contraexemplo.
- Grade só horizontal, clara, atrás dos dados; sem molduras superior e direita; legenda sem caixa, preferindo rótulo direto.
- Categorias ordenadas pelo valor, salvo quando a ordem natural (hora, mês) importa.
- Proporção padrão 16:9 (8 × 4,5 pol.) para figuras e animações; painéis múltiplos usam larguras próprias quando 16:9 esmaga a leitura. Exportação PNG a 150 dpi; animações GIF a 80 dpi com `PillowWriter`, sempre acompanhadas de um PNG com o quadro final.

## 4. Acessibilidade e leitura crítica

- O significado nunca depende só da cor: linhas usam tracejado para a alternativa, marcadores para séries curtas, rótulos diretos e `n` por grupo.
- Contraste: texto `#20324A` sobre branco; cinza `#8794A3` só para contexto, nunca para o dado principal.
- Pontos sobrepostos recebem tamanho pequeno e transparência (`dispersao_sobreposicao.png`).
- Incerteza aparece quando existe: intervalos de confiança (`intervalos_materiais.png`, `02_grupos.png`), faixas p10–p90 (`04_janelas_de_capacidade.png`), intervalos de previsão (`arima_vs_linha_de_base.png`), bootstrap (caso 03).
- Filtros e remoções ficam registrados no título ou no script (ex.: "só casos até 300").
- Todo gráfico de correlação é acompanhado de texto que nega causalidade; a figura [correlacao_nao_causalidade.png](../figuras/geradas/correlacao_nao_causalidade.png) é o lembrete.
- Texto alternativo informativo em todas as imagens dos READMEs.

## 5. Antes e depois de um gráfico do material original

A figura `mediana_rating_por_produto.png` do material das aplicações (barras verticais em paleta viridis, rótulos inclinados, título que repete o eixo) foi reproduzida e refeita com os mesmos números pelo script [04_visualizacao/06_antes_e_depois.py](../04_visualizacao/06_antes_e_depois.py). As mudanças e os motivos estão comentados no script e no [README da unidade 04](../04_visualizacao/README.md). Outras figuras originais refeitas com conferência dos valores: perfil de consumo por hora (energia), boxplots dos valores pagos (TSA), dendrograma (supermercado), métricas locais e comunidades do karatê (redes). As originais permanecem em `original/aplicacao_zip/*/figuras/` para comparação.

## 6. Animações

Sete animações didáticas em `animacoes/geradas/`, geradas por `animacoes/fontes/`: média e mediana com um valor extremo; histograma crescendo; k-means passo a passo; formação do dendrograma; limiar e matriz de confusão; construção da matriz de adjacência; componentes de uma série e janelas de validação. Regras: eixos e paleta fixos durante toda a animação (só o que muda se move), um quadro parado no fim, texto que diz o que está acontecendo, tamanho entre 40 e 270 KB.

## 7. Como regenerar

Da pasta principal, com o ambiente ativado:

```
python scripts/executar_todos.py figuras/fontes animacoes/fontes
```

Cada unidade e caso regenera as próprias figuras ao executar seus scripts (`python scripts/executar_todos.py 04_visualizacao`, por exemplo). Sementes fixas garantem o mesmo resultado a cada execução.
