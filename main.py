#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np

from population import Population

from meeple import Meeple



meeple_1 = Meeple( 1, tuple([1]), 1)

score = 0

meeple_1.brain.set_input(0, 1)
meeple_1.brain.fire_network()
print( "Brain says:", meeple_1.brain.get_output(0))
print( "Error:", meeple_1.brain.errorscore(np.array([0])))
#meeple_1.brain.backpropegate(np.array([1]))


meeple_1.brain.set_input(0, 0)
meeple_1.brain.fire_network()
print( "Brain says:", meeple_1.brain.get_output(0))
print( "Error:", meeple_1.brain.errorscore(np.array([1])))








logging.critical("End of main")