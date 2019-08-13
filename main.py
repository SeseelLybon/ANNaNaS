#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import pyglet
from pyglet.window import key
import logging
logging.basicConfig(level=logging.DEBUG)

import numpy as np

from population import Population

window = pyglet.window.Window(1200,500)
pyglet.gl.glClearColor(0.7,0.7,0.7,1)

import obstacle as obt
from obstacle import Vector2f



#pops = Population(100)

showGraph = False
skip_once = False
score = 0

obstacle_drawlist = [obt.obstacle(Vector2f(1200,40),Vector2f(40,60)),
                     obt.obstacle(Vector2f(1700,40),Vector2f(20,30)),
                     obt.obstacle(Vector2f(2200,40),Vector2f(40,60))]

@window.event
def on_draw():
    global window
    global skip_once
    global score

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

    score+=1

    obt.ground.draw()

    if len(obstacle_drawlist) < 2:
        dice_throw = np.random.rand()
        pos_adjust = 1200 + np.random.rand()*300//1

        if dice_throw < 0.20: # spawn large cacti
            obstacle_drawlist.append( obt.obstacle(Vector2f(pos_adjust,40),Vector2f(40,60)) )
        elif dice_throw < 0.40: # Spawn smol cacti
            obstacle_drawlist.append( obt.obstacle(Vector2f(pos_adjust,40),Vector2f(20,30)) )
        elif dice_throw < 0.40: # spawn flying dino
            obstacle_drawlist.append( obt.obstacle(Vector2f(pos_adjust,200),Vector2f(20,30)) )

    markforremoval = list()
    for obst in obstacle_drawlist:
        obst.update(score)
        if obst.isLeftofScreen(-20):
            markforremoval.append(obst)
            continue

        obst.draw()

    obstacle_drawlist[:] = [x for x in obstacle_drawlist if x not in markforremoval]


    obt.dino1.update()
    obt.dino1.draw()





@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print("jumping")
        obt.dino1.jump()

    if symbol == key.DOWN:
        obt.dino1.duck()


def falseupdate(dt):
    pass


pyglet.clock.schedule_interval_soft(falseupdate, 1 / 60)
pyglet.app.run()


logging.critical("End of main")