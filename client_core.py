#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import pyglet
from typing import List

import numpy as np
from population import Population

import serpent

#window = pyglet.window.Window(1200,800)
pyglet.gl.glClearColor(0.7,0.7,0.7,1)


client_population:Population = Population(1, input_size=1, hidden_size=tuple([0]), output_size=1, isHallow=True)

inputsize:int = None
hiddensize:tuple = None
outputsize:int = None

showGraph = False
skip_once = False


# Temp
from meeple import Meeple

max_attempts = 10 # amount of attempts a mastermind can make before being considered dead
max_dif_pegs = 6 # numbers simulate the diffirent colours of pegs
max_pegs = 4 # how many pegs have to be guessed







client_isDone = False



runi = 1
#runm = 4096
runm = 10

def update(dt):
    global runi
    global runm
    global client_isDone
    global client_population

    if runi <= runm:

        # generate new solution to test all meeps against
        # Not sure if this generation works, as in the memory, unused output is 0
        #mastermind_solution = np.random.randint(1, max_dif_pegs+1, max_pegs, )

        mastermind_solution = generate_mastermind_solution("unique")

        print("starting run", runi, mastermind_solution)

        # reset meeps every run except score
        for meep in client_population.pop:
            meep: Meeple = meep
            meep.results_list = []  # whipe it's memory of attempts
            meep.epochs = max_attempts  # reset the amount of times it can try
            meep.isAlive = True
            meep.isDone = False

        # run all meeps against this until pop.isDone.
        while not client_population.isDone():
            client_population.updateAlive(mastermind_solution, max_dif_pegs, max_pegs, max_attempts, runi)

        runi+=1


    # Test, could meep.results_lists fuck things?
    # for meep in client_population.pop:
    #    del meep.results_list


    if runi > runm:
        print("--------------------------------------------")
        print("All dino's are either done or dead.")
        best_score = max([meep.brain.score for meep in client_population.pop])
        print("Best score this batch:", best_score)
        pyglet.clock.unschedule(update)
        client_isDone = True




def dojob(job):
    global client_population
    global client_isDone
    global runi
    #global score
    #global bestfitness
    #global lastspawnscore
    #global best_score

    client_isDone = False

    print("Starting the job batch")

    # For Mastermind, a job is testing a meep against x diffirent randomized solutions.
    # Score is a function of the amount of correctly solved solutions aiming for 100%


    # unpack job (a pickle of a list of meeple brains)
    client_population = Population(len(job), input_size=inputsize, hidden_size=hiddensize, output_size=outputsize, isHallow=True)

    client_population.unpickle_population_from_list(job)

    for meep in client_population.pop:
        meep.brain.score = 0
        meep.brain.fitness = 0

    runi = 1

    # start the simulation and poll if it's done
    pyglet.clock.schedule_interval_soft(update, 1 / 1000)


def generate_mastermind_solution(t='unique'):
    global max_dif_pegs
    global max_pegs

    if t == 'unique':
        temp_rng = list(range(1, max_dif_pegs + 1))
        np.random.shuffle(temp_rng)
        mastermind_solution = temp_rng[:max_pegs]
    else:
        mastermind_solution = np.random.randint(1, max_dif_pegs+1, max_pegs, dtype=np.uint64)
    return mastermind_solution






def test():
    max_attempts = 10  # amount of attempts a mastermind can make before being considered dead
    max_dif_pegs = 6  # numbers simulate the diffirent colours of pegs
    max_pegs = 4  # how many pegs have to be guessed

    inputsize=(max_attempts-1)*max_pegs*2 # Double to count for the 'hit and blow'
    hiddensize=tuple([(max_attempts-1)*max_pegs*2, max_pegs*(max_attempts-1), max_pegs*max_dif_pegs])
    # hiddensize=tuple([60, 40, 20])
    outputsize = max_pegs * max_dif_pegs

    testpop:Population = Population(50, input_size=inputsize, hidden_size=hiddensize, output_size=outputsize, isHallow=False)


    print("starting run", runi)
    # generate new solution to test all meeps against

    mastermind_solution = np.random.randint(1, max_dif_pegs+1, max_pegs, dtype=np.uint64)

    # run all meeps against this until pop.isDone.
    while not testpop.isDone():
        print("----")
        testpop.updateAlive(mastermind_solution, max_dif_pegs, max_pegs, max_attempts, 1)

    print("--------------------------------------------")
    print("All dino's are either done or dead.")
    best_score = max([meep.brain.score for meep in testpop.pop])
    print("Best score this batch:", best_score)


    testpop.naturalSelection()



if __name__ == '__main__':
    import cProfile

    p = cProfile.Profile()
    #p.runctx('oldbrain.ReLU(x)', locals={}, globals={'oldbrain':oldbrain} )
    p.runcall(test)
    p.print_stats()
