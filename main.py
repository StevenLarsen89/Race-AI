# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:03:30 2019

My first attempt at a game in python
This is a racing game.
Game will stop if car crashes

@author: Steven
"""
## preample ##

# import library
import pygame
import time
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

# initiate pygame
pygame.init()

# pygame module for loading and playing sounds
pygame.mixer.init()

# define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (112, 209, 48)
gray = (109, 109, 109)
beige = (237, 207, 132)

car_width = 100
car_height = 100
carSpeed = 5

## GAME OPTIONS ##

# game resolution
display_width = 800
display_height = 600

rdpaint = [200, 300, 400, 500, 600]

# set size of game display
gameDisplay = pygame.display.set_mode((display_width, display_height))
# title of game window
pygame.display.set_caption('Ghost Driver')
# define game clock
clock = pygame.time.Clock()

# ASSETS

# Load graphics
playerImg = pygame.image.load(path.join(img_dir, 'car.png')).convert_alpha()


# Sprites
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerImg, (car_width, car_height))
        self.rect = self.image.get_rect()
        self.rect.centerx = display_width / 2
        self.rect.bottom = display_height * 0.8
        self.speedx = 0
        self.speedy = 0

    def update(self):

        # stops movement when no keys are pressed
        self.speedx = 0
        self.speedy = 0

        # player movement
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -carSpeed
        if keystate[pygame.K_RIGHT]:
            self.speedx = carSpeed
        self.rect.x += self.speedx

        if keystate[pygame.K_UP]:
            self.speedy = -carSpeed
        if keystate[pygame.K_DOWN]:
            self.speedy = carSpeed
        self.rect.y += self.speedy


class Object(pygame.sprite.Sprite):
    def __init__(self, nr):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, 'Car_{0}.png'.format(nr))).convert_alpha()
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.scale(self.image, (car_width, car_height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(display_width * 0.25 - self.rect.width / 2,
                                       display_width * 0.75 - self.rect.width / 2)
        self.rect.y = random.randrange(-1200, -100)
        self.speedy = 6

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > display_height + 45:
            self.rect.x = random.randrange(display_width * 0.25 - self.rect.width / 2,
                                           display_width * 0.75 - self.rect.width / 2)
            self.rect.y = random.randrange(-1200, -100)
            self.speedy = 6


class Road(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((display_width * 0.6, display_height))
        self.image.fill(gray)
        self.rect = self.image.get_rect()
        self.rect.centerx = display_width / 2
        self.rect.bottom = display_height


class Roadside(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((display_width * 0.7, display_height))
        self.image.fill(beige)
        self.rect = self.image.get_rect()
        self.rect.centerx = display_width / 2
        self.rect.bottom = display_height


class Roadpaint(pygame.sprite.Sprite):
    def __init__(self, xloc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 30))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = xloc
        self.rect.y = -100
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy

        if self.rect.top > display_height:
            self.kill()


# Definitions
def time_passed(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Time passed: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def distance(cord_x, cord_y, text_loc_y, object):
    font = pygame.font.SysFont(None, 25)
    text = font.render(str(object) + ": (" + str(cord_x) + ", " + str(cord_y) + ")", True, black)
    gameDisplay.blit(text, (0, text_loc_y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, placement_x, placement_y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (placement_x, placement_y)
    surf.blit(text_surface, text_rect)


def show_go_screen():
    gameDisplay.fill(white)
    draw_text(gameDisplay, 'Ghost Driver', 64, display_width / 2, display_height / 4)
    draw_text(gameDisplay, 'Arrow keys to move', 32, display_width / 2, display_height / 2)
    draw_text(gameDisplay, 'Press any key to start', 24, display_width / 2, display_height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def game_loop():
    # game stop parameter
    gameExit = False
    gameOver = True
    n_objects = 7

    # game will run so long as crashed is equal to false
    while not gameExit:
        # define clock / frames per second
        clock.tick(80)
        if gameOver:
            show_go_screen()
            gameOver = False
            startTime = time.time()
            all_sprites = pygame.sprite.Group()
            road_sprites = pygame.sprite.Group()
            road_paint_sprites = pygame.sprite.Group()
            blocks = pygame.sprite.Group()
            player = Player()
            road = Road()
            roadside = Roadside()
            road_sprites.add(roadside)
            road_sprites.add(road)
            all_sprites.add(player)

            for i in range(1, n_objects + 1):
                m = Object(nr=random.randrange(1, 6))
                # overlap = pygame.sprite.spritecollide(m, blocks, False, pygame.sprite.collide_mask)
                all_sprites.add(m)
                blocks.add(m)
                # draw_text(gameDisplay, 'No overlap', 32, display_width / 2, display_height / 2)

        timePassed = round((time.time() - startTime), 1)

        # spawns road paint
        if timePassed % 1 == 0:
            for i in range(0, 5):
                r = Roadpaint(xloc=rdpaint[i])
                road_paint_sprites.add(r)

        ## EVENTS ##
        # gets all events happening in the game cursor movements, key clicks etc. 
        for event in pygame.event.get():
            # if user clicks on 'x' in top right corner, set 'crashed' to True, thereby ending game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        ## UPDATE GAME STATE ##

        # update all_sprites group
        all_sprites.update()
        road_paint_sprites.update()

        # TODO: If object collide then kill() them

        # TODO: Change care speed when in ditch

        # TODO: Add new objects to ditch

        # collision detection
        hits = pygame.sprite.spritecollide(player, blocks, False, pygame.sprite.collide_mask)

        # hits = pygame.sprite.collide_mask(player, object)
        if hits:
            gameOver = True

        timePassed = round((time.time() - startTime), 4)

        ## RENDER ###
        # background color of game
        gameDisplay.fill(green)

        # pygame.draw.rect(gameDisplay, white, [display_width/2, display_height/2, 50, 50])

        # sprites
        road_sprites.draw(gameDisplay)
        # road_paint_sprites.draw(gameDisplay)
        all_sprites.draw(gameDisplay)

        # score
        time_passed(timePassed)

        # distance
        list_blocks = blocks.sprites()
        # y_dist = player.rect.top - list_blocks[1].rect.bottom
        # x_dist = player.rect.center[0] - list_blocks[1].rect.center[0]

        for i in range(0, n_objects):
            y_dist = list_blocks[i].rect.center[1]
            x_dist = list_blocks[i].rect.center[0]
            down = 25 * (i + 1)
            distance(x_dist, y_dist, down, "Car " + str(i + 1))

        # update display after events
        pygame.display.flip()


# run game loop
game_loop()

# stop pygame
pygame.quit()

# stop .py program
quit()
