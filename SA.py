from pathlib import Path
import math
import random
import matplotlib.pyplot as plt


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
    def __init__(self,name=None, mitigation_factor=0.99, solution_quantity=None, initial_solution=None, initial_temp = None, penalty=3):
        self.name = name
        self.linhas = None
        self.num_prog = None
        self.num_modules = None
        self.temperature = initial_temp
        self.solution = initial_solution 
        self.penalty = penalty
        self.mitigation_factor = mitigation_factor
        
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
        
    
    def open_file(self):
        print("Arquivos: ")
        for file in FILE_DIR.iterdir():
            if file.suffix == '.txt':
                print(f"{file.stem}")
        open_file = input("Escolha o arquivo que deseja abrir: ")
        self.name = open_file.upper()
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
        
        self.print_list_dicts(self.workers) 
        self.solution = [{
            "tasks":[],
            "worker_id":None
        } for _ in range(self.num_prog)]  # Inicializando o número de listas
        solution_cost = 0
        # Vetor para armazenar as diferenças entre a menor e segunda menor tarefa de cada coluna
        difference_vector = sorted(self.regret(), key=lambda x: x["difference"], reverse=True)     
        #print(difference_vector)
        
        for i in range(self.num_modules):
            module_id = difference_vector[i]["task_id"]
            aux = []
            aux_module = []
            
            for j in range(self.num_prog):
                aux.append(self.workers[j]["recurso_por_tarefa"][module_id]) 
                aux_module.append(aux)
                
            #Loop para verificar a linha menor
            for j in range(self.num_prog):
                if aux[j] == min(aux):
                    worker_id = j
                    break
            #Caso o recurso com essa tarefa for ficar maior que o recurso maximo, repassar a tarefa para o proximo programador
            if self.workers[worker_id]["recurso_atual"] + self.workers[worker_id]["recurso_por_tarefa"][module_id] <= self.workers[worker_id]["recurso_max"]:
                self.workers[worker_id]["recurso_atual"] += self.workers[worker_id]["recurso_por_tarefa"][module_id]
                self.workers[worker_id]["tarefas"].append(module_id)
                self.solution[worker_id]["tasks"].append(module_id)
                self.solution[worker_id]["worker_id"] = worker_id
                solution_cost += self.workers[worker_id]["custo_por_tarefa"][module_id]
            else:
                for j in range(self.num_prog):
                    if self.workers[j]["recurso_atual"] + self.workers[j]["recurso_por_tarefa"][module_id] <= self.workers[j]["recurso_max"]:
                        self.workers[j]["recurso_atual"] += self.workers[j]["recurso_por_tarefa"][module_id]
                        self.workers[j]["tarefas"].append(module_id)
                        self.solution[j]["tasks"].append(module_id)
                        self.solution[j]["worker_id"] = j
                        solution_cost += self.workers[j]["custo_por_tarefa"][module_id]
                        break
           
            

        #self.print_list_dicts(self.workers)
        #print(f"Solution cost: {solution_cost}") 

        
        return solution_cost

        #self.print_list_dicts(self.workers)
    
        
    def search_neighbors(self):
        neighbors = []
        new_cost = 0
        
        #Calcular numero de vizinhos
        neighbors_quantity = math.ceil(self.num_modules * self.num_prog * 0.15) #15% do total de vizinhos
        
        for i in range(neighbors_quantity):
            #Trabalhador que irá ceder a tarefa
            worker_send_id = random.randint(0, self.num_prog - 1)
            
            while(len(self.solution[worker_send_id]["tasks"]) == 0):
                worker_send_id = random.randint(0, self.num_prog - 1)
                
            task_id = random.randint(0, len(self.solution[worker_send_id]["tasks"]) - 1)
            #Salvar essa tarefa em uma variavel auxiliar
            switch_task = self.solution[worker_send_id]["tasks"][task_id]
            #Remover a tarefa do trabalhador
            self.solution[worker_send_id]["tasks"].pop(task_id)
            #Trabalhador que irá receber a tarefa
            worker_receive_id = random.randint(0, self.num_prog - 1)
            #Caso o trabalhador que irá receber a tarefa seja o mesmo que irá ceder, escolher outro trabalhador 
            while worker_receive_id == worker_send_id:
                worker_receive_id = random.randint(0, self.num_prog - 1)
                
            self.solution[worker_receive_id]["tasks"].append(switch_task)
            
            #Aplicando penalidade da solução atual, a penalidade sera aplicada no programador  que exceder o tempo maximo
            if(self.workers[worker_receive_id]["recurso_atual"] > self.workers[worker_receive_id]["recurso_max"]):
                #o recurso do programador atual recebe o excedente vezes a penalidade
                self.workers[worker_receive_id]["recurso_atual"] += (self.workers[worker_receive_id]["recurso_atual"] - self.workers[worker_receive_id]["recurso_max"]) * self.penalty
                
                    
            #calcular o novo custo
            for i in range(self.num_prog):
                for j in self.solution[i]["tasks"]:
                    if(self.workers[worker_receive_id]["recurso_atual"] > self.workers[worker_receive_id]["recurso_max"]):
                        new_cost += self.workers[i]["custo_por_tarefa"][j] + (self.workers[worker_receive_id]["recurso_atual"] - self.workers[worker_receive_id]["recurso_max"]) * self.penalty
                    else:
                        new_cost += self.workers[i]["custo_por_tarefa"][j]
                    
            
            neighbors.append({
                "solution": self.solution,
                "cost": new_cost
            })
        return neighbors
            

    def simulated_annealing(self):
        actual_cost = self.calc_initial_solution()
        
        
        print("Custo inicial: " + str(actual_cost))
        if self.temperature is None:
            #Calculo da temperatura inicial se baseia em procurar num_prog -1 vizinhos e calcualr uma media entre as soluções após as trocas
            soma = 0
            for i in range(self.num_prog - 1):
                neighbors = self.search_neighbors()
                #print("Vizinho: " + str(i+1))
               # print(neighbors)
                soma += neighbors[0]["cost"]
            
        #Inicializar a solução atual
        actual_solution = self.solution
        best_soluction = {
            "solution": actual_solution,
            "cost": actual_cost
        }
        #Inicializar o custo da solução atual
        print("Solução inicial: ")
        print(actual_solution)
        
        self.temperature = soma / (self.num_prog - 1)
        all_solutions_vector = [{
            "iteration": 0,
            "cost": actual_cost
        }]

        best_solutions_vector = [
            {
                "iteration": 0,
                "cost": actual_cost
            }
        ]
        temperature_vector = [{
            "iteration": 0,
            "temperature": self.temperature
        
        }]
        
        print("Temperatura inicial: " + str(self.temperature))
        cont = 0
        
        #Enquanto a temperatura for maior que 1
        while self.temperature > 1:
            cont += 1
            #Vizinhos
            neighbors = self.search_neighbors()
            #Escolher um vizinho aleatório
            random_neighbor = random.choice(neighbors)
            #Calcular a variação do custo
            actual_variation = random_neighbor["cost"] - actual_cost
            #salvar todas as soluções
           
            #Se a variação for menor que 0, a solução é aceita
            if actual_variation < 0:
                actual_cost = random_neighbor["cost"]
                actual_solution = random_neighbor["solution"]
                if actual_cost < best_soluction["cost"]:
                    best_soluction["cost"] = actual_cost
                    best_soluction["solution"] = actual_solution
                    
                    best_solutions_vector.append({
                        "iteration": cont,
                        "cost": actual_cost
                    })

                
                
              
            else:
                #Se a variação for maior que 0, a solução é aceita com uma probabilidade
                probability = self.acceptance_probability(actual_variation, self.temperature)
                if random.random() < probability:
                    actual_cost = random_neighbor["cost"]
                    actual_solution = random_neighbor["solution"]
                    
            if best_solutions_vector[cont-1]["iteration"] != cont:
                best_solutions_vector.append({
                    "iteration": cont,
                    "cost": best_soluction["cost"]
                })
            if all_solutions_vector[cont-1]["iteration"] != cont:
                all_solutions_vector.append({
                    "iteration": cont,
                    "cost": actual_cost
                })


            temperature_vector.append({
                "iteration": cont,
                "temperature": self.temperature
            })
            #Reduzir a temperatura
            self.reduct_temperature(self.temperature)
            
        
        print("Solução final: ")
        print(best_soluction["solution"])
        print("Custo final: ",best_soluction["cost"])
        self.plot2d(temperature_vector, all_solutions_vector, best_solutions_vector)
        
        
        
        
        
        
    def reduct_temperature(self,old_temperature):
        self.temperature = self.mitigation_factor * old_temperature
    
    def acceptance_probability(self, actual_variation, actual_temperature):
        #∆E=E(i+1) − Ei=100 − 85= 15
        temperature = math.e ** (-(actual_variation/actual_temperature))
        return temperature
    
    def plot2d(self, vet_temp, vet_cost, vet_best_cost):
        # Preparar os dados
        x1 = [item['iteration'] for item in vet_best_cost]
        y1 = [item['cost'] for item in vet_best_cost]

        x2 = [item['iteration'] for item in vet_cost]
        y2 = [item['cost'] for item in vet_cost]

        x3 = [item['iteration'] for item in vet_temp]
        y3 = [item['temperature'] for item in vet_temp]

        # Plotar os dados
        plt.plot(x1, y1, label='Melhor Solução')
        plt.plot(x2, y2, label='Todas as Soluções')
        plt.plot(x3, y3, label='Temperatura')

        # Configurar o gráfico
        plt.xlabel('Iteração')
        plt.ylabel('Valor')
        plt.title(f'{self.name} - Simulated Anealing')
        plt.legend()

        # Mostrar o gráfico
        plt.show()
        
    
    
