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
max_dif_pegs = 5 # numbers simulate the diffirent colours of pegs
max_pegs = 4 # how many pegs have to be guessed







client_isDone = False





#score_label = pyglet.text.Label('score: ' + str(score),
#                  font_name='Times New Roman',
#                  font_size=12,
#                  x=50, y=450,
#                  anchor_x='left', anchor_y='center')
#score_best_label = pyglet.text.Label('best score: ',
#                  font_name='Times New Roman',
#                  font_size=12,
#                  x=50, y=425,
#                  anchor_x='left', anchor_y='center')
#dinos_live_label = pyglet.text.Label("Dino's alive: ",
#                   font_name='Times New Roman',
#                   font_size=12,
#                   x=50, y=400,
#                   anchor_x='left', anchor_y='center')

#@window.event
#def on_draw():
#    global client_population
#    global window
#    global score
#    global lastspawnscore
#    global showGraph
#
#    window.clear()
#
#    return
#
##    if client_population.bestMeeple is not None and showGraph:
##        client_population.bestMeeple.brain.updateposGFX([600, 750], [550, 500])
##        client_population.bestMeeple.brain.updateintensityGFX([2, 2,  # dinner pos
##                                                               0.5, 2, 3, 3,  # first object
##                                                               1.5])       # score
##        client_population.bestMeeple.brain.draw()
##
##    # Run the game here
##    # Move the objects/obstacles on the platform, not the dino or the platform
##    # Use the update() and isDone() function
##
##    score_label.text = 'score: ' + str(score)
##    score_label.draw()
##    score_best_label.text = 'best score: ' + str(client_population.highestScore)
##    score_best_label.draw()
##    dinos_live_label.text = "Dino's alive: " + str(client_population.countAlive()) + " of " + str(client_population.size)
##    dinos_live_label.draw()
##
##    obt.ground.draw()
##
##    client_population.drawAlife()
##
##    for obst in obstacle_drawlist:
##        obst.draw()
##    #pops.bestMeeple.draw()

runi = 0
runm = 50

def update(dt):
    global runi
    global runm
    global client_isDone
    global client_population

    if runi < runm:

        # generate new solution to test all meeps against
        # Not sure if this generation works, as in the memory, unused output is 0
        mastermind_solution = np.random.randint(0, max_dif_pegs, max_pegs)

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
            client_population.updateAlive(mastermind_solution, max_dif_pegs, max_pegs)

        runi+=1


    # Test, could meep.results_lists fuck things?
    # for meep in client_population.pop:
    #    del meep.results_list


    if runi >= runm:
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

    runi = 0

    # start the simulation and poll if it's done
    pyglet.clock.schedule_interval_soft(update, 1 / 1000)










#if __name__ == '__main__':
#    max_attempts = 10
#
#    input_size=max_pegs*max_attempts+4*max_attempts
#    hidden_size=tuple([0])
#    output_size=max_dif_pegs*max_pegs
#
#
#    client_population = Population(10, input_size=input_size, hidden_size=hidden_size, output_size=output_size,
#                                   isHallow=False)
#
#
#    for meep in client_population.pop:
#        meep.brain.score = 0
#        meep.brain.fitness = 0
#
#
#    # Run test
#    for runi in range(100):
#        print("starting run", runi)
#        # generate new solution to test all meeps against
#        mastermind_solution = np.random.randint(1, max_dif_pegs, max_pegs)
#
#        # reset meeps every run except score
#        for meep in client_population.pop:
#            meep: Meeple = meep
#            meep.results_list = []  # whipe it's memory of attempts
#            meep.epochs = max_attempts # reset the amount of times it can try
#            meep.isAlive = True
#            meep.isDone = False
#
#        # run all meeps against this until pop.isDone.
#        while not client_population.isDone():
#            client_population.updateAlive(mastermind_solution, max_dif_pegs)
#
#    print("--------------------------------------------")
#    print("All dino's are either done or dead.")
#    print("Best score this batch:", max([meep.brain.score for meep in client_population.pop]))



if __name__ == '__main__':

    inputsize = max_pegs * max_attempts * 2
    hiddensize = tuple([max_pegs * max_attempts])
    outputsize = max_dif_pegs * max_pegs

    testpop:Population = Population(1, input_size=inputsize, hidden_size=hiddensize, output_size=outputsize, isHallow=False)

    print("starting run", runi)
    # generate new solution to test all meeps against
    mastermind_solution = np.random.randint(1, max_dif_pegs, max_pegs)



    # run all meeps against this until pop.isDone.
    while not testpop.isDone():
        print("----")
        testpop.updateAlive(mastermind_solution, max_dif_pegs, max_pegs)




    if runi >= runm:
        print("--------------------------------------------")
        print("All dino's are either done or dead.")
        best_score = max([meep.brain.score for meep in testpop.pop])
        print("Best score this batch:", best_score)
        pyglet.clock.unschedule(update)
        client_isDone = True



