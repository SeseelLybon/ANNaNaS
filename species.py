
from meeple import Meeple
import numpy as np


class Species:
    def __init__(self, speciesID, meep:Meeple  ):
        self.speciesID = speciesID
        self.bestMeeple:Meeple = meep
        self.meeples:list = [meep]
        self.sizeChromosome = meep.brain.getAmountWeights()

        self.similairy_threshold_total = 0.90 # 1 = 100%
        self.similairy_threshold_gene = 1 # 1 = 1
        self.mutateChance = 1/40    # 1 = 100%
        self.mutateStrength = 0.5

        self.staleness = 0 # stagnation
        self.fitnessSum = 0
        self.averageFitness = 0
        self.bestFitness = 0


    def addToSpecies(self, meep:Meeple):
        self.meeples.append(meep)


    def checkSimilarSpecies(self, meep:Meeple)->bool:
        temp = self.bestMeeple.brain

        similair_genes = self.getAmtSimilarGenes(self.bestMeeple, meep)

        if (similair_genes/self.sizeChromosome) >= self.similairy_threshold_total:
            return True
        else:
            return False

    def sortSpecie(self):
        self.meeples.sort(key=lambda meep: meep.brain.fitness, reverse=True)

        if self.bestFitness < self.meeples[0].brain.fitness:
            self.bestFitness = self.meeples[0].brain.fitness
            self.bestMeeple = self.meeples[0]
            self.staleness=0
        else:
            self.staleness+=1


    # Returns the number of weights that are the same between two meeples
    # The weights are the genes
    def getAmtSimilarGenes(self, meep1:Meeple, meep2:Meeple)->float:
        similairweights:float = 0.0

        #if meep1.brain.input_size == meep2.brain.input_size and \
        #    meep1.brain.hidden_size == meep2.brain.hidden_size and \
        #    meep1.brain.output_size == meep2.brain.output_size and \
        #    meep1.brain.getAmountWeights() == meep2.brain.getAmountWeights():

        if meep1.brain.input_size == meep2.brain.input_size and \
           meep1.brain.hidden_size == meep2.brain.hidden_size and \
           meep1.brain.output_size == meep2.brain.output_size:

            if meep1.brain.hidden_size[0] != 0:
                # crossover the hidden layers
                for hli in range(len(meep1.brain.hidden_size)):  # hli: hidden layer index
                    # crossover the output layer
                    temp_P1 = meep1.brain.model.layers[hli].get_weights()
                    temp_P2 = meep2.brain.model.layers[hli].get_weights()
                    for owi in range(len(temp_P1[0][hli])):  # owi; output weight index
                        # copy either the self or parent2 ***weight*** of this weight on this layer into the child
                        if (temp_P1[0][hli][owi] > 0) == (temp_P2[0][hli][owi] > 0): # test if both variables have the same sign
                            if abs(temp_P1[0][hli][owi] - temp_P2[0][hli][owi]) < self.similairy_threshold_gene:
                                similairweights += 1

            # mutate the output layer# crossover the output layer
            temp_P1 = meep1.brain.model.layers[-1].get_weights()
            temp_P2 = meep2.brain.model.layers[-1].get_weights()
            for owi in range(len(temp_P1[0][-1])):  # owi; output weight index
                # copy either the self or parent2 ***weight*** of this weight on this layer into the child
                if (temp_P1[0][-1][owi] > 0) == (temp_P2[0][-1][owi] > 0): # test if both variables have the same sign
                    if abs(temp_P1[0][-1][owi] - temp_P2[0][-1][owi]) < self.similairy_threshold_gene:
                        similairweights += 1

        else:
            pass


        return similairweights


    # Returns the average weight diffirence between meeples.
    def averageWeightDiff(self, meep1:Meeple, meep2:Meeple):
        # fakeTODO: not needed at the moment
        return float("inf")

    def selectParent(self)->Meeple:
        rand = np.random.randint(0, max(self.fitnessSum, 1))
        runningSum = 0
        for i in range(len(self.meeples)):
            runningSum +=  self.meeples[i].brain.fitness
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
            if parent1.brain.fitness > parent2.brain.fitness:
                child = parent1.crossover(parent2)
            else:
                child = parent2.crossover(parent1)

        child.brain.mutate(self.mutateChance, self.mutateStrength)

        return child



    def calculateFitnessSum(self):
        self.fitnessSum = 0
        for i in range(len(self.meeples)):
            self.fitnessSum += self.meeples[i].brain.fitness
        return

    def generateAverageFitness(self):
        self.calculateFitnessSum()
        self.averageFitness = round(self.fitnessSum/len(self.meeples), 1)

    def cull(self):
        #self.sortSpecie()
        if len(self.meeples) > 2:
            self.meeples[:] = self.meeples[0:len(self.meeples)//2]







#if __name__ == "__main__":
#    meep1 = Meeple(786,tuple([200,200,200]),20)
#    meep2 = Meeple(786,tuple([200,200,200]),20)
#
#    genes1 = meep1.brain.getAmountWeights()
#    genes2 = meep2.brain.getAmountWeights()
#    specie1 = Species(meep1)
#    similar_genes = specie1.getAmtSimilarGenes(meep1, meep2)
#
#    print( "genes =", genes1, "|genes =", genes2, "| similar genes = ", similar_genes )
#    print( "similarity =", round((similar_genes/genes1)*100, 2), "%" )