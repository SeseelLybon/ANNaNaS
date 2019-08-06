
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


class KnapsackBruteForce:

    @classmethod
    def knapSack(cls, W, wt, val, n):

        if n == 0 or W == 0:
            return 0

        if (wt[n - 1] > W):
            return cls.knapSack(W, wt, val, n - 1)


        else:
            return max(val[n - 1] + cls.knapSack(W - wt[n - 1], wt, val, n - 1),
                       cls.knapSack(W, wt, val, n - 1))


temp1set = set()
while len(temp1set) < 100:
    temp1set.add( Item(np.random.randint(1,30), np.random.randint(1,30)) )

items_list = np.array( list(temp1set), Item)


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

if __name__ == "__main__":
    values = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4]
    wt = [1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4]
    weight = 2
    n = len(values)
    print(KnapsackBruteForce.knapSack(weight, wt, values, n))

