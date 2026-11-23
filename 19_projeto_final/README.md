# 19 · Projeto final

> As datas de entrega de cada turma ficam no [site da disciplina](https://sites.google.com/ic.ufal.br/ciencia-de-dados/documentos?authuser=0). Esta página reúne tudo o que é preciso para fazer o projeto.

**Pergunta inicial:** você analisou os dados, achou um padrão interessante e o gestor pergunta: "e o que eu faço com isso?". O projeto termina quando você consegue responder com uma ação, sustentada por um resultado medido e verificado, e com uma forma de saber se ela funcionou.

## O que o projeto pede

Aplicar técnicas de Ciência de Dados a uma base escolhida pela equipe, **com foco em gerar conhecimento útil para apoiar uma decisão real ou simulada**, e apresentar o resultado como se fosse para um gestor, um cliente ou uma banca. Três aspectos são avaliados:

- **Conteúdo técnico:** as etapas de análise, preparação, modelagem e avaliação.
- **Aplicação prática:** como os resultados apoiam uma decisão concreta.
- **Comunicação:** a defesa da solução, com clareza e evidência.

## A base de dados

A escolha é livre, desde que a base permita encontrar padrões e apoiar uma decisão. Ela deve ter:

- de preferência **mais de 5 000 linhas** e **pelo menos 10 colunas úteis** (sem contar identificadores);
- variáveis numéricas e categóricas, com pelo menos uma que sirva como resultado principal (o que se quer explicar, prever ou melhorar);
- um **problema claro** ligado a uma decisão (por exemplo: reduzir cancelamentos, prever vendas, identificar clientes que vão sair, melhorar o desempenho de alunos, avaliar campanhas);
- potencial para modelagem;
- necessidade real de preparação (ausentes, transformações, novas variáveis, inconsistências, valores extremos);
- potencial para **pelo menos três achados que levem a ação**.

**Não são permitidas** as bases usadas nas listas de exercícios da disciplina nem a base "Hotel Booking". Pode-se combinar mais de uma base. A origem tem de ser clara e citada: repositórios públicos (UCI, Kaggle, SNAP), portais de dados abertos, bases governamentais. Estudantes de mestrado devem preferir uma base ligada ao tema da pesquisa.

## Do resultado à recomendação

A parte que mais distingue um bom projeto é a passagem da análise para a decisão. Os estudos de caso da unidade [18](../18_estudos_de_caso/) seguem sempre a mesma ordem, e o projeto deve segui-la também:

1. **Encontrar o resultado.** Um padrão medido, com números, teste estatístico e tamanho do efeito quando houver comparação de grupos.
2. **Verificar o resultado** em dados que não foram usados para encontrá-lo: outro período, outro grupo, outra divisão dos dados, outra semente do algoritmo, ou contra o acaso.
3. **Decidir** uma ação concreta que decorra diretamente do resultado verificado.
4. **Medir o efeito da decisão**, com um modelo ou uma simulação aplicados a dados que não foram usados para construí-la: quantos dias de espera a menos, quantas faltas de estoque a menos, quanto da receita em risco a ação alcança. Meça também o **custo** (quem espera mais, quanto estoque a mais, quantas vagas a mais).
5. **Definir como acompanhar**, usando como referência os valores medidos no passo anterior.

Duas armadilhas a evitar:

- **Prometer em vez de medir:** "a ação deve reduzir X em 20%" é uma meta, não um resultado. O efeito tem de sair de um cálculo sobre dados reais.
- **Ficar em cima do muro:** recomendar uma ação e, no mesmo parágrafo, dizer que os dados não a sustentam. Se um padrão não se confirmou, ele não sustenta a decisão; procure a decisão que o padrão confirmado sustenta. No estudo de caso do [supermercado](../18_estudos_de_caso/03_vendas_supermercado/), o padrão horário caiu na verificação, e foi a ausência de padrão que indicou a política de estoque, com efeito medido.

Formas de medir o efeito, todas usadas nos estudos de caso:

| Forma de medir | Exemplo |
|---|---|
| Simular o processo com os desfechos reais de um período que o modelo não viu | [TSA](../18_estudos_de_caso/01_reclamacoes_tsa/): espera até o pagamento −25% |
| Avaliar uma política por origem móvel (cada período só vê o passado) | [supermercado](../18_estudos_de_caso/03_vendas_supermercado/): semanas com falta 48% → 7% |
| Aplicar a regra a outro grupo, sem ajuste | [educação](../18_estudos_de_caso/05_educacao_desempenho/): 109 de 130 alunos alcançados, contra 56 de um sorteio |
| Treinar num período e medir no seguinte | [varejo](../18_estudos_de_caso/06_varejo_online/): 55% da receita em risco numa lista de 10% dos clientes |
| Esconder parte das observações e medir o acerto nelas | [Wikipédia](../18_estudos_de_caso/07_votacoes_wikipedia/): 15,4% de acerto contra 5,9% |
| Medir cada unidade contra uma referência construída nos dados | [energia](../18_estudos_de_caso/02_energia_domestica/): 229 kWh acima da referência de verão |

Formato sugerido para cada um dos três achados:

> **Observamos** [padrão], medido por [número, teste, intervalo], e **verificamos** que ele [se repetiu] em [outro período, outro grupo...].
> **Portanto decidimos** [ação concreta].
> **Porque**, medido em [dados não usados na construção, com que modelo ou simulação], a ação produz [efeito, com número e unidade], ao custo de [custo medido].
> **Acompanhamento:** [indicador], com referência [valor medido]; se sair de [faixa], [o que fazer].

Toda afirmação do tipo "o grupo A tem desempenho significativamente menor" precisa de um teste estatístico que a sustente.

## O documento técnico

Formato de artigo da Sociedade Brasileira de Computação (SBC), com **no máximo 12 páginas**. Há modelo pronto no Overleaf ("SBC Conferences Template"). Seções:

1. **Aplicação:** problema, justificativa, objetivos e a decisão que se quer apoiar.
2. **Base de dados:** origem, contexto, número de registros, variáveis; pré-processamento aplicado (limpeza, ausentes, inconsistências, integração, transformação, seleção de atributos), com o número de linhas que cada etapa remove.
3. **Estatística descritiva e inferência:** distribuições, medidas de centro e dispersão, correlações, comparações entre grupos, testes de hipótese quando adequado.
4. **Métodos avaliados:** classificação, regressão, agrupamento, regras de associação, séries temporais, redução de dimensionalidade ou outros, com justificativa da escolha.
5. **Métricas de avaliação:** acurácia, precisão, revocação, F-measure, AUC, erro médio absoluto, erro quadrático médio, R², matriz de confusão ou outras adequadas ao custo dos erros do problema.
6. **Métodos de avaliação:** treino e teste, validação cruzada k-fold, leave-one-out, bootstrap, validação temporal quando os dados têm ordem no tempo, com justificativa.
7. **Resultados e discussão:** os resultados sustentam a recomendação? Verificação, limitações e problemas encontrados; a decisão recomendada e o indicador que permitirá avaliá-la.
8. **Conclusão.**
9. **Referências.**

## Entregas

### Parte 1 · Definição da base e proposta inicial (2,0 pontos)

Um PDF de **até 2 páginas**, entregue pela turma virtual cerca de uma semana depois do lançamento do projeto, com:

- tema e origem da base;
- descrição da base (registros, variáveis, período);
- justificativa da escolha;
- problema e tipo de decisão que se pretende apoiar;
- hipóteses iniciais;
- métodos que se pretende usar.

### Parte 2 · Entrega final (8,0 pontos)

Um arquivo compactado com o documento em PDF, o código, a apresentação e arquivos adicionais.

- **Apresentação (5,0 pontos)**, até 20 minutos:
  - **5 minutos de *pitch*:** problema → oportunidade → evidências → decisão → efeito medido;
  - **15 minutos técnicos:** base → preparação → métodos → métricas → resultados → verificação → medição do efeito da decisão → limitações.
- **Documento técnico (3,0 pontos).**

Critérios da apresentação: clareza do problema; domínio da base; metodologia; qualidade das análises e das visualizações; interpretação dos resultados; relação entre achados, métricas e decisão; clareza na justificativa da decisão (que ação e que indicador mostrará seu efeito); organização e comunicação.

### Pontuação extra (1,0 a 2,0 pontos)

Avaliada pela qualidade, relevância e utilidade: painel interativo, aplicação web simples, modelo publicado (*deploy*), relatório automatizado, técnicas avançadas, integração com APIs, visualizações interativas, comparação aprofundada de abordagens, uso de modelos de linguagem (LLMs) integrado à análise.

## Roteiro de trabalho

| Etapa | O que fazer | Onde a trilha ensinou |
|---|---|---|
| Escolher a pergunta | Comece pela decisão que alguém precisa tomar, não pelo algoritmo. Escreva a pergunta em uma frase que os dados possam responder. | [01](../01_conceitos_e_big_data/), seção "A situação" de cada estudo de caso |
| Conhecer a base | Linhas, colunas, tipos, período, unidade de observação, o que a base **não** mede. Registre origem, data de acesso e licença. | [03](../03_primeiros_dados/), Passo 1 dos estudos de caso |
| Preparar | Duplicatas, ausentes (e por que faltam), categorias, escala, datas, variáveis derivadas. Documente cada filtro e quantas linhas ele remove. | [06](../06_preprocessamento/), Passo 2 dos estudos de caso |
| Descrever e inferir | Distribuições, comparações com teste **e** tamanho do efeito, intervalos de confiança, correlação sem causalidade. | [04](../04_estatistica/), estudo de caso [05](../18_estudos_de_caso/05_educacao_desempenho/) |
| Visualizar | Um gráfico por pergunta, título que afirma o achado, escala fiel. | [05](../05_visualizacao/), [manual visual](../materiais/manual_visual.md) |
| Modelar, se ajudar | Linha de base primeiro; separação honesta (estratificada ou no tempo); métrica adequada ao custo do erro; validação cruzada. | [07](../07_aprendizagem_de_maquina/) a [16](../16_recomendacao_de_modelos/) |
| Verificar | O achado se repete em outro período, outro grupo, outra semente? É diferente do acaso? | Passo de verificação de cada estudo de caso |
| Medir o efeito | Simulação, origem móvel, outro grupo ou observações escondidas: quanto a decisão muda, e a que custo. | Último passo de cada estudo de caso |
| Recomendar | Achado verificado → decisão → efeito medido → acompanhamento. | Seção "Recomendação" de cada estudo de caso |
| Comunicar | *Pitch* com uma ideia central; apresentação técnica que mostra como se chegou lá. | [05](../05_visualizacao/) (contar uma história com dados) |

## Lista de verificação antes de entregar

- [ ] A pergunta cabe em uma frase e diz quem decide.
- [ ] A base tem origem, data de acesso e licença registradas; cada filtro está documentado com números.
- [ ] Toda comparação entre grupos tem teste, tamanho do efeito e tamanho das amostras.
- [ ] Todo modelo foi comparado com uma linha de base e avaliado em dados que não viu (nada do teste, do futuro ou do alvo vaza para o treino).
- [ ] A métrica escolhida reflete o custo dos erros do problema.
- [ ] Cada achado usado numa recomendação foi verificado em dados que não serviram para encontrá-lo.
- [ ] Cada decisão decorre de um achado verificado e tem efeito medido (com número e unidade) em dados não usados para construí-la, junto com o custo medido.
- [ ] Os indicadores de acompanhamento têm uma referência medida nos dados (faixa de variação, valor no período de teste).
- [ ] Cada gráfico responde a uma pergunta, tem título informativo, unidades e escala fiel.
- [ ] As limitações estão escritas, inclusive o que a base não mede e o que seria preciso coletar.
- [ ] O código roda do início ao fim num ambiente limpo (o script `scripts/executar_todos.py` é um modelo de como conferir).

## Exemplos

Os sete [estudos de caso](../18_estudos_de_caso/) foram escritos no formato que o projeto pede: cada um termina com decisões e efeitos medidos. Em três deles ([supermercado](../18_estudos_de_caso/03_vendas_supermercado/), [varejo on-line](../18_estudos_de_caso/06_varejo_online/) e [Wikipédia](../18_estudos_de_caso/07_votacoes_wikipedia/)), a verificação derrubou a ação que a análise inicial parecia sugerir, e a decisão final veio do que a verificação mostrou.
