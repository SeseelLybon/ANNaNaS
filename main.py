#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np

#from population import Population

from meeple import Meeple

print("\n\nStart of main code\n\n")


meeple_1 = Meeple( 2, tuple([4]), 4)
learnrate = 0.10
errorrounding = 3
outputrounding = 3
avgerrors = []

epochs = 200

desiredoutput = np.array([[1,0,0,0],
                         [0,1,0,0],
                         [0,0,1,0],
                         [0,0,0,1]])

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
    print("\nAverage error:", avgerrors[-1])
    if avgerrors == float("inf"):
        print("Average explodes to NaN and is going nowhere")
        break




print("\n\n",avgerrors)
print("\n\nEnd of main")