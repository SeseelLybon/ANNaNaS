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


meeple_1 = Meeple( 1, tuple([1]), 1)

epochs = 10
for i in range(epochs):
    print("\nEpoch", i, "\n")
    desiredoutput = np.array([0])
    meeple_1.brain.set_inputs([1])
    meeple_1.brain.fire_network()
    print( "Desired:", desiredoutput)
    print( "Brain says:", meeple_1.brain.get_outputs())
    print( "Error:", meeple_1.brain.costfunction(desiredoutput))
    meeple_1.brain.backpropegate(desiredoutput)


    #desiredoutput = np.array([1])
    #meeple_1.brain.set_inputs([0])
    #meeple_1.brain.fire_network()
    #print( "Desired:", desiredoutput)
    #print( "Brain says:", meeple_1.brain.get_outputs())
    #print( "Error:", meeple_1.brain.costfunction(desiredoutput))
    #meeple_1.brain.backpropegate(desiredoutput)








print("\n\nEnd of main")