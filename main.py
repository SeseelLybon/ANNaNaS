#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np

import math

from population import Population
from population import training_data
from population import training_answers

from meeple import Meeple

print("\n\nStart of main code\n\n")


errorrounding = 3
outputrounding = 3

epochs = 200
learnrate = 0.10

bestmeep:Meeple

pop = Population(10, 3, tuple([16]), 8)

counter = 0

running = True
print("-------------------|")
while running:
    if counter % 10 == 0:
        print("-", end="")
    counter+=1

    meep = pop.updateAlive()

    if meep is None:
        if pop.isDone():
            print("\n--------------------------------------------")
            print("All meeps's are dead but not done yet. Time for a new batch!")
            print("Best score this generation:", pop.bestMeeple.score)
            print("startin generation", pop.generation)
            pop.naturalSelection()
    else:
        running=False
        bestmeep=meep

errorlist = np.ndarray([len(training_data)], dtype=float)

for testi in range(len(training_data)):
    print("\nInput:", training_data[testi])
    bestmeep.brain.set_inputs(training_data[testi])
    bestmeep.brain.fire_network()
    print( "Desired:", training_answers[testi])
    print( "Brain says:", [ round(x, outputrounding) for x in bestmeep.brain.get_outputs()])
    errorlist[testi] = round( bestmeep.brain.costfunction(training_answers[testi]), 3)
    print( "Error:", errorlist[testi])

print( "avg error:", round(sum(errorlist)/8, 3) )



print("\n\nEnd of main")