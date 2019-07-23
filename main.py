#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import pyglet
from pyglet.window import key
import logging

logging.basicConfig(level=logging.DEBUG)

from population import Population

window = pyglet.window.Window(700,900)
pyglet.gl.glClearColor(0.3,0.3,0.3,1)




pops = Population(1000)

pops.patern = 0

showGraph = False
perfectBrainFound = False
patern = 0
skip_once = False

@window.event
def on_draw():
    global window
    global showGraph
    global perfectBrainFound
    global patern
    global skip_once

    window.clear()

    print("startin generation", pops.generation)

    if skip_once:
        pops.naturalSelection()
    skip_once = True



    # First test if it can turn on all the correct one.

    pops.update()

    #pops.players[braini].set_input(0, checkergrid.paterns[paterni][0, 0])
    #
    #pops.players[braini].fire_network()
    #
    #for i in range(16): # Going through all outputs! Not paterns
    #    temp = pops.players[braini].get_output(i)
    #    if paterni == i and temp >= 0.9:
    #        score_patern_c+=17
    #    if paterni != i and temp <= 0.1:
    #        score_patern_w+=1
    #
    #pops.players[braini].fitness=score_total




    pops.setBestBrain()

    print("Best of generation is", pops.bestPlayeri, pops.players[pops.bestPlayeri].fitness)
    print("Generating new generation")
    #generate new brains
    pops.calculateFitnessSum()
    #pops.naturalSelection()




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