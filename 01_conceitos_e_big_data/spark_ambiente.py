# Prepara o Apache Spark (PySpark) para os scripts 08 a 12 desta unidade.
# requer: pyspark
#
# Para conferir a instalacao, execute este arquivo sozinho:
#   python 01_conceitos_e_big_data/spark_ambiente.py
#
# O que ele resolve, para que os outros scripts fiquem curtos:
# 1) O Spark roda na maquina virtual Java (JVM). Procuramos um Java 17 ou mais novo em JAVA_HOME,
#    no PATH e em ~/.jdk (a pasta onde o pacote install-jdk instala).
# 2) No Windows, o Hadoop (a biblioteca que o Spark usa para ler e gravar arquivos) pede dois programas
#    nativos, winutils.exe e hadoop.dll. Em vez deles, usamos um sistema de arquivos escrito so em Java
#    (hadoop-bare-naked-local-fs, 9 KB), baixado do Maven Central e conferido pelo SHA-256.
# 3) Tudo o que os scripts baixam ou geram fica FORA do repositorio, em ~/ciencia-de-dados-big-data
#    (ou na pasta da variavel de ambiente CIENCIA_DADOS_BIG_DATA). Apague essa pasta quando terminar.

import atexit
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import warnings
import zipfile
from pathlib import Path

PASTA_UNIDADE = os.path.dirname(os.path.abspath(__file__))
PASTA_FIGURAS = os.path.join(PASTA_UNIDADE, 'figuras')
ESTILO = os.path.join(PASTA_UNIDADE, '..', 'figuras', 'estilo.mplstyle')
RAIZ_DADOS = os.environ.get('CIENCIA_DADOS_BIG_DATA',
                            os.path.join(os.path.expanduser('~'), 'ciencia-de-dados-big-data'))

JAR_URL = ('https://repo1.maven.org/maven2/com/globalmentor/hadoop-bare-naked-local-fs/0.1.0/'
           'hadoop-bare-naked-local-fs-0.1.0.jar')
JAR_SHA256 = 'e0cc30fb0531eb0b59468dc0abf5b257533d2365b5e9f45e795edd707aa78c62'

COMO_INSTALAR_JAVA = '''
Nao encontrei o Java 17 (ou mais novo), necessario para o Spark. Instale de uma destas formas:
  - qualquer sistema, sem administrador:   pip install install-jdk
                                           python -c "import jdk; jdk.install('17')"
  - Windows ou macOS: instalador do Eclipse Temurin 17 em https://adoptium.net
  - Linux (Ubuntu/Debian):                 sudo apt install openjdk-17-jdk
Depois feche e abra o terminal e rode de novo.
Erro: o Spark precisa do Java 17 ou mais novo, e ele nao foi encontrado.'''


def pasta_dados(*partes):
    """Pasta (fora do repositorio) onde os scripts guardam dados baixados ou gerados."""
    caminho = os.path.join(RAIZ_DADOS, *partes)
    os.makedirs(caminho, exist_ok=True)
    return caminho


def _versao_java(executavel):
    try:
        saida = subprocess.run([executavel, '-version'], capture_output=True, text=True, timeout=60).stderr
    except (OSError, subprocess.SubprocessError):
        return 0
    achado = re.search(r'version "(\d+)(?:\.(\d+))?', saida)
    if not achado:
        return 0
    maior = int(achado.group(1))
    return int(achado.group(2) or 0) if maior == 1 else maior      # "1.8.0" e o Java 8


def preparar_java():
    """Encontra um Java >= 17 e ajusta JAVA_HOME para o PySpark. Devolve a versao encontrada."""
    nome = 'java.exe' if os.name == 'nt' else 'java'
    candidatos = []
    if os.environ.get('JAVA_HOME'):
        candidatos.append(('JAVA_HOME', os.path.join(os.environ['JAVA_HOME'], 'bin', nome)))
    if shutil.which('java'):
        candidatos.append(('PATH', shutil.which('java')))
    for padrao in ('*', os.path.join('*', 'Contents', 'Home')):          # Linux/Windows e macOS
        for achado in sorted(glob.glob(os.path.join(os.path.expanduser('~'), '.jdk', padrao, 'bin', nome)),
                             reverse=True):
            candidatos.append(('~/.jdk', achado))
    for origem, executavel in candidatos:
        versao = _versao_java(executavel) if os.path.isfile(executavel) else 0
        if versao >= 17:
            if origem == 'PATH':
                os.environ.pop('JAVA_HOME', None)          # o PySpark usara o java do PATH
            else:
                os.environ['JAVA_HOME'] = _caminho_curto(os.path.dirname(os.path.dirname(executavel)))
            return versao
    raise SystemExit(COMO_INSTALAR_JAVA)


def _jar_confere(caminho):
    if not os.path.exists(caminho):
        return False
    with open(caminho, 'rb') as arq:
        return hashlib.sha256(arq.read()).hexdigest() == JAR_SHA256


def _jar_sistema_de_arquivos():
    """Instala o jar e devolve o caminho a acrescentar ao classpath (None se nao precisar).
    O lugar preferido e a pasta 'jars' do proprio pyspark, que o Java ja carrega ao iniciar:
    assim nao e preciso passar caminho nenhum, o que evita erros com espacos ou acentos no caminho."""
    import pyspark
    nome = os.path.basename(JAR_URL)
    nos_jars = os.path.join(os.path.dirname(pyspark.__file__), 'jars', nome)
    reserva = os.path.join(pasta_dados('_spark'), nome)
    if _jar_confere(nos_jars):
        return None
    if _jar_confere(reserva):
        conteudo = open(reserva, 'rb').read()
    else:
        print('Baixando do Maven Central o sistema de arquivos em Java para o Windows (9 KB)...')
        try:
            with urllib.request.urlopen(JAR_URL, timeout=60) as resposta:
                conteudo = resposta.read()
        except OSError as erro:
            raise SystemExit(f'Nao consegui baixar {JAR_URL} ({erro}). Na primeira execucao no Windows '
                             'e preciso internet; tente de novo.')
        if hashlib.sha256(conteudo).hexdigest() != JAR_SHA256:
            raise SystemExit('O arquivo baixado nao confere com o SHA-256 esperado; nada foi gravado.')
    try:
        with open(nos_jars, 'wb') as arq:
            arq.write(conteudo)
        return None
    except OSError:                                      # sem permissao na pasta do pyspark
        with open(reserva, 'wb') as arq:
            arq.write(conteudo)
        return reserva


def _classe_checkpoint():
    # A classe mudou de pacote entre versoes do Spark: procuramos o nome dentro do proprio jar.
    import pyspark
    for jar in glob.glob(os.path.join(os.path.dirname(pyspark.__file__), 'jars', 'spark-sql_*.jar')):
        with zipfile.ZipFile(jar) as arquivo:
            for nome in arquivo.namelist():
                if nome.endswith('/FileSystemBasedCheckpointFileManager.class'):
                    return nome[:-len('.class')].replace('/', '.')
    return None


def _config_log():
    # Mostra so erros do Java, para que a saida dos scripts fique legivel.
    caminho = os.path.join(pasta_dados('_spark'), 'log4j2.properties')
    texto = ('rootLogger.level = warn\n'
             'rootLogger.appenderRef.saida.ref = saida\n'
             'appender.console.type = Console\n'
             'appender.console.name = saida\n'
             'appender.console.target = SYSTEM_ERR\n'
             'appender.console.filter.limite.type = ThresholdFilter\n'
             'appender.console.filter.limite.level = error\n'
             'appender.console.layout.type = PatternLayout\n'
             'appender.console.layout.pattern = %d{HH:mm:ss} %p %c{1}: %m%n\n')
    with open(caminho, 'w', encoding='utf-8') as arq:
        arq.write(texto)
    return Path(caminho).as_uri()


def _caminho_curto(caminho):
    # Os scripts .cmd do Spark no Windows quebram com espacos no caminho (por exemplo, no nome do usuario).
    # O nome curto do Windows (formato 8.3) aponta para o mesmo lugar e nao tem espacos.
    if os.name != 'nt' or ' ' not in caminho:
        return caminho
    import ctypes
    buffer = ctypes.create_unicode_buffer(32768)
    tamanho = ctypes.windll.kernel32.GetShortPathNameW(caminho, buffer, 32768)
    return buffer.value if 0 < tamanho < 32768 else caminho


def _silenciar_ao_sair():
    # No Windows, o PySpark encerra o Java com o comando taskkill, que escreve "EXITO: o processo ...".
    # Esta funcao e registrada depois do PySpark, entao roda antes dele e desvia essas mensagens.
    sys.stdout.flush()
    sys.stderr.flush()
    nulo = os.open(os.devnull, os.O_WRONLY)
    os.dup2(nulo, 1)
    os.dup2(nulo, 2)


def iniciar_spark(nome, memoria='2g', nucleos='*', config=None):
    """Cria uma sessao Spark local: um 'cluster' cujos trabalhadores sao os nucleos deste computador."""
    preparar_java()
    import pyspark
    python = _caminho_curto(sys.executable)
    os.environ['PYSPARK_PYTHON'] = python                 # o mesmo Python (e ambiente) deste script
    os.environ['PYSPARK_DRIVER_PYTHON'] = python
    os.environ['SPARK_HOME'] = _caminho_curto(os.path.dirname(pyspark.__file__))   # o Spark que veio com o pip
    warnings.filterwarnings('ignore', message='.*pandas >= 3.0.0.*')
    from pyspark.sql import SparkSession

    particoes = os.cpu_count() if nucleos == '*' else int(nucleos)
    construtor = (SparkSession.builder.master(f'local[{nucleos}]').appName(nome)
                  .config('spark.driver.memory', memoria)
                  .config('spark.driver.host', '127.0.0.1')
                  .config('spark.driver.bindAddress', '127.0.0.1')
                  .config('spark.ui.enabled', 'false')
                  .config('spark.ui.showConsoleProgress', 'false')
                  .config('spark.sql.shuffle.partitions', str(particoes))
                  .config('spark.sql.session.timeZone', 'UTC')
                  .config('spark.sql.warehouse.dir', Path(pasta_dados('_spark', 'warehouse')).as_uri())
                  .config('spark.driver.extraJavaOptions', f'-Dlog4j2.configurationFile={_config_log()}'))
    if os.name == 'nt':
        caminho_extra = _jar_sistema_de_arquivos()
        if caminho_extra:
            construtor = construtor.config('spark.driver.extraClassPath', caminho_extra)
        construtor = construtor.config('spark.hadoop.fs.file.impl',
                                       'com.globalmentor.apache.hadoop.fs.BareLocalFileSystem')
        classe = _classe_checkpoint()
        if classe:
            construtor = construtor.config('spark.sql.streaming.checkpointFileManagerClass', classe)
    for chave, valor in (config or {}).items():
        construtor = construtor.config(chave, valor)
    spark = construtor.getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')
    if os.name == 'nt':
        atexit.register(_silenciar_ao_sair)
    return spark


def coletar(df):
    """Traz um resultado PEQUENO do Spark para um DataFrame do pandas (para imprimir e desenhar)."""
    import pandas as pd
    return pd.DataFrame([linha.asDict() for linha in df.collect()])


def memoria_pico_mb(pid=None):
    """Maior quantidade de RAM ja ocupada por um processo (o atual, se pid=None), em MB."""
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes

        class Contadores(ctypes.Structure):
            _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD),
                        ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                        ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                        ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]

        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        psapi = ctypes.WinDLL('psapi', use_last_error=True)
        kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        kernel32.OpenProcess.restype = wintypes.HANDLE
        kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Contadores), wintypes.DWORD]
        alca = kernel32.GetCurrentProcess() if pid is None else kernel32.OpenProcess(0x1000 | 0x0010, False, pid)
        contadores = Contadores()
        contadores.cb = ctypes.sizeof(Contadores)
        ok = psapi.GetProcessMemoryInfo(alca, ctypes.byref(contadores), contadores.cb)
        if pid is not None:
            kernel32.CloseHandle(alca)
        return contadores.PeakWorkingSetSize / 1e6 if ok else float('nan')
    if pid is not None:
        try:
            with open(f'/proc/{pid}/status') as arq:                    # Linux
                for linha in arq:
                    if linha.startswith('VmHWM:'):
                        return int(linha.split()[1]) / 1e3
        except OSError:
            return float('nan')
        return float('nan')
    import resource
    pico = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return pico / 1e6 if sys.platform == 'darwin' else pico / 1e3


def memoria_jvm_pico_mb(spark):
    """Pico de RAM do processo Java onde o Spark faz o trabalho pesado."""
    pid = spark.sparkContext._jvm.java.lang.ProcessHandle.current().pid()
    return memoria_pico_mb(int(pid))


def memoria_total_mb():
    """RAM total deste computador, em MB."""
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes

        class Estado(ctypes.Structure):
            _fields_ = [('dwLength', wintypes.DWORD), ('dwMemoryLoad', wintypes.DWORD),
                        ('ullTotalPhys', ctypes.c_ulonglong), ('ullAvailPhys', ctypes.c_ulonglong),
                        ('ullTotalPageFile', ctypes.c_ulonglong), ('ullAvailPageFile', ctypes.c_ulonglong),
                        ('ullTotalVirtual', ctypes.c_ulonglong), ('ullAvailVirtual', ctypes.c_ulonglong),
                        ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]

        estado = Estado()
        estado.dwLength = ctypes.sizeof(Estado)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(estado))
        return estado.ullTotalPhys / 1e6
    return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / 1e6


if __name__ == '__main__':
    inicio = time.time()
    versao_java = preparar_java()
    spark = iniciar_spark('verificacao')
    print(f'Python {sys.version.split()[0]} | PySpark {spark.version} | Java {versao_java}')
    print(f'Sessao criada em {time.time() - inicio:.1f} s, com {spark.sparkContext.defaultParallelism} nucleos')
    print('Dados grandes e caches ficam em:', RAIZ_DADOS)
    teste = os.path.join(pasta_dados('_spark'), 'teste_escrita')
    spark.range(1_000_000).selectExpr('id % 10 AS grupo').write.mode('overwrite').parquet(teste)
    contagem = spark.read.parquet(teste).groupBy('grupo').count().count()
    print(f'Gravar e ler Parquet: ok ({contagem} grupos)')
    shutil.rmtree(teste, ignore_errors=True)
    spark.stop()
    print('Tudo pronto para os scripts 08 a 12.')
