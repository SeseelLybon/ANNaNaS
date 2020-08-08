

import numpy as np
from typing import List
from species import Species
import math
#import pyglet - not drawing stuff atm
from meeple import Meeple

import time

import serpent
from os import rename as os_rename
from os import remove as os_remove



class Population:

    def __init__(self, size, input_size:int, hidden_size:tuple, output_size:int, training_data=None, training_answers=None, isHallow=False):
        self.pop = np.ndarray([size], dtype=Meeple)
        self.species:List[Species] = []
        self.speciesCreated = 0

        self.size = size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.generation = 0

        self.training_data = training_data
        self.training_answers = training_answers

        self.maxStaleness = 10 # how often a species can not improve before it's considered stale/stuck

        for i in range(self.pop.shape[0]):
            self.pop[i] = Meeple(input_size, hidden_size, output_size, isHallow=isHallow)

        self.bestMeeple:Meeple = self.pop[0]
        self.highestFitness = 0
        self.highestScore = 0

        self.MassExtingtionEvent = False


    #update all the meeps that are currently alive
    def updateAlive(self, mastermind_solution, max_dif_pegs, max_pegs, max_attempts, cur_run):

#        print("Updating all alive", self.countAlive())
        #Run through all meeps
        for meep in self.pop:
            meep:Meeple = meep # trick forcing typecasting

            # if meep isn't alive or already found the solution, skip it
            #if meep.isAlive or not meep.isDone:
            if meep.isAlive:
                meep.epochs -= 1
                meep.brain.set_inputs(sanitize_input(meep.results_list, max_pegs, max_attempts))
                meep.brain.fire_network()
                output = meep.brain.get_outputs()
                attempt = sanitize_output(output, max_pegs, max_dif_pegs)
                result = check_attempt(attempt, mastermind_solution)


                soutput=sanitize_output_inv(mastermind_solution,max_pegs,max_dif_pegs)
                meep.brain.train(sanitize_input(meep.results_list, max_pegs, max_attempts), soutput, 0.01 )


                meep.results_list.append((attempt, result))


                if np.array_equal(attempt, mastermind_solution):
                    meep.wins += 1
                    meep.brain.score += min(meep.epochs, 6)+1 # 1
                    meep.brain.fitness += min(meep.epochs, 6)+1
                    print("someone found a solution...", meep.ID, meep.epochs, meep.brain.score, round((meep.wins/cur_run)*100, 2))
                    #meep.isDone = True
                    meep.isAlive = False
                    continue
                elif meep.epochs <= 0:
                    meep.isAlive = False
                    continue



    def drawAlife(self):
        pass
        # I've no idea how I'd show Mastermind on this scale.

        #aliveBatch = pyglet.graphics.Batch()
        #for dinner in self.pop:
        #    if dinner.isAlive:
        #        dinner.sprite.batch = aliveBatch
        #    else:
        #        dinner.sprite.batch = None
        #aliveBatch.draw()


    #returns bool if all the players are dead or done
    def isDone(self)-> bool:
        for meep in self.pop:
            #if meep.isAlive or not meep.isDone: # Doesn't work atm
            if meep.isAlive:
                return False
        return True

    def countAlive(self)->int:
        tot = 0
        for meep in self.pop:
            if meep.isAlive:
                tot+=1
        return tot


    def naturalSelection(self):

        last_time = time.time()

        self.print_deathrate()
        runonce = True
        UnMassExtingtionEventsAttempt = 0
        species_pre_speciate:int = -1
        species_pre_cull:int = -1

        print(deltaTimeS(last_time),"s - Starting Natural Selection")

        while self.MassExtingtionEvent == True or runonce:
            if UnMassExtingtionEventsAttempt >= 3:

                #Reset the population from the ground up
                self.pop = np.ndarray([self.size], dtype=Meeple)
                for i in range(self.pop.shape[0]):
                    self.pop[i] = Meeple(self.input_size, self.hidden_size, self.output_size, isHallow=False)

                self.bestMeeple: Meeple = self.pop[0]
                self.highestFitness = 0
                self.highestScore = 0
                self.generation = 0
                self.species.clear()
            else:
                UnMassExtingtionEventsAttempt+=1
                print(deltaTimeS(last_time),"s - Attempt", UnMassExtingtionEventsAttempt, "to speciate")

            runonce = False
            self.MassExtingtionEvent = False

            print(deltaTimeS(last_time), "s - Speciating")
            species_pre_speciate = len(self.species)
            self.speciate()  # seperate the existing population into species for the purpose of natural selection
            species_pre_cull = len(self.species)
            print(deltaTimeS(last_time), "s - Sorting Species")
            self.calculateFitness()  # calc fitness of each meeple, currently not needed
            self.sortSpecies()  # sort all the species to the average fitness, best first. In the species sort by meeple's fitness

            # Clean the species
            print(deltaTimeS(last_time), "s - Culling Species")
            self.cullSpecies()
            self.setBestMeeple()

            print(deltaTimeS(last_time), "s - Killing Species")
            self.killBadSpecies()
            self.killStaleSpecies()




        print("highest score", self.highestScore)
        print("highest fitness", self.highestFitness)

        if species_pre_cull - species_pre_speciate > 0:
            print("Added", species_pre_cull - species_pre_speciate, "new species")

        print(deltaTimeS(last_time), "s- Species prespeciate:precull:postcull", species_pre_speciate, species_pre_cull, len(self.species))

        id_s = []
        for spec in self.species:
            # Specie's ID
            # Amount of meeps in Specie
            # How stale Specie is
            # Highest fitness in Specie
            # Average fitness of Specie
            id_s.append((spec.speciesID, len(spec.meeples),spec.staleness,spec.bestFitness, spec.averageFitness))
        id_s.sort(key=lambda x: x[4])
        id_s.reverse()
        id_s[:] = id_s[:50]
        print(deltaTimeS(last_time), "s- Species ID's", id_s )

        self.bestMeeple = self.bestMeeple.clone()
        #self.bestMeeple.sprite.color = (0,200,100)
        children:List[Meeple] = [self.bestMeeple]

        print(deltaTimeS(last_time), "s- Making new meeps from parents")

        for specie in self.species:
            #add the best meeple of a specie to the new generation list
            children.append(specie.bestMeeple.clone())

            #generate number of children based on how well the species is doing compared to the rest; the better the bigger.
            newChildrenAmount = math.floor((specie.averageFitness/self.getAverageFitnessSum()) *self.pop.size) -1

            for i in range(newChildrenAmount):
                children.append(specie.generateChild())

        print(deltaTimeS(last_time), "s- Making new meeps from scratch")

        # If the pop-cap hasn't been filled yet, keep getting children from the best specie till it is filled
        while len(children) < self.size:
            children.append(self.species[0].generateChild())

        self.pop = np.array(children, dtype=Meeple)
        self.generation += 1


    def setBestMeeple(self):

        maxFit = 0

        #go through all meeples in the population and test if their fitness is higher than the previous one
        for specie_i in range(len(self.species)):
            if self.species[specie_i].bestFitness > maxFit:
                maxFit = self.species[specie_i].bestFitness

                self.bestMeeple = self.species[specie_i].bestMeeple
                self.highestFitness = self.bestMeeple.brain.fitness
                self.highestScore = self.bestMeeple.brain.score



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
            meep.brain.fitness = meep.brain.score**2

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
        elif len(markedForRemoval)+2 >= len(self.species):
            print("MASS EXTINGTION EVENT")
            print("Going to kill too many species")
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
            if meep.brain.score in scoredict:
                scoredict[meep.brain.score] += 1
            else:
                scoredict[meep.brain.score] = 1

        highestscore = max(scoredict.keys())

        scorebins = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
        for meep in self.pop:
            score = round( meep.brain.score / max(highestscore*0.1, 1), 0)
            if score in scorebins:
                scorebins[score] += 1
            else:
                scorebins[score] = 1

        newline:str = ""
        with open("spreadsheetdata.txt", "a") as f:
            temp_string = ""
            for value in scorebins.values():
                temp_string+= "\t" + str(value)

            f.write(str(time.time()) + "\t" +
                    str(self.highestScore) + "\t" +
                    str(max(self.pop, key=lambda kv: kv.brain.score).brain.score) + "\t" +
                    str(self.generation) + "\n")# +
                    #temp_string + "\n")
            # Time, Highest score overall, highst score generation, generation, deathbin



            #for specie in self.species[:max(10, len(self.species))]:
            #    specie.sortSpecie()
            #    newline += "\t" + \
            #              str(specie.speciesID) + "\t" + \
            #              str(len(specie.meeples)) + "\t" + \
            #              str(specie.meeples[0].brain.fitness) + "\t" + \
            #              str(specie.meeples[len(specie.meeples)//2] ) + "\t" + \
            #              str(specie.meeples[-1].brain.fitness) + "\t" + \
            #              str(specie.averageFitness) + "\t" + "\n"
            #    f.write( newline )
        #for key, value in sorted(scorebins.items(), key=lambda kv: kv[0]):
        #    print(key,":",value, " - ")
        print("death bin:amount,", sorted(scorebins.items(), key=lambda kv: kv[0]))
        print(newline)

    def pickle_population_to_file(self):

        ser_bytes_meeps = []

        for meep in self.pop:
            ser_bytes_meeps.append(meep.brain.serpent_serialize())

        try:
            os_remove('pickledmeeps.picklejar_old')
        except FileNotFoundError:
            pass
            # File doesn't exist, so doesn't need to be removed
        finally:
            try:
                os_rename('pickledmeeps.picklejar', 'pickledmeeps.picklejar_old')
            except FileNotFoundError:
                pass
                # File doesn't exist, so doesn't need to be renamed

        with open('pickledmeeps.picklejar', 'wb') as the_file:
            serpent.dump( [self.generation, Meeple.global_ID[0]-self.size, ser_bytes_meeps], the_file)


    def pickle_bestmeep_to_file(self):

        try:
            os_remove('pickledbestmeep.picklejar_old')
        except FileNotFoundError:
            pass
            # File doesn't exist, so doesn't need to be removed
        finally:
            try:
                os_rename('pickledbestmeep.picklejar', 'pickledbestmeep.picklejar_old')
            except FileNotFoundError:
                pass
                # File doesn't exist, so doesn't need to be renamed

        with open('pickledbestmeep.picklejar', 'wb') as the_file:
            serpent.dump( [self.bestMeeple.brain.serpent_serialize()], the_file)


    def unpickle_bestmeep_from_file(self):

        with open('pickledbestmeep.picklejar', 'rb') as the_file:
            unpickledjar = serpent.load(the_file)

        self.bestMeeple = unpickledjar[0]



    def unpickle_population_from_file(self):

        with open('pickledmeeps.picklejar', 'rb') as the_file:
            unpickledjar = serpent.load(the_file)

        self.generation = unpickledjar[0]
        Meeple.global_ID = [unpickledjar[1]]
        unpickled_meeps = unpickledjar[2]

        self.pop = np.ndarray([self.size], dtype=Meeple)
        for i in range(self.pop.size):
            self.pop[i] = Meeple(self.input_size, self.hidden_size, self.output_size, isHallow=True)
            self.pop[i].brain.serpent_deserialize(unpickled_meeps[i])


    def pickle_population_to_list(self):

        serbytes_meeples_list = []

        for meep in self.pop:
            serbytes_meeples_list.append(meep.brain.serpent_serialize())

        return serbytes_meeples_list


    def unpickle_population_from_list(self, pickled_brains):

        print(len(pickled_brains))
        self.pop = np.ndarray([self.size], dtype=Meeple)
        for i in range(self.pop.size):
            self.pop[i] = Meeple(self.input_size, self.hidden_size, self.output_size, isHallow=True)

            self.pop[i].brain.serpent_deserialize(pickled_brains[i])


def deltaTimeS(last_time):
    return int((time.time()-last_time)//60)


# Custom Code for Mastermind

def check_attempt(attempt, mastermind_solution)->List[int]:

    result:List[int] = []
    #Some code that tests the current attempt for hits (number, location) and blows (number)
    # 0 - miss
    # 1 - blow (correct number, not correct location)
    # 2 - hit (correct number, correct location)

    for i in range(len(attempt)):
        if attempt[i] == mastermind_solution[i]:
            # if the right peg is in the right place
            result.append(2)
        elif attempt[i] in mastermind_solution:
            # if the right peg is in the wrong place
            result.append(1)
        else:
            # if the wrong peg
            result.append(0)
    result.sort(reverse=True)

    # Obscufate as the player can't know which exact one is blow or hit.
    return result

# Turn the output of the ANN into a 'choice'
def sanitize_output(usputput, # unsanitized output from ANN
                    max_pegs,
                    max_dif_pegs):
    #soutput = [ np.argmax(output[:max_dif_pegs*1]),
    #            np.argmax(output[max_dif_pegs*1:max_dif_pegs*2]),
    #            np.argmax(output[max_dif_pegs*2:max_dif_pegs*3]),
    #            np.argmax(output[max_dif_pegs*3:])
    #            ]

    soutput = np.ndarray([max_pegs], dtype=int)

    for i in range(max_pegs):
        # The +/-1 is because I need to shift the solution a bit as 0 is an empty peg.
        # atm of writing I dunno if this  works correctly.
        #   still dont.
       soutput[i] = int( np.argmax( usputput[max_dif_pegs*i:max_dif_pegs*(i+1)] )
                         +1 )

    return soutput

# Turn the mastermind solution into what the ANN output should look like.
def sanitize_output_inv(solution, max_pegs, max_dif_pegs):
    #make an array the size of the output
    soutput = np.zeros([max_dif_pegs*max_pegs], dtype=int)

    for i in range(max_pegs):
        soutput[i*max_dif_pegs+(solution[i]-1)] = 1

    return soutput

# Turn the results list into the input the ANN wants
def sanitize_input(results, max_pegs, max_attempts):
    #sinput = np.zeros([max_attempts*max_pegs*2], dtype=int )
    # max_attempt-1 because the ANN shouldn't try to run an 11th attempt
    sinput = np.zeros([(max_attempts-1)*max_pegs*2], dtype=int )

    for ai in range(0, len(results)):#, max_pegs*2): #ai =attempt index
        for j in range(max_pegs):
            sinput[ai*max_pegs*2+j] = results[ai][0][j]
            sinput[ai*max_pegs*2+j+max_pegs] = results[ai][1][j]

    return sinput


def testpopo():
    print("running testpopo")
    max_attempts = 10  # amount of attempts a mastermind can make before being considered dead
    max_dif_pegs = 6  # numbers simulate the diffirent colours of pegs
    max_pegs = 4  # how many pegs have to be guessed

    inputsize=max_pegs*max_attempts*2 # Double to count for the 'hit and blow'
    hiddensize=tuple([max_pegs*max_attempts*2, max_pegs*max_attempts, max_pegs*max_dif_pegs])
    #hiddensize=tuple([60, 40, 20])
    outputsize=max_pegs*max_dif_pegs

    mastermind_solution = np.random.randint(1, max_dif_pegs+1, max_pegs)

    meep:Meeple = Meeple(input_size=inputsize, hidden_size=hiddensize, output_size=outputsize,
                             isHallow=False)


    #for i in range(10):
    meep.brain.set_inputs(sanitize_input(meep.results_list, max_pegs, max_attempts))
    meep.brain.fire_network()
    output = meep.brain.get_outputs()
    attempt = sanitize_output(output, max_pegs, max_dif_pegs)
    result = check_attempt(attempt, mastermind_solution)

    soutput = sanitize_output_inv(mastermind_solution, max_pegs, max_dif_pegs)
    meep.brain.train(sanitize_input(meep.results_list, max_pegs, max_attempts), soutput, 0.01)

    meep.results_list.append((attempt, result))


if __name__ == '__main__':
    import time

    cur_time = time.time()

    import cProfile
    #import pstats
#
    #profiler = cProfile.Profile()
    #cProfile.runctx('testpopo()', globals(), locals(), filename="population.profile")
    #profiler.run('testpopo')
    testpopo()
#
    #profiler.print_stats()
    ##p = pstats.Stats('population.profile')
    ##p.sort_stats('cumulative').print_stats(10)



    #time_dif = time.time()- cur_time
    #print("time total s :", time_dif)
    #print("time total *250 s:", time_dif * 250)
    #print("time total *250*4k s:", time_dif * 250*4096)
    #print("time total *250*4k m:", (time_dif * 250*4096 )/60 )
    #print("time total *250*4k h:", ((time_dif * 250*4096 )/60)/60)
    #print("time total *250*4k d:", (((time_dif * 250*4096 )/60)/60)/24)


    print("start profile")
    cProfile.runctx('testpopo()', globals(), locals(), filename="population.profile")
    print("done profile")

    #cur_time = time.time()
    #testpopo()
    #time_dif = time.time()- cur_time
    #print("time total s :", time_dif)
    #print("time total *250 s:", time_dif * 250)
    #print("time total *250*4k s:", time_dif * 250*4096)
    #print("time total *250*4k m:", (time_dif * 250*4096 )/60 )
    #print("time total *250*4k h:", ((time_dif * 250*4096 )/60)/60)
    #print("time total *250*4k d:", (((time_dif * 250*4096 )/60)/60)/24)