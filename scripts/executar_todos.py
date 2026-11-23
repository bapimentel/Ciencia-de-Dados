# Executa todos os scripts .py de uma ou mais pastas, sem abrir janelas de grafico,
# e informa quais terminaram sem erro. Serve para conferir o repositorio inteiro.
#
# Uso, a partir da pasta principal do repositorio:
#   python scripts/executar_todos.py                 # todas as unidades e estudos de caso
#   python scripts/executar_todos.py 03_estatistica  # so uma pasta
#
# Cada script roda em um processo separado, com MPLBACKEND=Agg (matplotlib nao
# interativo). O resultado fica em scripts/relatorio_execucao.txt.

import os
import sys
import time
import subprocess

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pastas_padrao = [
    '00_como_comecar', '01_python', '02_primeiros_dados', '03_estatistica',
    '04_visualizacao', '05_preprocessamento', '06_classificacao_e_avaliacao',
    '07_agrupamento', '08_series_temporais', '09_redes_sociais',
    '10_estudos_de_caso', 'figuras/fontes', 'animacoes/fontes',
]
pastas = sys.argv[1:] if len(sys.argv) > 1 else pastas_padrao

# Scripts que exigem dependencias opcionais ou arquivos grandes nao incluidos
ignorar = ['opcional']

scripts = []
for pasta in pastas:
    caminho = os.path.join(raiz, pasta)
    for atual, subpastas, arquivos in os.walk(caminho):
        if os.path.sep + 'original' in atual or os.path.basename(atual) == 'dados':
            continue
        for nome in sorted(arquivos):
            if nome.endswith('.py') and not any(p in nome for p in ignorar):
                scripts.append(os.path.join(atual, nome))

ambiente = dict(os.environ)
ambiente['MPLBACKEND'] = 'Agg'
ambiente['PYTHONIOENCODING'] = 'utf-8'

linhas = []
falhas = 0
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
    print(linha)
    linhas.append(linha)

resumo = f'\n{len(scripts) - falhas} de {len(scripts)} scripts executaram sem erro.'
print(resumo)
with open(os.path.join(raiz, 'scripts', 'relatorio_execucao.txt'), 'w', encoding='utf-8') as arq:
    arq.write('\n'.join(linhas) + resumo + '\n')

sys.exit(1 if falhas else 0)
