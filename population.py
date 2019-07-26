from neuralnetwork import NeuralNetwork
import pyglet
import numpy as np
import logging
#import garbage


class Population:


    generation = 1
    bestBraini = -1

    stagnatedGenerations = 0
    prev_bestFitness = 0

    def __init__(self, size):
        self.brains = np.ndarray([size], dtype=NeuralNetwork)
        self.size = size
        self.fitnessSum = 0

        for i in range(self.brains.shape[0]):
            self.brains[i] = NeuralNetwork(4,tuple([0]),16)
            #self.brains[i] = NeuralNetwork(4+1,tuple([5,3]),16)

    def update(self):
        pass

    def selectParent(self)->NeuralNetwork:
        rand = np.random.randint(0, self.fitnessSum)
        runningSum = 0
        for i in range(self.brains.shape[0]):
            runningSum +=  self.brains[i].fitness
            if runningSum > rand:
                return self.brains[i]

    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for i in range(self.brains.shape[0]):
            self.fitnessSum += self.brains[i].fitness

    def naturalSelection(self):
        newBrains = np.ndarray([self.size], dtype=NeuralNetwork)
        self.setBestBrain()

        # save the best brain
        newBrains[0] = self.brains[self.bestBraini].clone()

        mutatechance=1/30

        if self.brains[self.bestBraini].fitness == self.prev_bestFitness:
            self.stagnatedGenerations += 1
        else:
            self.stagnatedGenerations = 0

        self.prev_bestFitness = self.brains[self.bestBraini].fitness

        print(self.stagnatedGenerations)

        # then use select parent and fill the list of new brains with them as parents
        for i in range(1,newBrains.shape[0]):
            #newBrains[i] = self.selectParent().clone()

            if np.random.rand() < 0.25:
                child = self.selectParent().clone()
            else:

                parent1:NeuralNetwork = self.selectParent()
                parent2:NeuralNetwork = self.selectParent()

                if parent1.fitness > parent2.fitness:
                    child:NeuralNetwork = parent1.crossover(parent2)
                else:
                    child:NeuralNetwork = parent2.crossover(parent1)

            newBrains[i] = child

            newBrains[i].mutate(mutatechance)
            newBrains[i].fitness = 0

        #swap out the old brains for the new brains
        self.brains = newBrains
        self.generation += 1


    def setBestBrain(self):
        maxFit = 0
        tempbestBraini = -1
        for i in range(self.brains.shape[0]):
            if self.brains[i].fitness >= maxFit:
                tempbestBraini = i
                maxFit = self.brains[i].fitness
        self.bestBraini = tempbestBraini

