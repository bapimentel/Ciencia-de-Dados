# Ciência de Dados

**Uma loja vendeu mais neste mês. Ela deveria comprar mais estoque para o próximo?**

Parece uma pergunta simples. Basta olhar as vendas, certo?

Mas e se o aumento aconteceu em um único dia? E se foi uma promoção que não vai se repetir? E se as vendas cresceram, mas alguns produtos ficaram encalhados? Uma tabela pode mostrar que alguma coisa mudou. Entender o que mudou, e decidir o que fazer, exige um pouco mais.

É disso que trata este repositório.

A ideia é começar com o básico de Python e, aos poucos, aprender a investigar dados de verdade: contar, comparar, visualizar, formular hipóteses, testar modelos e reconhecer quando uma conclusão ainda não está suficientemente sustentada. No final, você deverá conseguir defender uma recomendação diante de alguém que pergunte: **"Por que deveríamos fazer isso?"**

## Por onde começar?

Não precisa saber Python. Comece pela primeira etapa e siga no seu ritmo. Cada unidade diz o que reaproveita das anteriores e o que acrescenta.

| Etapa | O que você vai investigar |
|---|---|
| [00 · Como começar](00_como_comecar/) | Instalar o Python e executar seus primeiros comandos |
| [01 · Python do zero](01_python/) | Como transformar perguntas simples em instruções |
| [02 · Primeiros dados](02_primeiros_dados/) | Como ler uma tabela e encontrar padrões |
| [03 · Estatística](03_estatistica/) | Por que duas médias iguais podem contar histórias diferentes |
| [04 · Visualização](04_visualizacao/) | Que gráfico ajuda a responder cada pergunta, e quais enganam |
| [05 · Pré-processamento](05_preprocessamento/) | O que fazer quando os dados têm erros, faltas ou escalas diferentes |
| [06 · Classificação e avaliação](06_classificacao_e_avaliacao/) | Quando um modelo acerta, e quando o erro pode custar caro |
| [07 · Agrupamento](07_agrupamento/) | Como identificar perfis sem categorias prontas, e quando eles não existem |
| [08 · Séries temporais](08_series_temporais/) | Como separar mudanças duradouras de variações de calendário |
| [09 · Redes sociais](09_redes_sociais/) | O que as conexões entre pessoas ou entidades revelam |
| [10 · Estudos de caso](10_estudos_de_caso/) | Como reunir técnicas para investigar problemas reais |
| [11 · Projeto final](11_projeto_final/) | Como responder uma pergunta e recomendar uma ação verificável |

## Sua primeira experiência

Instale o [Python](https://www.python.org/downloads/), baixe este repositório e, na pasta principal, execute:

```
python 01_python/01_operadores_e_variaveis.py
```

Comece mudando os números. Tente prever o resultado antes de executar. Depois modifique uma variável e veja o que acontece. Fazer perguntas ao código é uma boa maneira de aprender a programar. A unidade [00](00_como_comecar/) explica a instalação completa, com ambiente virtual e as bibliotecas de `requirements-basico.txt`; a 01 e a 02 só precisam do Python e do `pandas`.

Se algum termo ainda for desconhecido, volte uma etapa. Não há necessidade de entender tudo de uma vez.

## Quando uma imagem explica melhor

Uma média pode aumentar muito por causa de um único valor. Um gráfico mostra isso em um instante.

![Animação: um valor extremo entra na amostra e cresce; a média se desloca, a mediana quase não se move](animacoes/geradas/media_e_mediana.gif)

*Animação gerada em Python por [animacoes/fontes/media_e_mediana.py](animacoes/fontes/media_e_mediana.py). Dados simulados com semente fixa.*

![Três passos: uma lista em Python vira tabela e depois gráfico de barras](figuras/geradas/lista_para_grafico.png)

*Figura gerada por [figuras/fontes/lista_para_grafico.py](figuras/fontes/lista_para_grafico.py).*

No conteúdo você encontrará gráficos, demonstrações passo a passo e sete animações produzidas pelos próprios exemplos, todas com o código ao lado. O objetivo não é enfeitar a página. É tornar visível o que o cálculo está fazendo. As regras que as figuras seguem, e de onde vêm, estão em [materiais/manual_visual.md](materiais/manual_visual.md).

## Sete problemas para investigar

Três deles vêm do livro que acompanha a disciplina; quatro são extensões deste repositório com bases públicas. Em todos, a pergunta vem antes da técnica.

**Reclamações em aeroportos** ([caso 01](10_estudos_de_caso/01_reclamacoes_tsa/)). Como o valor pago se distribui? Que situações aparecem associadas a cada desfecho? Um modelo poderia ordenar a fila de análise sem substituir a avaliação humana?

**Energia doméstica** ([caso 02](10_estudos_de_caso/02_energia_domestica/)). Em quais horários e meses o uso se concentra? O custo é proporcional ao consumo? Que teste honesto mediria uma mudança de hábito?

**Vendas em supermercado** ([caso 03](10_estudos_de_caso/03_vendas_supermercado/)). Há períodos de maior movimento? Os cupons formam perfis? O que um experimento de "+10% no preço" mede de fato, e por que a base não autoriza mexer em preços?

**Bicicletas compartilhadas** ([caso 04](10_estudos_de_caso/04_mobilidade_bicicletas/)). Quando a demanda é maior? Clima e calendário preveem o uso melhor que repetir a semana anterior? O que falta para falar de estações?

**Desempenho escolar** ([caso 05](10_estudos_de_caso/05_educacao_desempenho/)). Que características se associam à reprovação? Faltas importam tanto quanto se supõe? Uma regra simples alcança quase todos os alunos em risco?

**Varejo on-line** ([caso 06](10_estudos_de_caso/06_varejo_online/)). Quanto valem os cancelamentos e onde se concentram? Que segmentos de clientes existem? "Abandono de carrinho" é uma pergunta que esta base responde?

**Votações na Wikipédia** ([caso 07](10_estudos_de_caso/07_votacoes_wikipedia/)). Quem ocupa posição central, segundo que definição? Há comunidades? O que a estrutura de uma rede permite concluir sobre comportamento, e o que não permite?

Os dados, os scripts e as imagens estão organizados para que você possa refazer as análises, mudar hipóteses e discordar de interpretações. Em dois casos a conclusão honesta é que a base não sustenta a decisão que se queria tomar. Aprender a dizer isso também faz parte.

## A pergunta final

No [projeto final](11_projeto_final/), você escolherá um problema e construirá uma análise capaz de sustentar uma decisão. Ela deverá dizer o que foi observado, que explicação é plausível, que ação seria recomendável e que indicador permitiria avaliar o resultado depois de um período definido. O roteiro segue o documento do projeto da disciplina e reúne o que cada unidade ensinou.

Uma descoberta interessante pode terminar em uma nova pergunta. Uma recomendação responsável precisa dizer também como saberemos se ela deu certo.

## Aulas e livro

Este material acompanha a disciplina de Ciência de Dados do Instituto de Computação da Universidade Federal de Alagoas (UFAL). As [aulas da disciplina](https://sites.google.com/ic.ufal.br/ciencia-de-dados/documentos?authuser=0) aprofundam os conceitos; a correspondência entre cada unidade, as aulas e os capítulos do livro está em [materiais/roteiro_das_aulas.md](materiais/roteiro_das_aulas.md).

Para quem quiser acompanhar a fundamentação teórica e o desenvolvimento mais detalhado das aplicações, escrevi o livro **_Ciência de Dados: da teoria à prática_** (UICLAP, 2025). A Parte I (capítulos 1 a 10) trata de conceitos, Big Data, estatística, pré-processamento, classificação, avaliação de classificadores, aprendizagem não supervisionada, séries temporais, análise de redes sociais e meta-aprendizagem. A Parte II desenvolve três aplicações, que reaparecem neste repositório como estudos de caso:

| Capítulo do livro | Estudo de caso no repositório |
|---|---|
| 11 · Aplicação 1: Reclamações por Perdas | [10_estudos_de_caso/01_reclamacoes_tsa](10_estudos_de_caso/01_reclamacoes_tsa/) |
| 12 · Aplicação 2: Energia Doméstica | [10_estudos_de_caso/02_energia_domestica](10_estudos_de_caso/02_energia_domestica/) |
| 13 · Aplicação 3: Vendas em Supermercado | [10_estudos_de_caso/03_vendas_supermercado](10_estudos_de_caso/03_vendas_supermercado/) |

A aula de [redes sociais](09_redes_sociais/) se baseia no capítulo 9. Os casos 04 a 07 não fazem parte do livro; são extensões com dados reais, e cada um indica os capítulos teóricos que ajudam a entendê-lo ([materiais/mapa_capitulos_aplicacoes.md](materiais/mapa_capitulos_aplicacoes.md)).

Você pode conhecer o livro na [página oficial](https://github.com/bapimentel/livro), na [Amazon](https://www.amazon.com.br/gp/product/6501351715) ou na [UICLAP](https://loja.uiclap.com/titulo/ua86619/). O livro é uma opção de aprofundamento; tudo o que está aqui roda e se estuda sem ele.

## Como está organizado

```
00_como_comecar/ … 11_projeto_final/   trilha, uma pasta por unidade, com README, scripts e figuras
10_estudos_de_caso/0X_.../             dados/, figuras/, scripts numerados e README de cada caso
dados/                                 bases pequenas das unidades iniciais
figuras/  animacoes/                   estilo.mplstyle, fontes/ (geradores) e geradas/ (saídas)
materiais/                             roteiro das aulas, mapa com o livro, manual visual, relatório
original/                              repositório de 2019 e material do livro, sem alterações
scripts/                               executar_todos.py e verificar_links.py
```

Para conferir que tudo roda, da pasta principal e com o ambiente ativado:

```
python scripts/executar_todos.py
```

Os scripts rodam com `matplotlib` em modo não interativo e gravam as figuras; o resultado fica em `scripts/relatorio_execucao.txt`.

Material organizado por **Bruno Pimentel**, professor do Instituto de Computação da UFAL.

*Licença: o repositório original não declarava licença e nenhuma foi presumida aqui. Antes da publicação, defina a licença do código e confira a de cada base de dados ([dados/README.md](dados/README.md) e os READMEs dos casos). As bases da UCI usadas nos casos 04 a 06 estão sob CC BY 4.0.*
