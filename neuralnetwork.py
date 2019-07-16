import numpy




class NeuralNetwork:

    def __init__(self, input_size=4, hidden_layers=(4), output_size=2):
        self.input_layer = numpy.array([Node(0), Node(0), Node(0),Node(0)])
        self.bias = Node(0)

        self.hidden_layer = numpy.array([Node(1),Node(1),Node(1),Node(1)])
        self.output_layer = numpy.array([Node(2),Node(2)])




    # Fires all input nodes
    # TODO: Optimize which nodes are recalculated and which aren't. depth-first

    def fire_network(self):

        # TODO: for later; optimized that calls a node old if one of it's parents is old,
        #   Except for the input layer, which is only oldified if it is changed,
        #   (if it hasn't changed since the last fire, its children probably don't need to changed either).


        # Go through each layer left2right excluding input layer
        # for layer in hidden_layers:
        #     for node in layer:
        for node in self.hidden_layer:
            temp=0
            for weight, intens in zip(node, self.input_layer):
                temp+=intens*weight
            node.intenstiy = temp
            node.hasChanged = True

        for node in self.output_layer:
            temp=0
            # for yadayada in zip(node, self.hidden_layer[-1]):
            for weight, intens in zip(node, self.hidden_layer):
                temp+=intens*weight
            node.intenstiy = temp
            node.hasChanged = True

    # simplified version to get output intensities
    def get_output(self, num):
        return self.output_layer[num].intensity

    # don't set inputs directly! would put them on private, but Python has no privates
    def set_input(self, num, intense):
        self.input_layer[num].intensity = intense
        self.input_layer[num].hasChanged = True

class Node:
    def __init__(self, layer, parent_size=0):
        self.number = self.genid()
        self.layer = layer
        self.intenstiy = 0
        self.weights = numpy.zeros(parent_size)
        self.hasChanged = True

    def activate(self):
        pass

    @classmethod
    def genid(cls, ids=[-1]):
        ids+=1
        return ids