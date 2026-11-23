# Estudo de caso 3 · Vendas em supermercado

> Estudo de caso do capítulo 13 do livro *Ciência de Dados: da teoria à prática*. Técnicas usadas: verificação do significado das colunas, comparação de grupos (Kruskal-Wallis), decomposição de séries, verificação de estabilidade de um padrão, agrupamento hierárquico, crítica de um experimento com modelo, política de estoque (modelo do jornaleiro) avaliada por origem móvel, avaliação fora da amostra de uma escala de trabalho.

## A situação

Uma rede de supermercados com três filiais em Mianmar entrega à equipe de dados os cupons de janeiro a março de 2019 e pergunta:

1. Alguma linha de produto ou filial se destaca?
2. Há dias ou horários de maior movimento, para organizar caixas e reposição?
3. Os clientes formam perfis diferentes?
4. Aumentar preços aumentaria o faturamento?
5. Com quanto estoque cada linha de produto deve começar a semana?

Este caso ensina uma lição que aparece em todo projeto real: **um padrão encontrado no total precisa ser conferido em partes dos dados antes de virar decisão**. Aqui, a conferência derruba o padrão horário, e é justamente a **ausência** de padrão que indica a decisão certa de estoque, cujo efeito é medido em semanas que o modelo não viu.

## Os dados

`dados/supermarket_sales - Sheet1.csv`: 1 000 cupons (base pública "Supermarket sales", disponível no Kaggle). Uma linha por cupom, com um único produto por cupom.

| Coluna | Conteúdo |
|---|---|
| `Invoice ID` | identificador do cupom |
| `Branch`, `City` | filial (A, B, C) e cidade (Yangon, Mandalay, Naypyitaw) |
| `Customer type`, `Gender` | cliente cadastrado ou não; gênero |
| `Product line` | seis linhas de produto |
| `Unit price`, `Quantity` | preço unitário e quantidade |
| `Tax 5%`, `Total` | imposto e total do cupom |
| `Date`, `Time` | data e hora |
| `Payment` | forma de pagamento |
| `cogs`, `gross margin percentage`, `gross income` | custo, margem e receita bruta (ver Passo 1) |
| `Rating` | avaliação do cliente (4 a 10) |

**O que a base não tem:** identificação do cliente (só do cupom), custo real, estoque, histórico de preços de um mesmo produto.

## Scripts

| Passo | Script | Figuras |
|---|---|---|
| 1. Conhecer e comparar grupos | `01_conhecer_os_dados.py` | `01_distribuicoes_por_linha.png`, `01_mediana_avaliacao.png` |
| 2. Análise temporal | `02_analise_temporal.py` | `02_decomposicao_semanal.png`, `02_dia_da_semana_e_hora.png` |
| 3. O padrão se repete? | `03_o_padrao_se_repete.py` | `03_o_padrao_se_repete.png` |
| 4. Perfis de vendas | `04_perfis_de_vendas.py` (grava `dados/perfis.csv`) | `04_dendrograma_perfis.png` |
| 5. O que o preço explica | `05_o_que_o_preco_explica.py` | `05_preco_x_quantidade.png` |
| 6. Quanto dado seria preciso | `06_quanto_dado_seria_preciso.py` | `06_quanto_dado_seria_preciso.png` |
| 7. Reposição de estoque | `07_reposicao_de_estoque.py` | `07_reposicao_de_estoque.png` |
| 8. Escala de caixas | `08_escala_de_caixas.py` | `08_escala_de_caixas.png` |

---

## Passo 1 · Conhecer os dados e comparar linhas de produto e filiais

**Pergunta:** o que as colunas significam? Alguma linha de produto ou filial se destaca?

Antes de calcular qualquer média, conferimos o que as colunas de dinheiro medem:

```python
(vendas['Total'] - vendas['Unit price'] * vendas['Quantity'] * 1.05).abs().max()   # 0
vendas['gross margin percentage'].unique()                                         # um único valor
(vendas['gross income'] - vendas['Tax 5%']).abs().max()                             # 0
```

**O que saiu:** `Total` é exatamente preço × quantidade × 1,05; a "margem bruta" é a mesma constante em todos os cupons; e `gross income` é idêntico ao imposto de 5%. **A base não mede lucro.** Nenhuma conclusão sobre margem é possível.

Comparando as seis linhas de produto e as três filiais com o teste de Kruskal-Wallis (que compara as distribuições de vários grupos):

| Variável | Entre linhas de produto (p) | Entre filiais (p) |
|---|---|---|
| Preço unitário | 0,82 | 0,66 |
| Quantidade | 0,33 | 0,85 |
| Avaliação | 0,74 | 0,13 |
| Total do cupom | 0,83 | 0,81 |

As filiais faturaram 106 200, 106 198 e 110 569 no trimestre. As avaliações medianas por linha ficam entre 6,7 e 7,3.

![Distribuições por linha](figuras/01_distribuicoes_por_linha.png)

![Mediana da avaliação](figuras/01_mediana_avaliacao.png)

**Conclusão do passo:** nenhum teste aponta diferença. Linhas de produto e filiais são, para todos os fins práticos, parecidas. Não há base para priorizar uma linha ou uma filial.

## Passo 2 · Há dias ou horários de maior movimento?

**Pergunta:** o movimento muda com o dia da semana ou com a hora?

O script monta a série diária (89 dias com vendas), decompõe com período semanal e agrega por dia da semana e por hora.

**O que saiu:**

- A componente semanal da quantidade por cupom tem amplitude de menos de uma unidade, e o teste de Kruskal-Wallis entre dias da semana dá **p = 0,58**: a quantidade por cupom não muda com o dia.
- Em número de cupons por dia, terça (12,2) e sábado (12,6) ficam à frente de segunda (10,4).
- Por hora, somando os três meses, **as 19h têm o maior faturamento** (446 por dia, contra 258 às 20h).

![Decomposição semanal](figuras/02_decomposicao_semanal.png)

![Dia da semana e hora](figuras/02_dia_da_semana_e_hora.png)

Parece haver uma recomendação pronta: reforçar caixas às 19h, às terças e aos sábados. Antes de fazê-la, o Passo 3 confere se esse padrão é real.

## Passo 3 · O padrão se repete em cada mês e em cada filial?

**Pergunta:** a hora de pico aparece em todos os meses e em todas as filiais, ou só no total?

Um padrão útil para organizar a operação precisa se **repetir**. Repetimos a análise por hora separadamente para janeiro, fevereiro e março, e para cada filial.

```python
por_mes = vendas.pivot_table(index='Hora', columns='Mes', values='Total', aggfunc='sum')
participacao = por_mes / por_mes.sum()
participacao.idxmax()          # hora de maior faturamento em cada mês
participacao.corr()            # os perfis dos meses se parecem?
```

**O que saiu:**

| | Hora de maior faturamento | Correlação entre perfis horários |
|---|---|---|
| Janeiro | 13h | jan × fev: 0,27 |
| Fevereiro | 15h | jan × mar: 0,14 |
| Março | 19h | fev × mar: −0,12 |
| Filial A | 11h | A × B: 0,16 |
| Filial B | 19h | A × C: 0,27 |
| Filial C | 19h | B × C: 0,53 |

- **A hora de pico muda a cada mês.** O "pico das 19h" vem quase todo de março (52 cupons às 19h, contra 35 em janeiro e 26 em fevereiro).
- Os perfis horários de meses diferentes quase não se correlacionam (−0,12 a 0,27).
- Testes: o número de cupons por hora vai de 74 a 113, e o teste contra "todas as horas iguais" dá p = 0,050, no limite. A distribuição por hora não difere entre os meses de forma detectável (p = 0,51), e o valor por cupom não muda com a hora (p = 0,37).
- **Metade × metade:** dividindo os 89 dias em duas metades sorteadas, 1 000 vezes, a correlação entre os perfis horários das duas metades tem mediana de **0,30** (90% dos sorteios entre −0,07 e 0,65). Metade dos dias mal prevê o perfil da outra metade.

O mesmo acontece com os dias da semana:

| Cupons por dia | seg | ter | qua | qui | sex | sáb | dom |
|---|---|---|---|---|---|---|---|
| Janeiro | 11,0 | 12,4 | 10,4 | 11,0 | 10,0 | **14,0** | 10,8 |
| Fevereiro | 10,5 | **9,5** | 11,2 | 10,0 | 12,0 | 10,8 | 11,8 |
| Março | 9,8 | **14,5** | 11,5 | 10,8 | 10,2 | 13,0 | 10,8 |

Em fevereiro, a terça é o dia **mais fraco**.

![O padrão se repete?](figuras/03_o_padrao_se_repete.png)

**Conclusão do passo:** os "picos" do Passo 2 são, em grande parte, ruído de uma amostra pequena (cerca de 90 cupons por hora em três meses). O movimento é aproximadamente uniforme ao longo do dia e da semana.

## Passo 4 · Os cupons formam perfis?

**Pergunta:** há grupos de compras com comportamento diferente?

Usamos agrupamento hierárquico (método de Ward) sobre preço, quantidade, avaliação e hora, padronizados. `Total` e imposto ficam de fora porque são funções de preço × quantidade.

| Número de grupos | Tamanhos | Silhueta |
|---|---|---|
| 2 | 352 e 648 | 0,127 |
| 3 | 352, 227, 421 | 0,139 |
| 4 | 352, 227, 166, 255 | 0,142 |

Com dois grupos: o perfil 1 tem preço médio de 36 e avaliação de 6,4; o perfil 2, preço de 66 e avaliação de 7,3. Filial, linha de produto e tipo de cliente se distribuem igualmente nos dois (por exemplo, 51% e 50% de clientes cadastrados).

![Dendrograma e perfis](figuras/04_dendrograma_perfis.png)

**Como ler:** silhuetas abaixo de 0,15 indicam que **não há grupos naturais**: o algoritmo sempre devolve grupos, mas aqui eles só fatiam uma nuvem contínua. Os perfis servem para descrever (compras de itens baratos × caros), não para orientar ações por "tipo de cliente". Além disso, a base identifica cupons, não clientes.

**Um erro comum, para comparar.** Se codificarmos filial, cidade e produto como 0, 1, 2 e agruparmos junto com as numéricas, surgem grupos de 251 e 749 cupons que se separam em parte pela cidade (Yangon vira "mais distante" de Naypyitaw do que de Mandalay só por causa dos números escolhidos). A concordância com os perfis anteriores é nula (ARI = −0,01). A codificação criou a estrutura.

## Passo 5 · Aumentar o preço aumentaria o faturamento?

**Pergunta:** um modelo que prevê o total pode dizer o efeito de um aumento de preço?

Um experimento frequente: treinar, em cada perfil, uma floresta que prevê o total a partir de preço, produto, filial e cliente; depois aumentar o preço em 10% e ver o que o modelo prevê.

**O que saiu:** a mediana prevista sobe de 184 para 206 (perfil 1) e de 361 para 399 (perfil 2), com teste de Wilcoxon p < 0,0001. Parece uma evidência forte.

Mas o que o teste mediu? O total **é** preço × quantidade × 1,05. Ao ver um preço maior com tudo o mais igual, o modelo só pode prever um total maior. A pergunta real é se **a quantidade cairia** com o preço mais alto, e a base não tem como responder:

| Faixa de preço unitário | Cupons | Quantidade média |
|---|---|---|
| 10–27 | 200 | 5,54 |
| 27–47 | 200 | 5,38 |
| 47–65 | 200 | 5,48 |
| 65–83 | 200 | 5,66 |
| 83–100 | 200 | 5,49 |

![Preço e quantidade](figuras/05_preco_x_quantidade.png)

A correlação entre preço e quantidade é 0,01. Cada cupom é um produto diferente com seu próprio preço; não há o **mesmo** produto vendido a preços diferentes. Para medir o efeito de preço seria preciso um experimento (o mesmo item com preços diferentes em lojas ou semanas comparáveis) ou um histórico de preços.

**Conclusão do passo:** a base não permite afirmar que aumentar preços aumenta o faturamento.

## Passo 6 · Quanto histórico seria preciso para confiar num perfil por hora?

**Pergunta:** se o padrão horário não é confiável com três meses, com quanto tempo seria?

Medimos, nos próprios dados, a concordância entre os perfis horários de duas amostras **independentes** de dias, aumentando o tamanho das amostras:

| Dias em cada amostra | 5 | 10 | 15 | 20 | 30 | 44 |
|---|---|---|---|---|---|---|
| Correlação mediana | 0,04 | 0,07 | 0,10 | 0,14 | 0,22 | 0,32 |

A concordância cresce devagar. A fórmula de Spearman-Brown, usada para estimar a confiabilidade de uma medida com mais dados, $r_m = m\,r/(1 + (m-1)\,r)$, indica que, para chegar a 0,8, seriam necessárias cerca de **9 vezes mais dias**: em torno de **377 dias por amostra**, ou seja, mais de um ano de cupons em cada metade.

![Quanto dado seria preciso](figuras/06_quanto_dado_seria_preciso.png)

A projeção supõe que exista um padrão estável e que os dias sejam independentes; ela dá uma **ordem de grandeza** para planejar a coleta, não um número exato.

## Passo 7 · Com quanto estoque cada linha deve começar a semana?

**Pergunta:** se as vendas não têm padrão de dia ou de hora, como decidir quanto repor de cada linha de produto?

Os Passos 1 a 3 mostraram que a demanda semanal de cada linha **oscila em torno de uma média**, sem tendência nem padrão que se repita. Essa é exatamente a situação do problema clássico de estoque conhecido como **modelo do jornaleiro** (*newsvendor*): a melhor quantidade para começar o período é

$$\text{estoque-alvo} = \text{média} + z \times \text{desvio-padrão}$$

da demanda das semanas anteriores, com $z$ escolhido pelo **nível de serviço** desejado ($z = 1{,}28$ para que, em 90% das semanas, não falte produto).

Comparamos quatro políticas por **origem móvel**: para cada semana, da 5ª à 11ª, a política só vê as semanas anteriores e é comparada com a demanda real daquela semana. São 7 semanas × 6 linhas = **42 linhas-semana** que nenhuma política viu.

```python
for i in range(4, len(semanal)):
    alvo = semanal.iloc[:i].mean() + 1.282 * semanal.iloc[:i].std()
    demanda = semanal.iloc[i]
    falta += (demanda - alvo).clip(lower=0).sum()
```

**O que saiu:**

| Política | Linhas-semana com falta | Unidades em falta | Unidades que sobraram | Estoque médio por linha |
|---|---|---|---|---|
| Repor o que vendeu na semana anterior | 20/42 (**48%**) | 423 | 502 | 74,1 |
| Média das semanas anteriores | 17/42 (40%) | 336 | 489 | 75,8 |
| Média + 0,67 dp (75% de serviço) | 12/42 (29%) | 111 | 841 | 89,6 |
| **Média + 1,28 dp (90% de serviço)** | **3/42 (7%)** | **12** | 1 263 | **102,0** |

![Reposição de estoque](figuras/07_reposicao_de_estoque.png)

**Como ler:**

- "Repor o que vendeu na semana anterior", a regra mais intuitiva, é a **pior**: ela persegue a oscilação da semana passada, que (Passo 3) não se repete.
- A política de 90% de serviço deixou faltar produto em **3 de 42** linhas-semana (7%), muito perto dos 10% que ela promete. O modelo cumpriu, em semanas que não viu, o que foi construído para fazer.
- O custo também está medido: o estoque médio no início da semana sobe de 74 para 102 unidades por linha (+38%).

## Passo 8 · Distribuir os caixas pelo perfil horário, ou por igual?

**Pergunta:** uma escala de caixas montada pelo perfil horário reduziria a fila?

Montamos duas escalas com os cupons de janeiro e fevereiro, com o mesmo total de horas de caixa, e as aplicamos a **março** (345 cupons, 30 dias):

- **por perfil:** horas de caixa proporcionais à participação de cada hora em jan–fev;
- **uniforme:** as mesmas horas divididas igualmente pelas 11 horas de funcionamento.

Medimos, em cada dia e hora de março, os cupons que chegaram acima da capacidade da hora (fila):

| Capacidade total | Cupons acima da capacidade: por perfil | Uniforme |
|---|---|---|
| igual à demanda média | 135 | 132 |
| +20% de folga | 110 | 112 |
| +50% de folga | 80 | 82 |

![Escala de caixas](figuras/08_escala_de_caixas.png)

**Conclusão do passo:** montar a escala pelo perfil horário **não reduz a fila** de março: as duas escalas ficam a menos de 3% uma da outra em todas as folgas. É a confirmação, em dados novos, do que o Passo 3 indicou: o perfil horário destes três meses não prevê o mês seguinte.

---

## Recomendação, a partir do que foi encontrado

**1. Achados.**
- Linhas de produto e filiais não diferem em preço, quantidade, avaliação ou total (Passo 1).
- O "pico das 19h" e a vantagem de terça e sábado não se repetem entre meses nem entre filiais (Passo 3); uma escala por perfil não reduziu a fila de março (Passo 8).
- A demanda semanal de cada linha oscila em torno de uma média estável: é o caso em que a política de estoque do jornaleiro se aplica (Passo 7).

**2. Decisão principal.** Repor cada linha de produto, no início da semana, até **média + 1,28 desvio-padrão** das vendas das semanas anteriores, recalculando a cada semana.

**3. Efeito medido** (origem móvel, 42 linhas-semana que a política não viu), em comparação com a prática de repor o que vendeu na semana anterior:
- linhas-semana com falta de produto: **48% → 7%**;
- unidades em falta: **423 → 12 (−97%)**;
- custo: estoque médio no início da semana **+38%** (74 → 102 unidades por linha).

Se o custo de manter estoque pesar mais que o de faltar produto, a política de 75% de serviço é a alternativa medida: falta em 29% das linhas-semana, com 21% a mais de estoque.

**4. Decisão sobre a escala de caixas.** Manter as horas de caixa distribuídas por igual entre as horas de funcionamento. **Efeito medido:** a escala por perfil, que daria mais trabalho de planejar, deixaria a mesma fila em março (diferença menor que 3% em todas as folgas).

**5. Preços.** O experimento de "+10% no preço" (Passo 5) mede uma fórmula, não o comportamento dos clientes; nenhuma decisão de preço é tomada com esta base.

**6. Como acompanhar:**

| Indicador | Referência medida | Ação se sair da faixa |
|---|---|---|
| % das linhas-semana com falta de produto | 7% no teste (meta da política: 10%) | acima de 15% por quatro semanas seguidas: recalcular média e desvio só com as semanas recentes |
| Estoque médio no início da semana | 102 unidades por linha | se subir sem queda das faltas, a demanda mudou de patamar |
| Fila por hora (cupons acima da capacidade) | 132 cupons em março com escala uniforme | se uma hora acumular fila em três meses seguidos, revisar a escala daquela hora |

## Limites

- Três meses e mil cupons; um único produto por cupom. A base é pública e foi publicada para exercícios; as quantidades são as da amostra, não as de um supermercado inteiro.
- A política de estoque supõe que a demanda continue oscilando em torno da mesma média; o indicador de faltas existe para detectar quando isso deixar de valer.
- Os custos de faltar e de sobrar não estão na base; por isso a escolha entre 75% e 90% de serviço é apresentada com os dois efeitos medidos.

## Atividades

1. **Reprodução.** Rode os scripts 01 a 08 e confira os números deste texto.
2. **Variação.** No script `04`, inclua `Total` entre as variáveis do agrupamento. Os perfis mudam? Por que isso era esperado?
3. **Validação.** Repita o Passo 3 para a forma de pagamento: a proporção de pagamentos em dinheiro por hora se repete entre os meses?
4. **Crítica.** Um gerente lê o gráfico do Passo 2 e diz: "está claro, o pico é às 19h". Escreva, em cinco linhas, o que você responderia usando os números do Passo 3.
5. **Planejamento.** Desenhe um teste de preço para uma linha de produto: o que seria comparado, em quais lojas, por quanto tempo, e que medida diria se funcionou?
