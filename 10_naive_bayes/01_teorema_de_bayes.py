# Teorema de Bayes: como "inverter" uma probabilidade condicional.
# Um exame acerta 98% dos doentes e 97% dos saudaveis. A doenca atinge 0,8% da populacao.
# Se o exame deu positivo, qual a chance de a pessoa estar doente?

import os
import numpy as np
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

prevalencia = 0.008          # P(doente)
sensibilidade = 0.98         # P(positivo | doente)
especificidade = 0.97        # P(negativo | saudavel)  ->  P(positivo | saudavel) = 0,03

# Bayes: P(doente | positivo) = P(positivo | doente) P(doente) / P(positivo)
p_pos_e_doente = sensibilidade * prevalencia
p_pos_e_saudavel = (1 - especificidade) * (1 - prevalencia)
p_positivo = p_pos_e_doente + p_pos_e_saudavel
posterior = p_pos_e_doente / p_positivo
print(f'P(positivo e doente)   = {p_pos_e_doente:.4f}')
print(f'P(positivo e saudavel) = {p_pos_e_saudavel:.4f}')
print(f'P(doente | positivo)   = {posterior:.3f}')
# Apenas ~21%! A classe de maior probabilidade a posteriori (MAP) e "saudavel", mesmo com o exame positivo.
# Motivo: a doenca e rara; os 3% de falsos positivos sobre 99,2% de saudaveis superam os verdadeiros positivos.

# A mesma conta em "frequencias naturais": 10 000 pessoas
n = 10_000
doentes = n * prevalencia
verdadeiros_pos = doentes * sensibilidade
falsos_pos = (n - doentes) * (1 - especificidade)
print(f'\nEm {n} pessoas: {doentes:.0f} doentes; {verdadeiros_pos:.0f} positivos verdadeiros e {falsos_pos:.0f} positivos falsos')
print(f'Entre os {verdadeiros_pos + falsos_pos:.0f} positivos, {verdadeiros_pos:.0f} estao doentes: {verdadeiros_pos / (verdadeiros_pos + falsos_pos):.0%}')

# Como a resposta muda com a prevalencia (o "a priori")
prevalencias = np.linspace(0.001, 0.5, 300)
posteriores = sensibilidade * prevalencias / (sensibilidade * prevalencias + (1 - especificidade) * (1 - prevalencias))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.4))
# grade de 10 000 pontos resumida em 100 x 100 celulas: cada celula = 1 pessoa
grade = np.zeros(n)
grade[:int(round(verdadeiros_pos))] = 2                                         # doente e positivo
grade[int(round(verdadeiros_pos)):int(round(doentes))] = 3                     # doente e negativo
grade[int(round(doentes)):int(round(doentes + falsos_pos))] = 1                 # saudavel e positivo
esq.imshow(grade.reshape(100, 100), cmap=plt.matplotlib.colors.ListedColormap(['#E6EBF0', '#D69A35', '#BD5B58', '#20324A']),
           interpolation='nearest')
esq.set_xticks([])
esq.set_yticks([])
esq.grid(False)
esq.set_title(f'10 000 pessoas: {verdadeiros_pos:.0f} doentes positivas (vermelho)\ncontra {falsos_pos:.0f} saudáveis positivas (âmbar)', fontsize=11)
dir.plot(100 * prevalencias, 100 * posteriores, color='#2F648F', linewidth=2)
dir.axvline(100 * prevalencia, color='#D69A35', linestyle='--')
dir.text(100 * prevalencia + 1, 15, f'prevalência 0,8%\n→ {posterior:.0%}', color='#D69A35')
dir.set_xlabel('Prevalência da doença (%)')
dir.set_ylabel('P(doente | exame positivo) (%)')
dir.set_title('O mesmo exame vale muito mais onde a doença é comum', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'teorema_de_bayes.png'))
plt.show()
