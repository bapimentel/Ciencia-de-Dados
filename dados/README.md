# Dados compartilhados pelas unidades

Bases usadas pelas unidades 01 a 17. As bases dos estudos de caso ficam em `18_estudos_de_caso/*/dados/`, cada uma descrita no README do seu caso. Várias unidades também usam bases que acompanham o scikit-learn (íris, vinhos, câncer de mama, dígitos) e que não precisam de arquivo.

| Arquivo | O que é | Origem | Licença / uso | Usado nas unidades |
|---|---|---|---|---|
| `supermercado.csv` | 1 000 cupons de três filiais de um supermercado em Mianmar, jan–mar/2019 | base pública "Supermarket sales" (Kaggle); a mesma do estudo de caso 03, com nome de arquivo simplificado | confira os termos da página de origem antes de redistribuir | 01, 03, 04, 05, 06, 08 |
| `Data.csv` | 10 clientes: região, idade, renda, comprador on-line; duas lacunas | exemplo didático clássico de pré-processamento | dados fictícios | 03, 06, 08 |
| `alunos_portugues.csv` | 649 alunos de duas escolas portuguesas, 2005–2006 (turma de português) | *Student Performance*, UCI id 320 (<https://archive.ics.uci.edu/dataset/320/student-performance>); separador `;` | CC BY 4.0; acesso em 23/11/2026 | 04, 11 |
| `bicicletas_dia.csv` | 731 dias de aluguel de bicicletas em Washington D.C., 2011–2012 | *Bike Sharing Dataset*, UCI id 275 (<https://archive.ics.uci.edu/dataset/275/bike-sharing-dataset>), arquivo `day.csv` | CC BY 4.0; acesso em 23/11/2026 | 04, 05, 06, 11 |
| `sms_spam.tsv` | 5 574 mensagens SMS rotuladas como spam ou não | *SMS Spam Collection*, UCI id 228 (<https://archive.ics.uci.edu/dataset/228/sms+spam+collection>) | CC BY 4.0; acesso em 23/11/2026 | 10 |
| `Drugs.csv` | 204 meses de vendas de antidiabéticos na Austrália, jul/1991 a jun/2008 | série "a10" de Hyndman e Athanasopoulos, *Forecasting: Principles and Practice* | uso educacional | 05, 15 |
| `SPCS20RPSNSA.csv` | 237 meses de pares de vendas de imóveis no índice S&P/Case-Shiller de 20 cidades, jan/2000 a set/2019 | FRED, <https://fred.stlouisfed.org/series/SPCS20RPSNSA> | termos do FRED/S&P Dow Jones Indices; uso educacional | 15 |

Nenhuma base contém dados pessoais identificáveis: os alunos e clientes aparecem apenas como linhas, sem nome.

## Bases baixadas durante a execução

A parte de Big Data da unidade 01 (scripts 10 e 11) usa duas fontes reais grandes demais para guardar no repositório. Os scripts as buscam na hora e guardam o que precisam em `~/ciencia-de-dados-big-data`, fora do repositório; veja [01_conceitos_e_big_data/README.md](../01_conceitos_e_big_data/README.md#onde-ficam-os-dados).

| Fonte | O que é | Origem | Licença / uso | Script |
|---|---|---|---|---|
| Corridas de táxi amarelo de Nova York, 2024 | 12 arquivos Parquet mensais, 41.169.720 corridas, 693 MB; mais a tabela das 265 zonas (CSV) | Taxi & Limousine Commission (TLC), <https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page> | dados abertos da prefeitura de Nova York; confira os termos de uso da página; acesso em 23/11/2026 | 10 |
| Alterações recentes da Wikimedia | fluxo ao vivo de todas as edições em todos os projetos da Wikimedia, dezenas de eventos por segundo | Wikimedia EventStreams, <https://stream.wikimedia.org/v2/stream/recentchange> | fluxo público; o script guarda só campos técnicos (wiki, tipo, robô ou pessoa, bytes alterados), nada de nomes de usuários, títulos ou comentários, e apaga tudo ao terminar | 11 |

**Antes de publicar o repositório**, confirme a licença de redistribuição de `supermercado.csv` e das bases dos estudos de caso 01 (TSA, dados governamentais dos EUA, em geral de domínio público) e 02 (energia doméstica).
