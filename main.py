#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np
#np.random.seed(2)

import math

#from population import Population

from meeple import Meeple

print("\n\nStart of main code\n\n")


errorrounding = 3
outputrounding = 3

epochs = 800
learnrate = 0.01

#inputs = np.array([[0,0,0],
#                   [1,0,0],
#                   [0,1,0],
#                   [1,1,0],
#                   [0,0,1],
#                   [1,0,1],
#                   [0,1,1],
#                   [1,1,1]])
#
#desiredoutput = np.array([[1,0,0,0,0,0,0,0],
#                          [0,1,0,0,0,0,0,0],
#                          [0,0,1,0,0,0,0,0],
#                          [0,0,0,1,0,0,0,0],
#                          [0,0,0,0,1,0,0,0],
#                          [0,0,0,0,0,1,0,0],
#                          [0,0,0,0,0,0,1,0],
#                          [0,0,0,0,0,0,0,1]])

inputs = np.array([[1,1,1]])
desiredoutput = np.array([[0,0,0,0,0,0,0,1]])

meeple_1 = Meeple(3, tuple([16]), 8)
avgerrors = []

#for nan_test_attempt in range(4000):
#    print("Testing, hoping to spawn a NaN:", nan_test_attempt)
#    meeple_1 = Meeple( 2, tuple([4]), 4)
#    avgerrors = []
for i in range(1,epochs+1):
    print("\nEpoch", i)

    errorlist = np.ndarray([len(inputs)], dtype=float)

    for testi in range(len(inputs)):
        print("\nInput:", inputs[testi])
        meeple_1.brain.set_inputs(inputs[testi])
        meeple_1.brain.fire_network()
        print( "Desired:", desiredoutput[testi])
        print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
        errorlist[testi] = round( meeple_1.brain.costfunction(desiredoutput[testi]), errorrounding)
        print( "Error:", errorlist[testi])
        meeple_1.brain.backpropegateOnline(desiredoutput[testi], learnrate)


    avgerrors.append( round(sum(errorlist)/4, 3) )
    #avgerrors.append( round(errorlist[0], 3) )
    print("\nAverage error:", avgerrors[-1])

    if math.isnan(avgerrors[-1]):
        print("Average explodes to NaN and is going nowhere")
        break




print("\n\nAverage Error List", avgerrors)
print("Lowest Avg. Error", min(avgerrors))
print("Highset Avg. Error", max(avgerrors))




print("\n\nEnd of main")