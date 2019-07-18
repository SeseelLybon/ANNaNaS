import pyglet
import logging
import numpy
import random
logging.basicConfig(level=logging.DEBUG)

import checkergrid
import neuralnetwork

window = pyglet.window.Window(640,460)
pyglet.gl.glClearColor(0.3,0.3,0.3,1)


#randpater = numpy.random.random_integers(0,1,[2,2])
#inputchecker = checkergrid.Checker([40,300],randpater, scale=1.5)

# output checkers are just for visuals
outputchecker_1 = checkergrid.Checker([400,300],checkergrid.paterns[5], scale=1.5)

outputchecker_2 = checkergrid.Checker([400,200],checkergrid.paterns[10], scale=1.5)

'''

nodei1 = neuralnetwork.visualnode([110,100],0,1.5)
nodei2 = neuralnetwork.visualnode([110,200],0,1.5)
nodei3 = neuralnetwork.visualnode([110,300],0,1.5)
nodei4 = neuralnetwork.visualnode([110,400],0,1.5)

nodeh01 = neuralnetwork.visualnode([160,100],0,1.5)
nodeh02 = neuralnetwork.visualnode([160,200],0,1.5)
nodeh03 = neuralnetwork.visualnode([160,300],0,1.5)
nodeh04 = neuralnetwork.visualnode([160,400],0,1.5)

nodeh11 = neuralnetwork.visualnode([210,100],0,1.5)
nodeh12 = neuralnetwork.visualnode([210,200],0,1.5)
nodeh13 = neuralnetwork.visualnode([210,300],0,1.5)
nodeh14 = neuralnetwork.visualnode([210,400],0,1.5)


nodeo1 = neuralnetwork.visualnode([300,300],0,1.5)
nodeo2 = neuralnetwork.visualnode([300,200],0,1.5)
'''

brain = neuralnetwork.NeuralNetwork()
brain.updatepos([110, 300], [240, 300])

ptrn = 0
def nxt():
    global ptrn
    ptrn+=1
    ptrn=ptrn%16

@window.event
def on_draw():
    global window
    window.clear()

    #inputchecker = checkergrid.Checker([40, 300], random.choice(checkergrid.paterns), scale=1.5)
    inputchecker = checkergrid.Checker([40, 300], checkergrid.paterns[ptrn], scale=1.5)
    nxt()

    brain.set_input(0,inputchecker.patern[0,0])
    #nodei1.change(inputchecker.patern[0,0])

    brain.set_input(1,inputchecker.patern[1,0])
    #nodei2.change(inputchecker.patern[1,0])

    brain.set_input(2,inputchecker.patern[0,1])
    #nodei3.change(inputchecker.patern[0,1])

    brain.set_input(3,inputchecker.patern[1,1])
    #nodei4.change(inputchecker.patern[1,1])

    brain.fire_network()

    #nodeh01.change(brain.get_hidden(0,0))
    #nodeh02.change(brain.get_hidden(1,0))
    #nodeh03.change(brain.get_hidden(2,0))
    #nodeh04.change(brain.get_hidden(3,0))

    #nodeh11.change(brain.get_hidden(0,1))
    #nodeh12.change(brain.get_hidden(1,1))
    #nodeh13.change(brain.get_hidden(2,1))
    #nodeh14.change(brain.get_hidden(3,1))

    #nodeo1.change(brain.get_output(0))
    #nodeo2.change(brain.get_output(1))

    brain.updateintensity()

    checkergrid.batch.draw()

@window.event
def on_mouse_release(x, y, button, modifiers):
    pass

def falseupdate(dt):
    pass

#pyglet.clock.schedule_interval_soft(falseupdate, 1 / 1)
pyglet.app.run()

logging.critical("End of main")