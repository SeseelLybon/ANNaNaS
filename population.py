from neuralnetwork import NeuralNetwork
import pyglet
import numpy
#import garbage


class Population:


    generation = 1
    bestBraini = -1

    def __init__(self, size):
        self.brains = [None]*size
        self.size = size
        self.fitnessSum = 0

        for i in range(len(self.brains)):
            self.brains[i] = NeuralNetwork(4,4,2)

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

        # then use select parent and fill the list of new brains with them as parents
        for i in range(1,len(newBrains)):
            newBrains[i] = self.selectParent().clone()
            newBrains[i].mutate()
            newBrains[i].fitness = 0

        #swap out the old brains for the new brains
        self.brains = newBrains
        self.generation += 1


    def setBestBrain(self):
        maxFit = 0
        tempbestBraini = -1
        for i in range(len(self.brains)):
            if self.brains[i].fitness > maxFit:
                tempbestBraini = i
                maxFit = self.brains[i].fitness
        self.bestBraini = tempbestBraini

