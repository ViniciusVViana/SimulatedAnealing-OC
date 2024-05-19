from SA import SimulatedAnealing
import random

simulatedAnealing = SimulatedAnealing()
simulatedAnealing.open_file()
simulatedAnealing.create_matrix()

initial_solution = [list() * i for i in range(simulatedAnealing.num_prog)]

min_value = []
second_min_value = []
trans = [list(i) for i in zip(*simulatedAnealing.prog_hour_cost)]
for row in trans:
    min_value.append(row.pop(row.index(min(row))))
    for i in row:
        if(i == min_value[-1]):
            row.pop(row.index(i))
    second_min_value.append(row.pop(row.index(min(row))))
diff = []
for i in range(len(min_value)):
    diff.append(second_min_value[i] - min_value[i])

print(min_value)
print(second_min_value)
print(diff)
print(initial_solution)