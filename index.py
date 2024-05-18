from pathlib import Path
import os
# SIMULATED ANEALING

# abrindo o arquivo e lendo o conteúdo
ROOT_DIR = Path(__file__).parent
FILE_DIR = ROOT_DIR / 'Files'

for file in FILE_DIR.iterdir():
    if file.suffix == '.txt':
        with open(file, "r") as arquivo:
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