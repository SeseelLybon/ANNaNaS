from neuralnetwork import NeuralNetwork
import pyglet
import numpy as np
from typing import List
from species import Species
from math import floor

from meeple import Meeple


class Population:



    def __init__(self, size):
        self.pop = np.ndarray([size], dtype=Meeple)
        self.species:List[Species] = []

        self.size = size
        self.generation = 0

        self.bestMeeple:Meeple = None

        for i in range(self.pop.shape[0]):
            self.pop[i] = Meeple(4, tuple([0]), 16)
            #self.brains[i] = NeuralNetwork(4+1,tuple([5,3]),16)

    #update all the meeps that are currently alive
    def updateAlive(self):
        # faketodo: Not needed right now
        pass


    #returns bool if all the players are dead or done
    def isDone(self)-> bool:
        # faketodo: Not needed right now
        return True


    def naturalSelection(self):
        self.speciate() # seperate the existing population into species for the purpose of natural selection
        #self.calculateFitness() # calc fitness of each meeple, currently not needed
        self.sortSpecies() #sort all the species to the average fitness, best first. In the species sort by meeple's fitness

        # Clean the species
        self.cullSpecies()
        self.setBestMeeple()
        self.killStaleSpecies()
        self.killBadSpecies()


        children:List[Meeple] = []

        for specie in self.species:
            #add the best meeple of a specie to the new generation list
            children.append(specie.bestMeeple)

            #generate number of children based on how well the species is soing compared to the rest; the better the bigger.
            newChildrenAmount = floor((specie.averageFitness/self.getAverageFitnessSum()) *self.pop.size) -1

            for i in range(newChildrenAmount):
                children.append(specie.generateChild())

        # If the pop-cap hasn't been filled yet, keep getting children from the best specie till it is filled
        while len(children) < self.size:
            children.append(self.species[0].generateChild())

        self.pop = np.array(children, dtype=Meeple)
        self.generation += 1


    def setBestMeeple(self):
        maxFit = 0
        tempbestMeeplei = -1
        #go through all meeples in the population
        for i in range(self.pop.shape[0]):
            if self.pop[i].fitness >= maxFit:
                tempbestMeeplei = i
                maxFit = self.pop[i].fitness
        self.bestMeeple = self.pop[tempbestMeeplei]


    def speciate(self):

        #clear all exising species
        #champion is saved, so they're not useless
        for specie in self.species:
            self.species:List[Species] = []

        for meep in self.pop:
            speciesfound = False
            for specie in self.species:
                if specie.checkSameSpecies(meep):
                    specie.addToSpecies(meep)
                    speciesfound = True
                    break
            if not speciesfound:
                self.species.append(Species(meep=meep))


    def calculateFitness(self):
        # faketodo: Not needed right now
        pass

    #get the sum of averages from each specie
    def getAverageFitnessSum(self)->float:
        tempsum = 0
        for specie in self.species:
            tempsum+= specie.averageFitness
        return tempsum

    #sort the species by fitness of their champion
    def sortSpecies(self):
        for specie in self.species:
            specie.sortSpecie()

        self.species.sort(key=lambda specie: specie.bestMeeple.fitness)


    def killStaleSpecies(self):

        markedForRemoval = list()

        for specie in self.species:
            if specie.staleness >= 15:
                markedForRemoval.append(specie)

        for mark in markedForRemoval:
            self.species.remove(mark)


    def killBadSpecies(self):

        averageSum = 0
        for specie in self.species:
            specie.generateAverage()
            averageSum += specie.averageFitness

        markedForRemoval = list()

        for specie in self.species:
            # this calculates how many children a specie is allowed to produce in Population.naturalSelection()
            # If this is less then one, the specie did so bad, it won't generate a child then. So it basically just died here.
            if specie.averageFitness/averageSum * len(self.pop) < 1:
                markedForRemoval.append(specie)

        for mark in markedForRemoval:
            self.species.remove(mark)


    def cullSpecies(self):
        for specie in self.species:
            specie.cull()