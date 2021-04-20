# import packages
from gobject import *

# projectiles (pew pew)
class Projectile(Gobject):
    def __init__(self, game, x, y, w, h, color='black'):
        super().__init__(game, x, y, w, h)

        # draw projectile
        self.id = self.canvas.create_oval(x, y, x+w, y+h, 
                            outline='black', fill=color)
        self.canvas.pack()

        # initialize as not dead
        self.dead = False
        
    # handle movement
    def move(self, speed): 
        # destroy if outside of screen
        if self.y <= 0 or self.y >= self.game.height:
            self.destruct()
            return
        
        # move up / down
        y_movement = speed / self.game.fps
        self.y += y_movement

        # draw movement
        self.canvas.move(self.id, 0, y_movement)
        self.canvas.pack()

    # destroys projectile by declaring dead and removing from canvas
    def destruct(self):
        self.dead = True
        self.canvas.delete(self.id) 

# player projectile (for player and attacks enemies)
class PlayerProjectile(Projectile):
    def __init__(self, game, x, y, w, h):
        super().__init__(game, x, y, w, h, 'pink')

    # general update in game loop function
    def update(self):
        # moves upwards
        self.move(-250)

        # checks for collision with all surviving aliens
        for alien in self.game.aliens:
            if self.intersect(alien):
                alien.destruct()
                self.destruct()

# enemy projectile (for alien and attacks player)
class EnemyProjectile(Projectile):
    def __init__(self, game, x, y, w, h):
        super().__init__(game, x, y, w, h, 'purple')

    # general update in game loop function
    def update(self):
        # moves downwards
        self.move(250)

        # checks for collision with player
        if self.intersect(self.game.player):
            self.destruct()
            self.game.lose = True
            return
    