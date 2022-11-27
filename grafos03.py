import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class Tarefa:
    def __init__(self, nome, duracao, precedentes: list):
        self.nome = nome
        self.duracao = duracao
        self.precedentes = precedentes
        self.id = 0
        self.inicio_cedo = 0
        self.inicio_tarde = 0
        self.saida_cedo = duracao
        self.saida_tarde = 0
        self.fim = False
    
    def print(self):
        print(f'id: {self.id} nome: {self.nome} duracao: {self.duracao} precendentes: {self.precedentes} inicio_cedo: {self.inicio_cedo} inicio_tarde: {self.inicio_tarde} saida_cedo: {self.saida_cedo} saida_tarde: {self.saida_tarde} Fim: {self.fim}' )


class Tabela():
    def __init__(self):
        self.tabelaTarefas = []
        self.id = 0

        tarefa = Tarefa('Inicio', 0, [])
        self.adicionaTarefa(tarefa)

    def adicionaTarefa(self, tarefa):
        tarefa.id = self.id
        self.tabelaTarefas.append(tarefa)
        self.id += 1

    def print(self):
        for i in self.tabelaTarefas:
            i.print()

    def caminhoDeIda(self):
        nao_visitados = self.tabelaTarefas.copy()

        #Encontra o ponto inicial da análise
        for t in self.tabelaTarefas:
            if len(t.precedentes) == 0:
                prox_tarefa =  t
        
        del(nao_visitados[prox_tarefa.id])

        while True:
            tarefa = prox_tarefa
            #print('Tarefa:')
            #tarefa.print()
            adjacentes = self.encontrarAdjacente(tarefa)

            #adiciona os valores de chagada e saída de cada tarefa
            for adjacente in adjacentes:
                adjacente.inicio_cedo = self.maiorTempoDuracao(adjacente)
                adjacente.saida_cedo = adjacente.inicio_cedo + adjacente.duracao

            #print('Adjacentes da tarefa:')
            #for i in adjacentes:
             #   i.print()

            if len(nao_visitados) == 0:
                return

            prox_tarefa = nao_visitados.pop(0)
            

    #Retorna listaConexoes de tarefas que tem como precedente a tarefa passada por parametro
    def encontrarAdjacente(self, tarefa):
        listaTarefas = []

        for t in self.tabelaTarefas:
            if tarefa.id in t.precedentes:
                listaTarefas.append(t)

        return listaTarefas

    #Encontra o precedente de menor tempo da tarefa indicada. retorna o tempo
    def menorTempoDuracao(self, tarefa):
        menor_tempo = 1000000
        for precedente in tarefa.precedentes:
            if self.tabelaTarefas[precedente].saida_cedo < menor_tempo:
                menor_tempo = self.tabelaTarefas[precedente].saida_cedo
        
        return menor_tempo

    #Encontra o precedente de maior tempo da tarefa indicada. retorna o tempo
    def maiorTempoDuracao(self, tarefa):
        maior_tempo = 0
        for precedente in tarefa.precedentes:
            if self.tabelaTarefas[precedente].saida_cedo > maior_tempo:
                maior_tempo = self.tabelaTarefas[precedente].saida_cedo
        
        return maior_tempo

    def printarGrafo(self):
        grafo = nx.Graph()

        grafo.add_node('Init')

        for i in range(0, len(self.tabelaTarefas) - 1):
            grafo.add_node(chr(i + 65))

        grafo.add_node('Fim')


        node_options = {
            'node_size' : 600,
        }

        arrow_options = {
            'arrowstyle' : '-|>',
            'arrowsize' : 25,
            'width' : 1
            }

        listaConexoes = []
        for tarefa in self.tabelaTarefas[1:]:
            if tarefa.fim:
                coordenada = (tarefa.nome, 'Fim')
                listaConexoes.append(coordenada)
            for precedente in tarefa.precedentes:
                if precedente == 0:
                    coordenada = ('Init', tarefa.nome)
                else:
                    coordenada = (chr(precedente + 64), tarefa.nome)

                listaConexoes.append(coordenada)


        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(grafo)
        nx.draw_networkx_nodes(grafo, pos, **node_options)
        nx.draw_networkx_labels(grafo, pos)
        nx.draw_networkx_edges(grafo, pos, edgelist = listaConexoes, arrows = True, **arrow_options)
        plt.show()

    def encontraFim(self):
        listaAux = []
        listaPrecedencia =[]
        listaFim = []


        for t in self.tabelaTarefas[1:]:
            listaAux.append(t.precedentes)
            

        listaPrecedencia = list(np.concatenate((listaAux), axis=None))


        listaPrecedencia = list(dict.fromkeys(listaPrecedencia))


        for j in self.tabelaTarefas[1:]:
            if j.id not in listaPrecedencia:
                listaFim.append(j.id)
                j.fim = True

        
        return listaFim

        

def criarTarefa(nome):
    nome = nome.upper()
    print(f'Tarefa: {nome}')
    duracao = int(input('Duração da tarefa: '))
    precedentes = input('Precedentes: ').upper()
        
    precedentes = list(precedentes)
    precedentesConvertidos = []

    for i in precedentes:
        precedentesConvertidos.append(ord(i) - 64)

    if(duracao is not None):
        tarefa = Tarefa(nome, duracao, precedentesConvertidos)
        return tarefa
        
    else:
        raise ValueError('Nome ou duracao vazio')

try:
    t1 = Tarefa('A', 6, [0])
    t2 = Tarefa('B', 2, [0])
    t3 = Tarefa('C', 3, [0])
    t4 = Tarefa('D', 10, [1])
    t5 = Tarefa('E', 3, [1])
    t6 = Tarefa('F', 2, [2])
    t7 = Tarefa('G', 4, [3])
    t8 = Tarefa('H', 5, [5])
    t9 = Tarefa('I', 8, [6, 7])
    t10 = Tarefa('J', 6, [7])
    t11 = Tarefa('K', 4, [9])
    t12 = Tarefa('L', 2, [10])
    
    t = Tabela()
    t.adicionaTarefa(t1)
    t.adicionaTarefa(t2)
    t.adicionaTarefa(t3)
    t.adicionaTarefa(t4)
    t.adicionaTarefa(t5)
    t.adicionaTarefa(t6)
    t.adicionaTarefa(t7)
    t.adicionaTarefa(t8)
    t.adicionaTarefa(t9)
    t.adicionaTarefa(t10)
    t.adicionaTarefa(t11)
    t.adicionaTarefa(t12)

    t.caminhoDeIda()
    t.encontraFim()
    t.print()
    t.printarGrafo()

except ValueError as error:
    print(error)