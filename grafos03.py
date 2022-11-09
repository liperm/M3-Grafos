import numpy as np

class Tarefa:
    def __init__(self, id, duracao, precedentes):
        self.id = id
        self.duracao = duracao
        self.precedentes = precedentes

class Tabela():
    def __init__(self, tarefas = []):
        self.tabelaTarefas = np.array(tarefas)

    def adicionaTarefa(self, tarefa):
        np.append(self.tabelaTarefas, tarefa)

def criarTarefa():
    id = input('Nome da tarefa:')
    duracao = int(input('Duração da tarefa:'))
    precedentes = input('Precedentes:')
        
    precedentes = list(precedentes)

    if(len(id) != 0 and duracao is not None):
        tarefa = Tarefa(id, duracao, precedentes)
        return tarefa
        
    else:
        raise ValueError('Id ou duracao vazio')

try:
    tarefa = criarTarefa()

    tabela = Tabela()
    tabela.adicionaTarefa(tarefa)

except ValueError as error:
    print(error)