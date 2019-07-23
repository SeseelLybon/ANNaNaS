import numpy as np

class Dart_Player:

    def __init__(self):
        self.score:int = 701 # the max
        self.isDone:bool = False # if score == 0
        self.isDead:bool = False # if brain.steps == 0
        self.brain:Brain = Brain(15)
        self.fitness = 0
        self.isBest:bool = False

    def throw(self):
        if not self.isDone and not self.isDead:
            if self.brain.actions.shape[0] > self.brain.attempt:
                hit = self.brain.actions[self.brain.attempt,:]
                self.setScore( hit[0] * hit[1] )
                self.brain.attempt += 1
            else:
                #ran out of attempts
                self.isDead = True
            self.checkifDone()

    def calcFitness(self):
        if self.isDone:
            self.fitness = 10000/(self.brain.attempt**2)
        else:
            self.fitness = 1/self.score


    def checkifDone(self):
        if self.score == 0:
            self.isDone = True
        else:
            return

    def setScore(self, x):
        if self.score-x >= 0:
            self.score-=x
        elif self.score-x < 0:
            return

    def reproduce(self):
        clone:Dart_Player = Dart_Player()
        clone.brain = self.brain.clone()
        return clone

    def mutate(self):
        self.brain.mutate()


class Brain:
    def __init__(self, size:int):
        self.attempt = 0
        self.actions = np.ndarray([size, 2], dtype=int)
        for throwi in range(self.actions.shape[0]):
            self.actions[throwi, 0] = np.random.randint(1, 21)
            self.actions[throwi, 1] = np.random.randint(1, 4)

    def clone(self):
        clone:Brain = Brain(self.actions.shape[0])
        for throwi in range(self.actions.shape[0]):
            clone.actions[throwi, 0] = self.actions[throwi, 0]
            clone.actions[throwi, 1] = self.actions[throwi, 1]
        return clone

    def mutate(self):
        mutationChance = 1/15
        for throwi in range(self.actions.shape[0]):
            if np.random.rand() <= mutationChance:
                self.actions[throwi, 0] = np.random.randint(1, 21)
            if np.random.rand() <= mutationChance:
                self.actions[throwi, 1] = np.random.randint(1, 4)