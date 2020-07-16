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
score = 0
best_score = 0
bestfitness = 0
lastspawnscore = 0


# Temp
from meeple import Meeple

max_attempts = 30 # amount of attempts a mastermind can make before being considered dead
max_dif_pegs = 6 # numbers simulate the diffirent colours of pegs
max_pegs = 4 # how many pegs have to be guessed







client_isDone = False





score_label = pyglet.text.Label('score: ' + str(score),
                  font_name='Times New Roman',
                  font_size=12,
                  x=50, y=450,
                  anchor_x='left', anchor_y='center')
score_best_label = pyglet.text.Label('best score: ',
                  font_name='Times New Roman',
                  font_size=12,
                  x=50, y=425,
                  anchor_x='left', anchor_y='center')
dinos_live_label = pyglet.text.Label("Dino's alive: ",
                   font_name='Times New Roman',
                   font_size=12,
                   x=50, y=400,
                   anchor_x='left', anchor_y='center')

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



def dojob(job):
    global client_population
    global client_isDone
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



    # Run test
    for runi in range(10):
        print("starting run", runi)
        # generate new solution to test all meeps against
        mastermind_solution = np.random.randint(1, max_dif_pegs, max_pegs)

        # reset meeps every run except score
        for meep in client_population.pop:
            meep: Meeple = meep
            meep.results_list = []  # whipe it's memory of attempts
            meep.epochs = max_attempts # reset the amount of times it can try
            meep.isAlive = True
            meep.isDone = False

        # run all meeps against this until pop.isDone.
        while not client_population.isDone():
            client_population.updateAlive(mastermind_solution, max_dif_pegs)


    # Test, could meep.results_lists fuck things?
    for meep in client_population.pop:
        del meep.results_list

    print("--------------------------------------------")
    print("All dino's are either done or dead.")
    best_score = max([meep.brain.score for meep in client_population.pop])
    print("Best score this batch:", best_score)
    client_isDone = True










test = 1

if __name__ == '__main__' and test == 1:
    max_attempts = 20

    input_size=max_pegs*max_attempts+4*max_attempts
    hidden_size=tuple([0])
    output_size=max_dif_pegs*max_pegs


    client_population = Population(10, input_size=input_size, hidden_size=hidden_size, output_size=output_size,
                                   isHallow=False)


    for meep in client_population.pop:
        meep.brain.score = 0
        meep.brain.fitness = 0


    # Run test
    for runi in range(100):
        print("starting run", runi)
        # generate new solution to test all meeps against
        mastermind_solution = np.random.randint(1, max_dif_pegs, max_pegs)

        # reset meeps every run except score
        for meep in client_population.pop:
            meep: Meeple = meep
            meep.results_list = []  # whipe it's memory of attempts
            meep.epochs = max_attempts # reset the amount of times it can try
            meep.isAlive = True
            meep.isDone = False

        # run all meeps against this until pop.isDone.
        while not client_population.isDone():
            client_population.updateAlive(mastermind_solution, max_dif_pegs)

    print("--------------------------------------------")
    print("All dino's are either done or dead.")
    print("Best score this batch:", max([meep.brain.score for meep in client_population.pop]))



elif __name__ == '__main__' and test == 2:
    from population import check_attempt
    from population import sanitize_output
    from population import sanitize_input

    input_size = max_pegs * max_attempts + 4 * max_attempts
    hidden_size = tuple([0])
    output_size = max_dif_pegs * max_pegs

    meep1:Meeple = Meeple( input_size=input_size, hidden_size=hidden_size, output_size=output_size, isHallow=False)
    amount_runs = 500
    run_scores = []
    run_amount:int=0

    for run_amount in range(amount_runs):
        print("run", run_amount)

        attempt_list = []
        mastermind_solution = np.random.randint(1,max_dif_pegs,max_pegs)


        meep1.brain.set_inputs(np.zeros(max_pegs*max_attempts+4*max_attempts))
        meep1.brain.fire_network()
        output = meep1.brain.get_outputs()
        attempt = sanitize_output(output, max_dif_pegs)
        result = check_attempt(attempt, mastermind_solution)
        #print("attempt:", 1, attempt, "result:",result)
        attempt_list.append((attempt, result))

        for i in range(2,max_attempts+1):

            meep1.brain.set_inputs(sanitize_input(attempt_list))
            meep1.brain.fire_network()
            output = meep1.brain.get_outputs()
            attempt = sanitize_output(output, max_dif_pegs)
            result = check_attempt(attempt, mastermind_solution)
            #print("attempt:", i, attempt, "result:",result)
            attempt_list.append((attempt, result))

            if result == [2,2,2,2]:
                break

        if result == [2,2,2,2]:
            run_scores.append(1)
            print("Got the solution!")
        else:
            run_scores.append(0)

    print("Meep had an accuracy of", round(run_scores.count(1)/(amount_runs+1),4), "% or ", run_scores.count(1), "out of ", (run_amount+1))

    pass


