import pygame
import sys
import os
import random
import math
from menu import *


class Player(pygame.sprite.Sprite):
    # constructor for this class
    def __init__(self):
        # call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images','player.png'))
        self.rect = self.image.get_rect()
        self.speed = [0, 0]
        self.radius = 18

    def left(self):
        self.speed[0] -= 8

    def right(self):
        self.speed[0] += 8

    def up(self):
        self.speed[1] -= 8

    def down(self):
        self.speed[1] += 8

    def move(self):
        # move the rect by the displacement ("speed")
        self.rect = self.rect.move(self.speed)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'enemy.png'))
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(75,525), random.randint(75,525)
        self.speed = [random.randint(-5,5),random.randint(-5,5)]
        self.radius = 20

class Bullet(pygame.sprite.Sprite):
    def __init__(self,start,finish,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images','bullet.png'))
        self.rect = self.image.get_rect()
        self.speed = [0,0]	
	self.rect.center = start
	diffx = finish[0]-start[0]
	diffy = finish[1]-start[1]
	dist = math.sqrt(pow(diffx,2)+pow(diffy,2))
	diffx = diffx/dist
	diffy = diffy/dist
	self.speed = [speed[0]+15*diffx,speed[1]+15*diffy]

    def move(self):
        self.rect = self.rect.move(self.speed)

def event_loop():
    # get the pygame screen and create some local vars
    screen = pygame.display.get_surface()
    screen_rect = screen.get_rect()
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    # set up font
    basicFont = pygame.font.SysFont(None, 48)
    # initialize a clock
    clock = pygame.time.Clock()
    # initialize the score counter
    score = 0
    # initialize the enemy speed and direction
    enemy_number = 2
    curr_number = 2  

    # create a sprite group for the player and enemy
    # so we can draw to the screen
    enemy_list = pygame.sprite.Group()
    enemy_list.add(Enemy())
    enemy_list.add(Enemy())
    player = Player()
    player_list = pygame.sprite.Group()
    player_list.add(player)
    bullet_list = pygame.sprite.Group()

    end = 1

    # main game loops
    while end:
        # handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.left()
                elif event.key == pygame.K_d:
                    player.right()
                elif event.key == pygame.K_w:
                    player.up()
                elif event.key == pygame.K_s:
                    player.down()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.right()
                elif event.key == pygame.K_d:
                    player.left()
                elif event.key == pygame.K_w:
                    player.down()
                elif event.key == pygame.K_s:
                    player.up()
	    elif event.type == pygame.MOUSEBUTTONDOWN:
		if event.button == 1:
	            bullet_list.add(Bullet(player.rect.center,pygame.mouse.get_pos(),player.speed))

	if len(enemy_list)==0:
	    enemy_number += 2
            curr_number = enemy_number
	    for i in xrange(curr_number):
		enemy_list.add(Enemy())     

        # call the move function for the player
	for bullet in bullet_list:
	    bullet.move()
        player.move()

        # check player bounds
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > screen_width:
            player.rect.right = screen_width
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > screen_height:
            player.rect.bottom = screen_height

        # reverse the movement direction if enemy goes out of bounds
	for it in enemy_list:
            if it.rect.left < 0 or it.rect.right > screen_width:
                it.speed[0] = -it.speed[0]
            if it.rect.top < 0 or it.rect.bottom > screen_height:
                it.speed[1] = -it.speed[1]

        # another way to move rects
	for it in enemy_list:
            it.rect.x += it.speed[0]
            it.rect.y += it.speed[1]

        # detect all collisions between the player and enemy
        if pygame.sprite.spritecollide(player, enemy_list, False,pygame.sprite.collide_circle):
	        enemy_list.empty()
	        player_list.empty()
	        bullet_list.empty()
 	        screen.fill((0,0,0))
	        end = 0
	#detect all collisions between the enemy and bullets
	for bullet in bullet_list:
	    blocks_shot_list = pygame.sprite.spritecollide(bullet,enemy_list,False,pygame.sprite.collide_circle)
	    if blocks_shot_list:
	        bullet.kill()
	        for enemy in blocks_shot_list:
	            enemy.speed = [enemy.speed[0]+0.5*bullet.speed[0],enemy.speed[1]+0.5*bullet.speed[1]]

	# detect collisions between the enemies, if collision occurs, remove enemies
	for it in enemy_list.sprites():
	    blocks_hit_list = pygame.sprite.spritecollide(it,enemy_list,False,pygame.sprite.collide_circle)
	    if len(blocks_hit_list) > 1:
	        for hit in blocks_hit_list:
	            hit.kill()
                    curr_number -= 1
                    score += 1

        # black background
        screen.fill((0, 0, 0))

        # set up the score text
        text = basicFont.render('Score: %d' % score, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.centerx = screen_rect.centerx
        textRect.centery = screen_rect.centery
        
        # draw the text onto the surface
	if(end == 1):
            screen.blit(text, textRect)

        # draw the player and enemy sprites to the screen
        bullet_list.draw(screen)
	enemy_list.draw(screen)
	player_list.draw(screen)

        # update the screen
        pygame.display.flip()

        # limit to 45 FPS
        clock.tick(45)

def main():
    # initialize pygame
    pygame.init()

    # create the window
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)

    # set the window title
    pygame.display.set_caption("You Only Live Once")

    # create the menu
    menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
                 [('Start Game',   1, None),
                  ('Exit',         2, None)])
    # center the menu
    menu.set_center(True, True)
    menu.set_alignment('center', 'center')

    # state variables for the finite state machine menu
    state = 0
    prev_state = 1
    rect_list = []

    while 1:
        # check if the state has changed, if it has, then post a user event to
        # the queue to force the menu to be shown at least once
        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state

        # get the next event
        e = pygame.event.wait()

        # update the menu
        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
            if state == 0:
                # "default" state
                rect_list, state = menu.update(e, state)
            elif state == 1:
                # start the game
                event_loop()
		state = 0
            else:
                # exit the game and program
                pygame.quit()
                sys.exit()

            # quit if the user closes the window
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # update the screen
        pygame.display.update(rect_list)

if __name__ == '__main__':
    main()
