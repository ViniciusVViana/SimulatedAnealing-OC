from SA import SimulatedAnealing
import random

simulatedAnealing = SimulatedAnealing()
simulatedAnealing.open_file()
simulatedAnealing.create_matrix()

initial_solution = [list() * i for i in range(simulatedAnealing.num_prog)]

min_value = []
for mod in range(simulatedAnealing.num_modules):
     min_value.append(min(row[mod] for row in simulatedAnealing.prog_hour_cost))

print(min_value)

""" second_min_value = []
aux = simulatedAnealing.prog_hour_cost
for mod in range(simulatedAnealing.num_modules):
    while True:                                      SOU UM INCOMPETENTE!!!!
        value = min(row[mod] for row in aux)
        if(value == min_value[mod]): 

print(value) """