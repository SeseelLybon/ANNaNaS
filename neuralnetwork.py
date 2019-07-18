import logging
import math
import numpy
import pyglet
import checkergrid


class NeuralNetwork:

    def __init__(self, input_size=4, hidden_layers=(4), output_size=2):
        self.input_layer = numpy.array([Node(0), Node(0), Node(0), Node(0)])

        self.hidden_layers = list()
        self.hidden_layers.append(numpy.array([Node(1,4,weights=[1,0,0,0],bias=0),
                                               Node(1,4,weights=[0,1,0,0],bias=0),
                                               Node(1,4,weights=[0,0,1,0],bias=0),
                                               Node(1,4,weights=[0,0,0,1],bias=0)])
                                  )
        self.hidden_layers.append(numpy.array([Node(2,4,weights=[1,0,0,0],bias=0),
                                               Node(2,4,weights=[0,1,0,0],bias=0),
                                               Node(2,4,weights=[0,0,1,0],bias=0),
                                               Node(2,4,weights=[0,0,0,1],bias=0)])
                                  )

        self.output_layer = numpy.array([Node(3,4,weights=[-1,1,1,-1],bias=-1),
                                         Node(3,4,weights=[1,-1,-1,1],bias=-1)])




    # Fires all input nodes
    # TODO: Optimize which nodes are recalculated and which aren't. depth-first

    def fire_network(self):

        # TODO: for later; optimized that calls a node old if one of it's parents is old,
        #   Except for the input layer, which is only oldified if it is changed,
        #   (if it hasn't changed since the last fire, its children probably don't need to changed either).

        # Go through each layer left2right excluding input layer
        previous_layer = self.input_layer

        for layeri in range(len(self.hidden_layers)):
            for i in range(len(self.hidden_layers[layeri])):
            #for node in self.hidden_layer:
                temp=0
                for weight, in_node in zip(self.hidden_layers[layeri][i].weights, previous_layer):
                    temp+=in_node.intensity*weight
                self.hidden_layers[layeri][i].intensity = temp+self.hidden_layers[layeri][i].bias
                self.hidden_layers[layeri][i].hasChanged = True
            previous_layer = self.hidden_layers[layeri]

        for i in range(len(self.output_layer)):
            temp=0
            # for yadayada in zip(node, self.hidden_layer[-1]):
            for weight, in_node in zip(self.output_layer[i].weights, self.hidden_layers[-1]):
                temp+=in_node.intensity*weight
            self.output_layer[i].intensity = temp+self.output_layer[i].bias
            self.output_layer[i].hasChanged = True

    # simplified version to get output intensities
    def get_output(self, num):
        return self.output_layer[num].intensity

    # simplified version to get hidden intensities
    def get_hidden(self, num, layer):
        return self.hidden_layers[layer][num].intensity

    # don't set inputs directly! would put them on private, but Python has no privates
    def set_input(self, num, intense):
        self.input_layer[num].intensity = intense
        self.input_layer[num].hasChanged = True

    @staticmethod
    def Sigmoid(x):
        return 1 / 1+math.e**-x


    # Tries to position the nodes of the neural network using Pyglet at this position, within these dimentions
    def updatepos(self, pos, dim):

        #position input nodes
        temp_am_nodes = len(self.input_layer)
        for nodei in range(temp_am_nodes):
            self.input_layer[nodei].sprite.update(pos[0], pos[1]-(dim[1]/temp_am_nodes)*nodei)

        am_layers = len(self.hidden_layers)+1
        for layeri in range(len(self.hidden_layers)):
            #position the hidden layer layeri nodes
            temp_am_nodes = len(self.hidden_layers[0])
            for nodei in range(temp_am_nodes):
                self.hidden_layers[layeri][nodei].sprite.update(pos[0]+dim[0]/am_layers*(layeri+1),
                                                                pos[1]-(dim[1]/temp_am_nodes)*nodei)
        '''
        #position the hidden layer 0 nodes
        temp_am_nodes = len(self.hidden_layers[0])
        for nodei in range(temp_am_nodes):
            self.hidden_layers[0][nodei].sprite.update(pos[0]+dim[0]/3*1, pos[1]-(dim[1]/temp_am_nodes)*nodei)

        #position the hidden layer 1 nodes
        temp_am_nodes = len(self.hidden_layers[1])
        for nodei in range(temp_am_nodes):
            self.hidden_layers[1][nodei].sprite.update(pos[0]+dim[0]/3*2, pos[1]-(dim[1]/temp_am_nodes)*nodei)
        '''

        #position output nodes
        temp_am_nodes = len(self.output_layer)
        for nodei in range(temp_am_nodes):
            self.output_layer[nodei].sprite.update(pos[0]+dim[0], pos[1]-(dim[1]/temp_am_nodes)*nodei)


    def updateintensity(self):

        # update intensities of input nodes
        temp_am_nodes = len(self.input_layer)
        for nodei in range(temp_am_nodes):
            if self.input_layer[nodei].intensity == 1:
                self.input_layer[nodei].sprite.image = image_whiteneuron
            else:
                self.input_layer[nodei].sprite.image = image_blackneuron

        # update intensities of hidden layer nodes
        for layeri in range(len(self.hidden_layers)):
            for nodei in range(len(self.hidden_layers[layeri])):
                if self.hidden_layers[layeri][nodei].intensity == 1:
                    self.hidden_layers[layeri][nodei].sprite.image = image_whiteneuron
                else:
                    self.hidden_layers[layeri][nodei].sprite.image = image_blackneuron


        '''
        # update intensities of hidden layer 0 nodes
        temp_am_nodes = len(self.hidden_layers[0])
        for nodei in range(temp_am_nodes):
            if self.hidden_layers[0][nodei].intensity == 1:
                self.hidden_layers[0][nodei].sprite.image = image_whiteneuron
            else:
                self.hidden_layers[0][nodei].sprite.image = image_blackneuron
        '''

        # update intensities of output nodes
        temp_am_nodes = len(self.output_layer)
        for nodei in range(temp_am_nodes):
            if self.output_layer[nodei].intensity == 1:
                self.output_layer[nodei].sprite.image = image_whiteneuron
            else:
                self.output_layer[nodei].sprite.image = image_blackneuron


class Node:
    ids = [-1]
    def __init__(self, layer, parent_size=0, weights=None, bias=0):
        self.number = self.genid()
        self.layer = layer
        self.intensity = 0
        if weights is None:
            self.weights = numpy.random.random_integers(-1,1,[parent_size,])
        else:
            self.weights=weights
        self.hasChanged = True
        self.bias = bias
        self.sprite = pyglet.sprite.Sprite(image_whiteneuron, x=0,
                                                              y=0,
                                           batch=checkergrid.batch )

    def activate(self):
        pass

    def genid(self):
        self.ids[0]+=1
        return self.ids[0]


image_blackneuron = pyglet.resource.image("resources/" + "blackneuron.png")
image_whiteneuron = pyglet.resource.image("resources/" + "whiteneuron.png")

class visualnode:
    def __init__(self, position):
        self.pos = checkergrid.vector2d(position)
        self.sprite = pyglet.sprite.Sprite(image_whiteneuron, x=self.pos.x,
                                                              y=self.pos.y,
                                           batch=checkergrid.batch )


    def change(self, new):
        if new == 1:
            self.sprite.image = image_whiteneuron
        else:
            self.sprite.image = image_blackneuron