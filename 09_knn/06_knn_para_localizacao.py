# k-NN para prever um numero (regressao): localizar uma etiqueta dentro de um predio pela forca do sinal.
# Etiquetas de referencia com posicao conhecida + 4 leitores que medem a forca do sinal (RSSI).
# A posicao de uma etiqueta nova e a media ponderada das posicoes das k referencias com sinal mais parecido:
#   E_r = distancia euclidiana entre os vetores de sinal; peso W_r = (1/E_r^2) / soma(1/E_c^2)
# Dados SIMULADOS com um modelo simples de propagacao (semente fixa), para fins didaticos.

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
gerador = np.random.default_rng(6)

leitores = np.array([[0, 0], [20, 0], [0, 15], [20, 15]])           # sala de 20 m x 15 m

def sinal(posicao, ruido=2.0):
    # forca do sinal (dBm) cai com o logaritmo da distancia a cada leitor, mais ruido
    d = np.sqrt(((leitores - posicao) ** 2).sum(axis=1)) + 0.5
    return -40 - 25 * np.log10(d) + gerador.normal(0, ruido, size=len(leitores))

# Referencias: uma etiqueta a cada 2,5 m
referencias = np.array([[x, y] for x in np.arange(1.25, 20, 2.5) for y in np.arange(1.25, 15, 2.5)])
sinais_ref = np.array([sinal(p) for p in referencias])
print('Etiquetas de referencia:', len(referencias))

def localizar(sinal_novo, k):
    E = np.sqrt(((sinais_ref - sinal_novo) ** 2).sum(axis=1))
    mais_proximas = np.argsort(E)[:k]
    pesos = 1 / E[mais_proximas] ** 2
    pesos = pesos / pesos.sum()
    return (pesos[:, None] * referencias[mais_proximas]).sum(axis=0), mais_proximas

# Avaliar com 300 etiquetas em posicoes aleatorias
verdadeiras = gerador.uniform([0, 0], [20, 15], size=(300, 2))
erros = {}
for k in [1, 2, 4, 6, 10, 20]:
    estimadas = np.array([localizar(sinal(p), k)[0] for p in verdadeiras])
    erros[k] = np.sqrt(((estimadas - verdadeiras) ** 2).sum(axis=1))
    print(f'k={k:2d}: erro mediano de posicao {np.median(erros[k]):.2f} m | 90% dos erros abaixo de {np.percentile(erros[k], 90):.2f} m')

exemplo = np.array([13.0, 6.0])
estimada, usadas = localizar(sinal(exemplo), 4)
fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.4), gridspec_kw={'width_ratios': [1.3, 1]})
esq.scatter(referencias[:, 0], referencias[:, 1], color='#8794A3', s=20, label='etiquetas de referência')
esq.scatter(leitores[:, 0], leitores[:, 1], marker='s', s=90, color='#20324A', label='leitores')
esq.scatter(referencias[usadas, 0], referencias[usadas, 1], color='#2F648F', s=60, label='4 com sinal mais parecido')
esq.scatter(*exemplo, marker='*', s=260, color='#168A8A', label='posição real')
esq.scatter(*estimada, marker='X', s=140, color='#D69A35', label='posição estimada')
esq.set_aspect('equal')
esq.set_xlabel('m')
esq.set_ylabel('m')
esq.set_title(f'Erro neste exemplo: {np.linalg.norm(estimada - exemplo):.1f} m', fontsize=11)
esq.legend(fontsize=8, loc='upper left', bbox_to_anchor=(1.0, 1.0))
dir.boxplot([erros[k] for k in erros], tick_labels=[str(k) for k in erros], medianprops=dict(color='#D69A35', linewidth=2))
dir.set_xlabel('k (referências usadas)')
dir.set_ylabel('Erro de posição (m)')
dir.set_title('Simulado: com k entre 4 e 6 o erro é menor', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'knn_localizacao.png'))
plt.show()
