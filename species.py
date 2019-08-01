
from meeple import Meeple


class Species:
    def __init__(self, meep:Meeple ):
        self.bestMeeple:Meeple = meep
        self.meeples:list = [meep]


    def checkSameSpecies(self, meep:Meeple):
        pass


    # Returns the number of weights that are not the same between two meeples
    # The weights are the genes
    def getExcessDisjoint(self, meep1:Meeple, meep2:Meeple)->float:
        difweights:float = 0.0

        # TODO: Go through all the nodes of all the meep's brains

        meep1_last_layer = meep1.brain.input_layer
        meep2_last_layer = meep2.brain.input_layer

        # must assume hidden layers are the same.
        if meep1.brain.hidden_layers[0] == 0 and meep2.brain.hidden_layers[0] == 0:
            for meep1_layer, meep2_layer in zip(meep1.brain.hidden_layers, meep2.brain.hidden_layers):
                for meep1_node, meep2_node in zip(meep1_layer, meep2_layer):
                    for meep1_weight, meep2_weight in zip(meep1_node.weights):
                        if meep1_weight != meep2_weight:
                            # TODO: track how much they differ and how (sign matters most, then amount within sign)

        else:
            #no hidden layers
            pass


        return difweights


    # Returns the average weight diffirence between meeples.
    def averageWeightDiff(self, meep1:Meeple, meep2:Meeple):
        return float("inf")