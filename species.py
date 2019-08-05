
from meeple import Meeple


class Species:
    def __init__(self, meep:Meeple ):
        self.bestMeeple:Meeple = meep
        self.meeples:list = [meep]


    def checkSameSpecies(self, meep:Meeple):
        pass


    # Returns the number of weights that are not the same between two meeples
    # The weights are the genes
    @staticmethod
    def getExcessDisjoint(meep1:Meeple, meep2:Meeple)->float:
        difweights:float = 0.0

        # TODO: Currently returns the nodes that match, not the amount that doesn't.
        #   Does this matter though?

        # must assume hidden layers are the same.
        if meep1.brain.hidden_layers[0] != 0 and meep2.brain.hidden_layers[0] != 0:
            #go through all the layers
            for meep1_layer, meep2_layer in zip(meep1.brain.hidden_layers, meep2.brain.hidden_layers):
                #go through all the nodes
                for meep1_node, meep2_node in zip(meep1_layer, meep2_layer):
                    #go through all the weights
                    for meep1_weight, meep2_weight in zip(meep1_node.weights, meep2_node.weights):
                        if meep1_weight == meep2_weight:
                            difweights+=1
                            pass
                        elif (meep1_weight > 0) == (meep2_weight > 0):
                            difweights+=2/(meep1_weight-meep2_weight**1+1)
                            pass
                        else:
                            #Give no points
                            pass

        else:
            #no hidden layers
            pass

        for meep1_node, meep2_node in zip(meep1.brain.output_layer, meep2.brain.output_layer):
            # go through all the weights
            for meep1_weight, meep2_weight in zip(meep1_node.weights, meep2_node.weights):
                if (meep1_weight > 0) == (meep2_weight > 0):
                    if (meep1_weight - meep2_weight) < 0.2:
                        difweights += 1
                    pass

                #elif (meep1_weight > 0) == (meep2_weight > 0):
                #    #difweights += 1 / ((meep1_weight - meep2_weight) ** 2 + 1)
                #    # TODO: ALt; if they're closer than 25% in the same sign, they still get a point
                #    pass
                #else:
                #    # Give no points
                #    pass


        return difweights


    # Returns the average weight diffirence between meeples.
    @staticmethod
    def averageWeightDiff(meep1:Meeple, meep2:Meeple):
        # TODO: Finish code
        return float("inf")


if __name__ == "__main__":
    meep1 = Meeple(4,tuple([0]),16)
    meep2 = Meeple(4,tuple([0]),16)
    print(Species.getExcessDisjoint(meep1, meep2))