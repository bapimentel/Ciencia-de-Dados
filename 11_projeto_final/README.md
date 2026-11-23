# 11 · Projeto final

**Pergunta inicial:** você analisou os dados, achou um padrão interessante e o gerente pergunta: "e o que eu faço com isso?". O projeto final termina quando você consegue responder essa pergunta com uma ação, um indicador e um prazo.

Esta página organiza o que a trilha ensinou em um roteiro para o projeto da disciplina. A fonte prioritária é o documento **Projeto (2026-1).pdf**, disponível na seção *Projeto* do [site da disciplina](https://sites.google.com/ic.ufal.br/ciencia-de-dados/documentos?authuser=0), lido integralmente em novembro de 2026 para escrever este roteiro. As regras de nota e de entrega são as do documento; aqui elas só são resumidas. Em caso de dúvida, vale o PDF e a orientação do professor.

## O que o projeto pede

Aplicar técnicas de Ciência de Dados a uma base escolhida pela equipe, **com foco na geração de conhecimento útil para apoiar uma tomada de decisão real ou simulada**, e apresentar o resultado em formato de *pitch*. Três aspectos são avaliados: conteúdo técnico (etapas de análise, tratamento, modelagem, avaliação), aplicação prática (como os resultados apoiam uma decisão em contexto real) e comunicação (defender a solução como se fosse para um gestor, empresa, cliente ou banca).

### A base de dados

Escolha livre, desde que relacionada a um problema que permita análise, padrões e *insights*. O documento pede:

- preferencialmente mais de 5 000 linhas e pelo menos 10 colunas úteis (sem contar identificadores);
- variáveis numéricas e categóricas, com pelo menos uma que sirva como resultado principal;
- um problema de negócio claro (aumentar reservas, reduzir cancelamentos, prever vendas, identificar churn, melhorar desempenho de alunos, campanhas ou produtos);
- potencial para modelagem;
- necessidade de preparação (ausentes, transformações, novas colunas, inconsistências, *outliers*);
- potencial para pelo menos **três insights acionáveis**.

Não é permitido usar as bases das listas 1 e 2 nem a base "Hotel Booking". Pode-se combinar mais de uma base. Fontes aceitas: repositórios públicos, bases governamentais, Kaggle, UCI, dados abertos, desde que a origem seja clara e referenciada. Mestrandos: preferir base ligada ao tema de pesquisa.

### O insight acionável

O documento define o formato que esta trilha inteira treinou:

> Percebemos que [padrão nos dados]. Isso sugere que [interpretação do problema ou oportunidade]. Por isso, recomendamos [ação prática]. A decisão foi sustentada por [métrica/evidência usada na análise]. Após [período], o sucesso da ação pode ser avaliado por [métrica principal] e acompanhado por [métrica auxiliar]. A ação será considerada bem-sucedida se [critério objetivo de sucesso].

E acrescenta um aviso que vale repetir: afirmações como "desempenho significativamente menor" **devem ser sustentadas por teste estatístico**. Os três exemplos do documento (hotel, e-commerce e educação) seguem esse formato; os estudos de caso deste repositório fazem o mesmo, com uma diferença deliberada: quando a evidência não sustenta uma ação, eles dizem isso, em vez de inventar uma.

### Estrutura do documento técnico

1. **Aplicação**: problema, justificativa, objetivos, relação com a decisão.
2. **Base de dados**: origem, contexto, número de registros, variáveis; pré-processamento aplicado (limpeza, ausentes, inconsistências, integração, transformação, redução ou seleção de atributos).
3. **Estatística descritiva e inferência**: distribuições, tendência central, dispersão, correlações, comparações entre grupos; testes de hipótese quando adequado.
4. **Métodos avaliados**: classificação, regressão, agrupamento, regras de associação, séries temporais, redução de dimensionalidade ou outros, com justificativa.
5. **Métricas de avaliação**: acurácia, precisão, revocação, F-measure, AUC, erro médio absoluto, erro quadrático médio, R², matriz de confusão, outras adequadas ao problema.
6. **Métodos de avaliação**: treino/teste, k-fold, leave-one-out, bootstrap, validação temporal quando aplicável, com justificativa.
7. **Resultados e discussão**: os resultados justificam a proposta? Limitações, problemas encontrados, interpretações; a decisão recomendada e a métrica que evidencia seu impacto.
8. **Conclusão.** 9. **Bibliografia.**

Formato: modelo de artigo da SBC (há modelo no Overleaf), no máximo 12 páginas.

### Entregas, apresentação e avaliação (resumo do PDF)

- **Parte 1 — Definição da base e proposta inicial** (2,0 pontos): PDF de até 2 páginas com tema e origem da base, descrição, justificativa, problema, tipo de decisão a apoiar, hipóteses iniciais e possíveis métodos. Entrega pela turma virtual, uma semana após a proposta do projeto.
- **Parte 2 — Entrega final** (8,0 pontos): arquivo compactado com documento em PDF, código, apresentação e arquivos adicionais. Apresentação de até 20 minutos: 5 de *pitch* (problema → oportunidade → evidências → decisão → impacto esperado) e 15 técnicos (base → preparação → métodos → métricas → resultados → limitações → justificativa da decisão). Vale 5,0 pontos; o documento final, 3,0.
- Critérios da apresentação: clareza do problema, domínio da base, metodologia, qualidade das análises e visualizações, interpretação, relação entre *insights*, métricas e decisão, clareza na justificativa da decisão (qual ação e qual métrica evidencia o impacto), organização e comunicação.
- Pontuação extra (1,0 a 2,0): dashboard interativo, aplicação web simples, *deploy* de modelo, relatório automatizado, técnicas avançadas, integração com APIs, visualizações interativas, comparação aprofundada de abordagens, integração com LLMs, avaliados por qualidade, relevância e utilidade.

## Roteiro de trabalho com o que a trilha ensinou

| Etapa do projeto | O que fazer | Onde a trilha ensinou |
|---|---|---|
| Escolher a pergunta | Comece pela decisão que alguém precisa tomar, não pelo algoritmo. Escreva a pergunta em uma frase que os dados possam responder. | [01](../01_python/), [02](../02_primeiros_dados/), todos os estudos de caso (seção 1 de cada README) |
| Conhecer a base | Linhas, colunas, tipos, período, unidade de observação, o que a base **não** mede. Registre a origem, a data de acesso e a licença. | [02](../02_primeiros_dados/), scripts `01_conhecer_os_dados.py` dos casos |
| Preparar | Duplicatas, ausentes (e por que faltam), categorias, escala, datas, variáveis derivadas. Documente cada filtro e quantas linhas ele remove. | [05](../05_preprocessamento/), scripts `02_preparar_os_dados.py` |
| Descrever e inferir | Distribuições, comparações entre grupos com teste **e** tamanho do efeito, correlações sem causalidade. | [03](../03_estatistica/), caso [05](../10_estudos_de_caso/05_educacao_desempenho/) |
| Visualizar | Um gráfico por pergunta, título que afirma o achado, escala fiel, manual visual. | [04](../04_visualizacao/), [materiais/manual_visual.md](../materiais/manual_visual.md) |
| Modelar, se ajudar | Linha de base primeiro; separação honesta (estratificada ou cronológica); métrica adequada ao custo do erro; validação cruzada ou janelas. | [06](../06_classificacao_e_avaliacao/), [07](../07_agrupamento/), [08](../08_series_temporais/), [09](../09_redes_sociais/) |
| Recomendar | Achado → explicação plausível e limites → ação → indicador principal e auxiliar → prazo → critério de sucesso. Metas são metas, não resultados. | Scripts `0X_avaliar_uma_decisao.py` de cada caso |
| Comunicar | *Pitch* de 5 minutos com uma Grande Ideia; apresentação técnica que mostra como se chegou lá. | [04](../04_visualizacao/) (história com dados) |

## Lista de verificação antes de entregar

- [ ] A pergunta cabe em uma frase e diz quem decide.
- [ ] A base tem origem, data de acesso e licença registradas; os filtros aplicados estão documentados com números.
- [ ] Toda comparação entre grupos tem teste, tamanho do efeito e tamanho das amostras.
- [ ] Todo modelo foi comparado com uma linha de base e avaliado em dados que não viu, na ordem certa (nada do teste, do futuro ou do alvo vaza para o treino).
- [ ] A métrica escolhida reflete o custo dos erros do problema, não a convenção.
- [ ] Cada gráfico responde a uma pergunta, tem título informativo, unidades e escala fiel.
- [ ] Os três *insights* seguem o formato (achado, interpretação, ação, evidência, prazo, métrica principal, auxiliar, critério).
- [ ] As limitações estão escritas, inclusive o que a base não mede e o que seria preciso coletar.
- [ ] Nenhuma correlação foi apresentada como causa; nenhuma meta foi apresentada como resultado.
- [ ] O código roda do início ao fim em um ambiente limpo (`python scripts/executar_todos.py` é um modelo de como conferir).

## Exemplos no repositório

Os sete estudos de caso em [10_estudos_de_caso](../10_estudos_de_caso/) foram escritos no formato que o projeto pede. Três deles reproduzem as aplicações do livro (capítulos 11, 12 e 13) e quatro usam bases públicas novas. Em dois deles ([supermercado](../10_estudos_de_caso/03_vendas_supermercado/) e [Wikipédia](../10_estudos_de_caso/07_votacoes_wikipedia/)) a conclusão honesta é que a base não sustenta a decisão que se queria tomar. Saber dizer isso também é resultado.

A aula do projeto (`Aula_cd_projeto.pdf`, na mesma seção do site) não foi incorporada a este roteiro.
