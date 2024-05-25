import random


def randomActivity():
    neurons = range(25 * 25)
    sample = random.sample(neurons, random.randint(1, 100))
    matrix = []
    for i in range(25):
        row = []
        for j in range(25):
            neuron = (i+1)*(j+1)
            row.append(
                0 if neuron not in sample else random.uniform(0, 1))
        matrix.append(row)
    return matrix
