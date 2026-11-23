# Executa todos os scripts .py das unidades, dos estudos de caso e dos geradores de figuras,
# sem abrir janelas de grafico, e informa quais terminaram sem erro.
#
# Uso, a partir da pasta principal do repositorio:
#   python scripts/executar_todos.py                  # tudo
#   python scripts/executar_todos.py 04_estatistica   # so uma pasta (ou varias, separadas por espaco)
#
# Cada script roda em um processo separado, a partir da propria pasta, com MPLBACKEND=Agg
# (matplotlib nao interativo). O resultado fica em scripts/relatorio_execucao.txt.

import os
import re
import sys
import time
import subprocess

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if len(sys.argv) > 1:
    pastas = sys.argv[1:]
else:
    # Todas as pastas numeradas (00_..., 01_..., ...) na ordem, mais os geradores de figuras
    pastas = sorted(p for p in os.listdir(raiz) if re.match(r'^\d\d_', p))
    pastas += [os.path.join('figuras', 'fontes'), os.path.join('animacoes', 'fontes')]

# Scripts que exigem dependencias opcionais nao incluidas no requirements-basico.txt
ignorar = ['opcional']

scripts = []
for pasta in pastas:
    caminho = os.path.join(raiz, pasta)
    for atual, subpastas, arquivos in os.walk(caminho):
        subpastas.sort()
        if os.path.basename(atual) in ('dados', 'figuras'):
            continue
        for nome in sorted(arquivos):
            if nome.endswith('.py') and not any(p in nome for p in ignorar):
                scripts.append(os.path.join(atual, nome))

ambiente = dict(os.environ)
ambiente['MPLBACKEND'] = 'Agg'
ambiente['PYTHONIOENCODING'] = 'utf-8'

linhas = []
falhas = 0
inicio_geral = time.time()
for script in scripts:
    inicio = time.time()
    resultado = subprocess.run([sys.executable, '-X', 'utf8', script], cwd=os.path.dirname(script),
                               capture_output=True, text=True, env=ambiente, encoding='utf-8')
    duracao = time.time() - inicio
    relativo = os.path.relpath(script, raiz)
    if resultado.returncode == 0:
        linha = f'OK     {duracao:6.1f}s  {relativo}'
    else:
        falhas += 1
        ultima = resultado.stderr.strip().splitlines()[-1] if resultado.stderr.strip() else 'sem mensagem'
        linha = f'ERRO   {duracao:6.1f}s  {relativo}\n         {ultima}'
    print(linha, flush=True)
    linhas.append(linha)

resumo = f'\n{len(scripts) - falhas} de {len(scripts)} scripts executaram sem erro ({time.time() - inicio_geral:.0f} s no total).'
print(resumo)
with open(os.path.join(raiz, 'scripts', 'relatorio_execucao.txt'), 'w', encoding='utf-8') as arq:
    arq.write('\n'.join(linhas) + resumo + '\n')

sys.exit(1 if falhas else 0)
