# import packages
from tkinter import *
from alien import *
from projectile import *
from player import *
import time
import random

class Game(object):
    # initialize application
    def __init__(self, fps, width=400, height=400, enemies=3):
        # general configuration
        self.width = width
        self.height = height
    
        self.fps = fps
        self.enemies = enemies
        
        # tkinter configuration
        self.root = Tk()
        self.root.geometry(str(width) + 'x' + str(height))
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()

        # handle keyboard input
        def key_handler(event):
            # keystroke debugging vvv
            # print(event.char, event.keysym, event.keycode)

            if event.keycode == 32: # space key
                self.player.shoot()
            elif event.keycode == 37: # left key
                self.player.move(-200)
            elif event.keycode == 39: # right key
                self.player.move(200)
        self.root.bind("<Key>", key_handler)
 
        # starts a game session
        self.start_game()
    
    # beginning of a game
    def start_game(self):
        # remove anything currently on canvas
        self.canvas.delete("all")
        
        # initialize player and alien objects
        self.player = Player(self, 200, 350, 15, 15)

        self.aliens = []            
        for i in range(self.enemies):
            self.spawn_enemy(random.randint(10, 381), random.randint(0, 341))

        # initialize win / lose states
        self.win = False
        self.lose = False

        # playable part of the game
        self.game_loop()
        
    def spawn_enemy(self, x, y):
        new_alien = Alien(self, x, y, 10, 10)
        self.aliens.append(new_alien)

    # main game loop
    def game_loop(self):
        while True:
            # update player and alien objects
            self.player.update()
            
            for alien in self.aliens:
                alien.update()

                # remove alien when they're dead (including projectiles)
                if alien.can_remove: 
                    self.aliens.remove(alien)
                    del alien
            
            # tk update
            self.root.update_idletasks()
            self.root.update()

            # frame rate handling
            time.sleep(1.0 / self.fps)
            
            # win if there are no more aliens
            if len(self.aliens)==0: 
                self.win = True

            # handle win / loss
            if self.win:
                self.game_win()
                return
            elif self.lose:
                self.game_over()
                return

    # when game is won
    def game_win(self):
        # 'you win' text and new start game button
        self.canvas.delete("all")
        self.canvas.create_text(200, 200, text="You Win")
        self.canvas.pack()
        restart_button = Button(self.canvas, text="Restart Game", width=20,
                            command=lambda: self.stop_win())
        restart_button.pack()
        restart_button.place(x=130, y=300)

        # tk update
        while self.win:
            self.root.update()
            self.root.update_idletasks()

        # destroy button widget then start new game (restart_button clicked)
        restart_button.destroy()
        self.start_game()

    # helper win screen function for button widget
    def stop_win(self):
        self.win = False

    # when game is loss
    def game_over(self):
        # removes all alien objects
        for alien in self.aliens:
            self.aliens.remove(alien)
            alien.destruct()

        # create 'game over' text and start game button widget
        self.canvas.delete("all")
        self.canvas.create_text(200, 200, text="Game Over")
        self.canvas.pack()
        restart_button = Button(self.canvas, text="Restart Game", width=20,
                            command=lambda: self.stop_lose())
        restart_button.pack()
        restart_button.place(x=130, y=300)

        # tk update
        while self.lose:
            self.root.update()
            self.root.update_idletasks()

        # destroy button widget then start new game (restart_button clicked)
        restart_button.destroy()
        self.start_game()

    # helper lose screen function for button widget
    def stop_lose(self):
        self.lose = False

# create a game with 60 fps
game = Game(60)