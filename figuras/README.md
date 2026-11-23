# figuras/ e animacoes/

- `estilo.mplstyle`: o tema único de todas as figuras do repositório (explicado em [materiais/manual_visual.md](../materiais/manual_visual.md)).
- `fontes/`: scripts que geram as figuras didáticas usadas nos READMEs. `../animacoes/fontes/` faz o mesmo para os GIFs.
- `geradas/`: as saídas. Cada unidade e cada estudo de caso tem ainda a própria pasta `figuras/`, preenchida pelos seus scripts.

Regenerar tudo, da pasta principal:

```
python scripts/executar_todos.py figuras/fontes animacoes/fontes
```
