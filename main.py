from SA import SimulatedAnealing
import random

simulatedAnealing = SimulatedAnealing()
simulatedAnealing.open_file()
simulatedAnealing.create_matrix()

initial_solution = [list() * i for i in range(simulatedAnealing.num_prog)]

min_value = []
for mod in range(simulatedAnealing.num_modules):
   min_value.append(min(row[mod] for row in simulatedAnealing.prog_hour_cost))
    
second_min_value = []
for mod in range(simulatedAnealing.num_modules):
    secondi


print(min_value)