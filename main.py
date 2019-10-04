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

loadfromfile = True
savePopulation = True

if loadfromfile:
    print("Loading population from file")
    pops = Population(50, input_size=7, hidden_size=tuple([4]), output_size=2, isHallow=True)
    pops.unpickle_population_from_file()
else:
    print("Generating new population")
    pops = Population(50, input_size=7, hidden_size=tuple([4]), output_size=2)

showGraph = False
skip_once = False
score = 0
best_score = 0
bestfitness = 0
lastspawnscore = 0
max_obstacles = 3

obstacle_drawlist:List[obt.obstacle] = []

score_label = pyglet.text.Label('score: ' + str(score),
                  font_name='Times New Roman',
                  font_size=12,
                  x=50, y=450,
                  anchor_x='left', anchor_y='center')
score_best_label = pyglet.text.Label('best score: ',
                  font_name='Times New Roman',
                  font_size=12,
                  x=50, y=425,
                  anchor_x='left', anchor_y='center')
dinos_live_label = pyglet.text.Label("Dino's alive: ",
                   font_name='Times New Roman',
                   font_size=12,
                   x=50, y=400,
                   anchor_x='left', anchor_y='center')

@window.event
def on_draw():
    global window
    global score
    global lastspawnscore

    window.clear()

    if pops.bestMeeple is not None:
        pops.bestMeeple.brain.updateposGFX([600, 750], [550, 500])
        pops.bestMeeple.brain.updateintensityGFX([2,2,      # dinner pos
                                                  0.5,2,3,3,  # first object
                                                  1.5])       # score
        pops.bestMeeple.brain.draw()

    # Run the game here
    # Move the objects/obstacles on the platform, not the dino or the platform
    # Use the update() and isDone() function

    score_label.text = 'score: ' + str(score)
    score_label.draw()
    score_best_label.text = 'best score: ' + str(pops.highestScore)
    score_best_label.draw()
    dinos_live_label.text = "Dino's alive: " + str(pops.countAlive()) + " of " + str(100)
    dinos_live_label.draw()

    obt.ground.draw()

    pops.drawAlife()

    for obst in obstacle_drawlist:
        obst.draw()
    #pops.bestMeeple.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print("Stopping program")
        pyglet.app.exit()
        if savePopulation:
            print("Saving population to file")
            pops.pickle_population_to_file()
        else:
            print("Not saving population to file")

def update(dt):
    global score
    global bestfitness
    global lastspawnscore

    global_inputs  = []

    # -----------------
    # getting data to set the inputs of the brain

    #go through each obstacle and append inputs
    if len(obstacle_drawlist) > 0:
        closestobst = obstacle_drawlist[0]
    else:
        closestobst = None

    if closestobst is None:
        obst_distance = 2000
        obst_height = 0
        obst_x = 0
        obst_y = 0
    else:
        obst_distance = closestobst.pos.x
        obst_height = closestobst.pos.y
        obst_x = closestobst.dim.x
        obst_y = closestobst.dim.y


    global_inputs += [obst_distance,
                      obst_height,
                      obst_x,
                      obst_y]

    ##generate fake data for the obstacles that are missing
    #if len(obstacle_drawlist) < max_obstacles:
    #    for fake_obst in range( max_obstacles-len(obstacle_drawlist) ):
    #        global_inputs += [5000,
    #                          0,
    #                          0,
    #                          0]


    global_inputs.append(score)
    # -----------------

    pops.updateAlive(obstacle_drawlist, score, global_inputs)


    if pops.isDone():
        print("--------------------------------------------")
        print("All dino's are dead. Time for a new batch!")
        print("Best score this generation:", score)
        print("startin generation", pops.generation)
        pops.naturalSelection()
        obstacle_drawlist[:] = []
        score = 0
        bestfitness = 0
        lastspawnscore = 0

    score = round(score+0.3, 1)
    if score - lastspawnscore > 40:
        spawnupdater(1)
        lastspawnscore = score


    # Obstacle garbage projection
    markforremoval = list()
    for obst in obstacle_drawlist:
        obst.update(score)
        if obst.isLeftofScreen(-100):
            markforremoval.append(obst)
            continue

    if len(markforremoval) > 0:
        obstacle_drawlist[:] = [x for x in obstacle_drawlist if x not in markforremoval]



def scoreupdate(dt):
    global score
    score+=1

def spawnupdater(dt):
    # TODO: This doesn't work. as it'll still doesn't space the objects out evenly as the game speeds up
    #if len(obstacle_drawlist) < max_obstacles:
    dice_throw = np.random.rand()
    pos_adjust = 1500# + np.random.rand() * 300 // 1

    if score < 400:
        if dice_throw < 0.50:  # spawn large cacti
            obstacle_drawlist.append(obt.obstacle(Vec2d(pos_adjust, 40), Vec2d(40, 60)))
        else:  # Spawn smol cacti
            obstacle_drawlist.append(obt.obstacle(Vec2d(pos_adjust, 40), Vec2d(20, 30)))
    else:
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


pyglet.clock.schedule_interval_soft(update, 1 / 75)
#pyglet.clock.schedule_interval_soft(spawnupdater, 1.5)
pyglet.clock.schedule_interval_soft(scoreupdate, 1 / 10)
pyglet.app.run()


logging.critical("End of main")