# Dados compartilhados pelas unidades

Bases pequenas usadas pelas unidades 01 a 09. As bases dos estudos de caso ficam em `10_estudos_de_caso/*/dados/`.

| Arquivo | O que é | Origem | Licença / uso | Usado em |
|---|---|---|---|---|
| `Data.csv` | 10 clientes: região, idade, renda, comprador on-line; duas lacunas | repositório de 2019 (`Dados/Data.csv`); exemplo didático comum em cursos de pré-processamento | sem licença declarada; dados fictícios | 02, 05, 07 |
| `Drugs.csv` | 204 meses de vendas de antidiabéticos na Austrália, jul/1991 a jun/2008 (série "a10") | repositório de 2019 (`Dados/Drugs.csv`); série publicada em Hyndman e Athanasopoulos, *Forecasting: Principles and Practice* | uso educacional habitual; sem licença declarada no repositório | 04, 08 |
| `SPCS20RPSNSA.csv` | 237 meses de pares de vendas de imóveis, índice S&P/Case-Shiller 20 cidades, jan/2000 a set/2019 | repositório de 2019 (`Dados/SPCS20RPSNSA.csv`); FRED, <https://fred.stlouisfed.org/series/SPCS20RPSNSA> | termos do FRED/S&P Dow Jones Indices; uso educacional | 08 |
| `supermercado.csv` | 1 000 cupons de três filiais, jan–mar/2019 | cópia de `supermarket_sales - Sheet1.csv` do material do livro, com nome simplificado | base pública usada em cursos; origem primária não registrada no material; conferir antes de redistribuir | 02, 03, 04, 05, 07 |

As bases dos casos adicionais (UCI *Bike Sharing*, *Student Performance*, *Online Retail*, licença CC BY 4.0; SNAP *Wiki-Vote*) têm origem, data de acesso e licença no README de cada caso.

Antes de publicar o repositório, confirme a licença de redistribuição de `supermercado.csv`, `D202.csv` (energia) e `claims-data-2015-as-of-feb-9-2016.xlsx` (dados governamentais dos EUA, em geral de domínio público). Nenhuma base contém dados pessoais identificáveis; os IDs de cliente do *Online Retail* são códigos numéricos sem nome.
