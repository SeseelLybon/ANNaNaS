import pyglet
import logging
logging.basicConfig(level=logging.DEBUG)

import checkergrid

window = pyglet.window.Window(640,460)

@window.event
def on_draw():
    global window
    window.clear()


def falseupdate(dt):
    pass

pyglet.clock.schedule_interval_soft(falseupdate, 1 // 1)
pyglet.app.run()

logging.critical("End of main")