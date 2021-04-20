# import packages
from gobject import *
from projectile import *

# player (shoot at enemies and win!)
class Player(Gobject):
    def __init__(self, game, x, y, w, h):
        super().__init__(game, x, y, w, h)

        # draw player on canvas
        self.id = self.canvas.create_oval(x, y, x+w, y+h, 
                    outline='black', fill='lime')
                    
        # initialize list of bullets
        self.bullets = []

    # general update in game loop function
    def update(self):
        # update all player bullets
        for bullet in self.bullets:
            bullet.update()

    # handle movement (called by keystroke handler)
    def move(self, speed):
        # change movement
        x_movement = speed / self.game.fps
        self.x += x_movement 

        # move on canvas
        self.canvas.move(self.id, x_movement, 0)
        self.canvas.pack()

    # shoot player projectile (upwards and attacks enemies)
    def shoot(self):
        self.bullets.append(PlayerProjectile(
            self.game, self.x, self.y, self.w/2, self.h/1.5))