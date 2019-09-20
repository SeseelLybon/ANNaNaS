

from neuralnetwork import NeuralNetwork

class Meeple:
    def __init__(self, input_size:int, hidden_size:tuple, output_size:int, isHallow=False):
        self.fitness = 0
        self.score = float("-inf")
        self.epochs = 100
        self.brain: NeuralNetwork
        self.isAlive = True
        self.isDone = False
        self.isKilled = False

        if isHallow:
            self.brain = NeuralNetwork(input_size,hidden_size,output_size, isHollow=True)
        else:
            self.brain = NeuralNetwork(input_size,hidden_size,output_size)


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