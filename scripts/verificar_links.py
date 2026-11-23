# Confere se os links e imagens relativos dos arquivos Markdown apontam para arquivos que existem.
# Uso, a partir da pasta principal:  python scripts/verificar_links.py

import os
import re
import sys
from urllib.parse import unquote

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
padrao = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')

quebrados = []
total = 0
for atual, subpastas, arquivos in os.walk(raiz):
    if os.path.sep + '.' in atual or os.path.sep + 'venv' in atual:
        continue
    for nome in arquivos:
        if not nome.endswith('.md'):
            continue
        caminho = os.path.join(atual, nome)
        texto = open(caminho, encoding='utf-8').read()
        for alvo in padrao.findall(texto):
            if alvo.startswith(('http://', 'https://', 'mailto:', '#')):
                continue
            total += 1
            alvo_limpo = unquote(alvo.split('#')[0])
            destino = os.path.normpath(os.path.join(atual, alvo_limpo))
            if not os.path.exists(destino):
                quebrados.append((os.path.relpath(caminho, raiz), alvo))

print(f'{total} links relativos conferidos em arquivos .md')
if quebrados:
    print(f'{len(quebrados)} quebrados:')
    for arquivo, alvo in quebrados:
        print(f'  {arquivo}: {alvo}')
    sys.exit(1)
print('Nenhum link quebrado.')
