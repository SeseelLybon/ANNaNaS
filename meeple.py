
import numpy as np
import math
from neuralnetwork import NeuralNetwork

class Meeple:
    def __init__(self,input_size:int, hidden_size:tuple, output_size:int,):
        self.fitness = float("-inf")
        self.brain:NeuralNetwork = NeuralNetwork(NeuralNetwork(input_size,hidden_size,output_size))
        self.isAlive = True





if __name__ == "__main__":
    meeple1 = Meeple()
    print(meeple1.fitness)