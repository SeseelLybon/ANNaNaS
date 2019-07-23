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

#window = pyglet.window.Window(700,900)
#pyglet.gl.glClearColor(0.3,0.3,0.3,1)




pops = Population(500)
running = True
skipped_once = False

print("startin generation", pops.generation)

while running:


    if skipped_once and pops.allPlayersDone():
        print("Wipping up a new batch")
        pops.calculateFitness()
        print("Best of generation is", pops.bestPlayeri, pops.players[pops.bestPlayeri].fitness)
        pops.naturalSelection()
        print("startin generation", pops.generation)

    skipped_once = True

    pops.update()
    pops.setBestBrain()
    pops.calculateFitness()



logging.critical("End of main")