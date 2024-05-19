from pathlib import Path
import math
import random

'''

4 - num de programadores

8 -  num de módulos

7	7	10	8	16	16	0	17
10	5	9	9	14	4	16	11 - custo de execução de cada módulo
11	8	7	5	1	11	20	12 - para cada programador
5	7	6	8	16	7	15	17

10	14	16	12	8	20	10	16
13	12	15	13	9	18	9	18 - CH gasta por cada programador
8	8	13	8	8	17	16	14 - para cada módulo
15	17	18	15	12	15	16	18

30	25	20	40 - CH disponível por programador

'''

# salvando em variáveis o caminho dos diretórios e arquivos utilizados
ROOT_DIR = Path(__file__).parent
FILE_DIR = ROOT_DIR / 'Files'


# criação da classe utilizada para 
class SimulatedAnealing:
    def __init__(self, mitigation_factor=None, solution_quantity=None, initial_solution=None, initial_temp=None):
        self.name = None
        self.linhas = None
        self.num_prog = None
        self.num_modules = None
        self.temperature = None
        self.initial_solution = initial_solution
        self.initial_temp = initial_temp
        
        self.cost_modules = None
        self.prog_hour_cost = None
        self.mitigation_cost = mitigation_factor  # Fator de atenuação
        self.prog_hour_max_cost = None
        self.solution_quantity = solution_quantity

        self.dict_prog_modules = {}
        self.dict_prog_hours = {}

    def open_file(self):
        for file in FILE_DIR.iterdir():
            if file.suffix == '.txt':
                self.name = file.stem
                with open(file, "r") as arquivo:
                    self.linhas = arquivo.readlines()

    def create_matrix(self):
        self.num_prog = int(self.linhas[0])  # número de programadores
        self.num_modules = int(self.linhas[1])  # número de módulos
        # salvando em uma matriz o custo para realização por cada programador por módulo
        self.cost_modules = []
        for linha in self.linhas[2:self.num_prog+2]:
            self.cost_modules.append(list(map(int, linha.split())))

        # salvando em uma matriz o carga horária gasta por cada programador para realizar cada módulo
        self.prog_hour_cost = []
        for linha in self.linhas[self.num_prog+2:self.num_prog+2+self.num_prog]:
            self.prog_hour_cost.append(list(map(int, linha.split())))

        # salvando a carga horária total de cada programador
        self.prog_hour_max_cost = []
        for pHour in list(map(int, self.linhas[-1].split())):
            self.prog_hour_max_cost.append(pHour)
        
        #Criando um dicionario de listas
        for i in range(self.num_prog):
            self.dict_prog_modules[f"{i}"] = [self.cost_modules[i][j] for j in range(len(self.cost_modules[i]))]
            self.dict_prog_hours[f"{i}"] = [self.prog_hour_cost[i][j] for j in range(len(self.prog_hour_cost[i]))]

        print("Custo dos modulos programadores:")
        for i in range(len(self.dict_prog_hours)):
            print(i+1,":",self.dict_prog_modules[f"{i}"])
        
        print("Custo das horas programadores:")
        for i in range(len(self.dict_prog_hours)):
            print(i+1,":",self.dict_prog_hours[f"{i}"])

        print("Maximo de horas por programador:",self.prog_hour_max_cost)
        
    def choice_random_neighbors(self, actual_module, actual_prog): #Passando por parametro a tarefa atual e o programador que detém ela 
        random_neighbor = random.choice(self.dict_prog_modules)
        
    def reduct_temperature(self,old_temperature):
        self.temperature = self.mitigation_factor * old_temperature
    
    def acceptance_probability(self, actual_variation, actual_temperature):
        #∆E=E(i+1) − Ei=100 − 85= 15
        temperature = math.e ** (-(actual_variation/actual_temperature))
        return temperature
    
