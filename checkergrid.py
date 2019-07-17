

import numpy
import pyglet

batch = pyglet.graphics.Batch()

image_blacktile = pyglet.resource.image("resources/" + "blacktile.png")
image_whitetile = pyglet.resource.image("resources/" + "whitetile.png")

class Checker:

    def __init__(self, pos, patern,scale=1):
        self.pos = vector2d(pos)
        self.patern = patern
        self.scale = scale
        self.sprites = [[None, None], [None, None]]
        for x in range(0,len(self.patern)):
            for y in range(0,len(self.patern[x,:])):
                if self.patern[x,y] == 0:
                    self.sprites[x][y] = pyglet.sprite.Sprite(image_blacktile, x=self.pos.x+x*20*self.scale,
                                                                               y=self.pos.y+y*20*self.scale,
                                                             batch=batch )
                    self.sprites[x][y].scale = self.scale
                elif self.patern[x,y] == 1:
                    self.sprites[x][y] = pyglet.sprite.Sprite(image_whitetile, x=self.pos.x+x*20*self.scale,
                                                                               y=self.pos.y+y*20*self.scale,
                                                             batch=batch )
                    self.sprites[x][y].scale = self.scale

    def updatespritepos(self, pos):
        for x in range(0,len(self.patern)):
            for y in range(0,len(self.patern[x,:])):
                self.sprites[x][y].update(x=pos[0],y=pos[1])


class vector2d:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]




def gen_random_pater(dim):
    pass

paterns = numpy.array(numpy.meshgrid([0,1],[0,1],[0,1],[0,1])).T.reshape(16,2,2)

# -------- general storage of paterns
if __name__ == "__main__":
    print(paterns)

