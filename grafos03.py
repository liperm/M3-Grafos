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

    def caminhoCritico(self):
        nao_visitados = self.tabelaTarefas.copy()

        #Encontra o ponto inicial da análise
        for t in self.tabelaTarefas:
            if len(t.precedentes) == 0:
                prox_tarefa =  t
        
        del(nao_visitados[prox_tarefa.id])

        while True:
            tarefa = prox_tarefa
            print('Tarefa:')
            tarefa.print()
            adjacentes = self.encontrarAdjacente(tarefa)

            #adiciona os valores de chagada e saída de cada tarefa
            for adjacente in adjacentes:
                adjacente.chegada_minima = self.menorTempoDuracao(adjacente)
                adjacente.saida_minima = adjacente.chegada_minima + adjacente.duracao

            print('Adjacentes da tarefa:')
            for i in adjacentes:
                i.print()

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
    t4 = Tarefa('A', 4, [])
    t3 = Tarefa('B', 3, [0])
    t2 = Tarefa('C', 4, [0, 1])
    t = Tabela()
    t.adicionaTarefa(t4)
    t.adicionaTarefa(t3)
    t.adicionaTarefa(t2)
    t.print()
    t.caminhoCritico()

except ValueError as error:
    print(error)