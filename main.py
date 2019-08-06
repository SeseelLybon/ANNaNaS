#-------------------------------------
# Inspired by Code Bullet,
#             3blue1brown
#
#-------------------------------------


import pyglet
from pyglet.window import key
import logging
logging.basicConfig(level=logging.DEBUG)

import checkergrid
from population import Population

window = pyglet.window.Window(700,900)
pyglet.gl.glClearColor(0.3,0.3,0.3,1)


#randpater = numpy.random.random_integers(0,1,[2,2])
#inputchecker = checkergrid.Checker([40,300],randpater, scale=1.5)

# output checkers are just for visuals

outputcheckers = list()
for i in range(16):
        outputcheckers.append( checkergrid.Checker([600,800-50*i],
                                                   checkergrid.paterns[i],
                                                   scale=1) )

pops = Population(1000)


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

    if not perfectBrainFound:
        print("startin generation", pops.generation)

        if skip_once:
            print("Generating generation", pops.generation)
            pops.naturalSelection()
        skip_once = True

        print("Starting tests")
        #per brain
        for braini in range(len(pops.meeps)):
        #for braini in range(1):
            #per patern
            score_total = 0
            score_total_c = 0
            score_total_w = 0


            # First test if it can turn on all the correct one.
            for paterni in range(16):
                pops.meeps[braini].set_input(0, checkergrid.paterns[paterni][0, 0])
                pops.meeps[braini].set_input(1, checkergrid.paterns[paterni][1, 0])
                pops.meeps[braini].set_input(2, checkergrid.paterns[paterni][0, 1])
                pops.meeps[braini].set_input(3, checkergrid.paterns[paterni][1, 1])

                pops.meeps[braini].fire_network()

                score_patern_c = 0
                score_patern_w = 0

                for i in range(16): # Going through all outputs! Not paterns
                    temp = pops.meeps[braini].get_output(i)
                    if paterni == i and temp >= 0.9:
                        score_patern_c+=17
                    if paterni != i and temp <= 0.1:
                        score_patern_w+=1

                score_total_c+= score_patern_c
                score_total_w+= score_patern_w



            score_total+= score_total_c
            if score_total_c >= 17 * 16:  # 272
                score_total+= score_total_w




            #totalscoreavg=totalscoresum/16
            #pops.brains[braini].fitness=10/max(totalscoreavg, 0.001)
            pops.meeps[braini].fitness=score_total



        print("Done with testing")
        pops.setBestBrain()
        if pops.meeps[pops.bestBraini].fitness == 10/0.00001:
            print("found perfect brain")
            pyglet.clock.unschedule(falseupdate)
            showGraph = True
            perfectBrainFound = True
            print("Best of generation is", pops.bestBraini, pops.meeps[pops.bestBraini].fitness)
            return

        print("Best of generation is", pops.bestBraini, pops.meeps[pops.bestBraini].fitness)
        print("Generating new generation")
        #generate new brains
        pops.calculateFitnessSum()
        #pops.naturalSelection()

    else:

        inputchecker = checkergrid.Checker([10,600],checkergrid.paterns[patern], scale=1.5)
        pops.meeps[pops.bestBraini].set_input(0, checkergrid.paterns[patern][0, 0])
        pops.meeps[pops.bestBraini].set_input(1, checkergrid.paterns[patern][1, 0])
        pops.meeps[pops.bestBraini].set_input(2, checkergrid.paterns[patern][0, 1])
        pops.meeps[pops.bestBraini].set_input(3, checkergrid.paterns[patern][1, 1])

        pops.meeps[pops.bestBraini].fire_network()

        patern+=1
        patern=patern%16

    if pops.bestBraini != -1:
        pops.meeps[pops.bestBraini].updateposGFX([90, 810], [450, 800])
        pops.meeps[pops.bestBraini].updateintensityGFX()
        pops.meeps[pops.bestBraini].draw()
        checkergrid.checkerbatch.draw()




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