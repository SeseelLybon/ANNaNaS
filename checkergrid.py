

import numpy
import pyglet

batch = pyglet.graphics.Batch()

pyglet.resource.image("resources/" + "blacktile.png")
pyglet.resource.image("resources/" + "white.png")

class Checker:

    def __init__(self, pos, patern):
        self.position = pos
        self.patern = patern










# -------- general storage of paterns

PaternA = numpy.array([[1,0],
                       [0,1]])

PaternB = numpy.array([[0,1],
                       [1,0]])
