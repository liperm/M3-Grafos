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
        self.folga = 0
    
    def print(self):
        print(f'id: {self.id} nome: {self.nome} duracao: {self.duracao} precendentes: {self.precedentes} inicio_cedo: {self.inicio_cedo} inicio_tarde: {self.inicio_tarde} saida_cedo: {self.saida_cedo} saida_tarde: {self.saida_tarde} Folga: {self.folga} Fim: {self.fim}' )


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
            adjacentes = self.encontrarAdjacente(tarefa)

            #adiciona os valores de chagada e saída de cada tarefa
            for adjacente in adjacentes:
                adjacente.inicio_cedo = self.maiorTempoDuracao(adjacente)
                adjacente.saida_cedo = adjacente.inicio_cedo + adjacente.duracao

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

        for i in range(0, len(self.tabelaTarefas) - 2):
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

        arrow_options_colored = {
            'arrowstyle' : '-|>',
            'arrowsize' : 25,
            'width' : 1,
            'edge_color' : 'red'
            }

        listaConexoes = []
        listaConexoesCriticas = []
        for tarefa in self.tabelaTarefas[1:]:
            for precedente in tarefa.precedentes:
                if precedente == 0:
                    coordenada = ('Init', tarefa.nome)
                else:
                    coordenada = (chr(precedente + 64), tarefa.nome)
                if(tarefa.folga == 0 and self.tabelaTarefas[precedente].folga == 0):
                    listaConexoesCriticas.append(coordenada)
                elif(tarefa.nome == 'Fim' and self.tabelaTarefas[precedente].folga == 0):
                    listaConexoesCriticas.append(coordenada)
                else:
                    listaConexoes.append(coordenada)

        pos = nx.spring_layout(grafo)
        shift = [0.05, 0]
        shifted_pos ={node: node_pos + shift for node, node_pos in pos.items()}


        labels = {}
        for tarefa in self.tabelaTarefas[1:]:
            labels[tarefa.nome] = f'Duracao: {str(tarefa.duracao)}\nIC: {str(tarefa.inicio_cedo)}\nSC: {str(tarefa.saida_cedo)}\nIT: {str(tarefa.inicio_tarde)}\nST: {str(tarefa.saida_tarde)}\nFolga: {str(tarefa.folga)}'

        plt.figure(figsize=(10, 8), frameon=False)
        plt.axis('off')
        nx.draw_networkx_nodes(grafo, pos, **node_options)
        nx.draw_networkx_labels(grafo, pos)
        nx.draw_networkx_labels(grafo, shifted_pos, labels = labels, horizontalalignment="left", verticalalignment='top')
        nx.draw_networkx_edges(grafo, pos, edgelist = listaConexoes, arrows = True, **arrow_options)
        nx.draw_networkx_edges(grafo, pos, edgelist = listaConexoesCriticas, arrows = True, **arrow_options_colored)
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
        listaPrecedentes = []
        listaTarefa = []
        tarefaAtual = None

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

    def calcularFolga(self):
        for tarefa in self.tabelaTarefas:
            tarefa.folga = tarefa.saida_tarde - tarefa.saida_cedo
        return
        

def criarTarefa(nome):
    nome = nome.upper()
    print(f'Tarefa: {nome}')
    duracao = int(input('  Duração da tarefa: '))
    precedentes = input('  Precedentes: ').upper()
        
    precedentes = list(precedentes)
    precedentesConvertidos = []

    if len(precedentes) == 0:
        precedentesConvertidos.append(0)
    
    else:
        for i in precedentes:
            precedentesConvertidos.append(ord(i) - 64)

    if(duracao is not None):
        tarefa = Tarefa(nome, duracao, precedentesConvertidos)
        return tarefa
        
    else:
        raise ValueError('Nome ou duracao vazio')

def criarTabela():
    continua = True
    acao = ''
    nome = 'A'
    tabela = Tabela()

    while continua:
        tarefa = criarTarefa(nome)
        tabela.adicionaTarefa(tarefa)
        acao = input('Adicionar mais tarefas? [s/n]').upper()
        
        if acao != 'S':
            return tabela
        
        nome = chr(ord(nome) + 1)

def main():
    acao = '0'
    tabelaCriada = False

    while acao != '4':
        if not tabelaCriada:
            acao = input('1- Criar tabela de tarefas\n2- Sair\n')
            print('\n')
            match acao:
                case '1':
                    tabela = criarTabela()
                    tabela.encontraFim()
                    tabelaCriada = True
                
                case _ :
                    return
        else:
            acao = input('1- Calcular Caminho Critico\n2- Mostrar grafo\n3- Sair\n')
            print('\n')
            match acao:
                case '1':
                    tabela.caminhoDeIda()
                    tabela.caminhoDeVolta()
                    tabela.calcularFolga()
                    tabela.print()
                
                case '2':
                    tabela.printarGrafo()

                case _ :
                    return

        print('\n')

if __name__ == '__main__':
    main()
    print(':)')