
from meeple import Meeple
import numpy as np


class Species:
    def __init__(self, speciesID, meep:Meeple  ):
        self.speciesID = speciesID
        self.bestMeeple:Meeple = meep
        self.meeples:list = [meep]

        self.similairy_threshold_total = 0.50 # 1 = 100%
        self.similairy_threshold_gene = 1 # 1 = 1

        self.staleness = 0 # stagnation
        self.fitnessSum = 0
        self.averageFitness = 0
        self.bestFitness = 0


    def addToSpecies(self, meep:Meeple):
        self.meeples.append(meep)


    def checkSimilarSpecies(self, meep:Meeple)->bool:
        temp = self.bestMeeple.brain
        totalgenes = temp.getAmountWeights()

        similair_genes = self.getAmtSimilarGenes(self.bestMeeple, meep)

        if (similair_genes/totalgenes) >= self.similairy_threshold_total:
            return True
        else:
            return False

    def sortSpecie(self):
        self.meeples.sort(key=lambda meep: meep.fitness, reverse=True)

        if self.bestMeeple is not Meeple:
            self.bestMeeple = self.meeples[0].clone()
        elif self.bestMeeple.fitness > self.meeples[0].fitness:
            self.bestMeeple = self.meeples[0].clone()
        else: self.staleness+=1


    # Returns the number of weights that are the same between two meeples
    # The weights are the genes
    def getAmtSimilarGenes(self, meep1:Meeple, meep2:Meeple)->float:
        similairweights:float = 0.0

        # must assume hidden layers are the same.
        if meep1.brain.hidden_layers[0] is not 0 and meep2.brain.hidden_layers[0] is not 0:
            #go through all the layers
            for meep1_layer, meep2_layer in zip(meep1.brain.hidden_layers, meep2.brain.hidden_layers):
                #go through all the nodes
                for meep1_node, meep2_node in zip(meep1_layer, meep2_layer):
                    #go through all the weights
                    for meep1_weight, meep2_weight in zip(meep1_node.weights, meep2_node.weights):
                        if (meep1_weight > 0) == (meep2_weight > 0): # test if both variables have the same sign
                            if abs(meep1_weight - meep2_weight) < self.similairy_threshold_gene:
                                similairweights += 1

                            #elif (meep1_weight > 0) == (meep2_weight > 0):
                            #    difweights+=2/(meep1_weight-meep2_weight**1+1)
                            #    pass

        else:
            #no hidden layers
            pass

        for meep1_node, meep2_node in zip(meep1.brain.output_layer, meep2.brain.output_layer):
            # go through all the weights
            for meep1_weight, meep2_weight in zip(meep1_node.weights, meep2_node.weights):
                if (meep1_weight > 0) == (meep2_weight > 0): # test if both variables have the same sign
                    if abs(meep1_weight - meep2_weight) < self.similairy_threshold_gene:
                        similairweights += 1


        return similairweights


    # Returns the average weight diffirence between meeples.
    def averageWeightDiff(self, meep1:Meeple, meep2:Meeple):
        # fakeTODO: not needed at the moment
        return float("inf")

    def selectParent(self)->Meeple:
        rand = np.random.randint(0, self.fitnessSum)
        runningSum = 0
        for i in range(len(self.meeples)):
            runningSum +=  self.meeples[i].fitness
            if runningSum > rand:
                return self.meeples[i]

        # Unreachable code. If it is reached anyway, something terrible has happened
        raise Exception("No suitable parent could be selected, but this is is impossible, so there's a bug somehere in the code. Happy hunting. o/")
        #return self.meeples[0]

    def generateChild(self)->Meeple:
        child:Meeple

        if np.random.rand() < 0.25:
            child = self.selectParent().clone()
        else:
            parent1:Meeple = self.selectParent()
            parent2:Meeple = self.selectParent()
            if parent1.fitness > parent2.fitness:
                child = parent1.crossover(parent2)
            else:
                child = parent2.crossover(parent1)

        child.brain.mutate()

        return child



    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for i in range(len(self.meeples)):
            self.fitnessSum += self.meeples[i].fitness

    def generateAverageFitness(self):
        self.calculateFitnessSum()
        self.averageFitness = self.fitnessSum/len(self.meeples)

    def cull(self):
        #self.sortSpecie()
        if len(self.meeples) > 2:
            self.meeples[:] = self.meeples[0:len(self.meeples)//2]







if __name__ == "__main__":
    meep1 = Meeple(786,tuple([200,200,200]),20)
    meep2 = Meeple(786,tuple([200,200,200]),20)

    genes1 = meep1.brain.getAmountWeights()
    genes2 = meep2.brain.getAmountWeights()
    specie1 = Species(meep1)
    similar_genes = specie1.getAmtSimilarGenes(meep1, meep2)

    print( "genes =", genes1, "|genes =", genes2, "| similar genes = ", similar_genes )
    print( "similarity =", round((similar_genes/genes1)*100, 2), "%" )