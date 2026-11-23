# Naive Bayes para texto: um filtro de spam com mensagens SMS reais.
# Dados: dados/sms_spam.tsv, SMS Spam Collection (UCI, id 228; Almeida e Hidalgo, 2011; CC BY 4.0).
# 5 574 mensagens em ingles rotuladas como 'ham' (normal) ou 'spam'.

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))
sms = pd.read_csv(os.path.join(pasta, '..', 'dados', 'sms_spam.tsv'), sep='\t', header=None, names=['rotulo', 'texto'], quoting=3)
sms['spam'] = (sms['rotulo'] == 'spam').astype(int)
print('Mensagens:', len(sms), '| spam:', sms['spam'].sum(), f'({sms["spam"].mean():.1%})')
print(sms.head(3).to_string())

treino, teste = train_test_split(sms, test_size=0.3, random_state=0, stratify=sms['spam'])

# --- 1. A mao, para entender: vocabulario e contagem de palavras por classe (so com o treino)
def palavras(texto):
    return re.findall(r'[a-z0-9£$]+', texto.lower())

contagem = {0: {}, 1: {}}
for texto, classe in zip(treino['texto'], treino['spam']):
    for p in palavras(texto):
        contagem[classe][p] = contagem[classe].get(p, 0) + 1
vocabulario = set(contagem[0]) | set(contagem[1])
total_palavras = {c: sum(contagem[c].values()) for c in [0, 1]}
priori = treino['spam'].value_counts(normalize=True)
print(f'\nVocabulario: {len(vocabulario)} palavras | total de palavras em ham: {total_palavras[0]}, em spam: {total_palavras[1]}')

def prob_palavra(p, c):
    # P(palavra | classe) com suavizacao de Laplace: (n_k + 1) / (n + |Vocabulario|)
    return (contagem[c].get(p, 0) + 1) / (total_palavras[c] + len(vocabulario))

def classificar(texto):
    # soma de logaritmos em vez de produto, para nao estourar para zero com mensagens longas
    pontos = {c: np.log(priori[c]) + sum(np.log(prob_palavra(p, c)) for p in palavras(texto) if p in vocabulario) for c in [0, 1]}
    return max(pontos, key=pontos.get), pontos

exemplo = 'WINNER! You have been selected to receive a £900 prize. Call now to claim'
classe, pontos = classificar(exemplo)
print(f'\n"{exemplo}"\nlog-pontuacao ham = {pontos[0]:.1f} | spam = {pontos[1]:.1f} -> {"spam" if classe else "ham"}')
previsto_a_mao = np.array([classificar(t)[0] for t in teste['texto']])
print(f'Naive Bayes a mao no teste: acuracia {accuracy_score(teste["spam"], previsto_a_mao):.3f}')

# --- 2. Com scikit-learn: CountVectorizer (saco de palavras) + MultinomialNB
vetorizador = CountVectorizer(token_pattern=r'[a-z0-9£$]+', lowercase=True)
X_tr = vetorizador.fit_transform(treino['texto'])           # vocabulario aprendido SO no treino
X_te = vetorizador.transform(teste['texto'])
modelo = MultinomialNB(alpha=1.0).fit(X_tr, treino['spam'])
previsto = modelo.predict(X_te)
matriz = confusion_matrix(teste['spam'], previsto)
print('\nscikit-learn MultinomialNB no teste:')
print(f'acuracia {accuracy_score(teste["spam"], previsto):.3f} | precisao (spam) {precision_score(teste["spam"], previsto):.3f} | '
      f'revocacao (spam) {recall_score(teste["spam"], previsto):.3f}')
print('Matriz (linhas = real ham/spam; colunas = previsto):')
print(matriz)
print(f'Linha de base (tudo e ham): {1 - teste["spam"].mean():.3f}')

# Palavras mais indicativas de spam: maior razao P(palavra|spam) / P(palavra|ham)
log_razao = modelo.feature_log_prob_[1] - modelo.feature_log_prob_[0]
nomes = np.array(vetorizador.get_feature_names_out())
frequentes = np.asarray(X_tr.sum(axis=0)).ravel() >= 20
ordem = np.argsort(log_razao[frequentes])
top_spam = pd.Series(np.exp(log_razao[frequentes][ordem[-12:]]), index=nomes[frequentes][ordem[-12:]])
top_ham = pd.Series(np.exp(-log_razao[frequentes][ordem[:12]]), index=nomes[frequentes][ordem[:12]])
print('\nPalavras com maior razao spam/ham (aparecem 20+ vezes):', list(top_spam.index[::-1]))

fig, (esq, dir) = plt.subplots(1, 2, figsize=(12, 4.4))
esq.barh(top_spam.index, top_spam.values, color='#BD5B58')
esq.set_xscale('log')
esq.set_xlabel('P(palavra | spam) / P(palavra | ham)  (escala log)')
esq.set_title('Palavras que mais puxam para spam', fontsize=11)
esq.grid(axis='y', visible=False)
dir.barh(top_ham.index, top_ham.values, color='#2F648F')
dir.set_xscale('log')
dir.set_xlabel('P(palavra | ham) / P(palavra | spam)  (escala log)')
dir.set_title('Palavras que mais puxam para mensagem normal', fontsize=11)
dir.grid(axis='y', visible=False)
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'filtro_de_spam.png'))
plt.show()
