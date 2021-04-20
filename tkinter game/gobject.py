# custom object class for location
# has 'collision detection' by checking intersections
class Gobject(object):
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.canvas = game.canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    # check if intersecting other object
    def intersect(self, other):
        if self.x + self.w >= other.x and other.x + other.w >= self.x and \
            self.y + self.h >= other.y and other.y + other.h >= self.y:
                return True
        else:
            return False