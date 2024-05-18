# SIMULATED ANEALING

# abrindo o arquivo e lendo o conteúdo
with open("./Problema de Designação Generalizada/PDG1.txt", "r") as arquivo:
        linhas = arquivo.readlines()
# salvando o número de programadores e de módulos em variáveis
num_prog = int(linhas[0]) # número de programadores
num_mod = int(linhas[1]) # número de módulos

# salvando em uma matriz o custo para realização por cada programador por módulo
cost_mod = []
for linha in linhas[2:6]:
    cost_mod.append(list(map(int, linha.split())))

# salvando em uma matriz o carga horária gasta por cada programador para realizar cada módulo
per_h_prog = []
for linha in linhas[6:10]:
    per_h_prog.append(list(map(int, linha.split())))

# salvando a carga horária total de cada programador
h_prog = []
for pHour in list(map(int, linhas[10].split())):
    h_prog.append(pHour)

# printando para testar se os valores foram salcos corretamente
print(num_prog)
print(num_mod)
print(cost_mod)
print(per_h_prog)
print(h_prog)