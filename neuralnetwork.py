import math
import numpy as np
import pyglet

from pyglet.gl import *
from typing import List

import serpent
import copy

import tensorflow as tf


class NeuralNetwork:

    def __init__(self,
                 input_size:int,
                 hidden_size:tuple,
                 output_size:int,
                 isHollow=False,
                 activation='relu',
                 optimizer='adam',
                 loss=tf.keras.losses.poisson,
                 metrics='accuracy'):

        self.input_size:int = input_size
        self.hidden_size:tuple = hidden_size
        self.output_size:int = output_size
        self.optimizer=optimizer
        self.loss=loss
        self.metrics=metrics

        self.fitness = float('-inf')
        self.score = float('-inf')

        self.activation = activation
        self.model:tf.keras.Sequential

        #self.brain = tf.keras.models.Sequential([
        #    tf.keras.layers.Dense(5, input_dim=1, activation=tf.keras.activations.relu),
        #    tf.keras.layers.Dense(10, activation='relu'),
        #    tf.keras.layers.Dense(5, activation=tf.keras.activations.relu)
        #])
        if not isHollow:
            self.model = tf.keras.models.Sequential()

            if self.hidden_size[0] == 0:
                # if there are no hidden layers, I only need 1 layers, as input is defined in that layer
                self.model.add( tf.keras.layers.Dense(self.output_size, input_dim=self.input_size, activation=self.activation) )
            else:
                # if there are hidden layers, tell the first layer what [0] is and the input,
                #   then loop through the rest if they exist,
                #   and then add the output layer as last

                self.model.add(tf.keras.layers.Dense(self.hidden_size[0], input_dim=input_size, activation=self.activation))

                for hz_i in range(1, len(self.hidden_size)):
                    self.model.add(tf.keras.layers.Dense(self.hidden_size[hz_i], activation=self.activation))

                self.model.add(tf.keras.layers.Dense(self.output_size, activation=self.activation))

            self.model.compile(optimizer=optimizer,
                               loss=loss,
                               metrics=[metrics],
                               run_eagerly=False) # Turn this to True to be able to debug the models.

            self.model.build([None, self.input_size])
        else:
            self.model = None
            # For the love of god, don't forget to clone a model in here. >.>


    # Fires all input nodes
    def predict(self, input_array:np.array)->np.array:
        return self.model.predict(input_array)


    def train(self, training_data:np.array, training_answers:np.array, epochs:int=1, batch_size:int=1, verbose=0):
        self.model.fit(training_data, training_answers, epochs=epochs, batch_size=batch_size, verbose=verbose)


    def clone(self)->tf.keras.Model:
        clone = tf.keras.models.clone_model(self.model)

        if self.hidden_size[0] == 0:
            clone.layers[0].set_weights(self.model.layers[0].get_weights() )
            # if [0]==0, there are no hidden layers to deal with
        else:
            # clone first layer
            clone.layers[0].set_weights(self.model.layers[0].get_weights() )

            # clone hidden layers (except the first one)
            for hz_i in range(1, len(self.hidden_size)):
                clone.layers[hz_i].set_weights(self.model.layers[hz_i].get_weights() )

            # clone final layer
            clone.layers[-1].set_weights(self.model.layers[-1].get_weights() )

        clone.compile(optimizer=self.optimizer,
                      loss=self.loss,
                      metrics=[self.metrics]) # Turn this to True to be able to debug the models.

        clone.build([None, self.input_size])

        return clone



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










if __name__ == "__main__":



    brain1 = NeuralNetwork(1, (0,), 4)

    train_set = np.array( [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15]] )
    answer_set = np.array( [[0,0,0,0], # 0
                            [1,0,0,0],
                            [0,1,0,0],
                            [1,1,0,0], # 3

                            [0,0,1,0], # 4
                            [1,0,1,0],
                            [0,1,1,0],
                            [1,1,1,0], # 7

                            [0,0,0,1], # 8
                            [1,0,0,1],
                            [0,1,0,1],
                            [1,1,0,1], # 11

                            [0,0,1,1], # 12
                            [1,0,1,1],
                            [0,1,1,1],
                            [1,1,1,1], # 15
                            ] )

    print("training brain 1")
    brain1.train(train_set, answer_set, epochs=100, batch_size=16)

    print("predictions of brain 1")
    print(brain1.predict([[3]]))
    print(brain1.predict([[7]]))
    print(brain1.predict([[11]]))
    print(brain1.predict([[15]]))

    brain2 = NeuralNetwork(1, (0,), 4, isHollow=True)
    brain2.model = brain1.clone()

    print("training brain 1")
    #brain2.train(train_set, answer_set, epochs=100, batch_size=16)

    print("predictions of brain 1")
    print(brain2.predict([[3]]))
    print(brain2.predict([[7]]))
    print(brain2.predict([[11]]))
    print(brain2.predict([[15]]))



    #brain1.model.layers[0].set_weights()
    print(brain1.model.layers[-1].get_weights()[0] )
    print(brain2.model.layers[-1].get_weights()[0] )


    test_keras = False
    if test_keras:
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(5, input_dim=1, activation=tf.keras.activations.relu)#,
            #tf.keras.layers.Dense(10, activation='relu'),
            #tf.keras.layers.Dense(5, activation=tf.keras.activations.relu)
        ])

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.poisson,
                      metrics=['accuracy'])

        train_set = np.array( [[0],[1],[2],[3],[4]] )
        answer_set = np.array( [[1,0,0,0,0],
                                [0,1,0,0,0],
                                [0,0,1,0,0],
                                [0,0,0,1,0],
                                [0,0,0,0,1]] )

        model.fit(train_set, answer_set, epochs=100, batch_size=5)

        print( model.predict([[0]]) )
        print( model.predict([[1]]) )
        print( model.predict([[2]]) )
        print( model.predict([[3]]) )
        print( model.predict([[4]]) )
