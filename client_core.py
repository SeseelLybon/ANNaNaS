#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import pyglet
from typing import List

import numpy as np
from population import Population

import serpent

window = pyglet.window.Window(1200,800)
pyglet.gl.glClearColor(0.7,0.7,0.7,1)

import obstacle as obt

from pymunk import Vec2d

client_population:Population = Population(1, input_size=7, hidden_size=tuple([0]), output_size=2, isHallow=True)

showGraph = False
skip_once = False
score = 0
best_score = 0
bestfitness = 0
lastspawnscore = 0
max_obstacles = 3

client_isDone = False

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
    global client_population
    global window
    global score
    global lastspawnscore
    global showGraph

    window.clear()

    if client_population.bestMeeple is not None and showGraph:
        client_population.bestMeeple.brain.updateposGFX([600, 750], [550, 500])
        client_population.bestMeeple.brain.updateintensityGFX([2, 2,  # dinner pos
                                                               0.5, 2, 3, 3,  # first object
                                                               1.5])       # score
        client_population.bestMeeple.brain.draw()

    # Run the game here
    # Move the objects/obstacles on the platform, not the dino or the platform
    # Use the update() and isDone() function

    score_label.text = 'score: ' + str(score)
    score_label.draw()
    score_best_label.text = 'best score: ' + str(client_population.highestScore)
    score_best_label.draw()
    dinos_live_label.text = "Dino's alive: " + str(client_population.countAlive()) + " of " + str(100)
    dinos_live_label.draw()

    obt.ground.draw()

    client_population.drawAlife()

    for obst in obstacle_drawlist:
        obst.draw()
    #pops.bestMeeple.draw()



def update(dt):
    global client_population
    global client_isDone
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


    global_inputs.append(score)
    # -----------------

    client_population.updateAlive(obstacle_drawlist, score, global_inputs)


    if client_population.isDone():
        print("--------------------------------------------")
        print("All dino's are dead. Returning dino brains.")
        print("Best score this batch:", score)
        pyglet.clock.unschedule(update)
        pyglet.clock.unschedule(scoreupdate)
        client_isDone = True

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


def dojob(job):
    global client_population
    global client_isDone
    global score
    global bestfitness
    global lastspawnscore
    global best_score
    global obstacle_drawlist

    client_isDone = False

    print("Starting the job batch")

    # Resetting the variables of the sim...
    score = 0
    best_score = 0
    bestfitness = 0
    lastspawnscore = 0
    obstacle_drawlist = []

    # unpack job (a pickle of a list of meeple brains)
    client_population = Population(len(job), input_size=7, hidden_size=tuple([0]), output_size=2, isHallow=True)

    client_population.unpickle_population_from_list(job)

    for meep in client_population.pop:
        meep.brain.score = 0
        meep.brain.fitness = 0

    # start the simulation and poll if it's done
    pyglet.clock.schedule_interval_soft(update, 1 / 75)
    pyglet.clock.schedule_interval_soft(scoreupdate, 1 / 10)




