import logging
import math
import numpy as np
import pyglet
import copy
from pyglet.gl import *


class NeuralNetwork:

    def __init__(self, input_size=5, hidden_size=5, output_size=2, hollow=False):
        self.pos = (0,0)
        self.dim = (0,0)
        self.batch = pyglet.graphics.Batch()
        self.fitness = 0

        #self.input_layer = [None]*input_size
        self.input_layer = np.ndarray([input_size], Node)
        for i in range(input_size):
            self.input_layer[i] = Node(0, batch=self.batch, hollow=hollow)
        #set bias node
        self.input_layer[-1].intensity = 1

        if hidden_size == 0:# len(hidden_size) == 0:
            hidden_size = input_size
        else:
            self.hidden_layers = np.ndarray([1], np.ndarray)
            self.hidden_layers[0] = np.ndarray([hidden_size], Node)
            for i in range(hidden_size):
                self.hidden_layers[0][i] = Node(1, input_size, batch=self.batch, hollow=hollow)
            #set bias node
            self.hidden_layers[0][-1].intensity = 1


        self.output_layer = np.ndarray([output_size], Node)
        for i in range(output_size):
            self.output_layer[i] = Node(2, hidden_size, batch=self.batch, hollow=hollow)






    # Fires all input nodes
    # TODO: Optimize which nodes are recalculated and which aren't. depth-first
    def fire_network(self):

        previous_layer = self.input_layer

        #for layeri in range(len(self.hidden_layers)):
        #for nodei in range(len(self.hidden_layers[layeri])-1):
        for nodei in range(self.hidden_layers[0].size-1):
            temp=0
            for weight, in_node in zip(self.hidden_layers[0][nodei].weights, self.input_layer):
                temp+=in_node.intensity*weight
            self.hidden_layers[0][nodei].intensity = self.ReLU(temp)
            #previous_layer = self.hidden_layers[layeri]

        for nodei in range(self.output_layer.size):
            temp=0
            # for yadayada in zip(node, self.hidden_layer[-1]):
            for weight, hid_node in zip(self.output_layer[nodei].weights, self.hidden_layers[0]):
                temp+=hid_node.intensity*weight
            self.output_layer[nodei].intensity = self.ReLU(temp)

    # simplified version to get output intensities
    def get_output(self, num):
        return self.output_layer[num].intensity

    # don't set inputs directly! would put them on private, but Python has no privates
    def set_input(self, num, intense):
        self.input_layer[num].intensity = intense

    @staticmethod
    def Sigmoid(x):
        return 1 / (1+math.e**-x)

    @staticmethod
    def ReLU(x):
        return np.maximum(0, np.minimum(x,1 ))
        #return max(0, min(x,1))
    @staticmethod
    def ReLUd(x):
        if x <= 0:
            return 0
        else:
            return 1
        #return max(0, min(x,1))

    @staticmethod
    def Sigmoidi(x):
        temp = 1 / (1+math.e**-x)
        if temp > 0.5:
            return 1
        else:
            return 0

    def mutate(self,mutatechance=1/30):
        for nodei in range(self.input_layer.size):
            for weighti in range(self.input_layer[nodei].weights.size):
                if np.random.rand() <= mutatechance:
                    self.input_layer[nodei].weights[weighti] = np.random.uniform(-2,2)

        for nodei in range(self.hidden_layers[0].size):
            for weighti in range(self.hidden_layers[0][nodei].weights.size):
                if np.random.rand() <= mutatechance:
                    self.hidden_layers[0][nodei].weights[weighti] = np.random.uniform(-2,2)

        for nodei in range(self.output_layer.size):
            for weighti in range(self.output_layer[nodei].weights.size):
                if np.random.rand() <= mutatechance:
                    self.output_layer[nodei].weights[weighti] = np.random.uniform(-2,2)

    def clone(self):
        temp = NeuralNetwork(len(self.input_layer),
                             len(self.hidden_layers[0]),
                             len(self.output_layer),
                             hollow=True)

        for i in range(self.input_layer.size):
            temp.input_layer[i].weights = copy.deepcopy(self.input_layer[i].weights)

        for i in range(self.hidden_layers[0].size):
            temp.hidden_layers[0][i].weights = copy.deepcopy(self.hidden_layers[0][i].weights)

        for i in range(self.output_layer.size):
            temp.output_layer[i].weights = copy.deepcopy(self.output_layer[i].weights)

        return temp

    # Use after having set inputs and firing the network! Otherwise this doesn't work as intended!
    def backpropegate(self, desired_output):
        # TODO: ... something with back propegation.


        #Move through the output layer
        for nodei in range(self.output_layer.size):
            Z_j_L0 = 0
            C_0_d = 0
            a_j_L0_d = 0


            for nodei in range(self.output_layer.size):
                C_0_d += 2*(self.output_layer[nodei].intensity - desired_output[nodei] )
                for weighti in range(self.output_layer[nodei].weights.size):
                    Z_j_L0 += self.hidden_layers[-1][nodei].intensity * self.output_layer[nodei].weights[weighti]

            a_j_L0_d=self.ReLUd(Z_j_L0)

            d1_temp = C_0_d
            d2_temp = a_j_L0_d
            d3_temp = 0





            #Move through the hidden layers and adjust them.



    def pickle(self):
        pass
        # TODO: Basically save this NN for later use.

    def unpickle(self):
        pass
        # TODO: Basically load to put data in this NN
        #   Maybe also a better way than how clone does it?





    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------
    #------------------------ GRAPHICAL STUFF OF THE NEURAL NETWORK----------------------------------

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

        #position hidden layers' nodes
        am_layers = len(self.hidden_layers)+1
        for layeri in range(len(self.hidden_layers)):
            #position the hidden layer layeri nodes
            temp_am_nodes = len(self.hidden_layers[0])
            for nodei in range(temp_am_nodes):
                self.hidden_layers[layeri][nodei].sprite.update(int(pos[0]+dim[0]/am_layers*(layeri+1)),
                                                                int(pos[1]-(dim[1]/temp_am_nodes)*nodei))

        #position output nodes
        temp_am_nodes = len(self.output_layer)
        for nodei in range(temp_am_nodes):

            new_y = int(pos[1]-(dim[1]/temp_am_nodes)*nodei)

            self.output_layer[nodei].sprite.update(int(pos[0]+dim[0]),
                                                   new_y)


    def updateedgesGFX(self):

        # first hidden layer is special as it accesses input layer things
        for hnodei in range(len(self.hidden_layers[0])-1):
            #inodei can also be used to get the weights
            for inodei in range(len(self.input_layer)):
                weight = self.hidden_layers[0][hnodei].weights[inodei]
                if weight < 0:
                    weight*=-1
                    #RGB
                    col = (0, 0, 255,
                           0, 0, 255)
                    glLineWidth(weight+1)
                elif weight == 0:
                    continue
                    #col = (255, 255, 255,
                    #       255, 255, 255)
                    #glLineWidth(1)
                else: # weight > 0:
                    col = (255, 0, 0,
                           255, 0, 0)
                    glLineWidth(weight+1)

                pyglet.graphics.draw(2, GL_LINES, ('v2i', (self.input_layer[inodei].sprite.x+10,
                                                           self.input_layer[inodei].sprite.y + 10,
                                                           self.hidden_layers[0][hnodei].sprite.x + 10,
                                                           self.hidden_layers[0][hnodei].sprite.y + 10)
                                                   ),
                                                   ('c3B',col))

        # second to last hidden layers
        if len(self.hidden_layers) > 0:
            for layeri in range(1, len(self.hidden_layers)):
                for hnodei in range(len(self.hidden_layers[layeri])):

                    # inodei can also be used to get the weights
                    for inodei in range(len(self.input_layer)):

                        weight =self.hidden_layers[layeri][hnodei].weights[inodei]
                        if weight < 0:
                            weight*=-1
                            #RGB
                            col = (0, 0, 255,
                                   0, 0, 255)
                            glLineWidth(weight+1)
                        elif weight == 0:
                            continue
                            #col = (255, 255, 255,
                            #       255, 255, 255)
                            #glLineWidth(1)
                        else: # weight > 0:
                            col = (255, 0, 0,
                                   255, 0, 0)
                            glLineWidth(weight+1)

                        pyglet.graphics.draw(2, GL_LINES, ('v2i', (self.hidden_layers[layeri-1][inodei].sprite.x + 10,
                                                                   self.hidden_layers[layeri-1][inodei].sprite.y + 10,
                                                                   self.hidden_layers[layeri][hnodei].sprite.x + 10,
                                                                   self.hidden_layers[layeri][hnodei].sprite.y + 10)
                                                           ),
                                                          ('c3B', col))
        # last hidden layer to output layer
        for hnodei in range(len(self.hidden_layers[-1])):
            #inodei can also be used to get the weights
            for inodei in range(len(self.output_layer)):

                weight =self.output_layer[inodei].weights[hnodei]
                if weight < 0:
                    weight*=-1
                    #RGB
                    col = (0, 0, 255,
                           0, 0, 255)
                    glLineWidth(weight+1)
                elif weight == 0:
                    continue
                    #col = (255, 255, 255,
                    #       255, 255, 255)
                    #glLineWidth(1)
                elif weight > 0:
                    col = (255, 0, 0,
                           255, 0, 0)
                    glLineWidth(weight+1)

                pyglet.graphics.draw(2, GL_LINES, ('v2i', (self.output_layer[inodei].sprite.x+10,
                                                           self.output_layer[inodei].sprite.y + 10,
                                                           self.hidden_layers[-1][hnodei].sprite.x + 10,
                                                           self.hidden_layers[-1][hnodei].sprite.y + 10)
                                                   ),
                                                  ('c3B', col))

    def updateintensityGFX(self):

        # update intensities of input nodes
        temp_am_nodes = len(self.input_layer)
        for nodei in range(temp_am_nodes):
            intens = self.input_layer[nodei].intensity
            intens = min(intens*255, 255)
            self.input_layer[nodei].sprite.color = (intens,intens,intens)

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


#image_blackneuron = pyglet.resource.image("resources/" + "blackneuron.png")
image_whiteneuron = pyglet.resource.image("resources/" + "whiteneuron.png")

class Node:
    ids = [-1]
    def __init__(self, layer, parent_size=0, batch=None, hollow=False, weights=None):
        self.layer = layer
        self.intensity = 0

        if hollow:
            #If hollow, innitialize empty weights array
            self.weights = np.zeros(parent_size, dtype=float)
        elif weights is None:
            #If not hollow and no weights are provided, initiallize random weights
            self.weights = np.random.uniform(-2,2,[parent_size,])
        else:
            #Else use weights provided
            self.weights=weights

        self.sprite = pyglet.sprite.Sprite(image_whiteneuron, x=0,
                                                              y=0,
                                           batch=batch )

if __name__ == "__main__":
    oldbrain = NeuralNetwork()
    newbrain = oldbrain.clone()
    temp = False


