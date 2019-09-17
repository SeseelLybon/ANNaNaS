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

epochs = 20
for i in range(1,epochs+1):
    print("\nEpoch", i)

    errorlist = np.ndarray([4], dtype=float)

    desiredoutput = np.array([1,0,0,0])
    print("\nInput: [0,0]")
    meeple_1.brain.set_inputs([0,0])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
    errorlist[0] = round( meeple_1.brain.costfunction(desiredoutput), errorrounding)
    print( "Error:", errorlist[0])
    meeple_1.brain.backpropegateOnline(desiredoutput, learnrate)

    desiredoutput = np.array([0,1,0,0])
    print("\nInput: [1,0]")
    meeple_1.brain.set_inputs([1,0])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
    errorlist[1] = round( meeple_1.brain.costfunction(desiredoutput), errorrounding)
    print( "Error:", errorlist[1])
    meeple_1.brain.backpropegateOnline(desiredoutput, learnrate)

    desiredoutput = np.array([0,0,1,0])
    print("\nInput: [0,1]")
    meeple_1.brain.set_inputs([0,1])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
    errorlist[2] = round( meeple_1.brain.costfunction(desiredoutput), errorrounding)
    print( "Error:", errorlist[2])
    meeple_1.brain.backpropegateOnline(desiredoutput, learnrate)

    desiredoutput = np.array([0,0,0,1])
    print("\nInput: [1,1]")
    meeple_1.brain.set_inputs([1,1])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", [ round(x, outputrounding) for x in meeple_1.brain.get_outputs()])
    errorlist[3] = round( meeple_1.brain.costfunction(desiredoutput), errorrounding)
    print( "Error:", errorlist[3])
    meeple_1.brain.backpropegateOnline(desiredoutput, learnrate)

    print("\nAverage error:", sum(errorlist)/4)





print("\n\nEnd of main")