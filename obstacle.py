import numpy as np


class Vector2f:
    def __init__(self, x:float, y:float):
        self.x:float = x
        self.y:float = y


    def __add__(self, other):
        if isinstance(Vector2f, other):
            self.x+=other.x
            self.y+=other.y
            return
        raise ValueError


    def __sub__(self, other):
        if isinstance(Vector2f, other):
            self.x-=other.x
            self.y-=other.y
            return
        raise ValueError


class Vector1f:
    def __init__(self, x:float):
        self.x:float = x

    def __add__(self, other):
        if isinstance(Vector1f, other):
            self.x+=other.x
            return
        raise ValueError




class obstacle:
    def __init__(self, pos:Vector2f, size:Vector2f):
        self.pos:Vector2f = pos
        self.size:Vector2f = size

    def isOnScreen(self, leftbound, rightbound):
        if leftbound < self.pos.x < rightbound:
            return True
        else:
            return False


class dino:
    def __init__(self, pos:Vector2f, size:Vector2f):
        self.pos:Vector2f = pos
        self.size:Vector2f = size
        self.velocity:Vector2f = Vector2f(0,0)

    def update(self):

        #apply gravity
        if self.pos.y > 40:
            self.velocity -= 2



        self.pos.y += self.velocity.y

        #stop the dino from falling through the 'floor'
        self.pos.y = max(40, self.pos.y)

    def jump(self):
        self.velocity.y += 10

obstacle_set = {"smol_cacti": obstacle(pos=Vector2f(0,0),
                                       size=Vector2f(10,10))
                }





if __name__ == "__main__":
    vec1 = Vector2f([2,2])

    print(vec1)
    vec1[0] = 3
    print(vec1)