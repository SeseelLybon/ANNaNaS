

import numpy as np
from typing import List
from species import Species
from math import floor
import pyglet
from obstacle import dino


class Population:

    def __init__(self, size, input_size:int, hidden_size:tuple, output_size:int, training_data=None, training_answers=None):
        self.pop = np.ndarray([size], dtype=dino)
        self.species:List[Species] = []
        self.speciesCreated = 0

        self.size = size
        self.generation = 0

        self.training_data = training_data
        self.training_answers = training_answers

        self.maxStaleness = 7 # how often a species can not improve before it's considered stale/stuck


        for i in range(self.pop.shape[0]):
            self.pop[i] = dino(input_size, hidden_size, output_size)

        self.bestMeeple:dino = self.pop[0]
        self.highestFitness = 0
        self.highestScore = 0

        self.MassExtingtionEvent = False


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



            #return None


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

        self.print_deathrate()
        runonce = True
        UnMassExtingtionEventsAttempt = 0
        species_pre_speciate:int = -1
        species_pre_cull:int = -1

        while self.MassExtingtionEvent == True or runonce:
            if UnMassExtingtionEventsAttempt >= 3:
                break
                #let the program crash
            else:
                UnMassExtingtionEventsAttempt+=1
                print("Attempt", UnMassExtingtionEventsAttempt, "to speciate")

            runonce = False
            self.MassExtingtionEvent = False


            species_pre_speciate = len(self.species)
            self.speciate()  # seperate the existing population into species for the purpose of natural selection
            species_pre_cull = len(self.species)
            self.calculateFitness()  # calc fitness of each meeple, currently not needed
            self.sortSpecies()  # sort all the species to the average fitness, best first. In the species sort by meeple's fitness

            # Clean the species
            self.cullSpecies()
            self.setBestMeeple()

            self.killBadSpecies()
            self.killStaleSpecies()




        print("highest score", self.highestScore)
        print("highest fitness", self.highestFitness)

        if species_pre_cull - species_pre_speciate > 0:
            print("Added", species_pre_cull - species_pre_speciate, "new species")


        print("Species prespeciate:precull:postcull", species_pre_speciate, species_pre_cull, len(self.species))

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

        # TODO: Make it so that the best meeple of the population is tied to the species so that when the species dies
        #   The rest isn't compared/hold back to what is a dead species.
        #   SortSpecies has already happened, so the [0] of each specie is the best by default.
        #   Set the best meeple of pop by looking at the species top.
        #   This means that the max fitness can drop if a species dies, but won't drop if it's still going!

        maxFit = 0

        #go through all meeples in the population and test if their fitness is higher than the previous one
        for specie_i in range(len(self.species)):
            if self.species[specie_i].bestFitness > maxFit:
                maxFit = self.species[specie_i].bestFitness

                self.bestMeeple = self.species[specie_i].bestMeeple
                self.highestFitness = self.bestMeeple.fitness
                self.highestScore = self.bestMeeple.score

        ## make sure that the new fitness is actually higher than the previous one.
        #if self.highestFitness < self.pop[tempnewbestMeeplei].fitness:
        #    self.bestMeeple = self.pop[tempnewbestMeeplei]
        #    self.highestFitness = self.bestMeeple.fitness
        #    self.highestScore = self.bestMeeple.score
        #    print("New best meeple")
        #else:
        #    print("Best fitness this generation:", self.pop[tempnewbestMeeplei].fitness)



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
            if specie.staleness >= self.maxStaleness:
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
            if (specie.averageFitness/averageSum) * len(self.pop) < 1:
                markedForRemoval.append(specie)

        if len(markedForRemoval) > 0:
            print("Killing", len(markedForRemoval), "bad species")
        elif len(markedForRemoval) == len(self.species):
            print("MASS EXTINGTION EVENT")
            plan = "C"
            if plan == "A":
                pass
                # Let the program crash.
            elif plan == "B":
                pass
                # Reset the population; fill the population with new random meeples.
            elif plan == "C":
                pass
                self.MassExtingtionEvent = True

        self.species[:] = [ x for x in self.species if x not in markedForRemoval ]


    def cullSpecies(self):
        # remove the bottom half of all species.
        for specie in self.species:
            specie.cull()

    def print_deathrate(self, do_print=True):
        if not do_print:
            return
        # go through all meeps and add their score to a dict.
        # pick the highest score and bins for every x% of score from the max
        # print
        scoredict = dict()
        for meep in self.pop:
            if meep.score in scoredict:
                scoredict[meep.score] += 1
            else:
                scoredict[meep.score] = 1

        highestscore = max(scoredict.keys())

        scorebins = dict()
        for meep in self.pop:
            score = round( meep.score / (highestscore*0.1), 0)
            if score in scorebins:
                scorebins[score] += 1
            else:
                scorebins[score] = 1

        #for key, value in sorted(scorebins.items(), key=lambda kv: kv[0]):
        #    print(key,":",value, " - ")
        print("death bin:amount,", sorted(scorebins.items(), key=lambda kv: kv[0]))

        pass