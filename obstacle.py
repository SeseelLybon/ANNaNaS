import numpy as np
import pyglet
from pymunk import Vec2d



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




class dino:
    def __init__(self, pos:Vec2d, dim:Vec2d):
        self.pos:Vec2d = pos
        self.dim:Vec2d = dim
        self.velocity:Vec2d = Vec2d(0, 0)
        self.sprite = pyglet.sprite.Sprite(image_dino, x=pos.x, y=pos.y)
        self.sprite.update(scale_x=dim.x/image_dino_size.x, scale_y=dim.y/image_dino_size.y)

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

    def draw(self):
        self.sprite.draw()

class platform:
    def __init__(self, pos:Vec2d, dim:Vec2d):
        self.pos:Vec2d = pos
        self.dim:Vec2d = dim
        self.sprite = pyglet.sprite.Sprite(image_ground, x=pos.x, y=pos.y)

    def draw(self):
        self.sprite.draw()


def isColliding(dinner, stacle):
    # TODO: Collision detection
    if dinner.pos.x+dinner.dim.x < stacle.pos.x:
        return False # dinner is to the left of stacle
    elif dinner.pos.x > stacle.pos.x+stacle.dim.x:
        return False # dinner is to the right of stacle

    if dinner.pos.y > stacle.pos.y+stacle.dim.y:
        return False # dinner is above the stacle
    elif dinner.pos.y + dinner.dim.y > stacle.pos.y:
        return False # dinner is below the stacle

    return True




obstacle_set = dict()
obstacle_set["smol_cacti"] = obstacle(pos=Vec2d(0, 0),
                                      dim=Vec2d(10, 10))


dino1 = dino(Vec2d(100, 100), Vec2d(50, 60))
ground = platform(Vec2d(0, 10), Vec2d(1800, 60))

