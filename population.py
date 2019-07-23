import numpy as np
import logging
#import garbage
from dart_player import Dart_Player

class Population:


    generation = 1
    bestPlayeri = -1
    bestScore = 0


    def __init__(self, size:int):
        self.players = np.ndarray([size], Dart_Player)
        self.size = size
        self.fitnessSum = 0
        self.leastAttempts = float("inf")

        for i in range(self.players.size):
            self.players[i] = Dart_Player()

    def update(self):
        for i in range(self.players.shape[0]):
            if self.players[i].brain.attempt > self.leastAttempts:
                self.players[i].isDead = True
            elif self.players[i].isDone or self.players[i].isDead:
                continue
            else:
                self.players[i].throw()

    def selectParent(self):
        self.fitnessSum = max(self.fitnessSum, 1)
        rand = np.random.randint(0, self.fitnessSum)
        runningSum = 0
        for i in range(self.players.size):
            runningSum +=  self.players[i].fitness
            if runningSum > rand:
                return self.players[i]

    def calculateFitness(self):
        for i in range(self.players.size):
            self.players[i].calcFitness()

    def calculateFitnessSum(self):

        self.fitnessSum = 0
        for i in range(self.players.shape[0]):
            self.fitnessSum += self.players[i].fitness

    def naturalSelection(self):
        self.setBestBrain()
        self.calculateFitnessSum()
        newPlayers = np.ndarray([self.size], Dart_Player)

        # save the best player
        newPlayers[0] = self.players[self.bestPlayeri].reproduce()


        # then use select parent and fill the list of new brains with them as parents
        for i in range(1,newPlayers.size):
            newPlayers[i] = self.selectParent().reproduce()
            newPlayers[i].mutate()

        #swap out the old brains for the new brains
        self.players = newPlayers
        self.generation += 1


    def setBestBrain(self):
        maxFit = 0
        tempbestPlayeri = 0
        for i in range(self.players.shape[0]):
            if self.players[i].fitness > maxFit:
                tempbestPlayeri = i
                maxFit = self.players[i].fitness

        self.bestPlayeri = tempbestPlayeri
        self.bestScore = self.players[self.bestPlayeri].score

        if self.players[self.bestPlayeri].isDone:
            self.leastAttempts = self.players[self.bestPlayeri].brain.attempt

    def allPlayersDone(self)->bool:
        for i in range(self.players.shape[0]):
            if not self.players[i].isDead and not self.players[i].isDone:
                return False

        return True

