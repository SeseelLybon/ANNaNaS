

import numpy as np
from typing import List
from species import Species
from math import floor

from meeple import Meeple





class Population:

    def __init__(self, size, input_size:int, hidden_size:tuple, output_size:int, training_data, training_answers):
        self.pop = np.ndarray([size], dtype=Meeple)
        self.species:List[Species] = []
        self.speciesCreated = 0

        self.size = size
        self.generation = 0

        self.training_data = training_data
        self.training_answers = training_answers


        for i in range(self.pop.shape[0]):
            self.pop[i] = Meeple(input_size, hidden_size, output_size)

        self.bestMeeple:Meeple = self.pop[0]
        self.highestFitness = 0
        self.highestScore = 0


    #update all the meeps that are currently alive
    def updateAlive(self):

        for meep in self.pop:

            if meep.isAlive and not meep.isDone:

                meep.brain.train(training_data=self.training_data, training_answers=self.training_answers, learnrate=0.05)

                errorsum = 0
                for testi in range(self.training_data.shape[0]):
                    meep.brain.set_inputs(self.training_data[testi])
                    meep.brain.fire_network()
                    errorsum += round(meep.brain.costfunction(self.training_answers[testi]), 3)
                meep.score = errorsum/len(self.training_data)

            if meep.score <= 0.000001:
                meep.isDone = True
                return meep

            if np.isnan(meep.score) or (np.isinf(meep.score) and meep.score > 0) or meep.score >= 10 ** 100:
                meep.isAlive = False
                break

            if meep.epochs == 0:
                meep.isAlive = False
            else:
                meep.epochs -= 1

            #return None


    def drawAlife(self):
        pass


    #returns bool if all the players are dead or done
    def isDone(self)-> bool:
        for meep in self.pop:
            if meep.isAlive or meep.isDone:
                return False
        return True


    def naturalSelection(self):
        species_pre_speciate = len(self.species)
        self.speciate() # seperate the existing population into species for the purpose of natural selection
        species_pre_cull = len(self.species)
        self.calculateFitness() # calc fitness of each meeple, currently not needed
        self.sortSpecies() #sort all the species to the average fitness, best first. In the species sort by meeple's fitness

        # Clean the species
        self.cullSpecies()
        self.setBestMeeple()
        print("highest score", self.highestScore)
        print("highest fitness", self.highestFitness)

        if species_pre_cull-species_pre_speciate > 0:
            print("Added", species_pre_cull-species_pre_speciate, "new species")

        self.killBadSpecies()
        self.killStaleSpecies()


        print("Species prespeciate:precull:postcull", species_pre_speciate, species_pre_cull, len(self.species))

        id_s = []
        for spec in self.species:
            id_s.append((spec.speciesID,spec.staleness,spec.bestFitness, spec.averageFitness))
        id_s.reverse()
        print("Species ID's", id_s )

        self.bestMeeple = self.bestMeeple.clone()
        children:List[Meeple] = [self.bestMeeple]

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

        self.pop = np.array(children, dtype=Meeple)
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
        for meep in self.pop:
            if meep.score == 0:
                meep.fitness = np.inf
            else:
                meep.fitness = (1/meep.score)

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


