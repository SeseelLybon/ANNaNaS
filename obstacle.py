import numpy as np
import pyglet


class Vector2f:
    def __init__(self, x:float, y:float):
        self.x:float = x
        self.y:float = y


    def __add__(self, other):
        if isinstance(other, Vector2f):
            self.x+=other.x
            self.y+=other.y
            return
        raise ValueError


    def __sub__(self, other):
        if isinstance(other, Vector2f):
            self.x-=other.x
            self.y-=other.y
            return
        raise ValueError


class Vector1f:
    def __init__(self, x:float):
        self.x:float = x

    def __add__(self, other):
        if isinstance(other, Vector2f):
            self.x+=other.x
            return
        raise ValueError


image_dino:pyglet.resource.image    = pyglet.resource.image("resources/dino.png")
image_dino_size = Vector2f(40,60)
image_ground:pyglet.resource.image  = pyglet.resource.image("resources/ground.png")
# image for the sprite of the dino-bird
# image for the sprite of the short cactus
# image for the sprite of the high cactus
# image for the sprite of the long cactus



class obstacle:
    def __init__(self, pos:Vector2f, dim:Vector2f):
        self.pos:Vector2f = pos
        self.dim:Vector2f = dim
        self.sprite = pyglet.sprite.Sprite(image_dino, x=pos.x, y=pos.y)
        self.sprite.update(scale_x=dim.x/image_dino_size.x, scale_y=dim.x/image_dino_size.x)

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


class dino:
    def __init__(self, pos:Vector2f, dim:Vector2f):
        self.pos:Vector2f = pos
        self.dim:Vector2f = dim
        self.velocity:Vector2f = Vector2f(0,0)
        self.sprite = pyglet.sprite.Sprite(image_dino, x=pos.x, y=pos.y)
        self.sprite.update(scale_x=dim.x/image_dino_size.x, scale_y=dim.x/image_dino_size.x)

        self.jumping = False
        self.ducking = False


    def update(self):



        #apply gravity
        if self.pos.y > 41:
            self.velocity.y -= 1

        self.pos.y += self.velocity.y

        if self.pos.y <= 40:
            self.velocity.y = 0

        #stop the dino from falling through the 'floor'
        self.pos.y = max(40, self.pos.y)

        self.sprite.update(x=self.pos.x, y=self.pos.y)

    def jump(self):
        if self.pos.y <= 40:
            self.velocity.y += 20

    def duck(self):
        if self.pos.y > 40:
            print("Falling faster")
            self.velocity.y -= 20
        elif self.pos.y == 40:
            #TODO: Morph dino shape
            print("Morph")
            pass
        else:
            # TODO: Unmorph dino shape
            print("Unmorph")
            pass

    def draw(self):
        self.sprite.draw()

class platform:
    def __init__(self, pos:Vector2f, dim:Vector2f):
        self.pos:Vector2f = pos
        self.dim:Vector2f = dim
        self.sprite = pyglet.sprite.Sprite(image_ground, x=pos.x, y=pos.y)

    def draw(self):
        self.sprite.draw()


obstacle_set = {"smol_cacti": obstacle(pos=Vector2f(0,0),
                                       dim=Vector2f(10,10))
                }


dino1 = dino(Vector2f(100,100),Vector2f(50,60))
ground = platform(Vector2f(0,10),Vector2f(1800,60))

