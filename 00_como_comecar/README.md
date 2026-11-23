# 00 · Como começar

**Pergunta inicial:** o que acontece quando você digita `2 + 3` e aperta Enter?

Antes de analisar dados, você precisa de três coisas funcionando no seu computador: o Python, um editor e o conteúdo deste repositório. Esta unidade resolve isso. Ao final, você terá executado um programa e saberá onde os erros mais comuns aparecem.

Pré-requisitos: nenhum.

## 1. Instalar o Python

Baixe a versão 3.11 ou mais recente em <https://www.python.org/downloads/>. No Windows, marque a opção **Add Python to PATH** na primeira tela do instalador. Em Linux e macOS, o Python costuma vir instalado; confira com o comando abaixo.

Abra um terminal (no Windows, procure por *PowerShell*; no macOS, *Terminal*; no Linux, qualquer emulador de terminal) e digite:

```
python --version
```

Se aparecer algo como `Python 3.12.4`, está pronto. Se aparecer um erro, em Linux ou macOS tente `python3 --version`. Nos comandos seguintes use o nome que funcionou.

## 2. Escolher um editor

Dois caminhos funcionam bem com este material:

- **VS Code** (<https://code.visualstudio.com/>) com a extensão *Python*. Abra a pasta do repositório com *File > Open Folder*. Para executar um arquivo, use o botão de play no canto superior direito ou o terminal integrado.
- **Spyder** (vem com a distribuição Anaconda, ou `pip install spyder`). Abra o arquivo e aperte F5 para rodar tudo, ou selecione algumas linhas e aperte F9 para rodar só aquele trecho. Esse modo "linha a linha" é ótimo para a unidade 01.

Os scripts deste repositório são arquivos `.py` comuns. Não é preciso Jupyter.

## 3. Baixar o repositório

Na página do repositório no GitHub, clique em **Code > Download ZIP** e descompacte em uma pasta fácil de encontrar, por exemplo `Documentos/Ciencia-de-Dados`. Se você já usa Git:

```
git clone https://github.com/bapimentel/Ciencia-de-Dados.git
```

A partir daqui, todos os comandos consideram que o terminal está **dentro da pasta principal do repositório** (aquela que contém o arquivo `README.md`). Para entrar nela:

```
cd Documentos/Ciencia-de-Dados
```

## 4. Criar um ambiente virtual e instalar as bibliotecas

Um ambiente virtual é uma pasta onde as bibliotecas desta disciplina ficam separadas do resto do computador. Isso evita conflitos de versão.

Windows (PowerShell):

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-basico.txt
```

Se o PowerShell reclamar de "execução de scripts desabilitada", rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente de novo.

Linux ou macOS:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-basico.txt
```

Quando o ambiente está ativo, o nome `(.venv)` aparece no começo da linha do terminal. É preciso ativá-lo de novo toda vez que abrir um terminal novo. No VS Code, escolha esse ambiente como interpretador (*Python: Select Interpreter*).

A instalação baixa `numpy`, `pandas`, `matplotlib`, `scipy`, `scikit-learn`, `statsmodels` e `networkx`. As unidades 01 e 02 usam só o Python e o `pandas`; as outras bibliotecas entram quando forem necessárias.

## 5. Executar o primeiro programa

```
python 00_como_comecar/primeiro_programa.py
```

O programa imprime algumas contas e uma frase. Abra o arquivo [primeiro_programa.py](primeiro_programa.py), mude um número, salve e execute de novo. Prever o resultado antes de rodar é um bom hábito desde já.

## 6. Console interativo e script: duas formas de executar

Se você digitar apenas `python` no terminal, entra no **console interativo**. Nele, cada expressão que você digita mostra o resultado na hora:

```
>>> 2 + 3
5
```

Quando você executa um **arquivo** com `python nome.py`, o Python calcula as expressões, mas só mostra na tela o que estiver dentro de `print()`. Por isso os scripts da unidade 01 usam `print()` nos pontos em que você precisa ver algo. No Spyder, selecionar linhas e apertar F9 equivale ao console interativo.

Para sair do console, digite `exit()`.

## 7. Erros frequentes

| Mensagem | Causa provável | O que fazer |
|---|---|---|
| `python não é reconhecido` / `command not found` | Python fora do PATH | Reinstale marcando *Add to PATH* ou use `python3` |
| `No such file or directory` ao executar | Terminal em outra pasta | Use `cd` até a pasta principal do repositório |
| `FileNotFoundError: ... .csv` | Script procurando o arquivo de dados no lugar errado | Os scripts deste repositório localizam os dados a partir da própria pasta do script; se você copiou só o `.py` para outro lugar, copie também a pasta `dados` |
| `ModuleNotFoundError: No module named 'pandas'` | Ambiente virtual não ativado ou bibliotecas não instaladas | Ative o `.venv` e rode o `pip install` de novo |
| Gráfico não aparece | Execução em terminal sem interface gráfica | Os scripts também salvam os gráficos em arquivos `.png`; procure na pasta `figuras` da unidade |

## 8. Como os scripts encontram os arquivos de dados

Vários scripts começam com estas duas linhas:

```python
import os
pasta = os.path.dirname(os.path.abspath(__file__))
```

`__file__` é o caminho do próprio script. As duas linhas descobrem em que pasta ele está, para que `os.path.join(pasta, 'dados', 'arquivo.csv')` funcione independentemente de onde o terminal estiver. É a única "infraestrutura" que você verá nos scripts.

## Atividade

1. Execute `primeiro_programa.py` e anote o que apareceu na tela.
2. Troque o valor da variável `preco` por outro número e execute de novo. O resultado mudou como você esperava?
3. Abra o console interativo, digite `10 / 3` e depois `10 // 3`. Qual é a diferença?

## Próxima etapa

[01 · Python do zero](../01_python/)
