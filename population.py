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
        self.speciesCreated = 0

        self.size = size
        self.generation = 0


        for i in range(self.pop.shape[0]):
            self.pop[i] = dino(7, tuple([14, 7]), 2)
            #self.brains[i] = NeuralNetwork(4+1,tuple([5,3]),16)

        self.bestMeeple:dino = self.pop[0]
        self.highestFitness = 0
        self.highestScore = 0


    #update all the meeps that are currently alive
    def updateAlive(self, obstacle_drawlist, score, global_inputs):

        for dinner in self.pop:
            if dinner.isAlive:
                dinner.brain.set_input(0, dinner.pos.x)
                dinner.brain.set_input(1, dinner.pos.y)

                for i in range(len(global_inputs)):
                    i2=i+2
                    dinner.brain.set_input(i2, global_inputs[i])

                dinner.brain.fire_network()

            if dinner.brain.get_output(0) > 0.9:
                dinner.jump()
            if dinner.brain.get_output(1) > 0.9:
                dinner.duck()

            dinner.update(score)
            for obst in obstacle_drawlist:
                if dinner.isColliding( obst ):
                    dinner.isAlive = False

    def drawAlife(self):
        aliveBatch = pyglet.graphics.Batch()
        for dinner in self.pop:
            if dinner.isAlive:
                dinner.sprite.batch = aliveBatch
            else:
                dinner.sprite.batch = None
        aliveBatch.draw()


    #returns bool if all the players are dead or done
    def isDone(self)-> bool:
        for dinner in self.pop:
            if dinner.isAlive:
                return False
        return True

    def countAlive(self)->int:
        tot = 0
        for dinner in self.pop:
            if dinner.isAlive:
                tot+=1
        return tot


    def naturalSelection(self):
        self.speciate() # seperate the existing population into species for the purpose of natural selection
        species_pre_cull = len(self.species)
        self.calculateFitness() # calc fitness of each meeple, currently not needed
        self.sortSpecies() #sort all the species to the average fitness, best first. In the species sort by meeple's fitness

        # Clean the species
        self.cullSpecies()
        self.setBestMeeple()
        print("highest score", self.highestScore)
        print("highest fitness", self.highestFitness)
        self.killBadSpecies()
        self.killStaleSpecies()


        print("Species pre/post culling", species_pre_cull, len(self.species))

        id_s = []
        for spec in self.species:
            id_s.append((spec.speciesID,spec.staleness,spec.bestFitness, spec.averageFitness))
        id_s.reverse()
        print("Species ID's", id_s )

        self.bestMeeple = self.bestMeeple.clone()
        self.bestMeeple.sprite.color = (0,200,100)
        children:List[dino] = [self.bestMeeple]

        for specie in self.species:
            #add the best meeple of a specie to the new generation list
            children.append(specie.bestMeeple.clone())

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

        maxFit = self.highestFitness

        tempnewbestMeeplei = -1

        #go through all meeples in the population and test if their fitness is higher than the previous one
        for i in range(self.pop.size):
            if self.pop[i].fitness > maxFit:
                tempnewbestMeeplei = i
                maxFit = self.pop[i].fitness

        # make sure that the new fitness is actually higher than the previous one.
        if self.highestFitness < self.pop[tempnewbestMeeplei].fitness:
            self.bestMeeple = self.pop[tempnewbestMeeplei]
            self.highestFitness = self.bestMeeple.fitness
            self.highestScore = self.bestMeeple.score
            print("New best meeple")
        else:
            print("Best fitness this generation:", self.pop[tempnewbestMeeplei].fitness)



    def speciate(self):

        #clear all exising species
        #champion is saved, so they're not useless
        #for specie in self.species:
        #    specie.meeples.clear()

        for meep in self.pop:
            speciesfound = False
            for specie in self.species:
                if specie.checkSimilarSpecies(meep):
                    specie.addToSpecies(meep)
                    speciesfound = True
                    break
            if not speciesfound:
                self.species.append(Species(meep=meep, speciesID=self.speciesCreated))
                self.speciesCreated+=1


    def calculateFitness(self):
        for dinner in self.pop:
            dinner.fitness = dinner.score*2

    #get the sum of averages from each specie
    def getAverageFitnessSum(self)->float:
        tempsum = 0
        for specie in self.species:
            tempsum+= specie.averageFitness
        return tempsum

    #sort the population of a species by fitness
    #sort the species by the average of the species
    def sortSpecies(self):
        for specie in self.species:
            specie.sortSpecie()

        self.species.sort(key=lambda specie: specie.averageFitness)


    def killStaleSpecies(self):

        markedForRemoval = list()

        for specie in self.species:
            if specie.staleness >= 15:
                markedForRemoval.append(specie)

        if len(markedForRemoval) > 0:
            print("Killing", len(markedForRemoval), "stale species")
        self.species[:] = [ x for x in self.species if x not in markedForRemoval ]


    def killBadSpecies(self):

        averageSum = 0
        for specie in self.species:
            specie.generateAverageFitness()
            averageSum += specie.averageFitness

        markedForRemoval = list()

        for specie in self.species:
            # this calculates how many children a specie is allowed to produce in Population.naturalSelection()
            # If this is less then one, the specie did so bad, it won't generate a child then. So it basically just died here.
            if specie.averageFitness/averageSum * len(self.pop) < 1:
                markedForRemoval.append(specie)

        if len(markedForRemoval) > 0:
            print("Killing", len(markedForRemoval), "bad species")
        self.species[:] = [ x for x in self.species if x not in markedForRemoval ]


    def cullSpecies(self):
        # remove the bottom half of all species.
        for specie in self.species:
            specie.cull()