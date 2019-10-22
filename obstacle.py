import numpy as np
import pyglet
from pymunk import Vec2d

from meeple import Meeple

image_dino:pyglet.resource.image    = pyglet.resource.image("resources/dino.png")
image_dino_size = Vec2d(40, 60)
image_ground:pyglet.resource.image  = pyglet.resource.image("resources/ground.png")
# image for the sprite of the dino-bird
# image for the sprite of the short cactus
# image for the sprite of the high cactus
# image for the sprite of the long cactus


class obstacle:
    def __init__(self, pos:Vec2d, dim:Vec2d):
        self.pos:Vec2d = pos
        self.dim:Vec2d = dim
        self.sprite = pyglet.sprite.Sprite(image_dino, x=pos.x, y=pos.y)
        self.sprite.update(scale_x=dim.x/image_dino_size.x, scale_y=dim.y/image_dino_size.y)

    def isLeftofScreen(self, leftbound):
        if leftbound > self.pos.x:
            return True
        else:
            return False

    def update(self, cur_score=5):
        new_pos_x = self.pos.x-cur_score/100-5
        self.sprite.update(x=new_pos_x)
        self.pos.x = new_pos_x

    def draw(self):
        self.sprite.draw()




class dino(Meeple):
    def __init__(self, input_size:int, hidden_size:tuple, output_size:int, isHallow=False):
        #super(Meeple, self).__init__(input_size, hidden_size, output_size, isHallow)
        super().__init__(input_size, hidden_size, output_size, isHallow)

        self.pos:Vec2d = Vec2d(100, 100)
        self.dim:Vec2d = Vec2d(50, 60)
        self.velocity:Vec2d = Vec2d(0, 0)
        self.sprite = pyglet.sprite.Sprite(image_dino, x=self.pos.x, y=self.pos.y)
        self.sprite.update(scale_x=self.dim.x/image_dino_size.x, scale_y=self.dim.y/image_dino_size.y)
        self.sprite.color = (0,255,0)

        self.jumping = False
        self.ducking = False
        self.isAlive = True

    def update(self, score):
        if self.isAlive:
            #apply gravity
            if self.pos.y > 41:
                self.velocity.y -= 1

            self.pos.y += self.velocity.y

            if self.pos.y <= 40:
                self.velocity.y = 0

            #stop the dino from falling through the 'floor'
            self.pos.y = max(40, self.pos.y)

            self.sprite.update(x=self.pos.x, y=self.pos.y)
            self.brain.score = score



    def jump(self):
        if self.pos.y <= 40:
            self.velocity.y += 20

    def duck(self):
        if self.pos.y <= 40:
            self.velocity.y -= 10

    def draw(self):
        if self.isAlive:
            self.sprite.draw()

    def isColliding(self, other):
        # TODO: Collision detection
        if self.pos.x + self.dim.x < other.pos.x:
            return False  # dinner is to the left of stacle
        elif self.pos.x > other.pos.x + other.dim.x:
            return False  # dinner is to the right of stacle

        if self.pos.y + self.dim.y < other.pos.y:
            return False  # dinner is above the stacle
        elif self.pos.y > other.pos.y + other.dim.y:
            return False  # dinner is below the stacle

        return True

    def clone(self): #->dino:
        temp:dino = dino(self.brain.input_size-1,
                         tuple([x-1 for x in self.brain.hidden_size]),
                         self.brain.output_size,
                         isHallow=True
                         )
        temp.brain = self.brain.clone()
        return temp

#    def cloneinto(self, other):
#        #This is for dealing with python's soft pointers.
#        self.brain = other.brain
#        self.fitness = other.fitness
#        self.isAlive = True
#        self.score = other.score
#        self.pos:Vec2d = Vec2d(100, 100)
#        self.dim:Vec2d = Vec2d(50, 60)
#        self.velocity:Vec2d = Vec2d(0, 0)

    def crossover(self, parent2): #parent1:dino, parent2:dino) -> dino:
        temp:dino = dino(self.brain.input_size-1,
                         tuple([x-1 for x in self.brain.hidden_size]),
                         self.brain.output_size,
                         isHallow=True
                         )
        temp.brain = self.brain.crossover(parent2.brain)
        return temp

class platform:
    def __init__(self, pos:Vec2d, dim:Vec2d):
        self.pos:Vec2d = pos
        self.dim:Vec2d = dim
        self.sprite = pyglet.sprite.Sprite(image_ground, x=pos.x, y=pos.y)

    def draw(self):
        self.sprite.draw()







obstacle_set = dict()
obstacle_set["smol_cacti"] = obstacle(pos=Vec2d(0, 0),
                                      dim=Vec2d(10, 10))


ground = platform(Vec2d(0, 10), Vec2d(1800, 60))

