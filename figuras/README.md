# figuras/ e animacoes/

- `estilo.mplstyle`: o tema de todas as figuras do repositório (explicado no [manual visual](../materiais/manual_visual.md)).
- `fontes/`: scripts que geram as figuras de uso geral (paleta, lista → gráfico, correlação × causalidade, treino/teste × vazamento, fronteiras de decisão). `../animacoes/fontes/` gera as onze animações.
- `geradas/`: as saídas. Cada unidade e cada estudo de caso tem também a própria pasta `figuras/`, preenchida pelos seus scripts.

Para regenerar, da pasta principal:

```powershell
python scripts/executar_todos.py figuras/fontes animacoes/fontes
```
