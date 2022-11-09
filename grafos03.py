import numpy as np

class Tarefa:
    def __init__(self, nome, duracao, precedentes):
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

def criarTarefa():
    nome = input('Nome da tarefa: ')
    duracao = int(input('Duração da tarefa: '))
    precedentes = input('Precedentes: ')
        
    precedentes = list(precedentes)

    if(len(id) != 0 and duracao is not None):
        tarefa = Tarefa(nome, duracao, precedentes)
        return tarefa
        
    else:
        raise ValueError('Nome ou duracao vazio')

try:
    t1 = Tarefa('a', 2, [])
    t2 = Tarefa('b', 3, ['a'])
    t3 = Tarefa('c', 4, ['a','b'])
    t = Tabela()
    t.adicionaTarefa(t1)
    t.adicionaTarefa(t2)
    t.adicionaTarefa(t3)
    t.print()

except ValueError as error:
    print(error)