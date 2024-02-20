import random


class MockNeuralNet:
    def __init__(self):
        # fixed model params
        self.steps = 100
        self.areas = 6
        self.neuronsX = 25
        self.neuronsY = 25

        # the current version of the model parameters
        self.config = {
            'applySensoryInput': True,
            'applyMotorInput': True
        }

        self.current_step = 0

    # Mock neural network computation, return results to be emitted to the client
    def step(self):
        def silence(self):
            w, h = self.neuronsX, self.neuronsY
            return [[0 for x in range(w)] for y in range(h)]

        def randomActivity(self):
            neurons = range(self.neuronsX * self.neuronsY)
            sample = random.sample(neurons, random.randint(1, 100))
            matrix = []
            for i in range(self.neuronsX):
                row = []
                for j in range(self.neuronsY):
                    neuron = (i+1)*(j+1)
                    row.append(
                        0 if neuron not in sample else random.uniform(0, 1))
                matrix.append(row)
            return matrix

        self.current_step += 1

        return {
            'sensoryInput1': silence(self) if self.config.get('applySensoryInput') is False else randomActivity(self),
            'area1': randomActivity(self),
            'area2': randomActivity(self),
            'area3': randomActivity(self),
            'area4': randomActivity(self),
            'area5': randomActivity(self),
            'area6': randomActivity(self),
            'motorInput1': silence(self) if self.config.get('applyMotorInput') is False else randomActivity(self),
        }

    def update_config(self, config):
        self.config = config
