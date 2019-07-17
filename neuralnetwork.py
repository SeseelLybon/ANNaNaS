import numpy
import logging
import math


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

    def activate(self):
        pass

    def genid(self):
        self.ids[0]+=1
        return self.ids[0]

import numpy
import pyglet
import checkergrid

image_blackneuron = pyglet.resource.image("resources/" + "blackneuron.png")
image_whiteneuron = pyglet.resource.image("resources/" + "whiteneuron.png")

class visualnode:
    def __init__(self, position, intensity, scale):
        self.scale = scale
        self.pos = checkergrid.vector2d(position)

        if intensity == 0:
            self.sprite = pyglet.sprite.Sprite(image_blackneuron, x=self.pos.x,
                                                                           y=self.pos.y,
                                               batch=checkergrid.batch )
        else:
            self.sprite = pyglet.sprite.Sprite(image_whiteneuron, x=self.pos.x,
                                                                           y=self.pos.y,
                                              batch=checkergrid.batch )

    def change(self, new):
        if new == 1:
            self.sprite.image = image_whiteneuron
        else:
            self.sprite.image = image_blackneuron