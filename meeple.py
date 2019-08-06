
import numpy as np
import math
import random
from typing import List
from copy import deepcopy

class Meeple:
    def __init__(self, isHallow=False):

        self.fitness = float("-inf")

        self.knapsack = np.ndarray([len(items_list)], bool)

        if not isHallow:
            for i in range(self.knapsack.size):
                if np.random.rand() < 0.5:
                    self.knapsack[i]= False
                else:
                    self.knapsack[i]= True


    def clone(self): #->Meeple:
        child:Meeple = Meeple( isHallow=True )
        child.knapsack = deepcopy(self.knapsack)
        return child


    def crossover(self, parent2): #parent1:Meeple, parent2:Meeple) -> Meeple:

        tempKnapsack =  np.ndarray([len(items_list)], bool)

        for i in range(tempKnapsack.size):
            if np.random.rand() < 0.50:
                tempKnapsack[i] = self.knapsack[i]
            else:
                tempKnapsack[i] = parent2.knapsack[i]

        child: Meeple = Meeple( isHallow=True)
        child.knapsack = tempKnapsack

        return child


    def mutate(self):
        for i in range(self.knapsack.size):
            # 10% chance to flip the gene
            if np.random.rand() < 0.1:
                if self.knapsack[i]:
                    self.knapsack[i] = False
                else:
                    self.knapsack[i] = True


    def calcFitness(self, max_size):
        tempFitness = 0
        sum_value = 0
        sum_size = 0
        for i in range(self.knapsack.size):
            if self.knapsack[i]:
                if sum_size+items_list[i].size > max_size:
                    break
                sum_size += items_list[i].size
                sum_value += items_list[i].value

        # if the combined size is equal to the knapsack's size, we're filling optimally
        if sum_size == max_size:
            tempFitness = sum_value**2
        else:
            # else, pick the person with the size closest to the max.
            tempFitness = 1/((sum_size-max_size)**2)

        self.fitness = tempFitness


class Item:
    def __init__(self, size, value):
        self.size = size
        self.value = value

    def __repr__(self):
        return str(self.size) + ":" + str(self.value)

    def __hash__(self):
        return hash((self.size, self.value))

    def __eq__(self, other):
        if self.size == other.size and self.value == other.value:
            return True
        else:
            return False



#temp1set = set()
#while len(temp1set) < 100:
#    temp1set.add( Item(np.random.randint(1,30), np.random.randint(1,30)) )
#
#items_list = np.array( list(temp1set), Item)


# Following values are copied from https://developers.google.com/optimization/bin/knapsack
# to test if my own algoritm works.

values = [
    360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147,
    78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28,
    87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276,
    312
]
weights = [
    7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
    42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71,
    3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
]

items_list = list()
for value, weight in zip(values, weights):
    items_list.append( Item(weight, value) )

capacities = 850


#items_list = np.array( [Item(1, 1),
#                        Item(1, 2),
#                        Item(1, 3),
#                        Item(1, 4),
#                        Item(2, 1),
#                        Item(2, 2),
#                        Item(2, 3),
#                        Item(2, 4),
#                        Item(3, 1),
#                        Item(3, 2),
#                        Item(3, 3),
#                        Item(3, 4),
#                        Item(4, 1),
#                        Item(4, 2),
#                        Item(4, 3),
#                        Item(4, 4)
#                        ], Item)


items_total_size = 0
items_total_value = 0
for item in items_list:
    items_total_size += item.size
    items_total_value += item.value

