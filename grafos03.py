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
        self.sucessor = None
    
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

        pos = nx.spring_layout(grafo)
        shift = [0.05, 0]
        shifted_pos ={node: node_pos + shift for node, node_pos in pos.items()}


        labels = {}
        for tarefa in self.tabelaTarefas[1:]:
            labels[tarefa.nome] = f'Inicio cedo: {str(tarefa.inicio_cedo)} Saida cedo: {str(tarefa.saida_cedo)}\nInicio tarde: {str(tarefa.inicio_tarde)} Saida tarde: {str(tarefa.saida_tarde)}'

        plt.figure(figsize=(10, 8), frameon=False)
        plt.axis('off')
        nx.draw_networkx_nodes(grafo, pos, **node_options)
        nx.draw_networkx_labels(grafo, pos)
        nx.draw_networkx_labels(grafo, shifted_pos, labels = labels, horizontalalignment="left", verticalalignment='top')
        nx.draw_networkx_edges(grafo, pos, edgelist = listaConexoes, arrows = True, **arrow_options)
        plt.show()

    def encontraFim(self):
        listaAux = []
        listaPrecedencia =[]
        listaFim = []
        listaTarefaFinal = []


        for t in self.tabelaTarefas[1:]:
            listaAux.append(t.precedentes)
            

        listaPrecedencia = list(np.concatenate((listaAux), axis=None))


        listaPrecedencia = list(dict.fromkeys(listaPrecedencia))


        for j in self.tabelaTarefas[1:]:
            if j.id not in listaPrecedencia:
                listaFim.append(j.id)
                #j.fim = True


        tfim = Tarefa("Fim",0,listaFim)
        tfim.fim =True
        #tfim.inicio_tarde=tfim.saida_cedo
        self.adicionaTarefa(tfim)
        
        return listaFim

    def caminhoDeVolta(self):
        tempoVoltaInicial =0 
        listaPrecedentes = []
        listaTarefa = []
        tarefaAtual = None

      #  for t in self.tabelaTarefas[1:]:
      #      for j in t.precedentes:
      #          if j.saida_cedo > tempoVoltaInicial:
      #              tempoVoltaInicial = j.saida_cedo
                
      #  for t in self.tabelaTarefas[1:]:
      #      if t.fim :
      #          t.saida_tarde = tempoVoltaInicial
       #         listaFim.append(t)

        listaTarefa = self.tabelaTarefas.copy()
        tarefaAtual = listaTarefa.pop()
        tarefaAtual.inicio_tarde = tarefaAtual.inicio_cedo

        while True:
            
            if len(listaTarefa)>0:
                listaPrecedentes = tarefaAtual.precedentes

                for p in listaPrecedentes:
                    if (self.tabelaTarefas[p].saida_tarde > tarefaAtual.inicio_tarde) or self.tabelaTarefas[p].saida_tarde == 0 :
                        self.tabelaTarefas[p].saida_tarde = tarefaAtual.inicio_tarde
#tem que dar uma olhada nessa logica aqui
                    self.tabelaTarefas[p].inicio_tarde = self.tabelaTarefas[p].saida_tarde - self.tabelaTarefas[p].duracao
                    
            else:
                return

            
            tarefaAtual = listaTarefa.pop()

            
        
    


        

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
    t.caminhoDeIda()
    t.caminhoDeVolta()
    
    t.print()
    #t.printarGrafo()

    print('\n')
    tabela = Tabela()
    tarefa01 = Tarefa('A', 10, [0])
    tarefa02 = Tarefa('B', 4, [1])
    tarefa03 = Tarefa('C', 7, [1])
    tarefa04 = Tarefa('D', 5, [3])
    tarefa05 = Tarefa('E', 5, [2, 4])
    tarefa06 = Tarefa('F', 2, [3])
    tabela.adicionaTarefa(tarefa01)
    tabela.adicionaTarefa(tarefa02)
    tabela.adicionaTarefa(tarefa03)
    tabela.adicionaTarefa(tarefa04)
    tabela.adicionaTarefa(tarefa05)
    tabela.adicionaTarefa(tarefa06)
    tabela.encontraFim()
    tabela.caminhoDeIda()
    tabela.caminhoDeVolta()
    tabela.print()

    print('\n')
    tabela02 = Tabela()
    tarefa07 = Tarefa('A', 2, [0])
    tarefa08 = Tarefa('B', 4, [1])
    tarefa09 = Tarefa('C', 10, [2])
    tarefa10 = Tarefa('D', 6, [3])
    tarefa11 = Tarefa('E', 4, [3])
    tarefa12 = Tarefa('F', 5, [5])
    tarefa13 = Tarefa('G', 7, [4])
    tarefa14 = Tarefa('H', 9, [5, 7])
    tarefa15 = Tarefa('I', 7, [3])
    tarefa16 = Tarefa('J', 8, [6, 9])
    tarefa17 = Tarefa('K', 4, [10])
    tarefa18 = Tarefa('L', 5, [10])
    tarefa19 = Tarefa('M', 2, [8])
    tarefa20 = Tarefa('N', 6, [11, 12])
    tabela02.adicionaTarefa(tarefa07)
    tabela02.adicionaTarefa(tarefa08)
    tabela02.adicionaTarefa(tarefa09)
    tabela02.adicionaTarefa(tarefa10)
    tabela02.adicionaTarefa(tarefa11)
    tabela02.adicionaTarefa(tarefa12)
    tabela02.adicionaTarefa(tarefa13)
    tabela02.adicionaTarefa(tarefa14)
    tabela02.adicionaTarefa(tarefa15)
    tabela02.adicionaTarefa(tarefa16)
    tabela02.adicionaTarefa(tarefa17)
    tabela02.adicionaTarefa(tarefa18)
    tabela02.adicionaTarefa(tarefa19)
    tabela02.adicionaTarefa(tarefa20)
    tabela02.encontraFim()
    tabela02.caminhoDeIda()
    tabela02.caminhoDeVolta()
    tabela02.print()

except ValueError as error:
    print(error)