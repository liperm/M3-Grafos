import numpy as np

class Tarefa:
    def __init__(self, nome, duracao, precedentes: list):
        self.nome = nome
        self.duracao = duracao
        self.precedentes = precedentes
        self.id = 0
    
    def print(self):
        print(f'id: {self.id} nome: {self.nome} duracao: {self.duracao} precendentes: {self.precedentes}')


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
        #Encontra o ponto inicial da análise
        for t in self.tabelaTarefas:
            if len(t.precedentes) == 0:
                tarefa =  t

        lista = self.encontrarAdjacente(tarefa)
        
        return

    #Retorna lista de tarefas que tem como precedente a tarefa passada por parametro
    def encontrarAdjacente(self, tarefa):
        listaTarefas = []

        for t in self.tabelaTarefas:
            if tarefa.id in t.precedentes:
                listaTarefas.append(t)

        return listaTarefas


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
    t4 = criarTarefa('a')
    t3 = criarTarefa('b')
    t2 = criarTarefa('c')
    t = Tabela()
    t.adicionaTarefa(t4)
    t.adicionaTarefa(t3)
    t.adicionaTarefa(t2)
    t.caminhoCritico()

except ValueError as error:
    print(error)