import pyglet
from pyglet.window import key
import logging
import numpy
import random
import copy
logging.basicConfig(level=logging.DEBUG)

import checkergrid
import neuralnetwork

window = pyglet.window.Window(640,460)
pyglet.gl.glClearColor(0.3,0.3,0.3,1)


#randpater = numpy.random.random_integers(0,1,[2,2])
#inputchecker = checkergrid.Checker([40,300],randpater, scale=1.5)

# output checkers are just for visuals
outputchecker_1 = checkergrid.Checker([400,300],checkergrid.paterns[5], scale=1.5)

outputchecker_2 = checkergrid.Checker([400,200],checkergrid.paterns[10], scale=1.5)

label = pyglet.text.Label('score = dead',
                          font_name='Times New Roman',
                          font_size=12,
                          x=100, y=window.height-50,
                          anchor_x='center', anchor_y='center')

brains = list()
for i in range(50):
    brains.append( neuralnetwork.NeuralNetwork() )
    brains[i].updatepos( [110, 300], [240, 300])

fitnessscores = []*10


#brain = neuralnetwork.NeuralNetwork()

#brains[0].updatepos( [110, 300], [240, 300])

ptrn = 0
def nxt():
    global ptrn
    ptrn+=1

score = 0
attempt = 0
usingbrain = 0
generation = 0
pause = False
showGraph = False



@window.event
def on_draw():
    global ptrn
    global window
    global score
    global attempt
    global usingbrain
    global fitnessscores
    global generation
    global superbrainfound

    attempt += 1
    window.clear()

    #inputchecker = checkergrid.Checker([40, 300], random.choice(checkergrid.paterns), scale=1.5)
    inputchecker = checkergrid.Checker([40, 300], checkergrid.paterns[ptrn], scale=1.5)
    nxt()

    brains[usingbrain].set_input(0,inputchecker.patern[0,0])
    brains[usingbrain].set_input(1,inputchecker.patern[1,0])
    brains[usingbrain].set_input(2,inputchecker.patern[0,1])
    brains[usingbrain].set_input(3,inputchecker.patern[1,1])

    brains[usingbrain].fire_network()


    isgoodguess = False

    if brains[usingbrain].get_output(0) == 1 and brains[usingbrain].get_output(1) != 1:
        #print("1")
        if numpy.array_equal(inputchecker.patern, checkergrid.paterns[5]):
            isgoodguess = True
            #print("11")
    elif brains[usingbrain].get_output(0) != 1 and brains[usingbrain].get_output(1) == 1:
        #print("2")
        if numpy.array_equal(inputchecker.patern, checkergrid.paterns[10]):
            isgoodguess = True
            #print("22")
    elif brains[usingbrain].get_output(0) != 1 and brains[usingbrain].get_output(1) != 1:
        #print("3")
        if not numpy.array_equal(inputchecker.patern, checkergrid.paterns[10]) and not numpy.array_equal(inputchecker.patern, checkergrid.paterns[5]):
            isgoodguess = True
            #print("33")


    if isgoodguess:
        score+=1

    label.text = "score is " + str(int(score/attempt*100)) + "% out of " + str(attempt)
    label.draw()

    if showGraph:
        brains[usingbrain].updateintensity()
        checkergrid.checkerbatch.draw()
        brains[usingbrain].draw()


    if attempt == 16:

        if int(score / attempt * 100) > 99:
            pyglet.clock.unschedule(falseupdate)


        print("score of brain "+  str(usingbrain) + " is " + str(int(score/attempt*100)) + "% out of " + str(attempt))

        fitnessscores.append((usingbrain, int(score/attempt*100)))
        usingbrain+=1
        attempt=0
        score=0
        ptrn=0
        if usingbrain == 49:
            fitnessscores = sorted(fitnessscores, key=lambda x: x[1])
            print(fitnessscores[-1])

            #pyglet.app.exit()
            # if the fitness score is 100, remove the falseupdate
            #if fitnessscores[-1][1] == 100:
            #    pyglet.clock.unschedule(falseupdate)


            bestbrain = brains[fitnessscores[-1][0]]
            brains[fitnessscores[-1][0]] = None

            brains[0] = bestbrain
            for i in range(1, 50):
                brains[i] = bestbrain.clone()
                brains[i].mutateself(1/20)
            usingbrain = 0
            generation+=1
            print("Starting generation", generation)

        brains[usingbrain].updatepos([110, 300], [240, 300])




@window.event
def on_mouse_release(x, y, button, modifiers):
    pass

@window.event
def on_key_press(symbol, modifiers):
    global showGraph
    if symbol == key.SPACE:
        if showGraph:
            showGraph = False
        else:
            showGraph = True


def falseupdate(dt):
    pass

print("Starting first generation")

pyglet.clock.schedule_interval_soft(falseupdate, 1 / 120)
pyglet.app.run()


logging.critical("End of main")