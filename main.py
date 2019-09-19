#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np
np.random.seed(2)
import math

#from population import Population

from meeple import Meeple

print("\n\nStart of main code\n\n")


learnrate = 0.01
errorrounding = 3
outputrounding = 3

epochs = 400

desiredoutput = np.array([[1,0,0,0],
                         [0,1,0,0],
                         [0,0,1,0],
                         [0,0,0,1]])

meeple_1 = Meeple(2, tuple([16]), 4)
avgerrors = []

#for nan_test_attempt in range(4000):
#    print("Testing, hoping to spawn a NaN:", nan_test_attempt)
#    meeple_1 = Meeple( 2, tuple([4]), 4)
#    avgerrors = []
for i in range(1,epochs+1):
    print("\nEpoch", i)

    errorlist = np.ndarray([4], dtype=float)

    print("\nInput: [0,0]")
    meeple_1.brain.set_inputs([0,0])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput[0])
    print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
    errorlist[0] = round( meeple_1.brain.costfunction(desiredoutput[0]), errorrounding)
    print( "Error:", errorlist[0])
    meeple_1.brain.backpropegateOnline(desiredoutput[0], learnrate)

    print("\nInput: [1,0]")
    meeple_1.brain.set_inputs([1,0])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput[1])
    print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
    errorlist[1] = round( meeple_1.brain.costfunction(desiredoutput[1]), errorrounding)
    print( "Error:", errorlist[1])
    meeple_1.brain.backpropegateOnline(desiredoutput[1], learnrate)

    print("\nInput: [0,1]")
    meeple_1.brain.set_inputs([0,1])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput[2])
    print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
    errorlist[2] = round( meeple_1.brain.costfunction(desiredoutput[2]), errorrounding)
    print( "Error:", errorlist[2])
    meeple_1.brain.backpropegateOnline(desiredoutput[2], learnrate)

    print("\nInput: [1,1]")
    meeple_1.brain.set_inputs([1,1])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput[3])
    print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
    errorlist[3] = round( meeple_1.brain.costfunction(desiredoutput[3]), errorrounding)
    print( "Error:", errorlist[3])
    meeple_1.brain.backpropegateOnline(desiredoutput[3], learnrate)


    avgerrors.append( round(sum(errorlist)/4, 3) )
    #avgerrors.append( round(errorlist[0], 3) )
    print("\nAverage error:", avgerrors[-1])

    if math.isnan(avgerrors[-1]):
        print("Average explodes to NaN and is going nowhere")
        break

    #if math.isnan(avgerrors[-1]):
    #    break
print("\n\n", avgerrors)
    #print(avgerrors, "\n\n")




print("\n\nEnd of main")