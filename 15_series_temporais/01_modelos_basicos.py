# Quatro modelos basicos de serie temporal, simulados para conhecer a "cara" de cada um:
#   ruido i.i.d. (independente e identicamente distribuido): nenhuma observacao ajuda a prever a seguinte
#   processo binario: X_t = +1 com probabilidade p, -1 caso contrario
#   passeio aleatorio: S_t = X_1 + ... + X_t (soma acumulada de ruidos): cada valor = anterior + um passo
#   tendencia + sazonalidade + ruido: X_t = m_t + s_t + Y_t

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
gerador = np.random.default_rng(3)
t = np.arange(240)

ruido = gerador.normal(0, 1, len(t))                       # ruido branco gaussiano
binario = np.where(gerador.random(len(t)) < 0.5, 1, -1)
passeio = np.cumsum(gerador.normal(0, 1, len(t)))
completo = 10 + 0.05 * t + 3 * np.sin(2 * np.pi * t / 12) + gerador.normal(0, 1, len(t))

# Uma diferenca entre ruido e passeio: a correlacao entre um valor e o seguinte
for nome, x in [('ruido i.i.d.', ruido), ('passeio aleatorio', passeio)]:
    print(f'{nome:18s}: correlacao entre x_t e x_(t+1) = {np.corrcoef(x[:-1], x[1:])[0, 1]:+.2f}')
# O passeio aleatorio parece ter "tendencias", mas elas sao fruto do acaso: simulando de novo, mudam de direcao.
finais = [np.cumsum(np.random.default_rng(s).normal(0, 1, 240))[-1] for s in range(1000)]
print(f'1000 passeios de 240 passos: valor final medio {np.mean(finais):+.2f}, desvio {np.std(finais):.1f} '
      f'(teoria: raiz de 240 = {np.sqrt(240):.1f})')

fig, eixos = plt.subplots(4, 1, figsize=(10, 9))
dados = [(ruido, 'Ruído i.i.d.: sem memória, oscila em torno de zero', '#8794A3'),
         (binario, 'Processo binário: só +1 ou −1 (primeiros 60 passos)', '#8794A3'),
         (passeio, 'Passeio aleatório: soma dos ruídos; parece ter tendência, mas é acaso', '#BD5B58'),
         (completo, 'Tendência + sazonalidade (período 12) + ruído', '#2F648F')]
for eixo, (x, titulo, cor) in zip(eixos, dados):
    if x is binario:
        eixo.step(t[:60], x[:60], color=cor, where='mid')
    else:
        eixo.plot(t, x, color=cor, linewidth=1.2)
    eixo.set_title(titulo, fontsize=11)
eixos[3].plot(t, 10 + 0.05 * t, color='#D69A35', linestyle='--', label='tendência')
eixos[3].legend(loc='upper left')
eixos[3].set_xlabel('t')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'modelos_basicos.png'))
plt.show()
