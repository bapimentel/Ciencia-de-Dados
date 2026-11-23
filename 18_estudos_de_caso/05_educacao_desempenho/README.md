# Estudo de caso 5 · Educação: desempenho e acompanhamento preventivo

> **Aplicação adicional — não integra o livro.** Relaciona-se com as unidades de estatística (04), pré-processamento (06), avaliação de modelos (07) e regressão logística (11). Técnicas usadas: comparação de grupos com tamanho de efeito, proporções com intervalo de confiança, classificação com validação cruzada, comparação entre modelo e regra simples, validação externa.

## A situação

A coordenação de uma escola quer oferecer reforço e acompanhamento **antes** que os alunos reprovem. Os recursos são limitados: não dá para acompanhar todo mundo. As perguntas:

1. Que características observáveis durante o ano aparecem associadas à reprovação?
2. As faltas importam tanto quanto se costuma supor?
3. Dá para montar uma lista curta que inclua a maioria dos alunos que vão reprovar?
4. Essa lista funciona em **outros alunos**, que não foram usados para construí-la?

Uma lista de acompanhamento envolve pessoas. Ela deve ser um convite ao apoio, nunca um rótulo, e sempre passar por revisão humana.

## Os dados

*Student Performance*, UCI Machine Learning Repository (id 320), licença CC BY 4.0, acesso em 23/11/2026: <https://archive.ics.uci.edu/dataset/320/student-performance>. Alunos do ensino secundário de duas escolas portuguesas (GP e MS) no ano letivo 2005–2006 (Cortez e Silva, 2008). Dicionário em [dados/student.txt](dados/student.txt).

| Arquivo | Alunos | Uso neste estudo |
|---|---|---|
| `dados/student-por.csv` | 649 | turma de português: análise e construção da regra |
| `dados/student-mat.csv` | 395 | turma de matemática: validação externa (Passo 5) |

Principais colunas: `school`, `sex`, `age`, `address` (urbano/rural), `Medu`/`Fedu` (escolaridade dos pais), `studytime` (horas de estudo por semana, em faixas), `failures` (reprovações anteriores), `schoolsup` (apoio escolar), `higher` (quer fazer ensino superior), `absences` (faltas), `G1`, `G2`, `G3` (notas dos três períodos, de 0 a 20; aprova-se com 10).

**O que a base não tem:** motivo das faltas, renda, histórico de anos anteriores, o que a escola fez com cada aluno. É um retrato de um ano, em duas escolas portuguesas, há vinte anos. Não descreve escolas brasileiras.

## Scripts

| Passo | Script | Figuras |
|---|---|---|
| 1. Conhecer os dados | `01_conhecer_os_dados.py` | `01_notas_e_faltas.png` |
| 2. Comparar grupos | `02_comparar_grupos.py` | `02_grupos.png` |
| 3. Prever o risco | `03_prever_risco.py` (grava `dados/probabilidades_validacao.csv`) | `03_risco.png` |
| 4. Lista de acompanhamento | `04_lista_de_acompanhamento.py` | `04_lista_de_acompanhamento.png` |
| 5. Validar em outra turma | `05_validar_em_outra_turma.py` | `05_validacao_externa.png` |

---

## Passo 1 · Conhecer os dados

**Pergunta:** como se distribuem as notas e as faltas? O que significa uma nota zero?

```python
alunos = pd.read_csv('dados/student-por.csv', sep=';')    # separador é ponto e vírgula
(alunos['G3'] < 10).mean()                                 # fração de reprovados
alunos[['G1', 'G2', 'G3']].corr()
```

**O que saiu:**

- Nenhum valor ausente. Nota final (G3): mediana 12, de 0 a 19.
- **100 de 649 alunos (15,4%) reprovam** (G3 < 10). Quinze têm G3 = 0, o que costuma indicar abandono ou ausência na prova, não uma nota zero.
- Faltas: mediana de 2, média de 3,7, máximo de 32.
- 549 alunos nunca reprovaram; 70 reprovaram uma vez, 16 duas vezes e 14 três vezes.
- As notas dos três períodos são muito correlacionadas: G1 × G3 = 0,83 e **G2 × G3 = 0,92**.

![Notas e faltas](figuras/01_notas_e_faltas.png)

Essa última correlação define uma regra para o resto do estudo: **G2 não pode ser usada para prever G3**. Seria prever a nota final com uma nota quase igual a ela, e só estaria disponível tarde demais para ajudar.

## Passo 2 · Que grupos têm notas diferentes?

**Pergunta:** quais características aparecem associadas à nota final, e com que força?

Para cada comparação calculamos o teste de Mann-Whitney e o **delta de Cliff**, uma medida de tamanho do efeito que não depende de normalidade: a probabilidade de um aluno do primeiro grupo ter nota maior que um do segundo, menos a probabilidade contrária (vai de −1 a 1; acima de 0,47 costuma ser considerado grande).

| Comparação | Medianas | Delta de Cliff | p |
|---|---|---|---|
| Sem × com reprovação anterior | 12 × 10 | **+0,71** | < 0,0001 |
| Quer × não quer ensino superior | 12 × 10 | **+0,66** | < 0,0001 |
| Estuda 5h+ × menos de 5h por semana | 13 × 11 | +0,29 | < 0,0001 |
| Urbano × rural | 12 × 11 | +0,21 | < 0,0001 |
| Até 5 × mais de 5 faltas | 12 × 11 | +0,16 | 0,001 |
| Com × sem apoio escolar | 11 × 12 | −0,16 | 0,03 |

**Faltas em detalhe** (correlação de Spearman com G3: −0,16):

| Faltas no ano | Alunos | % reprovados | IC 95% |
|---|---|---|---|
| 0 | 244 | 13,9% | 10,1% – 18,8% |
| 1–2 | 122 | 13,1% | 8,2% – 20,2% |
| 3–5 | 112 | 14,3% | 9,0% – 22,0% |
| 6–10 | 122 | 18,0% | 12,2% – 25,8% |
| mais de 10 | 49 | 24,5% | 14,6% – 38,1% |

![Grupos](figuras/02_grupos.png)

**Como ler:**

- **Reprovação anterior é a associação mais forte.** Querer seguir estudando vem logo depois.
- **Faltas pesam menos do que se costuma supor**: a taxa de reprovação só sobe de forma visível acima de 10 faltas, e mesmo ali o intervalo é largo (49 alunos).
- **Apoio escolar aparece com nota menor.** Não é que o apoio prejudique: ele é dado a quem já tem dificuldade. É o exemplo clássico de associação que não mede efeito.

## Passo 3 · Dá para prever quem corre risco?

**Pergunta:** com o que se sabe no início do ano, e depois com a nota do 1º período, um modelo aponta quem vai reprovar?

Dois momentos de decisão:

- **Início do ano:** 29 variáveis sociais, familiares e escolares, sem notas.
- **Após o 1º período:** as mesmas, mais faltas e G1.

Avaliamos com validação cruzada estratificada de 5 dobras (cada aluno é previsto por um modelo que não o viu):

| Modelo | AUC | Revocação (limiar 0,5) | Precisão (limiar 0,5) |
|---|---|---|---|
| Linha de base ("ninguém reprova") | 0,500 | 0,00 | — |
| Logística, início do ano | 0,789 | 0,64 | 0,35 |
| Floresta, início do ano | 0,840 | 0,74 | 0,44 |
| Logística, após 1º período | 0,918 | 0,75 | 0,49 |
| Floresta, após 1º período | 0,928 | 0,87 | 0,55 |

![Risco](figuras/03_risco.png)

No início do ano, o maior coeficiente da logística é o das reprovações anteriores (0,79), seguido da escola MS (0,45). Depois do 1º período, **a nota G1 muda tudo**: a AUC sobe de 0,79 para 0,92.

## Passo 4 · Uma lista de acompanhamento: modelo ou regra simples?

**Pergunta:** se a escola acompanhar uma fração dos alunos, quantos dos que reprovariam estarão na lista?

Ordenamos os alunos pela probabilidade prevista (fora da amostra, do Passo 3) e contamos:

| Alunos na lista | Reprovados alcançados: início do ano | Após 1º período |
|---|---|---|
| 10% (65) | 35% | 45% |
| 20% (130) | 54% | 69% |
| 30% (195) | 66% | 90% |
| 40% (260) | 79% | 97% |

E comparamos com uma **regra transparente**, que qualquer professor entende: **acompanhar quem já reprovou ou tirou menos de 10 no 1º período**.

```python
regra = (alunos['failures'] > 0) | (alunos['G1'] < 10)
```

A regra coloca **187 alunos (29%)** na lista e alcança **94 dos 100 reprovados (94%)**. O modelo, com 30% dos alunos, alcança 90%.

![Lista de acompanhamento](figuras/04_lista_de_acompanhamento.png)

**Conclusão do passo:** a regra simples alcança tanto quanto o modelo, e pode ser explicada a alunos e famílias. Mas ela foi escolhida olhando estes mesmos alunos. Será que funciona em outros?

## Passo 5 · A regra funciona em alunos que não foram usados para criá-la?

**Pergunta:** aplicada **sem nenhum ajuste** a outra turma e a cada escola separadamente, a regra mantém a cobertura?

A turma de matemática tem 395 alunos, outra disciplina e uma taxa de reprovação muito maior (33%, contra 15% em português). É um bom teste: se a regra só funcionasse por acaso nos dados de português, falharia aqui.

| Grupo | Alunos | Reprovação | Na lista | Cobertura dos reprovados | Precisão da lista |
|---|---|---|---|---|---|
| Português (onde a regra foi criada) | 649 | 15% | 29% | 94% | 50% |
| **Matemática (validação externa)** | **395** | **33%** | **43%** | **84%** | **64%** |
| Português, escola GP | 423 | 8% | 19% | 91% | 36% |
| Português, escola MS | 226 | 30% | 47% | 96% | 61% |
| Matemática, escola GP | 349 | 32% | 43% | 82% | 62% |
| Matemática, escola MS | 46 | 37% | 46% | 94% | 76% |

O modelo logístico treinado em português e aplicado a matemática tem AUC de **0,904**. Com o mesmo número de alunos da regra (171), ele alcança **109** dos 130 reprovados, **exatamente o mesmo que a regra**.

Quem a regra deixa de fora em matemática? Os 21 reprovados fora da lista tiraram **10 ou 11 no 1º período**, logo acima do corte; 5 deles terminaram com G3 = 0 (provável abandono).

![Validação externa](figuras/05_validacao_externa.png)

**Conclusão do passo:** a regra mantém cobertura entre 82% e 96% em todas as combinações de turma e escola, inclusive na que não foi usada para criá-la. O tamanho da lista acompanha a taxa de reprovação de cada grupo (19% numa escola com 8% de reprovação, 47% noutra com 30%).

---

## Recomendação, a partir do que foi encontrado

**1. Achados.**
- Reprovação anterior é a característica mais associada à nota final (delta de Cliff 0,71); faltas só pesam acima de 10 (Passo 2).
- Após o 1º período, a regra "reprovou antes **ou** G1 < 10" alcança 94% dos reprovados com 29% dos alunos em português (Passo 4).
- Aplicada sem ajuste à turma de matemática, alcança 84%, o mesmo que um modelo estatístico, e entre 82% e 96% em cada escola (Passo 5).

**2. Ação.** Após o 1º período, convidar para acompanhamento os alunos que já reprovaram ou tiveram G1 abaixo de 10, usando a **regra**, e não o modelo: ela alcança o mesmo, é verificável por qualquer pessoa e pode ser explicada ao aluno. Prever de **20% a 45%** dos alunos na lista, conforme a taxa de reprovação histórica da turma (foi essa a faixa observada nos seis grupos).

**3. Cuidados.**
- A lista é um convite ao apoio, revisado por pessoas; não pode ser divulgada nem usada para selecionar, punir ou separar alunos.
- Quem tem G1 = 10 ou 11 fica de fora e responde pela maioria dos reprovados não alcançados em matemática. Professores devem poder incluir esses alunos por julgamento próprio.
- Nada aqui mostra que acompanhar **causa** aprovação. O Passo 2 mostrou o contrário de propósito: quem recebe apoio tem nota menor, porque o apoio vai a quem precisa.

**4. Como acompanhar, com referências medidas aqui:**

| Indicador | Referência medida | Sinal de alerta |
|---|---|---|
| Cobertura: % dos reprovados do ano que estavam na lista | 82% a 96% nos seis grupos | abaixo de 80%: a regra precisa ser revista para aquela turma |
| Tamanho da lista | 19% a 47% dos alunos | acima de 50%: a lista perde o foco e a capacidade de atendimento se esgota |
| Taxa de reprovação entre os alunos da lista | 50% a 76% (precisão da lista, sem nenhum acompanhamento) | é a referência para medir o efeito do acompanhamento: se, com acompanhamento, a reprovação na lista cair abaixo dessa faixa, há indício de efeito; para atribuir a queda ao acompanhamento, seria preciso comparar com alunos de mesmo perfil não acompanhados |

## Limites e ética

- Duas escolas portuguesas, 2005–2006. A regra precisa ser verificada com dados da escola que for usá-la, como fizemos no Passo 5.
- A turma de matemática não é totalmente independente da de português: parte dos alunos está nas duas. A validação é externa quanto à disciplina e às notas, não quanto às pessoas.
- Variáveis como escola, endereço ou escolaridade dos pais aparecem associadas à nota, mas usar características da família para selecionar alunos seria injusto; a regra recomendada usa apenas o histórico escolar do próprio aluno.

## Atividades

1. **Reprodução.** Rode os scripts 01 a 05 e confira os números deste texto.
2. **Ajuste com cuidado.** No script `05`, troque o corte para G1 < 11. A cobertura em matemática sobe? Por que essa mudança precisaria ser validada num terceiro conjunto de dados antes de ser adotada?
3. **Início do ano.** Construa uma regra que use só o que se sabe no início do ano (sem G1). Qual a melhor cobertura que você consegue com 30% dos alunos? Valide em matemática.
4. **Crítica.** Um diretor propõe usar o modelo do Passo 3 com todas as variáveis, inclusive endereço e profissão dos pais, porque a AUC é maior. Escreva um parágrafo com dois argumentos contra, um técnico (use o Passo 5) e um ético.
