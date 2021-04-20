# import packages
from projectile import *
from gobject import *
from utilities import *
import time
import random

# alien (enemies that shoot)
class Alien(Gobject):
    def __init__(self, game, x, y, w, h):
        super().__init__(game, x, y, w, h)

        # draw alien on canvas
        self.id = self.canvas.create_oval(x, y, x+w, y+h, outline='black', fill='red')
        self.canvas.pack()
        
        # initialize starting direction
        directions = ['right', 'left']
        self.direction = random.choice(directions)

        # initialize bullets, and timer for when to shoot next bullet
        self.bullets = []
        self.bullet_start = time.time()
        self.bullet_time = linear_random(1)

        # initialize alien as not dead and not removable
        self.dead = False
        self.can_remove = False
        
    # handle movement
    def move(self, speed):
        x_movement = 0
        fps = self.game.fps
        # moves in desired direction
        # if no more room to move, will reverse direction
        if self.direction == 'right':
            if self.x < self.game.width:
                x_movement += speed / fps
            else:
                self.direction = 'left'
                x_movement -= speed / fps
        elif self.direction == 'left':
            if self.x > 0:
                x_movement -= speed / fps
            else:
                self.direction = 'right'
                x_movement += speed / fps

        self.x += x_movement 

        # draws movement on canvas
        self.canvas.move(self.id, x_movement, 0)
        self.canvas.pack()
    
    # general update in game loop function
    def update(self):
        # calls move function
        self.move(100)

        # timer for when to shoot next bullet
        if time.time() - self.bullet_start >= self.bullet_time:
            self.bullet_start = time.time()
            self.bullet_time = linear_random(1)
            self.shoot()

        # updates all bullets
        for bullet in self.bullets:
            bullet.update()
            
            # if bullet is dead, remove from list
            if bullet.dead:
                self.bullets.remove(bullet)
                del bullet

        # when alien's dead and no more bullets alive, 
        # alien can be removed 
        if self.dead and len(self.bullets)==0: 
            self.can_remove = True

    # shoot enemy projectile to attack player
    def shoot(self):
        if not self.dead:
            self.bullets.append(EnemyProjectile(self.game, self.x, self.y, self.w/2, self.h/1.5))

    # destroy alien by removing on canvas and declaring dead
    def destruct(self):
        self.canvas.delete(self.id)
        self.dead = True

    # just for debugging :)
    def __str__(self):
        return 'Alien #' + str(self.id) + \
                ': (' + str(self.x) + ',' + str(self.y) + ')'