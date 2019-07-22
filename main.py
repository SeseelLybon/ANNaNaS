import pyglet
from pyglet.window import key
import logging
import numpy
import random
import copy
logging.basicConfig(level=logging.DEBUG)

import checkergrid
from population import Population

window = pyglet.window.Window(700,900)
pyglet.gl.glClearColor(0.3,0.3,0.3,1)


#randpater = numpy.random.random_integers(0,1,[2,2])
#inputchecker = checkergrid.Checker([40,300],randpater, scale=1.5)

# output checkers are just for visuals

outputcheckers = list()
for i in range(16):
        outputcheckers.append( checkergrid.Checker([600,800-50*i],
                                                   checkergrid.paterns[i],
                                                   scale=1) )

pops = Population(1000)

pops.patern = 0

showGraph = False
perfectBrainFound = False
patern = 0

@window.event
def on_draw():
    global window
    global showGraph
    global perfectBrainFound
    global patern

    window.clear()

    if not perfectBrainFound:
        print("startin generation", pops.generation)

        #per brain
        for braini in range(len(pops.brains)):
        #for braini in range(1):
            #per patern
            totalscoresum = 0
            for paterni in range(16):
                pops.brains[braini].set_input(0,checkergrid.paterns[paterni][0,0])
                pops.brains[braini].set_input(1,checkergrid.paterns[paterni][1,0])
                pops.brains[braini].set_input(2,checkergrid.paterns[paterni][0,1])
                pops.brains[braini].set_input(3,checkergrid.paterns[paterni][1,1])


                pops.brains[braini].fire_network()

                score = 0
                for i in range(16):
                    temp = pops.brains[braini].get_output(i)
                    if paterni == i:
                        score+=(1-temp)**2
                    else:
                        score +=(0-temp)**2
                totalscoresum+=10/max(score, 0.001)

            totalscoreavg=totalscoresum/16
            pops.brains[braini].fitness=10/max(totalscoreavg, 0.001)


                #if pops.brains[braini].get_output(0) == 1 and pops.brains[braini].get_output(1) != 1:
                #    pops.brains[braini].fitness+=0
                #    if paterni == 5:
                #        pops.brains[braini].fitness+=15
#
                #elif pops.brains[braini].get_output(0) != 1 and pops.brains[braini].get_output(1) == 1:
                #    pops.brains[braini].fitness+=0
                #    if paterni == 10:
                #        pops.brains[braini].fitness+=15
#
                #elif pops.brains[braini].get_output(0) != 1 and pops.brains[braini].get_output(1) != 1:
                #    if not paterni == 10\
                #            and not paterni == 5:
                #        pops.brains[braini].fitness+=1
                #        pass

        pops.setBestBrain()
        if pops.brains[pops.bestBraini].fitness == 10/0.00001:
            print("found perfect brain")
            pyglet.clock.unschedule(falseupdate)
            showGraph = True
            perfectBrainFound = True
            print("Best of generation is", pops.bestBraini, pops.brains[pops.bestBraini].fitness)
            return

        print("Best of generation is", pops.bestBraini, pops.brains[pops.bestBraini].fitness)
        print("Generating new generation")
        #generate new brains
        pops.calculateFitnessSum()
        pops.naturalSelection()

    else:

        inputchecker = checkergrid.Checker([10,600],checkergrid.paterns[patern], scale=1.5)
        pops.brains[pops.bestBraini].set_input(0,checkergrid.paterns[patern][0,0])
        pops.brains[pops.bestBraini].set_input(1,checkergrid.paterns[patern][1,0])
        pops.brains[pops.bestBraini].set_input(2,checkergrid.paterns[patern][0,1])
        pops.brains[pops.bestBraini].set_input(3,checkergrid.paterns[patern][1,1])

        pops.brains[pops.bestBraini].fire_network()

        patern+=1
        patern=patern%16

    if pops.bestBraini != -1:
        pops.brains[pops.bestBraini].updateposGFX([90,810],[450,800])
        pops.brains[pops.bestBraini].updateintensityGFX()
        pops.brains[pops.bestBraini].draw()
        checkergrid.checkerbatch.draw()




@window.event
def on_mouse_release(x, y, button, modifiers):
    pass

@window.event
def on_key_press(symbol, modifiers):
    global perfectBrainFound
    if symbol == key.SPACE:
        if perfectBrainFound:
            perfectBrainFound = False
            pyglet.clock.schedule_interval_soft(falseupdate, 1 / 1)
        else:
            perfectBrainFound = True
            pyglet.clock.unschedule(falseupdate)


def falseupdate(dt):
    pass


pyglet.clock.schedule_interval_soft(falseupdate, 1 / 1)
pyglet.app.run()


logging.critical("End of main")