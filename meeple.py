

from neuralnetwork import NeuralNetwork

class Meeple:

    global_ID = [0]

    def __init__(self, input_size:int, hidden_size:tuple, output_size:int, isHallow=False, epochs=10):
        self.ID = self.global_ID[0]
        self.global_ID[0] += 1
        self.epochs = epochs
        self.brain: NeuralNetwork
        self.isAlive = True
        self.isDone = False
        self.isKilled = False

        #Custom code; this is something that doens't need be cloned, though.
        self.results_list = []

        if isHallow:
            self.brain = NeuralNetwork(input_size,hidden_size,output_size, isHollow=True)
        else:
            self.brain = NeuralNetwork(input_size,hidden_size,output_size)

    # Clones Brain
    def clone(self): #->Meeple:
        temp:Meeple = Meeple(self.brain.input_size-1,
                             tuple([x-1 for x in self.brain.hidden_size]),
                             self.brain.output_size,
                             isHallow=True
                             )
        temp.brain = self.brain.clone()
        return temp

#    def cloneinto(self, other):
#        #This is for dealing with python's soft pointers.
#        self.brain = other.brain
#        self.fitness = other.fitness
#        self.isAlive = True
#        self.isKilled = False
#        self.isDone = False
#        self.score = other.score

    # Crosses the Brain of 2 meeps
    def crossover(self, parent2): #parent1:Meeple, parent2:Meeple) -> Meeple:
        temp:Meeple = Meeple(self.brain.input_size-1,
                             tuple([x-1 for x in self.brain.hidden_size]),
                             self.brain.output_size,
                             isHallow=True
                             )
        temp.brain = self.brain.crossover(parent2.brain)
        return temp



if __name__ == "__main__":
    meeple1 = Meeple(4,tuple([0]),16)
    print(meeple1.fitness)