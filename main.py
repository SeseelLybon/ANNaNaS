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


meeple_1 = Meeple( 2, tuple([0]), 4)

epochs = 100
for i in range(1,epochs+1):
    print("\nEpoch", i)

    errorlist = np.ndarray([4], dtype=float)

    desiredoutput = np.array([1,0,0,0])
    print("\nInput: [0,0]")
    meeple_1.brain.set_inputs([0,0])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", [ round(x, 2) for x in meeple_1.brain.get_outputs()])
    errorlist[0] = round( meeple_1.brain.costfunction(desiredoutput), 2)
    print( "Error:", errorlist[0])
    meeple_1.brain.backpropegateOnline(desiredoutput, 0.05)

    desiredoutput = np.array([0,1,0,0])
    print("\nInput: [1,0]")
    meeple_1.brain.set_inputs([1,0])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", [ round(x, 2) for x in meeple_1.brain.get_outputs()])
    errorlist[1] = round( meeple_1.brain.costfunction(desiredoutput), 2)
    print( "Error:", errorlist[1])
    meeple_1.brain.backpropegateOnline(desiredoutput, 0.05)

    desiredoutput = np.array([0,0,1,0])
    print("\nInput: [0,1]")
    meeple_1.brain.set_inputs([0,1])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", [ round(x, 2) for x in meeple_1.brain.get_outputs()])
    errorlist[2] = round( meeple_1.brain.costfunction(desiredoutput), 2)
    print( "Error:", errorlist[2])
    meeple_1.brain.backpropegateOnline(desiredoutput, 0.05)

    desiredoutput = np.array([0,0,0,1])
    print("\nInput: [1,1]")
    meeple_1.brain.set_inputs([1,1])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", [ round(x, 2) for x in meeple_1.brain.get_outputs()])
    errorlist[3] = round( meeple_1.brain.costfunction(desiredoutput), 2)
    print( "Error:", errorlist[3])
    meeple_1.brain.backpropegateOnline(desiredoutput, 0.05)

    print("\nAverage error:", sum(errorlist)/4)





print("\n\nEnd of main")