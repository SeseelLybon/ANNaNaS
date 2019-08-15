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

from pymunk import Vec2d
import pymunk
from pymunk.pyglet_util import DrawOptions

from population import Population

window = pyglet.window.Window(1200,500)
pyglet.gl.glClearColor(0.7,0.7,0.7,1)

import obstacle as obt



#pops = Population(100)

showGraph = False
skip_once = False
score = 0

obstacle_drawlist = [obt.obstacle(Vec2d(1200,40),Vec2d(40,60)),
                     obt.obstacle(Vec2d(1700,40),Vec2d(20,30)),
                     obt.obstacle(Vec2d(2200,40),Vec2d(40,60))]

score_label = pyglet.text.Label('score: ' + str(score),
                  font_name='Times New Roman',
                  font_size=12,
                  x=50, y=500 - 50,
                  anchor_x='left', anchor_y='center')


space = pymunk.Space()
space.gravity = (0.0, -1000.0)
space.sleep_time_threshold = 0.3

# TODO: Move this to the platform class
shape = pymunk.Segment(space.static_body, (5, 100), (595, 100), 1.0)
shape.friction = 1.0
space.add(shape)

options = DrawOptions()


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

    score_label.text = 'score: ' + str(score)
    score_label.draw()

    obt.ground.draw()



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

    space.step(1 / 60)
    space.debug_draw(options)




@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print("jumping")
        obt.dino1.jump()

    if symbol == key.DOWN:
        obt.dino1.duck()


def update(dt):
    space.step(dt)

def scoreupdate(dt):
    global score
    score+=1

def spawnupdater(dt):
    # TODO: This doesn't work. as it'll still doesn't space the objects out evenly as the game speeds up
    if len(obstacle_drawlist) < 1:
        dice_throw = np.random.rand()
        pos_adjust = 1200 + np.random.rand() * 300 // 1

        if dice_throw < 0.20:  # spawn large cacti
            obstacle_drawlist.append(obt.obstacle(Vec2d(pos_adjust, 40), Vec2d(40, 60)))
        elif dice_throw < 0.40:  # Spawn smol cacti
            obstacle_drawlist.append(obt.obstacle(Vec2d(pos_adjust, 40), Vec2d(20, 30)))
        elif dice_throw < 0.60:  # spawn low flying dino
            obstacle_drawlist.append(obt.obstacle(Vec2d(pos_adjust, 80), Vec2d(80, 20)))
        elif dice_throw < 0.80:  # spawn mid flying dino
            obstacle_drawlist.append(obt.obstacle(Vec2d(pos_adjust, 160), Vec2d(80, 20)))
        elif dice_throw < 1:  # spawn high flying dino
            obstacle_drawlist.append(obt.obstacle(Vec2d(pos_adjust, 240), Vec2d(80, 20)))


pyglet.clock.schedule_interval_soft(update, 1 / 60)

pyglet.clock.schedule_interval_soft(scoreupdate, 1 / 10)

pyglet.app.run()


logging.critical("End of main")