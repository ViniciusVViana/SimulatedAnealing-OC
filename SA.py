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
    def __init__(self,name=None, mitigation_factor=None, solution_quantity=None, initial_solution=None, initial_temp=None):
        self.name = name
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

        self.workers = []
        
    def print_list_dicts(self, list_dict):
        for i in list_dict:
            print(f"item {list_dict.index(i)}:")
            for k, v in i.items():
                print(f'{k}: {v}')
                
    def find_in_vet(self, vet, value):
        for i in range(len(vet)):
            if vet[i] == value:
                return i
        return -1
    
    def regret(self):
        # Vetor para armazenar as diferenças entre a menor e segunda menor tarefa de cada coluna
        difference_vector = []
        for i in range(self.num_modules):
            modules = []
            for j in range(self.num_prog):
                tarefa = self.workers[j]["recurso_por_tarefa"][i]
                modules.append(tarefa)
            modules.sort()
            difference = modules[1] - modules[0]
            difference_vector.append({"task_id": i, "difference": difference})
        return difference_vector
            
    def calc_initial_solution(self):
        self.initial_solution = [[{
            "tasks":[],
            "worker_id":None
        }] for _ in range(self.num_prog)]  # Inicializando o número de listas
        solution_cost = 0
        # Vetor para armazenar as diferenças entre a menor e segunda menor tarefa de cada coluna
        difference_vector = sorted(self.regret(), key=lambda x: x["difference"], reverse=True)     
        print(difference_vector)
        
        for i in range(self.num_modules):
            module_id = difference_vector[i]["task_id"]
            aux = []
            aux_module = []
            penalty = 0
            
            for j in range(self.num_prog):
                aux.append(self.workers[j]["recurso_por_tarefa"][module_id])  # Deus = copilot (santissima trindade(VSCode, Copilot, ChatGPT))
                aux_module.append(aux)
                
            #Loop para verificar a linha menor
            for j in range(self.num_prog):
                if aux[j] == min(aux):
                    worker_id = j
                    break
                
            if self.workers[worker_id]["recurso_atual"] + self.workers[worker_id]["recurso_por_tarefa"][module_id] <= self.workers[worker_id]["recurso_max"]:
                self.workers[worker_id]["recurso_atual"] += self.workers[worker_id]["recurso_por_tarefa"][module_id]
                self.workers[worker_id]["tarefas"].append(module_id)
                self.initial_solution[worker_id][0]["tasks"].append(module_id)
                self.initial_solution[worker_id][0]["worker_id"] = worker_id
                solution_cost += self.workers[worker_id]["custo_por_tarefa"][module_id]
            else:
                penalty = 1
                for j in range(self.num_prog):
                    if self.workers[j]["recurso_atual"] + self.workers[j]["recurso_por_tarefa"][module_id] <= self.workers[j]["recurso_max"]:
                        self.workers[j]["recurso_atual"] += self.workers[j]["recurso_por_tarefa"][module_id]
                        self.workers[j]["tarefas"].append(module_id)
                        self.initial_solution[j][0]["tasks"].append(module_id)
                        self.initial_solution[j][0]["worker_id"] = j
                        solution_cost += self.workers[j]["custo_por_tarefa"][module_id]
                        break
            solution_cost += self.workers[j]["custo_por_tarefa"][module_id]
        
        print("Trabalhadores: ")
        self.print_list_dicts(self.workers)
        print(f"Solution cost: {solution_cost}")
        print(self.initial_solution)
        print(difference_vector)
        
        return solution_cost

        #self.print_list_dicts(self.workers)
    
        
    def procurar_vizinhos(self, solution:list):
        #Vetor para armazenar os vizinhos
        neighbors = []
        
        
        random_worker = random.randint(0, self.num_prog)
        aux_worker = self.workers[random_worker]
        self.workers.pop(random_worker)

        
        random_module = random.choice(self.workers[random_worker]["tarefas"])
        
        change_module = self.initial_solution[random_worker]["tasks"]
        print(change_module)
        
        
        
        
    
    def open_file(self):
        print("Arquivos: ")
        for file in FILE_DIR.iterdir():
            if file.suffix == '.txt':
                self.name = file.stem
                print(f"{file.stem}")
        open_file = input("Escolha o arquivo que deseja abrir: ")
        open_file += ".txt"
        with open(f'{FILE_DIR}\\{open_file}', "r") as arquivo:
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
        

        #Passar a carga horária máxima, recurso por tarefa, custo por tarefa para o dicionário
        for i in range(self.num_prog):
            dict_prog = {
                "id":i,
                "custo_por_tarefa": self.cost_modules[i],
                "recurso_por_tarefa":self.prog_hour_cost[i],
                "recurso_atual": 0,
                "recurso_max": self.prog_hour_max_cost[i],
                "tarefas":[]
            }
            self.workers.append(dict_prog)
        
        #print(self.workers)            

    def choice_random_neighbors(self, actual_module, actual_prog): #Passando por parametro a tarefa atual e o programador que detém ela 
        random_neighbor = random.choice(self.dict_prog_modules)
        
    def reduct_temperature(self,old_temperature):
        self.temperature = self.mitigation_factor * old_temperature
    
    def acceptance_probability(self, actual_variation, actual_temperature):
        #∆E=E(i+1) − Ei=100 − 85= 15
        temperature = math.e ** (-(actual_variation/actual_temperature))
        return temperature
    
    
