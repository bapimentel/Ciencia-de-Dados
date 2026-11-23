# Estudo de caso 2 · Energia doméstica

> Estudo de caso do capítulo 12 do livro *Ciência de Dados: da teoria à prática*. Técnicas usadas: leitura e limpeza de séries de alta frequência, agregação, perfis horários, comparação entre períodos, previsão com linhas de base, análise de variação natural ("placebo").

## A situação

Uma família recebe da companhia de energia o registro do consumo elétrico da casa a cada 15 minutos, com o custo de cada intervalo. Ela quer gastar menos e pergunta:

1. Em que horas, dias e meses o consumo se concentra?
2. O custo depende da hora (tarifa variável) ou só da quantidade consumida?
3. O padrão é estável, ou muda de um ano para o outro?
4. Dá para prever o consumo dos próximos dias?
5. Se a família mudar um hábito, **os dados vão mostrar se funcionou**?

A última pergunta é a mais importante e a mais esquecida. Uma recomendação só é útil se for possível verificar o resultado.

## Os dados

`dados/D202.csv`: 70 368 leituras de 15 minutos de uma residência nos Estados Unidos, de 22/10/2016 a 24/10/2018 (733 dias).

| Coluna | Conteúdo |
|---|---|
| `TYPE` | sempre "Electric usage" |
| `DATE`, `START TIME`, `END TIME` | dia e intervalo de 15 minutos |
| `USAGE` | consumo do intervalo (kWh) |
| `UNITS` | sempre "kWh" |
| `COST` | custo do intervalo, como texto ("$0.01 ") |
| `NOTES` | vazia |

**O que a base não tem:** quais aparelhos estavam ligados, a temperatura externa, quantas pessoas estavam em casa, o tipo de tarifa. Tudo o que concluirmos sobre "hábitos" é inferência a partir do horário.

## Scripts

| Passo | Script | Figuras |
|---|---|---|
| 1. Conhecer os dados | `01_conhecer_os_dados.py` | `01_consumo_diario.png` |
| 2. Preparar e entender o custo | `02_preparar_os_dados.py` (grava `dados/energia_por_hora.csv` e `dados/energia_por_dia.csv`) | `02_tarifa_implicita.png` |
| 3. Procurar padrões | `03_procurar_padroes.py` | `03_perfil_horario.png`, `03_consumo_por_mes.png` |
| 4. Estabilidade e estações | `04_estabilidade_e_estacoes.py` | `04_estabilidade_e_estacoes.png` |
| 5. Prever o consumo | `05_prever_consumo.py` | `05_previsao_60_dias.png` |
| 6. Variação natural do consumo | `06_planejar_o_teste.py` | `06_variacao_natural.png` |
| 7. Medir o efeito da ação | `07_efeito_da_acao.py` | `07_efeito_da_acao.png` |

---

## Passo 1 · Conhecer os dados

**Pergunta:** o que há em cada coluna, e as leituras estão completas?

```python
energia = pd.read_csv('dados/D202.csv')
por_dia = energia.groupby('DATE').size()      # cada dia deveria ter 96 leituras
```

**O que saiu:**

- `TYPE`, `UNITS` e `NOTES` são constantes ou vazias: não trazem informação.
- 733 dias; quatro deles têm 92 ou 100 leituras em vez de 96. São os dias de mudança do horário de verão (uma hora pulada em março, uma hora repetida em novembro).
- O consumo por intervalo tem mediana de 0,05 kWh e máximo de 2,36 kWh; 272 intervalos registram zero.
- `COST` veio como texto com cifrão.
- Por dia: média de 11,7 kWh, mediana de 9,0, de 0 a 39,7. Seis dias têm menos de 2 kWh (casa vazia ou falha de medição).

![Consumo diário](figuras/01_consumo_diario.png)

O gráfico já mostra o fenômeno mais forte da série: o consumo **dobra no inverno**.

## Passo 2 · Preparar e entender o custo

**Pergunta:** o custo é proporcional ao consumo, ou a tarifa muda conforme a hora?

O script junta data e hora num único instante, converte o custo para número e verifica a tarifa implícita (custo ÷ consumo):

```python
energia['Instante'] = pd.to_datetime(energia['DATE'] + ' ' + energia['START TIME'], format='%m/%d/%Y %H:%M')
energia['Custo'] = energia['COST'].str.replace('$', '').str.strip().astype(float)
diario = energia.set_index('Instante').resample('D').sum()
diario['Tarifa'] = diario['Custo'] / diario['Consumo_kWh']
```

**O que saiu:** consumo total de 8 581 kWh e custo de US$ 1 736,95, ou seja, **US$ 0,202 por kWh**. A tarifa implícita diária tem mediana de 0,203 e metade dos dias fica entre 0,191 e 0,213. O custo por intervalo é arredondado ao centavo, por isso olhamos os totais diários.

![Tarifa implícita](figuras/02_tarifa_implicita.png)

**Conclusão do passo:** não há sinal de tarifa por horário. **Economizar dinheiro é economizar kWh**, em qualquer hora. Deslocar consumo de horário não reduziria a conta.

O script grava duas tabelas agregadas, por hora (17 592 linhas) e por dia (733 linhas), usadas nos passos seguintes.

## Passo 3 · Procurar padrões: hora, dia da semana, mês

**Pergunta:** em que momentos o consumo se concentra?

Calculamos o consumo **médio** por hora do dia, por dia da semana e por mês (médias, e não somas, para que períodos com números diferentes de dias fiquem comparáveis).

**Por hora do dia** (média dos dois anos): vale às 5h (0,25 kWh), picos às **7h (0,77)** e às **19h (0,95)**.

| Faixa | Participação no consumo total |
|---|---|
| Madrugada (0–5h) | 17,0% |
| Manhã (6–11h) | 26,7% |
| Tarde (12–17h) | 19,3% |
| **Noite (18–23h)** | **37,0%** |

**Dias úteis × fins de semana:**

| | Consumo médio por dia | Noite (18–23h) | Horas de maior consumo |
|---|---|---|---|
| Dias úteis | 11,1 kWh | 39,4% | 19h, 7h, 20h |
| Fins de semana | 13,2 kWh | 32,1% | 18h, 19h, 13h |

![Perfil horário](figuras/03_perfil_horario.png)

Nos dias úteis, a casa fica quase vazia entre 9h e 17h e o consumo se concentra antes e depois desse período. Nos fins de semana, o consumo se espalha pelo dia. A noite pesa nos dois casos, mais nos dias úteis.

**Por mês:**

![Consumo por mês](figuras/03_consumo_por_mes.png)

Dezembro (20,1 kWh/dia) e janeiro (19,5) consomem mais que o dobro de maio (7,9) e outubro (7,2).

## Passo 4 · O padrão é estável? O que muda no inverno?

**Pergunta:** um padrão observado num ano se repete no outro? E, quando o consumo sobe no inverno, em que horas sobe?

Se o perfil mudasse muito de um ano para o outro, recomendar com base nele seria arriscado. Comparamos os dois anos completos da base (out/2016–out/2017 e out/2017–out/2018):

| | Ano 1 | Ano 2 |
|---|---|---|
| Consumo total | 4 272 kWh | 4 304 kWh |
| Participação da noite | 35,7% | 38,3% |
| Hora de maior consumo | 19h | 19h |

A correlação entre os perfis horários dos dois anos é **0,91**. Mês a mês, a participação da noite varia de 25% a 48% (mediana de 38%), mas fica acima de 30% em quase todos os meses.

Depois, comparamos o inverno (dez–fev) com o verão (jun–ago), hora a hora. O inverno consome 18,4 kWh/dia e o verão 9,1: um excesso de 9,3 kWh por dia. Onde está esse excesso?

| Faixa | Excesso do inverno (kWh/dia) | % do excesso |
|---|---|---|
| Madrugada | 1,73 | 19% |
| Manhã | 2,57 | 28% |
| Tarde | 1,29 | 14% |
| **Noite** | **3,69** | **40%** |

![Estabilidade e estações](figuras/04_estabilidade_e_estacoes.png)

**Conclusão do passo:** o perfil é estável entre os anos, e a noite é a faixa que concentra tanto o consumo do ano inteiro (37%) quanto o aumento do inverno (40% do excesso). O fato de o excesso aparecer em todas as horas, inclusive na madrugada, é compatível com aquecimento elétrico, mas a base não permite confirmar.

## Passo 5 · Dá para prever o consumo dos próximos dias?

**Pergunta:** o histórico prevê o consumo melhor que uma regra simples?

Os últimos 60 dias ficam como teste; o resto é treino. Comparamos:

| Método | Erro médio absoluto (kWh/dia) |
|---|---|
| Repetir a última semana | 2,76 |
| **Média das últimas 4 semanas, por dia da semana** | **2,36** |
| SARIMA com sazonalidade semanal | 3,03 |
| Floresta com defasagens (1 dia à frente, usando o dia anterior real) | 2,14 |

![Previsão](figuras/05_previsao_60_dias.png)

No teste, o consumo médio foi de 8,0 kWh/dia com desvio-padrão de 2,8. Todos os erros são **da ordem da variação diária**: o que move o consumo de um dia para o outro (temperatura, presença, aparelhos) não está na base. O SARIMA perde para a média simples; a floresta só ganha porque prevê um dia de cada vez, com o dia anterior real, uma tarefa mais fácil.

**Conclusão do passo:** os dados servem para descrever padrões, mas não para prever o consumo de um dia específico com precisão.

## Passo 6 · Por que não medir uma mudança pelo "antes e depois"?

**Pergunta:** se a família mudar um hábito, basta comparar o consumo antes e depois?

Usamos um **teste placebo**: em todos os períodos de 8 semanas da base, **sem nenhuma intervenção**, comparamos o consumo noturno (18h–23h) com:

- (a) as 8 semanas imediatamente anteriores;
- (b) as mesmas 8 semanas do ano anterior.

As diferenças que aparecem sem ninguém mudar nada mostram o "ruído" de cada forma de comparar.

```python
media8 = noite_semanal.rolling(8).mean()
dif_anterior = media8 / media8.shift(8) - 1     # 8 semanas x 8 anteriores
dif_ano = media8 / media8.shift(52) - 1         # 8 semanas x mesmo período do ano anterior
```

**O que saiu** (consumo noturno médio: 30,4 kWh por semana):

| Comparação | Comparações sem intervenção | Desvio-padrão das diferenças | 90% das diferenças entre |
|---|---|---|---|
| × 8 semanas anteriores | 89 | 42% | −55% e +84% |
| × mesmo período do ano anterior | 45 | 18% | −19% e +41% |

![Variação natural](figuras/06_variacao_natural.png)

**Conclusão do passo:** comparações de períodos inteiros misturam a mudança de hábito com a estação e o acaso (até 55% de diferença sem ninguém mudar nada). Para medir o efeito de uma ação, precisamos de uma referência **noite a noite**, que não dependa da estação. É o que o Passo 7 constrói.

## Passo 7 · Quanto vale cortar a carga extra da madrugada?

**Pergunta:** entre 0h e 5h, quanto a casa consome além da carga que nunca desliga, e quanto isso custa?

De madrugada quase ninguém usa aparelhos. O que se consome ali é a **carga de base** (geladeira, aparelhos em espera) e, em algumas noites, uma **carga extra**: aquecimento ligado, um aparelho esquecido. O verão serve de modelo para a madrugada sem carga extra, porque não há aquecimento.

```python
madrugada = horario[horario.index.hour <= 5].resample('D').sum()
referencia = madrugada.loc['2018-06-01':'2018-08-31', 'Consumo_kWh'].quantile(0.9)
excesso = (madrugada.loc['2017-10-22':'2018-10-21', 'Consumo_kWh'] - referencia).clip(lower=0)
```

A referência é o **percentil 90** das madrugadas do verão de 2018: **1,92 kWh** por madrugada (0,32 kWh por hora). Usar o percentil 90, e não a mediana (1,12 kWh), é uma escolha conservadora: só conta como extra o consumo acima de 9 em cada 10 madrugadas de verão. O verão de 2017 não serve de referência porque tem madrugadas com carga extra (percentil 90 de 5,11 kWh).

**O que saiu, no ano mais recente (22/10/2017 a 21/10/2018):**

| Medida | Valor |
|---|---|
| Madrugadas acima da referência | 60 de 365 |
| Consumo acima da referência | **229 kWh** |
| Custo (tarifa do ano: US$ 0,210/kWh) | **US$ 48**, ou **5,3%** da conta do ano (US$ 902) |
| Parte do excesso entre novembro e março | 69% |
| Parte do excesso nas 10 piores madrugadas | 49% |
| Madrugadas de inverno (dez–fev) já no nível de verão | **76%** (68 de 90) |
| O mesmo cálculo no ano anterior | 84 madrugadas acima, 424 kWh |

![Efeito da ação](figuras/07_efeito_da_acao.png)

**Como ler:**

- O excesso é **episódico**: metade dele está em 10 madrugadas. Não é a casa inteira consumindo mais; são noites em que algo ficou ligado.
- Ele é **evitável nesta casa**: três de cada quatro madrugadas do inverno de 2017–18 ficaram no nível de verão. A carga extra não é necessária para atravessar o inverno.
- O valor é medido noite a noite, com a mesma régua para cada madrugada. Por isso não depende de comparar estações ou anos (o problema do Passo 6).

---

## Recomendação, a partir do que foi encontrado

**1. Achados.**
- A tarifa é única (US$ 0,20/kWh em todas as horas): deslocar consumo de horário não muda a conta. O efeito medido de timers ou baterias para "fugir do horário de pico" é **zero** (Passo 2).
- Em 60 madrugadas do ano mais recente, a casa consumiu acima do nível de verão; metade desse excesso está em 10 noites, e 76% das madrugadas de inverno já ficam abaixo da referência (Passo 7).

**2. Decisão.** Eliminar a carga extra da madrugada: programar o aquecimento e as tomadas dos aparelhos que podem ficar ligados (aquecedores portáteis, desumidificador, carregadores) para desligar entre 0h e 5h, e receber um **aviso pela manhã** sempre que a madrugada passar de 1,92 kWh.

**3. Efeito medido.** No ano mais recente, o consumo de madrugada acima da referência foi de **229 kWh = US$ 48 = 5,3% da conta**. É esse o valor que a ação elimina se as madrugadas ficarem no nível de verão. No ano anterior, o mesmo cálculo dá 424 kWh, o que mostra que o ganho é maior em invernos com mais noites de carga extra.

**4. Como acompanhar.** Como a referência é definida noite a noite, o efeito é verificado diretamente, sem esperar um ano:

| Indicador | Referência medida | Meta da ação |
|---|---|---|
| Madrugadas acima de 1,92 kWh por mês | de 0 a 13 por mês no ano mais recente (60 no ano; 13 em março) | zero; cada aviso indica um aparelho a desligar |
| kWh de madrugada acima da referência | 229 kWh/ano (até 47 kWh/mês, em dezembro) | zero |
| Consumo total do dia | para conferir se a carga não foi apenas transferida para outro horário | sem aumento nas outras faixas |

## Limites

- Uma única residência, dois anos. Nada aqui se generaliza para outras casas.
- A referência usa um verão; se a casa ganhar um aparelho de carga contínua (por exemplo, um aquário), a referência precisa ser recalculada.
- O efeito em dinheiro supõe a tarifa do ano mais recente (US$ 0,210/kWh).

## Atividades

1. **Reprodução.** Rode os scripts 01 a 07 e confira os números deste texto.
2. **Variação.** No script `06`, troque a janela de 8 para 16 semanas. O limite de detecção diminui? Por quê?
3. **Previsão.** No script `05`, mude o horizonte para 14 e para 120 dias. Qual método resiste melhor?
4. **Pergunta aberta.** No Passo 3, os fins de semana consomem mais durante o dia. Repita o Passo 4 só com fins de semana: o excesso do inverno se distribui da mesma forma?
5. **Crítica.** Um vizinho diz: "troquei as lâmpadas em março e meu consumo caiu 30% em abril". Usando o Passo 6, explique por que essa comparação não prova nada, e use a ideia do Passo 7 para propor uma régua melhor.`n6. **Variação.** No script `07`, troque a referência pelo percentil 75 e pela mediana do verão. Quanto muda o efeito medido? Qual escolha você defenderia, e por quê?
