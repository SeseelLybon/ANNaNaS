import numpy as np

from typing import List

import serpent

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
                 metrics='accuracy',
                 run_eagerly=False):

        self.input_size:int = input_size
        self.hidden_size:tuple = hidden_size
        self.output_size:int = output_size
        self.optimizer=optimizer
        self.loss=loss
        self.metrics=metrics
        self.run_eagerly=run_eagerly

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
                               run_eagerly=run_eagerly) # Turn this to True to be able to debug the models.

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

        # clone layers
        for hz_i in range(len(self.hidden_size)+1):
            clone.layers[hz_i].set_weights(self.model.layers[hz_i].get_weights() )

        clone.compile(optimizer=self.optimizer,
                      loss=self.loss,
                      metrics=[self.metrics]) # Turn this to True to be able to debug the models.

        clone.build([None, self.input_size])

        return clone



    def mutate(self,mutatechance=1/30, mutatestrength=1):
        ms_half = mutatestrength/2

        if self.hidden_size[0] != 0:
            # mutate the hidden layers
            for hli in range(len(self.hidden_size)): # hli: hidden layer index
                temp = self.model.layers[hli].get_weights()
                for owi in range( self.hidden_size[hli] ): # owi; output weight index
                    if np.random.rand() <= mutatechance:
                        temp[0][0][owi] += np.random.uniform(-ms_half,ms_half)
                        temp[1][owi] += np.random.uniform(-ms_half,ms_half)
                self.model.layers[hli].set_weights(temp)

        # mutate the output layer
        temp = self.model.layers[-1].get_weights()
        for owi in range(self.output_size):  # owi; output weight index
            if np.random.rand() <= mutatechance:
                temp[0][0][owi] += np.random.uniform(-ms_half, ms_half)
                temp[1][owi] += np.random.uniform(-ms_half, ms_half)
        self.model.layers[-1].set_weights(temp)



    def crossover(self,
                  parent2): # parent2: NeuralNetwork
                    # -> NeuralNetwork

        child:tf.keras.Model = tf.keras.models.clone_model(self.model)

        if self.hidden_size[0] != 0:
            # crossover the hidden layers
            for hli in range(len(self.hidden_size)):  # hli: hidden layer index
                # crossover the output layer
                temp_P1 = self.model.layers[hli].get_weights()
                temp_P2 = parent2.model.layers[hli].get_weights()
                temp_C = child.layers[hli].get_weights()
                for owi in range(self.hidden_size[hli]):  # owi; output weight index
                    # copy either the self or parent2 ***weight*** of this weight on this layer into the child
                    if np.random.rand() <= 0.5:
                        temp_C[0][0][owi] = temp_P1[0][0][owi]
                        print("P1-",end="")
                    else:
                        temp_C[0][0][owi] = temp_P2[0][0][owi]
                        print("P2-", end="")

                    # copy either the self or parent2 ***bias*** of this weight on this layer into the child
                    if np.random.rand() <= 0.5:
                        temp_C[1][owi] = temp_P1[0][0][owi]
                    else:
                        temp_C[1][owi] = temp_P2[0][0][owi]

                child.layers[hli].set_weights(temp_C)
            print()

        # crossover the output layer
        temp_P1 = self.model.layers[-1].get_weights()
        temp_P2 = parent2.model.layers[-1].get_weights()
        temp_C = child.layers[-1].get_weights()
        for owi in range(self.output_size): # owi; output weight index
            # copy either the self or parent2 ***weight*** of this weight on this layer into the child
            if np.random.rand() <= 0.5:
                temp_C[0][0][owi] = temp_P1[0][0][owi]
            else:
                temp_C[0][0][owi] = temp_P2[0][0][owi]

            # copy either the self or parent2 ***bias*** of this weight on this layer into the child
            if np.random.rand() <= 0.5:
                temp_C[1][owi] = temp_P1[1][owi]
            else:
                temp_C[1][owi] = temp_P2[1][owi]

            child.layers[-1].set_weights(temp_C)

        child.compile(optimizer=self.optimizer,
                      loss=self.loss,
                      metrics=[self.metrics])

        child.build([None, self.input_size])

        return child



    def serpent_serialize(self):

        #pickledbrain = serpent.dumps([self.model.get_config(),
        #                              [ [list(map(float, list(self.model.layers[0].get_weights()[0][0]))),
        #                                 list(map(float, list(self.model.layers[0].get_weights()[1]))) ] for i in range(len(self.model.layers))],
        #                              self.score])

        pickableweightslist = []

        for li in range(len(self.hidden_size)+1):
            temp_W = []
            temp_B = []
            for pli in range(len(self.model.layers[li].get_weights()[0])):
                temp_W += [self.model.layers[li].get_weights()[0][pli].tolist()]
            temp_B = self.model.layers[li].get_weights()[1].tolist()
            pickableweightslist.append([temp_W, temp_B])

        pickledbrain = serpent.dumps([self.model.get_config(),
                                      pickableweightslist,
                                      self.score])

        return pickledbrain


    def serpent_deserialize(self, pickledbrain):

        unpickledbrain = serpent.loads(serpent.tobytes(pickledbrain))
        self.score = unpickledbrain[2]

        self.model = tf.keras.Sequential.from_config(unpickledbrain[0])

        if self.hidden_size[0] != 0:
            for hli in range(len(self.hidden_size)): # hli: hidden layer index
                temp = self.model.layers[hli].get_weights()
                for pli in range(len(unpickledbrain[1][hli][0])):
                    for owi in range(len(unpickledbrain[1][hli][0][pli])): # owi; output weight index
                        # copy either the self or parent2 ***weight*** of this weight on this layer into the child
                        temp[0][pli][owi] = np.float32(unpickledbrain[1][hli][0][pli][owi])
                        pass

                for owi in range(len(unpickledbrain[1][hli][1])):
                    temp[1][owi] = unpickledbrain[1][hli][1][owi]

                self.model.layers[hli].set_weights(temp)


        temp = self.model.layers[-1].get_weights()
        for pli in range(len(unpickledbrain[1][-1][0])):
            for owi in range(len(unpickledbrain[1][-1][0][pli])): # owi; output weight index
                # copy either the self or parent2 ***weight*** of this weight on this layer into the child
                temp[0][pli][owi] = np.float32(unpickledbrain[1][-1][0][pli][owi])

        for owi in range(len(unpickledbrain[1][-1][1])):
            temp[1][owi] = unpickledbrain[1][-1][1][owi]

        self.model.layers[-1].set_weights(temp)

        self.model.compile(optimizer=self.optimizer,
                           loss=self.loss,
                           metrics=[self.metrics]) # Turn this to True to be able to debug the models.

        self.model.build([None, self.input_size])


    def getAmountWeights(self)->int:

        if self.hidden_size[0] == 0:
            totalWeights:int = self.output_size*self.input_size

        else:
            totalWeights:int = self.output_size*self.hidden_size[-1]
            for hli in range(len(self.hidden_size)-1, -1 ,-1):# hidden layer index
                totalWeights += self.hidden_size[-1]*self.hidden_size[hli]

        return totalWeights










if __name__ == "__main__":

    input_size = 1
    hidden_size = (5,5,5)
    output_size = 4

    brain1 = NeuralNetwork(input_size, hidden_size, output_size)

    train_set = np.array( [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15]] )
    answer_set = np.array( [[0,0,0,0],[1,0,0,0],[0,1,0,0],[1,1,0,0],
                            [0,0,1,0],[1,0,1,0],[0,1,1,0],[1,1,1,0],
                            [0,0,0,1],[1,0,0,1],[0,1,0,1],[1,1,0,1],
                            [0,0,1,1],[1,0,1,1],[0,1,1,1],[1,1,1,1],
                            ] )

    print("training brain 1")
    brain1.train(train_set, answer_set, epochs=100, batch_size=16)

    print("predictions of brain 1")
    print(brain1.predict([[3]]))
    print(brain1.predict([[7]]))
    print(brain1.predict([[11]]))
    print(brain1.predict([[15]]))

    print("Cloning brain 1 as brain 2")
    brain2 = NeuralNetwork(input_size, hidden_size, output_size, isHollow=True)
    brain2.model = brain1.clone()

    #print("training brain 1")
    #brain2.train(train_set, answer_set, epochs=100, batch_size=16)

    print("predictions of brain 2")
    print(brain2.predict([[3]]))
    print(brain2.predict([[7]]))
    print(brain2.predict([[11]]))
    print(brain2.predict([[15]]))

    print("mutating brain 2")
    brain2.mutate(mutatechance=0.9)
    print("predictions of brain 2 2")
    print(brain2.predict([[3]]))
    print(brain2.predict([[7]]))
    print(brain2.predict([[11]]))
    print(brain2.predict([[15]]))

    print("Crossing brain1 and brain2 to brain3")
    brain3  = NeuralNetwork(input_size, hidden_size, output_size)
    brain3.model = brain1.crossover(brain2)

    print("predictions of brain 3")

    #brain1.model.layers[0].set_weights()
    for mli in range(1): #len(brain1.model.layers)): # mli model layer index
        print("B1",brain1.model.layers[mli].get_weights()[0][0] )
        print("B2",brain2.model.layers[mli].get_weights()[0][0] )
        print("B3",brain3.model.layers[mli].get_weights()[0][0] )

    print("pickling brain 3")
    pickledbrain3 = brain3.serpent_serialize()
    print("setting up brain 4")
    brain4 = NeuralNetwork(input_size, hidden_size, output_size, isHollow=True)
    print("unpickling brain 3 into brain 4")
    brain4.serpent_deserialize(pickledbrain3)

    print("predictions of brain 4")
    print(brain3.predict([[3]]))
    print(brain4.predict([[3]]))
    print()
    print(brain3.predict([[7]]))
    print(brain4.predict([[7]]))
    print()
    print(brain4.predict([[11]]))
    print(brain3.predict([[11]]))
    print()
    print(brain4.predict([[15]]))
    print(brain3.predict([[15]]))

    #print(brain3.model.get_weights())
    #print(brain4.model.get_weights())