# Metricas globais: densidade, diametro, caminho medio, agrupamento medio e componentes.
# Comparamos tres redes pequenas para dar escala aos numeros.

import os
import networkx as nx
import matplotlib.pyplot as plt

pasta = os.path.dirname(os.path.abspath(__file__))
plt.style.use(os.path.join(pasta, '..', 'figuras', 'estilo.mplstyle'))

redes = {
    'aleatoria (20 nós, p=0,4)': nx.erdos_renyi_graph(20, 0.4, seed=42),
    'clube de karatê (34 nós)': nx.karate_club_graph(),
    'caminho (20 nós em fila)': nx.path_graph(20),
}

print(f'{"rede":28s} {"nós":>4s} {"arestas":>8s} {"densidade":>10s} {"diâmetro":>9s} {"cam. médio":>11s} {"agrup. médio":>13s}')
for nome, G in redes.items():
    densidade = nx.density(G)                       # arestas existentes / arestas possiveis
    diametro = nx.diameter(G)                       # maior distancia entre dois nos
    caminho_medio = nx.average_shortest_path_length(G)
    agrupamento = nx.average_clustering(G)          # media dos coeficientes locais
    print(f'{nome:28s} {G.number_of_nodes():4d} {G.number_of_edges():8d} {densidade:10.3f} {diametro:9d} {caminho_medio:11.2f} {agrupamento:13.3f}')

# Leitura: a rede aleatoria e densa e "curta"; o clube de karate tem agrupamento alto (amigos de amigos
# sao amigos) com densidade baixa; o caminho em fila e o extremo oposto: diametro 19, agrupamento 0.

# Componentes: partes desconectadas. Removendo um no-ponte, a rede pode se partir
G = nx.karate_club_graph()
print('\nComponentes conectados no clube de karate:', nx.number_connected_components(G))
pontes = list(nx.bridges(G))
print('Arestas-ponte (remove-las desconecta alguem):', pontes)
G_sem = G.copy()
G_sem.remove_node(0)
print('Componentes apos remover o no 0:', nx.number_connected_components(G_sem),
      '| tamanhos:', sorted((len(c) for c in nx.connected_components(G_sem)), reverse=True))

# Distribuicao de grau: quantos nos tem cada grau
fig, eixos = plt.subplots(1, 3, figsize=(11, 3.2))
for eixo, (nome, rede) in zip(eixos, redes.items()):
    graus = [d for _, d in rede.degree()]
    eixo.hist(graus, bins=range(0, max(graus) + 2), color='#2F648F', align='left')
    eixo.set_title(nome, fontsize=11)
    eixo.set_xlabel('grau')
eixos[0].set_ylabel('nós')
fig.suptitle('Distribuição de grau: a rede real tem poucos nós muito conectados e muitos com grau baixo', x=0.01, ha='left')
plt.tight_layout()
plt.savefig(os.path.join(pasta, 'figuras', 'distribuicao_grau.png'))
plt.show()

# Experimente: gere nx.barabasi_albert_graph(200, 2, seed=1) e compare a distribuicao de grau
# com a de nx.erdos_renyi_graph(200, 0.02, seed=1). Qual se parece mais com redes sociais reais?
