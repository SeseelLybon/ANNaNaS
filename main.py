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

from meeple import Meeple

training_data = np.array([[0,0,0],
                          [1,0,0],
                          [0,1,0],
                          [1,1,0],
                          [0,0,1],
                          [1,0,1],
                          [0,1,1],
                          [1,1,1]])

training_answers = np.array([[1,0,0,0,0,0,0,0],
                             [0,1,0,0,0,0,0,0],
                             [0,0,1,0,0,0,0,0],
                             [0,0,0,1,0,0,0,0],
                             [0,0,0,0,1,0,0,0],
                             [0,0,0,0,0,1,0,0],
                             [0,0,0,0,0,0,1,0],
                             [0,0,0,0,0,0,0,1]])


print("\n\nStart of main code\n\n")


errorrounding = 3
outputrounding = 3

epochs = 200
learnrate = 0.1

bestmeep:Meeple

pop = Population(100, 3, tuple([8,8,8]), 8, training_data, training_answers)

counter = 0

running = True
print("--------------------|")
while running:
    if counter % 1 == 0:
        print("-", end="")
    counter+=1

    meep = pop.updateAlive()

    if meep is None:
        if pop.isDone():
            print("\n|--------------------------------------------")
            print("All meeps's are dead but not done yet. Time for a new batch!")
            print("Best score this generation:", pop.bestMeeple.score)
            print("startin generation", pop.generation)
            pop.naturalSelection()
            print("-----------|")
            continue
    else:
        running=False
        bestmeep=meep

print("\n\nFound a meep with 0 error (probably something like > 0.0001.")
print("I present: the perfect meep")

errorlist = np.ndarray([len(training_data)], dtype=float)

for testi in range(len(training_data)):
    print("\nInput:", training_data[testi])
    bestmeep.brain.set_inputs(training_data[testi])
    bestmeep.brain.fire_network()
    print( "Desired:", training_answers[testi])
    print( "Brain says:", [ round(x, outputrounding) for x in bestmeep.brain.get_outputs()])
    errorlist[testi] = bestmeep.brain.costfunction(training_answers[testi])
    print( "Error:", errorlist[testi])

print("\navg error:", round(sum(errorlist)/8, 3) )

print("\nfinished in", pop.generation, "generations")



print("\n\nEnd of main")