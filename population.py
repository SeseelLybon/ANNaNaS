from neuralnetwork import NeuralNetwork
import pyglet
import numpy as np
import logging
#import garbage
from dart_player import Dart_Player

class Population:


    generation = 1
    bestPlayeri = -1

    stagnatedGenerations = 0
    prev_bestFitness = 0

    def __init__(self, size, x, y, z):
        self.players = np.ndarray([size], Dart_Player)
        self.size = size
        self.fitnessSum = 0

        for i in range(self.players.size):
            self.players[i] = Dart_Player(NeuralNetwork(1+1, 30+1, 60))

    def update(self):
        for i in range(self.players.size):
            self.players[i].update()

    def selectParent(self):
        rand = np.random.randint(0, self.fitnessSum)
        runningSum = 0
        for i in range(self.players.size):
            runningSum +=  self.players[i].fitness
            if runningSum > rand:
                return self.players[i]

    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for i in range(len(self.players)):
            self.fitnessSum += self.players[i].fitness

    def naturalSelection(self):
        newPlayers = np.ndarray([self.size], Dart_Player)
        self.setBestBrain()

        # save the best brain
        newPlayers[0] = self.players[self.bestPlayeri].clone()

        mutatechance=1/40

        if self.players[self.bestPlayeri].fitness == self.prev_bestFitness:
            self.stagnatedGenerations += 1
        else:
            self.stagnatedGenerations = 0

        self.prev_bestFitness = self.players[self.bestPlayeri].fitness

        #logging.debug(self.stagnatedGenerations)

        # then use select parent and fill the list of new brains with them as parents
        for i in range(1,newPlayers.size):
            newPlayers[i] = self.selectParent().clone()
            newPlayers[i].mutate(mutatechance)
            newPlayers[i].fitness = 0

        #swap out the old brains for the new brains
        self.players = newPlayers
        self.generation += 1


    def setBestBrain(self):
        maxFit = 0
        tempbestPlayeri = -1
        for i in range(self.players.size):
            if self.players[i].fitness >= maxFit:
                tempbestPlayeri = i
                maxFit = self.players[i].fitness
        self.bestPlayeri = tempbestPlayeri

