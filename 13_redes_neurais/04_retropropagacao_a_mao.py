# Retropropagacao (backpropagation) escrita a mao, para uma rede 2-2-1 com ativacao sigmoide, no XOR.
# Ideia: o erro da saida e "distribuido de volta" para a camada oculta pela regra da cadeia.
#   saida:  delta_o = (d - o) * o * (1 - o)
#   oculto: delta_h = y_h * (1 - y_h) * soma(delta_o * w_oh)
#   peso:   w = w + taxa * delta * (sinal que entra no peso)
# A primeira atualizacao e impressa passo a passo; depois treinamos por varias epocas.

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
d = np.array([0, 1, 1, 0], dtype=float)


def sigmoide(v):
    return 1 / (1 + np.exp(-v))


def treinar(semente, taxa=0.5, epocas=8000, mostrar=False):
    gerador = np.random.default_rng(semente)
    W1 = gerador.uniform(-1, 1, (2, 2))    # W1[j, i]: peso da entrada i para o oculto j
    b1 = gerador.uniform(-1, 1, 2)
    W2 = gerador.uniform(-1, 1, 2)         # peso do oculto j para a saida
    b2 = gerador.uniform(-1, 1)
    erros = []
    for epoca in range(epocas):
        soma_erro = 0.0
        for x, alvo in zip(X, d):
            # propagacao para frente
            y = sigmoide(W1 @ x + b1)
            o = sigmoide(W2 @ y + b2)
            e = alvo - o
            soma_erro += 0.5 * e ** 2
            # retropropagacao: gradientes locais
            delta_o = e * o * (1 - o)
            delta_h = y * (1 - y) * delta_o * W2
            if mostrar and epoca == 0 and x.tolist() == [0.0, 1.0]:
                print('Primeira passagem do exemplo x = (0, 1), desejado d = 1')
                print(f'  ocultos y = sigmoide(W1 x + b1) = {np.round(y, 4)}')
                print(f'  saida   o = sigmoide(W2 y + b2) = {o:.4f}   erro e = d - o = {e:+.4f}')
                print(f'  delta da saida  = e * o * (1-o)           = {delta_o:+.5f}')
                print(f'  deltas ocultos  = y(1-y) * delta_o * W2   = {np.round(delta_h, 5)}')
                print(f'  ajuste em W2    = taxa * delta_o * y      = {np.round(taxa * delta_o * y, 5)}')
            # atualizacao
            W2 = W2 + taxa * delta_o * y
            b2 = b2 + taxa * delta_o
            W1 = W1 + taxa * np.outer(delta_h, x)
            b1 = b1 + taxa * delta_h
        erros.append(soma_erro)
    saidas = np.array([sigmoide(W2 @ sigmoide(W1 @ x + b1) + b2) for x in X])
    return erros, saidas


erros, saidas = treinar(semente=1, mostrar=True)
print('\nDepois de 8000 epocas (semente 1):')
for x, alvo, o in zip(X, d, saidas):
    print(f'  x = {x.astype(int)}  desejado {int(alvo)}  saida {o:.3f}')

# A rede comeca de pesos sorteados. Algumas sementes param num minimo local (erro alto que nao cai).
print('\nSemente  erro final  resolveu?')
curvas = {}
for semente in range(10):
    erros_s, saidas_s = treinar(semente)
    resolveu = bool(np.all((saidas_s >= 0.5) == (d == 1)))
    curvas[semente] = (erros_s, resolveu)
    print(f'{semente:7d}  {erros_s[-1]:10.4f}  {"sim" if resolveu else "NAO"}')
print(f'Resolveram: {sum(r for _, r in curvas.values())} de 10')

fig, eixo = plt.subplots(figsize=(8, 4.2))
for semente, (erros_s, resolveu) in curvas.items():
    eixo.plot(erros_s, color='#2F648F' if resolveu else '#BD5B58', alpha=0.8, linewidth=1.4)
eixo.set_xscale('log')
eixo.set_xlabel('Época (escala log)')
eixo.set_ylabel('Erro quadrático no treino')
eixo.plot([], [], color='#2F648F', label='aprendeu o XOR')
eixo.plot([], [], color='#BD5B58', label='parou num mínimo local')
eixo.legend()
eixo.set_title('Dez inicializações: o erro fica parado um tempo e depois despenca (ou não)', fontsize=11)
plt.savefig(os.path.join(pasta, 'figuras', 'retropropagacao_xor.png'))
plt.show()
