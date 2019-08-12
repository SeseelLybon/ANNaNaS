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

window = pyglet.window.Window(1200,500)
pyglet.gl.glClearColor(0.7,0.7,0.7,1)

import obstacle



#pops = Population(100)

showGraph = False
skip_once = False

@window.event
def on_draw():
    global window
    global skip_once

    window.clear()

    #print("--------------------------------------------")
    #print("startin generation", pops.generation)
    #
    #if skip_once:
    #    print("\tSelecting Naturally (NaturalSelection())")
    #    pops.naturalSelection()
    #skip_once = True
    #if pops.bestMeeple is not None:
    #    pops.bestMeeple.brain.updateposGFX([90, 810], [450, 800])
    #    pops.bestMeeple.brain.updateintensityGFX()
    #    pops.bestMeeple.brain.draw()

    # Run the game here
    # Move the objects/obstacles on the platform, not the dino or the platform
    # Use the update() and isDone() function

    obstacle.dino1.update()

    obstacle.ground.draw()
    obstacle.dino1.draw()





@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print("jumping")
        obstacle.dino1.jump()


def falseupdate(dt):
    pass


pyglet.clock.schedule_interval_soft(falseupdate, 1 / 60)
pyglet.app.run()


logging.critical("End of main")