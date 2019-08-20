#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import pyglet
from pyglet.window import key
import logging
logging.basicConfig(level=logging.DEBUG)
from typing import List

import numpy as np

from population import Population

window = pyglet.window.Window(1200,800)
pyglet.gl.glClearColor(0.7,0.7,0.7,1)

import obstacle as obt

from pymunk import Vec2d



pops = Population(100)

showGraph = False
skip_once = False
score = 0

obstacle_drawlist:List[obt.obstacle] = []

score_label = pyglet.text.Label('score: ' + str(score),
                  font_name='Times New Roman',
                  font_size=12,
                  x=50, y=500 - 50,
                  anchor_x='left', anchor_y='center')

@window.event
def on_draw():
    global window
    global score

    window.clear()






    if pops.bestMeeple is not None:
        pops.bestMeeple.brain.updateposGFX([800, 500], [350, 300])
        pops.bestMeeple.brain.updateintensityGFX()
        pops.bestMeeple.brain.draw()

    # Run the game here
    # Move the objects/obstacles on the platform, not the dino or the platform
    # Use the update() and isDone() function

    score_label.text = 'score: ' + str(score)
    score_label.draw()

    obt.ground.draw()


    # -----------------
    # getting data to set the inputs of the brain
    no_distance = float("-inf")
    no_height = float("-inf")

    if obstacle_drawlist:
        next_obst = obstacle_drawlist[-1]

        for obst in obstacle_drawlist:
            if obst.pos.x > 125:
                if obst.pos.x < next_obst.pos.x:
                    next_obst = obst
            else:
                obst.sprite.color = (255,0,0)
        next_obst.sprite.color = (0,0,255)

        no_distance = next_obst.pos.x - 125
        no_height = next_obst.pos.y

    inputs = (no_distance,
              no_height,
              0,
              0)
    # -----------------

    pops.updateAlive(obstacle_drawlist, score, inputs)


    if pops.isDone():
        print("--------------------------------------------")
        print("All dino's are dead. Time for a new batch!")
        print("startin generation", pops.generation)
        pops.naturalSelection()
        obstacle_drawlist[:] = []
        score = 0



    # Obstacle garbage projection
    markforremoval = list()
    for obst in obstacle_drawlist:
        obst.update(score)
        if obst.isLeftofScreen(-100):
            markforremoval.append(obst)
            continue

        obst.draw()

    obstacle_drawlist[:] = [x for x in obstacle_drawlist if x not in markforremoval]







@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print("jumping")
        pops.pop[-1].jump()

    if symbol == key.DOWN:
        #obt.dino1.duck()
        pass


def falseupdate(dt):
    pass

def scoreupdate(dt):
    global score
    score+=1

def spawnupdater(dt):
    # TODO: This doesn't work. as it'll still doesn't space the objects out evenly as the game speeds up
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
    elif dice_throw < 1.00:  # spawn high flying dino
        obstacle_drawlist.append(obt.obstacle(Vec2d(pos_adjust, 240), Vec2d(80, 20)))


pyglet.clock.schedule_interval_soft(falseupdate, 1 / 60)
pyglet.clock.schedule_interval_soft(spawnupdater, 1.5)
pyglet.clock.schedule_interval_soft(scoreupdate, 1 / 10)
pyglet.app.run()


logging.critical("End of main")