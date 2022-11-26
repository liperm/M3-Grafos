class Tarefa:
    def __init__(self, nome, duracao, precedentes: list):
        self.nome = nome
        self.duracao = duracao
        self.precedentes = precedentes
        self.id = 0
        self.chegada_minima = 0
        self.chegada_maxima = 0
        self.saida_minima = duracao
        self.saida_maxima = 0
    
    def print(self):
        print(f'id: {self.id} nome: {self.nome} duracao: {self.duracao} precendentes: {self.precedentes} chegada_minima: {self.chegada_minima} chegada_maxima: {self.chegada_maxima} saida_minima: {self.saida_minima} saida_maxima: {self.saida_maxima}')


class Tabela():
    def __init__(self):
        self.tabelaTarefas = []
        self.id = 0

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
                adjacente.chegada_minima = self.maiorTempoDuracao(adjacente)
                adjacente.saida_minima = adjacente.chegada_minima + adjacente.duracao

            #print('Adjacentes da tarefa:')
            #for i in adjacentes:
             #   i.print()

            if len(nao_visitados) == 0:
                return

            prox_tarefa = nao_visitados.pop(0)
            

    #Retorna lista de tarefas que tem como precedente a tarefa passada por parametro
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
            if self.tabelaTarefas[precedente].saida_minima < menor_tempo:
                menor_tempo = self.tabelaTarefas[precedente].saida_minima
        
        return menor_tempo

    #Encontra o precedente de maior tempo da tarefa indicada. retorna o tempo
    def maiorTempoDuracao(self, tarefa):
        maior_tempo = 0
        for precedente in tarefa.precedentes:
            if self.tabelaTarefas[precedente].saida_minima > maior_tempo:
                maior_tempo = self.tabelaTarefas[precedente].saida_minima
        
        return maior_tempo

def criarTarefa(nome):
    nome = nome.upper()
    print(f'Tarefa: {nome}')
    duracao = int(input('Duração da tarefa: '))
    precedentes = input('Precedentes: ').upper()
        
    precedentes = list(precedentes)
    precedentesConvertidos = []

    for i in precedentes:
        precedentesConvertidos.append(ord(i) - 65)

    if(duracao is not None):
        tarefa = Tarefa(nome, duracao, precedentesConvertidos)
        return tarefa
        
    else:
        raise ValueError('Nome ou duracao vazio')

try:
    t0 = Tarefa('A', 0, [])
    t1 = Tarefa('B', 6, [0])
    t2 = Tarefa('C', 2, [0])
    t3 = Tarefa('D', 3, [0])
    t4 = Tarefa('E', 10, [1])
    t5 = Tarefa('F', 3, [1])
    t6 = Tarefa('G', 2, [2])
    t7 = Tarefa('H', 4, [3])
    t8 = Tarefa('I', 5, [5])
    t9 = Tarefa('J', 8, [6, 7])
    t10 = Tarefa('K', 6, [7])
    t11 = Tarefa('L', 4, [9])
    t12 = Tarefa('M', 2, [10])
    
    t = Tabela()
    t.adicionaTarefa(t0)
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
    t.print()

except ValueError as error:
    print(error)