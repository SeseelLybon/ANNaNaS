import neuralnetwork
import pyglet
import numpy
#import garbage


class Population:

    generation = 0
    def selectparent(self):
        pass
        #rand = numpy.random.rand(0, fitnesssum)
        runningsum = 0
        #go through all the brains in the population, and if at some point the runningsum > rand, then pick that brain as a parent,
        #do this untill the population is re-regenerated
        #also, remember to save the best brain from the last generation

    def naturalSelection(self):
        pass
        # temp_newbrains = listfornewbrains
        # pick the best brain and same him
        # then clone the best brain
        # then use select parent and fill the list of new brains with them as parents
        self.generation += 1
        #swap out the old brains for the new brains

