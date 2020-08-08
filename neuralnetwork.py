import math
import numpy as np

from pyglet.gl import *
from typing import List

import serpent
import copy


# atm code needs to be rewritten to use numba, but reading it up, it looks promising as a quick&dirty solution
#import numba as nb
#performance-debug info
#import llvmlite.binding as llvm
#llvm.set_option('', '--debug-only=loop-vectorize')


class NeuralNetwork:

    def __init__(self, input_size:int, hidden_size:tuple, output_size:int, isHollow=False):

        self.input_size = input_size+1
        if hidden_size[0] > 0:
            self.hidden_size = tuple([x+1 for x in hidden_size])
        else:
            self.hidden_size = hidden_size
        self.output_size = output_size

        self.pos:tuple = (0,0)
        self.dim:tuple = (0,0)
        #self.fitness = float("-inf")
        #self.score = float("-inf")
        self.fitness = 0
        self.score = 0

        #self.input_layer = [None]*input_size
        self.input_layer:np.ndarray = np.ndarray([self.input_size], Node)
        for i in range(self.input_size):
            self.input_layer[i] = Node(0, isHollow=isHollow)
        #set bias node
        self.input_layer[-1].intensity = 1


        self.hidden_layers:list
        if self.hidden_size[0] == 0: # Can do this, because there is no point in having a hidden layer with 0 nodes!
            self.hidden_layers = [0]
            self.hidden_size = tuple([self.input_size])
        else:
            # make the list with layers (np.ndarray)
            self.hidden_layers = [np.ndarray([x], Node) for x in self.hidden_size]
            # Go through each layer, then through each Node slot, construct a node and put it in the slot
            temp_lastlayer_size = self.input_size
            for layeri in range(len(self.hidden_layers)):
                for i in range(self.hidden_size[layeri]):
                    self.hidden_layers[layeri][i] = Node(1, temp_lastlayer_size, isHollow=isHollow)
                #set bias node
                self.hidden_layers[layeri][-1].intensity = 1
                temp_lastlayer_size = self.hidden_size[layeri]


        self.output_layer:np.ndarray = np.ndarray([self.output_size], Node)
        for i in range(self.output_size):
            self.output_layer[i] = Node(2, self.hidden_size[-1], isHollow=isHollow)






    # Fires all input nodes
    def fire_network(self):

        previous_layer = self.input_layer


        if self.hidden_layers[0] is not 0:
            for layeri in range(len(self.hidden_layers)):
                for nodei in range(self.hidden_layers[layeri].size-1):
                    temp=0
                    for weighti in range(self.hidden_layers[layeri][nodei].weights.shape[0]):
                        temp+=previous_layer[weighti].intensity*self.hidden_layers[layeri][nodei].weights[weighti]
                    self.hidden_layers[layeri][nodei].intensity = self.ReLU(temp)
                previous_layer = self.hidden_layers[layeri]

        for nodei in range(self.output_layer.size):
            temp=0 # Sum of weights and intensities

            for weighti in range(self.output_layer[nodei].weights.shape[0]):
                temp+=previous_layer[weighti].intensity*self.output_layer[nodei].weights[weighti]
            self.output_layer[nodei].intensity = self.ReLU(temp)

    # simplified version to get output intensities
    def get_output(self, num:int):
        return self.output_layer[num].intensity

    # get all values of all output nodes in order
    def get_outputs(self):
        return [node.intensity for node in self.output_layer]

    # don't set inputs directly! would put them on private, but Python has no privates
    def set_input(self, num:int, intense:float):
        self.input_layer[num].intensity = intense

    # set all values of all output nodes in order
    # if the list is shorter than the input layer, last nodes won't be updated
    # if the list is longer than the input layer, crash?
    def set_inputs(self, inputlist:np.ndarray):
        # If this gives an error, then inputlist is not the same size as the inputlayer-1
        for node_i in range(inputlist.size):
            self.input_layer[node_i].intensity = inputlist[node_i]



    @staticmethod
    def Sigmoid(x:float):
        return 1 / (1+math.e**-x)

    @staticmethod
    def ReLU(x:float):
        return np.maximum(0, x)
        #return max(0, min(x,1))

    @staticmethod
    def ReLUd(x:float):
        if x <= 0:
            return 0
        else:
            return 1
        #return max(0, min(x,1))

    @staticmethod
    def Sigmoidi(x:float):
        temp = 1 / (1+math.e**-x)
        if temp > 0.5:
            return 1
        else:
            return 0


    def mutate(self,mutatechance=1/30, mutatestrength=1):
        for nodei in range(self.input_layer.size):
            for weighti in range(self.input_layer[nodei].weights.size):
                if np.random.rand() <= mutatechance:
                    #self.input_layer[nodei].weights[weighti] = np.random.uniform(-5,5)
                    if np.random.rand() < 0.5:
                        self.input_layer[nodei].weights[weighti] += np.random.uniform(0,mutatestrength)
                    else:
                        self.input_layer[nodei].weights[weighti] -= np.random.uniform(0,mutatestrength)

        if self.hidden_layers[0] is not 0:
            for layeri in range(len(self.hidden_layers)):
                for nodei in range(self.hidden_layers[layeri].size):
                    for weighti in range(self.hidden_layers[layeri][nodei].weights.size):
                        if np.random.rand() <= mutatechance:
                            #self.hidden_layers[layeri][nodei].weights[weighti] = np.random.uniform(-5,5)
                            if np.random.rand() < 0.5:
                                self.hidden_layers[layeri][nodei].weights[weighti] += np.random.uniform(0,mutatestrength)
                            else:
                                self.hidden_layers[layeri][nodei].weights[weighti] -= np.random.uniform(0,mutatestrength)

        for nodei in range(self.output_layer.size):
            for weighti in range(self.output_layer[nodei].weights.size):
                if np.random.rand() <= mutatechance:
                    #self.output_layer[nodei].weights[weighti] = np.random.uniform(-5,5)
                    if np.random.rand() < 0.5:
                        self.output_layer[nodei].weights[weighti] += np.random.uniform(0,mutatestrength)
                    else:
                        self.output_layer[nodei].weights[weighti] -= np.random.uniform(0,mutatestrength)


    def clone(self):
        if self.hidden_layers[0] is not 0:
            temp = NeuralNetwork(self.input_size-1,
                                 tuple([x-1 for x in self.hidden_size]),
                                 self.output_size,
                                 isHollow=True)
        else:
            temp = NeuralNetwork(self.input_size-1,
                                 tuple([0]),
                                 self.output_size,
                                 isHollow=True)

        #clone ... what? the inputlayer has no weights.
        #for nodei in range(self.input_layer.size):
        #    temp.input_layer[nodei].weights = copy.deepcopy(self.input_layer[nodei].weights)

        if self.hidden_layers[0] is not 0:
            for layeri in range(len(self.hidden_layers)):
                for nodei in range(self.hidden_layers[layeri].size):
                    temp.hidden_layers[layeri][nodei].weights = copy.deepcopy(self.hidden_layers[layeri][nodei].weights)
        else:
            temp.hidden_layers = [0]

        for nodei in range(self.output_layer.size):
            temp.output_layer[nodei].weights = copy.deepcopy(self.output_layer[nodei].weights)

        return temp


    def crossover(self, parent2):
        child:NeuralNetwork

        if self.hidden_layers[0] is not 0:
            child = NeuralNetwork(self.input_size - 1,
                                 tuple([x - 1 for x in self.hidden_size]),
                                 self.output_size,
                                 isHollow=True)
        else:
            child = NeuralNetwork(self.input_size - 1,
                                 tuple([0]),
                                 self.output_size,
                                 isHollow=True)

        if self.hidden_layers[0] is not 0:
            for layeri in range(len(self.hidden_layers)):
                for nodei in range(self.hidden_layers[layeri].size):
                    for weighti in range(child.hidden_layers[layeri][nodei].weights.shape[0]):
                        if np.random.rand() < 0.50:
                            child.hidden_layers[layeri][nodei].weights[weighti] = self.hidden_layers[layeri][nodei].weights[weighti]
                        else:
                            child.hidden_layers[layeri][nodei].weights[weighti] = parent2.hidden_layers[layeri][nodei].weights[weighti]
        else:
            child.hidden_layers = [0]

        for nodei in range(self.output_layer.size):
            for weighti in range(self.output_layer[nodei].weights.shape[0]):
                if np.random.rand() < 0.50:
                    child.output_layer[nodei].weights[weighti] = self.output_layer[nodei].weights[weighti]
                else:
                    child.output_layer[nodei].weights[weighti] = parent2.output_layer[nodei].weights[weighti]

        return child


    def costfunction(self, correct_output:np.array)->float:
        if len(correct_output) != self.output_layer.size:
            raise ValueError
            # can't test error score if the 2 node arrays don't match in length
        total=0
        for cor_val, output_node in zip(correct_output, self.output_layer):
            total+= (output_node.intensity - cor_val)**2

        return total


    def train(self, training_data, training_answers, learnrate):

        deltaimages=None

        if len(training_data.shape) == 1:
            deltaimages = self.GradientDecentDelta(training_input=training_data, desired_output=training_answers)
        else:
            for data, answer in zip(training_data, training_answers):
                deltaimages = self.GradientDecentDelta(training_input=data, desired_output=answer, deltaimages=deltaimages)



        if isinstance(deltaimages, np.ndarray):
            self.ApplyGradientDecentDelta(learnrate, deltaimages, batchsize=training_data.shape[0])
        elif isinstance(deltaimages, tuple):
            self.ApplyGradientDecentDelta(learnrate, deltaimages[0], deltaimages[1], batchsize=training_data.shape[0])


    # Can only be used if there is a new output in that moment.
    # Use after having set inputs and firing the network! Otherwise this doesn't work as intended!
        # The amount that a weight needs to change is delta_cost/delta_weight = delta_intensity/delta_weight * delta_activation/delta_intensity * delta_activation/delta_cost
        # This goes from right to left and can be 'easily' chained.
    def GradientDecentDelta(self, training_input, desired_output, deltaimages=None):

        self.set_inputs(training_input)
        self.fire_network()

        DeltaHiddenLayersWeights:List[np.ndarray] = None
        DeltaNodeWeightsSums: np.ndarray = None
        DeltaOutputWeights: np.ndarray = None

        if self.hidden_layers[0] is not 0:
            layer_next = self.hidden_layers[-1]
        else:
            layer_next = self.input_layer

        if deltaimages is not None:
            if isinstance(deltaimages, np.ndarray):
                DeltaOutputWeights: np.ndarray = deltaimages
            elif isinstance(deltaimages, tuple):
                DeltaOutputWeights: np.ndarray = deltaimages[0]
                DeltaHiddenLayersWeights = deltaimages[1]
                DeltaNodeWeightsSums = np.array([np.zeros([layer.size],float) for layer in self.hidden_layers])
        else:
            DeltaOutputWeights:np.ndarray = np.zeros([self.output_layer.size, layer_next.size], dtype=float)
            if self.hidden_layers[0] is not 0:
                # [layeri][nodei, weighti]
                DeltaHiddenLayersWeights = [np.zeros([layer.size, layer[0].weights.size],float) for layer in self.hidden_layers]

        if self.hidden_layers[0] is not 0:
            # [layeri][nodei]
            DeltaNodeWeightsSums = np.array([np.zeros([layer.size],float) for layer in self.hidden_layers])

        # Making the delta image ----------

        # Move through the output layer to make its delta image
        for nodei in range(self.output_layer.size):
            dCost = 2*(self.output_layer[nodei].intensity - desired_output[nodei] )

            for weighti in range(layer_next.size):

                dIntensity = layer_next[weighti].intensity # intensity of node of preceding layer
#
                #if self.output_layer[nodei].intensity <= 0:
                #    dActivation = 0
                #else:
                #    dActivation = 1

                d1_temp =   dIntensity * dCost * -1# * dActivation
                DeltaOutputWeights[nodei, weighti] += d1_temp

                if self.hidden_layers[0] is not 0:
                    # [-1][weighti] the weighti is correct, because it's mapping from right to left!
                    DeltaNodeWeightsSums[-1][weighti] += self.output_layer[nodei].weights[weighti] * dCost# * dActivation

        #--------------

        # Move through the hidden layers to make its delta image
        if self.hidden_layers[0] is not 0:



            for layer_cur_i in range(len(self.hidden_layers)-1, -1, -1): #move in reverse. 'last' layer has already been handled above.
                if layer_cur_i == 0:
                    layer_prev = self.input_layer
                else:
                    layer_prev = self.hidden_layers[layer_cur_i-1]

                for nodei in range(self.hidden_layers[layer_cur_i].size-1):

                    for weighti in range(layer_prev.size):

                        dIntensity = layer_prev[weighti].intensity # intensity of node of preceding layer

                        #if self.hidden_layers[layer_cur_i][nodei].intensity <= 0:
                        #    dActivation = 0
                        #else:
                        #    dActivation = 1

                        # delta_cost
                        d1_temp = DeltaNodeWeightsSums[layer_cur_i][nodei] * dIntensity * -1# * dActivation
                        DeltaHiddenLayersWeights[layer_cur_i][nodei, weighti] = d1_temp

                        if self.hidden_layers[0] is not 0:
                            # [-1][weighti] the weighti is correct, because it's mapping from right to left!
                            if layer_cur_i > 0:
                                DeltaNodeWeightsSums[layer_cur_i-1][weighti] += self.hidden_layers[layer_cur_i][nodei].weights[weighti] * \
                                                                                DeltaNodeWeightsSums[layer_cur_i][nodei]# * dActivation


        if self.hidden_layers[0] is not 0:
            return DeltaOutputWeights, DeltaHiddenLayersWeights
        else:
            return DeltaOutputWeights

    def ApplyGradientDecentDelta(self, learnrate, DeltaOutputWeights, DeltaHiddenLayersWeights=None, batchsize=1):

        if self.hidden_layers[0] is not 0:
            precedinglayer = self.hidden_layers[-1]
        else:
            precedinglayer = self.input_layer

        for nodei in range(self.output_layer.size):
            for weighti in range(precedinglayer.size):
                self.output_layer[nodei].weights[weighti] += min( max((DeltaOutputWeights[nodei, weighti]/batchsize)  * learnrate, -4), 4 )

        if self.hidden_layers[0] is not 0:
            for layeri in range(len(self.hidden_layers)-1, -1, -1): # the layers of the delta image happen in reverse
                for nodei in range(self.hidden_layers[layeri].size):
                    for weighti in range(self.hidden_layers[layeri][nodei].weights.size):
                        self.hidden_layers[layeri][nodei].weights[weighti] += min( max((DeltaHiddenLayersWeights[layeri][nodei, weighti]/batchsize) * learnrate, -4), 4 )

    def serpent_serialize(self):

        if self.hidden_layers[0] is not 0:
            pickleblebrain = [[[None for j in range(self.hidden_layers[i].size)] for i in range(len(self.hidden_layers))],
                              [None for i in range(self.output_layer.size)]
                              ]

            # Get the weight lists from the hidden nodes
            for layer_i in range(len(pickleblebrain[0])):
                for node_i in range(len(pickleblebrain[0][layer_i])):
                    pickleblebrain[0][layer_i][node_i] = list(copy.deepcopy(self.hidden_layers[layer_i][node_i].weights))

            # Get the weight lists from the output nodes
            for i in range(len(pickleblebrain[1])):
                pickleblebrain[1][i] = list(copy.deepcopy(self.output_layer[i].weights))

            # TODO: Also pickle the fitness of the brain


        else:
            pickleblebrain = [None for i in range(self.output_layer.size)]

            # Get the weight lists from the output nodes
            for node_i in range(len(pickleblebrain)):
                pickleblebrain[node_i] = list(copy.deepcopy(self.output_layer[node_i].weights))

            # TODO: Also pickle the fitness of the brain

        pickledbrain = serpent.dumps([pickleblebrain, self.score])

        return pickledbrain


    def serpent_deserialize(self, pickledbrain):

        # TODO: Needs to also unpickle the fitness
        unpickledbrain = serpent.loads(serpent.tobytes(pickledbrain))
        self.score = unpickledbrain[1]
        unpickledbrain = unpickledbrain[0]


        if self.hidden_layers[0] is not 0:

            # Get the weight lists from the hidden nodes
            for layer_i in range(len(unpickledbrain[0])):
                for node_i in range(len(unpickledbrain[0][layer_i])):
                    self.hidden_layers[layer_i][node_i].weights = np.array(unpickledbrain[0][layer_i][node_i])

            # Get the weight lists from the output nodes
            for node_i in range(len(unpickledbrain[1])):
                self.output_layer[node_i].weights = np.array(unpickledbrain[1][node_i])
        else:

            for node_i in range(len(unpickledbrain)):
                self.output_layer[node_i].weights = np.array(unpickledbrain[node_i])


    def getAmountWeights(self)->int:

        totalWeights = 0


        if self.hidden_layers[0] is not 0:
            n_layers = [ self.input_layer.size ] + list(self.hidden_size) + [self.output_layer.size]

            for lsizei in range(1, len(n_layers)-1):
                totalWeights += n_layers[lsizei-1]*(n_layers[lsizei]-1)

            totalWeights += n_layers[-2] * n_layers[-1]


        else:
            totalWeights = self.input_layer.size * self.output_layer.size

        return totalWeights





class Node:
    ids = [-1]
    def __init__(self, layer:int, parent_size=0, isHollow=False, weights=None):
        self.layer = layer
        self.intensity = 0

        if isHollow:
            #If hollow, innitialize empty weights array
            self.weights = np.zeros(parent_size, dtype=float)
        elif weights is None:
            #If not hollow and no weights are provided, initiallize random weights
            self.weights = np.random.uniform(-1,1,[parent_size,])
            for weighti in range(self.weights.size):
                self.weights[weighti] *= math.sqrt(2/parent_size)
        else:
            #Else use weights provided
            self.weights=weights


        # TODO: removed this because it is a memory leak, stacking every generation
        #self.sprite = pyglet.sprite.Sprite(image_whiteneuron, x=0,
        #                                                      y=0,
        #                                   batch=batch )
        #self.sprite = None









if __name__ == "__main__":

    import timeit
    import cProfile
    print("Starting Neuralnetwork.py as main")
    import pickle

    print("Printing data old brain")
    oldbrain = NeuralNetwork(60,tuple([80,40,16]),16)
    oldbrain.set_inputs(np.array(range(60)))

    p = cProfile.Profile()
    #p.runctx('oldbrain.ReLU(x)', locals={'x': 5}, globals={'oldbrain':oldbrain} )
    p.runcall(oldbrain.fire_network)
    p.print_stats()

    print("Finished Neuralnetwork.py as main")


