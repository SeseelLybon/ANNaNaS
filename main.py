#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import logging
import time
logging.basicConfig(level=logging.DEBUG)

from population import Population
from meeple import items_list
from meeple import items_total_size

sack_size = 850
pops = Population(100, sack_size)

timestart = time.time()

skipped_once = False
ongoing = True
for i in range(1000):

    print("--------------------------")
    print("Wipping up a new batch")
    pops.naturalSelection()
    print("startin generation", pops.generation)
    print("Best of generation is", pops.bestMeeple.fitness)
    sum_value = 0
    sum_size = 0
    for i in range(pops.bestMeeple.knapsack.size):
        if pops.bestMeeple.knapsack[i]:
            if sum_size+items_list[i].size > sack_size:
                break
            sum_size += items_list[i].size
            sum_value += items_list[i].value

    print("Value:",sum_value, "- Size:", sum_size)
print("Sack size =", sack_size)
print("Took", time.time()-timestart, "seconds")

print("End of main")