import math
import numpy as np
import pyglet
import copy
from pyglet.gl import *


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
        self.batch = pyglet.graphics.Batch()
        self.fitness = 0

        #self.input_layer = [None]*input_size
        self.input_layer:np.ndarray = np.ndarray([self.input_size], Node)
        for i in range(self.input_size):
            self.input_layer[i] = Node(0, batch=self.batch, isHollow=isHollow)
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
                    self.hidden_layers[layeri][i] = Node(1, temp_lastlayer_size, batch=self.batch, isHollow=isHollow)
                #set bias node
                self.hidden_layers[layeri][-1].intensity = 1
                temp_lastlayer_size = self.hidden_size[layeri]


        self.output_layer:np.ndarray = np.ndarray([self.output_size], Node)
        for i in range(self.output_size):
            self.output_layer[i] = Node(2, self.hidden_size[-1], batch=self.batch, isHollow=isHollow)






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
    def set_inputs(self, inputlist):
        if len(inputlist) != self.input_layer.size-1:
            print("Neuralnetwork.set_inputs: inputlist is diffirent size than self.input_layer.size!")

        for node_i in range(len(inputlist)):
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

    def mutate(self,mutatechance=1/30, mutatestrength=2):
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


    # Can only be used if there is a new output in that moment.
    # Use after having set inputs and firing the network! Otherwise this doesn't work as intended!
        # The amount that a weight needs to change is delta_cost/delta_weight = delta_intensity/delta_weight * delta_activation/delta_intensity * delta_activation/delta_cost
        # This goes from right to left and can be 'easily' chained.
    def backpropegateOnline(self, desired_output, learnrate):

        DeltaHiddenLayersWeights: np.array = np.ndarray([1])
        DeltaHiddenLayersIdealIntensities: np.array = np.ndarray([1])

        if self.hidden_layers[0] is not 0:
            layer_next = self.hidden_layers[-1]
        else:
            layer_next = self.input_layer


        DeltaOutputWeights:np.array = np.ndarray([self.output_layer.size, layer_next.size], dtype=float)

        if self.hidden_layers[0] is not 0:
            DeltaHiddenLayersWeights:np.array = [np.ndarray([layer.size, layer[0].weights.size],float) for layer in self.hidden_layers]
            DeltaHiddenLayersIdealIntensities:np.array = [np.ndarray([layer.size],float) for layer in self.hidden_layers]

        # Making the delta image ----------

        #Move through the output layer
        for nodei in range(self.output_layer.size):
            dCost = 2*(self.output_layer[nodei].intensity - desired_output[nodei] )
            Intensity = self.output_layer[nodei].intensity
            if Intensity <= 0:
                dActivation = 0
            else:
                dActivation = 1

            for weighti in range(layer_next.size):

                dIntensity = layer_next[weighti].intensity # intensity of node of preceding layer

                d1_temp =   dIntensity * dCost * -1 #* dActivation
                DeltaOutputWeights[nodei, weighti] = d1_temp * learnrate

                if self.hidden_layers[0] is not 0:
                    dIntensityL1 = self.output_layer[nodei].weights[weighti]
                    d2_temp = dIntensityL1 * dCost * -1# * dActivation
                    DeltaHiddenLayersIdealIntensities[-1][nodei] = d2_temp * learnrate

        #Move through the hidden layers

        if self.hidden_layers[0] is not 0:

            for layer_cur_i in range(len(self.hidden_layers)-1, 0): #move in reverse. 'last' layer has already been handled above if there are hidden layers.
                if layer_cur_i == 0:
                    layer_next = self.input_layer
                else:
                    layer_next = self.hidden_layers[layer_cur_i-1]

                for nodei in range(self.hidden_layers[layer_cur_i].size):
                    #TODO dcost = 2*(current node - nudge to node)
                    dCost = 2*(self.hidden_layers[layer_cur_i][nodei].intensity - DeltaHiddenLayersIdealIntensities[layer_cur_i][nodei] )
                    Intensity = self.hidden_layers[layer_cur_i][nodei].intensity
                    if Intensity <= 0:
                        dActivation = 0
                    else:
                        dActivation = 1

                    for weighti in range(layer_next.size):

                        dIntensity = layer_next[weighti].intensity # intensity of node of preceding layer

                        d1_temp =   dIntensity * dActivation * dCost * -1
                        DeltaHiddenLayersWeights[layer_cur_i][nodei, weighti] = d1_temp * learnrate

                        if self.hidden_layers[0] is not 0:
                            dIntensityL1 = self.output_layer[nodei].weights[weighti]
                            d2_temp = dIntensityL1 * dActivation * dCost * -1
                            DeltaHiddenLayersIdealIntensities[layer_cur_i+1, nodei] = d2_temp * learnrate




        # Applying the delta image ----------


        if self.hidden_layers[0] is not 0:
            precedinglayer = self.hidden_layers[-1]
        else:
            precedinglayer = self.input_layer

        for nodei in range(self.output_layer.size):
            for weighti in range(precedinglayer.size):
                self.output_layer[nodei].weights[weighti] += DeltaOutputWeights[nodei, weighti]

        if self.hidden_layers[0] is not 0:
            for layeri in range(len(self.hidden_layers), 0): # the layers of the delta image happen in reverse
                for nodei in range(self.hidden_layers[layeri].size):
                    for weighti in range(self.hidden_layers[layeri][nodei].weights.size):
                        self.output_layer[nodei].weights[weighti] += DeltaHiddenLayersWeights[layeri][nodei, weighti]


    def pickle(self):
        pass
        # TODO: Save this NN for later use.

    def unpickle(self):
        pass
        # TODO: Load to put data in this NN
        #   Maybe also a better way than how clone does it?

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





    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------


    # Draw the neural network on a window
    def draw(self):
        self.batch.draw()

    # Tries to position the nodes of the neural network using Pyglet at this position, within these dimentions
    def updateposGFX(self, pos, dim):
        self.pos = pos
        self.dim = dim

        #position input nodes
        temp_am_nodes = len(self.input_layer)
        for nodei in range(temp_am_nodes):
            self.input_layer[nodei].sprite.update(int(pos[0]),
                                                  int(pos[1]-(dim[1]/temp_am_nodes)*nodei))
        if self.hidden_layers[0] is not 0:
            #position hidden layers' nodes
            am_layers = len(self.hidden_layers)+1
            for layeri in range(len(self.hidden_layers)):
                #position the hidden layer layeri nodes
                temp_am_nodes = len(self.hidden_layers[layeri])
                for nodei in range(temp_am_nodes):
                    self.hidden_layers[layeri][nodei].sprite.update(int(pos[0]+dim[0]/am_layers*(layeri+1)),
                                                                int(pos[1]-(dim[1]/temp_am_nodes)*nodei))

        #position output nodes
        temp_am_nodes = len(self.output_layer)
        for nodei in range(temp_am_nodes):

            new_y = int(pos[1]-(dim[1]/temp_am_nodes)*nodei)

            self.output_layer[nodei].sprite.update(int(pos[0]+dim[0]),
                                                   new_y)

    # Draws the edges (weights) of the neural network
    def updateedgesGFX(self):
        glLineWidth(2)
        edgebatch = pyglet.graphics.Batch()
        # first hidden layer is special as it accesses input layer things
        previous_layer = self.input_layer
        if self.hidden_layers[0] is not 0:
            for layeri in range(len(self.hidden_layers)):
                for fromnodei in range(self.hidden_layers[layeri].size-1):
                    #tonodei can also be used to get the weights
                    for tonodei in range(previous_layer.size):
                        weight = self.hidden_layers[layeri][fromnodei].weights[tonodei]
                        if weight < 0:
                            weight*=-1
                            #RGB
                            col = (0, 0, 255,
                                   0, 0, 255)
                            #glLineWidth(weight)
                        elif weight == 0:
                            continue
                            #col = (255, 255, 255,
                            #       255, 255, 255)
                            #glLineWidth(1)
                        else: # weight > 0:
                            col = (255, 0, 0,
                                   255, 0, 0)
                            #glLineWidth(weight)

                        edgebatch.add(2, GL_LINES, None, ('v2i', (previous_layer[tonodei].sprite.x+10,
                                                            previous_layer[tonodei].sprite.y + 10,
                                                            self.hidden_layers[layeri][fromnodei].sprite.x + 10,
                                                            self.hidden_layers[layeri][fromnodei].sprite.y + 10)
                                                    ),
                                                    ('c3B',col)
                                      )
                previous_layer = self.hidden_layers[layeri]


        if self.hidden_layers[0] is not 0:
            # last hidden layer to output layer
            for fromnodei in range(len(self.hidden_layers[-1])):
                #tonodei can also be used to get the weights
                for tonodei in range(len(self.output_layer)):

                    weight =self.output_layer[tonodei].weights[fromnodei]
                    if weight < 0:
                        weight*=-1
                        #RGB
                        col = (0, 0, 255,
                               0, 0, 255)
                        #glLineWidth(weight)
                    elif weight == 0:
                        continue
                        #col = (255, 255, 255,
                        #       255, 255, 255)
                        #glLineWidth(1)
                    else:# weight > 0:
                        col = (255, 0, 0,
                               255, 0, 0)
                        #glLineWidth(weight)

                    edgebatch.add(2, GL_LINES, None, ('v2i', (self.output_layer[tonodei].sprite.x+10,
                                                        self.output_layer[tonodei].sprite.y + 10,
                                                        self.hidden_layers[-1][fromnodei].sprite.x + 10,
                                                        self.hidden_layers[-1][fromnodei].sprite.y + 10)
                                                ),
                                               ('c3B', col)
                                  )
        else:
            # No hidden layers, so connect from input to output
            for fromnodei in range(self.input_layer.size):
                #tonodei can also be used to get the weights
                for tonodei in range(self.output_layer.size):

                    weight =self.output_layer[tonodei].weights[fromnodei]
                    if weight < 0:
                        weight*=-1
                        #RGB
                        col = (0, 0, 255,
                               0, 0, 255)
                        #glLineWidth(weight+1)
                    elif weight == 0:
                        continue
                        #col = (255, 255, 255,
                        #       255, 255, 255)
                        #glLineWidth(1)
                    else:# weight > 0:
                        col = (255, 0, 0,
                               255, 0, 0)
                        #glLineWidth(weight+1)

                    edgebatch.add(2, GL_LINES, None, ('v2i', (self.output_layer[tonodei].sprite.x+10,
                                                        self.output_layer[tonodei].sprite.y + 10,
                                                        self.input_layer[fromnodei].sprite.x + 10,
                                                        self.input_layer[fromnodei].sprite.y + 10)
                                                ),
                                               ('c3B', col)
                                  )
        edgebatch.draw()

    # Update the graphical intensities of the neurons
    def updateintensityGFX(self, intensmods:tuple=None):

        if intensmods is None:
            intensmods = tuple([1]*self.input_layer.size)
        else:
            intensmods = tuple( list(intensmods))

        if len(intensmods) != self.input_layer.size-1:
            raise ValueError

        # update intensities of input nodes
        temp_am_nodes = len(self.input_layer)
        for nodei in range(temp_am_nodes-1):
            intens = self.input_layer[nodei].intensity
            intens = min(intens*intensmods[nodei], 255)
            self.input_layer[nodei].sprite.color = (intens,intens,intens)

        if self.hidden_layers[0] is not 0:
            # update intensities of hidden layer nodes
            for layeri in range(len(self.hidden_layers)):
                for nodei in range(len(self.hidden_layers[layeri])):
                    intens = self.hidden_layers[layeri][nodei].intensity
                    intens = min(intens*255, 255)
                    self.hidden_layers[layeri][nodei].sprite.color = (intens,intens,intens)

        # update intensities of output nodes
        temp_am_nodes = len(self.output_layer)
        for nodei in range(temp_am_nodes):
            intens = self.output_layer[nodei].intensity
            intens = min(intens*255, 255)
            self.output_layer[nodei].sprite.color = (intens,intens,intens)
            #if self.output_layer[nodei].intensity >= 1:
            #    self.output_layer[nodei].sprite.image = image_whiteneuron
            #else:
            #    self.output_layer[nodei].sprite.image = image_blackneuron

        self.updateedgesGFX()

    # ------------------------ END OF GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    # ------------------------ END OF GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    # ------------------------ END OF GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    # ------------------------ END OF GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    # ------------------------ END OF GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------





image_whiteneuron = pyglet.resource.image("resources/" + "whiteneuron.png")

class Node:
    ids = [-1]
    def __init__(self, layer:int, parent_size=0, batch=None, isHollow=False, weights=None):
        self.layer = layer
        self.intensity = 0

        if isHollow:
            #If hollow, innitialize empty weights array
            self.weights = np.zeros(parent_size, dtype=float)
        elif weights is None:
            #If not hollow and no weights are provided, initiallize random weights
            self.weights = np.random.uniform(-5,5,[parent_size,])
        else:
            #Else use weights provided
            self.weights=weights

        self.sprite = pyglet.sprite.Sprite(image_whiteneuron, x=0,
                                                              y=0,
                                           batch=batch )

if __name__ == "__main__":
    oldbrain = NeuralNetwork(4,tuple([0]),16)
    newbrain = oldbrain.clone()
    temp = False


