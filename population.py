from neuralnetwork import NeuralNetwork
import pyglet
import numpy
import logging
#import garbage


class Population:


    generation = 1
    bestBraini = -1

    stagnatedGenerations = 0
    prev_bestFitness = 0

    def __init__(self, size):
        self.brains = [None]*size
        self.size = size
        self.fitnessSum = 0

        for i in range(len(self.brains)):
            self.brains[i] = NeuralNetwork(4+1,4+1,16)

    def update(self):
        pass

    def selectParent(self):
        rand = numpy.random.randint(0, self.fitnessSum)
        runningSum = 0
        for i in range(len(self.brains)):
            runningSum +=  self.brains[i].fitness
            if runningSum > rand:
                return self.brains[i]

    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for i in range(len(self.brains)):
            self.fitnessSum += self.brains[i].fitness

    def naturalSelection(self):
        newBrains = [None]*self.size
        self.setBestBrain()

        # save the best brain
        newBrains[0] = self.brains[self.bestBraini].clone()

        mutatechance=1/40

        if self.brains[self.bestBraini].fitness == self.prev_bestFitness:
            self.stagnatedGenerations += 1
        else:
            self.stagnatedGenerations = 0

        self.prev_bestFitness = self.brains[self.bestBraini].fitness

        logging.debug(self.stagnatedGenerations)

        # then use select parent and fill the list of new brains with them as parents
        for i in range(1,len(newBrains)):
            newBrains[i] = self.selectParent().clone()
            newBrains[i].mutate(mutatechance)
            newBrains[i].fitness = 0

        #swap out the old brains for the new brains
        self.brains = newBrains
        self.generation += 1


    def setBestBrain(self):
        maxFit = 0
        tempbestBraini = -1
        for i in range(len(self.brains)):
            if self.brains[i].fitness >= maxFit:
                tempbestBraini = i
                maxFit = self.brains[i].fitness
        self.bestBraini = tempbestBraini

