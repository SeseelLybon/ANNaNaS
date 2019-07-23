from neuralnetwork import NeuralNetwork

class Dart_Player:

    score = 0

    def __init__(self, brain:NeuralNetwork):
        self.score = 0 # the max
        self.isDone = False # if score is 0
        self.brain = brain
        self.throws = 0 # keep track of how many throws the player has made
        self.fitness = 0

    def checkifDone(self):
        if self.score == 0:
            self.isDone = True
        else:
            return

    def setScore(self, x):
        if self.score-x >= 0:
            self.score-=x
        elif self.score-x < 0:
            return

    def clone(self):
        return Dart_Player( self.brain.clone() )

    def mutate(self, mutatechance:float):
        self.brain.mutate(mutatechance)

    def update(self):

        self.brain.set_input(0, self.score)
        self.brain.fire_network()

        for i in range(self.brain.output_layer.size):
            pass