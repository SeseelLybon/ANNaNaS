from neuralnetwork import NeuralNetwork
import pyglet
import numpy as np
from typing import List
from species import Species
from math import floor

from meeple import Meeple

from obstacle import dino

class Population:



    def __init__(self, size):
        self.pop = np.ndarray([size], dtype=dino)
        self.species:List[Species] = []

        self.size = size
        self.generation = 0


        for i in range(self.pop.shape[0]):
            self.pop[i] = dino(4, tuple([4]), 1)
            #self.brains[i] = NeuralNetwork(4+1,tuple([5,3]),16)

        self.bestMeeple:dino = self.pop[0]

    #update all the meeps that are currently alive
    def updateAlive(self, obstacle_drawlist, score, inputs):



        for dinner in self.pop:
            dinner.brain.set_input(0, inputs[0])
            dinner.brain.set_input(1, inputs[1])
            dinner.brain.set_input(2, inputs[2])
            dinner.brain.set_input(3, inputs[3])

            dinner.brain.fire_network()

            if dinner.brain.get_output(0) > 0.8:
                dinner.jump()

            dinner.update(score)
            for obst in obstacle_drawlist:
                if dinner.isColliding( obst ):
                    dinner.isAlive = False
            dinner.draw()

        # Collision detection


    #returns bool if all the players are dead or done
    def isDone(self)-> bool:
        for dinner in self.pop:
            if dinner.isAlive:
                return False
        return True


    def naturalSelection(self):
        self.speciate() # seperate the existing population into species for the purpose of natural selection
        species_pre_cull = len(self.species)
        self.calculateFitness() # calc fitness of each meeple, currently not needed
        self.sortSpecies() #sort all the species to the average fitness, best first. In the species sort by meeple's fitness

        # Clean the species
        self.cullSpecies()
        self.setBestMeeple()
        print("Best fitness", self.bestMeeple.fitness)
        self.killStaleSpecies()
        self.killBadSpecies()


        print("Species pre/post culling", species_pre_cull, len(self.species))


        children:List[dino] = [self.bestMeeple]

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

        self.pop = np.array(children, dtype=dino)
        self.generation += 1


    def setBestMeeple(self):
        maxfit:float
        if self.bestMeeple:
            maxFit = self.bestMeeple.fitness
        else:
            maxFit = 0

        tempnewbestMeeplei = -1

        #go through all meeples in the population
        for i in range(self.pop.shape[0]):
            if self.pop[i].fitness >= maxFit:
                tempnewbestMeeplei = i
                maxFit = self.pop[i].fitness

        if self.bestMeeple:
            if self.bestMeeple.fitness < self.pop[tempnewbestMeeplei].fitness:
                self.bestMeeple = self.pop[tempnewbestMeeplei]
        else:
            self.bestMeeple = self.pop[tempnewbestMeeplei]

        self.bestMeeple.sprite.color = (0,0,0)


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
        for dinner in self.pop:
            dinner.fitness = dinner.score

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

        self.species[:] = [ x for x in self.species if x not in markedForRemoval ]


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

        self.species[:] = [ x for x in self.species if x not in markedForRemoval ]


    def cullSpecies(self):
        for specie in self.species:
            specie.cull()