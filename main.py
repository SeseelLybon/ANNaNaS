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



pops = Population(100)

showGraph = False
skip_once = False

@window.event
def on_draw():
    global window
    global skip_once

    window.clear()

    print("--------------------------------------------")
    print("startin generation", pops.generation)

    if skip_once:
        print("\tSelecting Naturally (NaturalSelection())")
        pops.naturalSelection()
    skip_once = True

    # Run the game here
    # Move the objects/obstacles on the platform, not the dino or the platform
    # Use the update() and isDone() function



    if pops.bestMeeple is not None:
        pops.bestMeeple.brain.updateposGFX([90, 810], [450, 800])
        pops.bestMeeple.brain.updateintensityGFX()
        pops.bestMeeple.brain.draw()




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