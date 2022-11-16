#notice: if using VS code IDE, firstly open the folder inside it and run the code
import random
import sys
from msilib.schema import Directory
from tkinter import CENTER
from turtle import color
from random import randint
import pygame
from pygame import mixer
from pygame.math import Vector2
import time
from time import sleep
pygame.init()
#class for snake object that contains functions that makes the object move/animated
count =0
class OBSTACLE:
    def __init__(self):
        self.body = [Vector2(8,3), Vector2(8,4), Vector2(8,5)]
        for i in range(6,9,1):
            self.body.append(Vector2(8,i))
        for i in range(8,2,-1):
            self.body.append(Vector2(i, 9))
        for i in range(3,9,1):
            self.body.append(Vector2(12,i))
        for i in range(12, 17,1):
            self.body.append(Vector2(i, 9))
        for i in range(18, 12, -1):
            self.body.append(Vector2(8, i))
        for i in range(8, 2, -1):
            self.body.append(Vector2(i, 12))
        for i in range(12,17,1):
            self.body.append(Vector2(i, 12))
        for i in range(18,12, -1):
            self.body.append(Vector2(12, i))
        
        
    def draw_obtacle(self):
        for index, block in enumerate(self.body):
            #We still need a rect for the positioning
            x_pos = int(block.x *cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            screen.blit(Obstacle_image, block_rect)

class SNAKE:
    scrore = 0
    def __init__(self):
        #three initial block, default snake length(vector 2 gives us chance to specify not only x, but also y positioning, these feature will be use to move snake smothly to different positions)
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        SNAKE.scrore = len(self.body)
        #initial direction when the game is started
        self.direction = Vector2(1,0)
        #setting initial condition that the snake doesn't append till the it would not be stated as true in other function inside snake class
        self.new_block = False
        #specifing and loading images for making our snake more or less beatutiful
        self.head_up = pygame.image.load("images/head_up.png").convert_alpha()
        self.head_down = pygame.transform.rotate(self.head_up, 180)
        self.head_right = pygame.transform.rotate(self.head_up, -90)
        self.head_left = pygame.transform.rotate(self.head_up, 90)

        self.tail_up = pygame.image.load('images/tail_up.png').convert_alpha()
        self.tail_down = pygame.transform.rotate(self.tail_up, 180)
        self.tail_right = pygame.transform.rotate(self.tail_up, -90)
        self.tail_left = pygame.transform.rotate(self.tail_up, 90)

        self.body_vertical = pygame.image.load('images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.transform.rotate(self.body_vertical, 90)

        self.body_tr = pygame.image.load('images/body_tr.png').convert_alpha()
        self.body_tl = pygame.transform.rotate(self.body_tr, 90)
        self.body_br = pygame.transform.rotate(self.body_tr, -90)
        self.body_bl = pygame.transform.rotate(self.body_tr, 180)
        #loading and creating variables for sound effects
        self.crunch_sound = pygame.mixer.Sound("audios/snake_eat.wav")
        self.following_sound = pygame.mixer.Sound("audios/rattle_snake.wav")
        #function for applying the loaded images as the graphics/giving specific image to different positioning and blocks
    def draw_snake(self):
        #for making the code clear condition for changing an image of specif block fas defined outside
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            #We still need a rect for the positioning
            x_pos = int(block.x *cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            #for what block do we need to put head image(at this point only about the block number, not position for change to left/right/bottom..)
            if index == 0:
                screen.blit(self.head, block_rect)
            #for what block do we need to put snake tail image(the case as for snake head)
            elif index == len(self.body) -1:
                screen.blit(self.tail, block_rect)
            #other blocks(by setting else we had specifed all other blocks)
            else:
                #positioning of previous and the next to it block is need to properly rotate image and have proper graphics
                previous_block = self.body[index + 1] - block
                next_block = self.body[index -1] - block
                #when the snake goes vertically, it's x remains and that means x of blocks will be the same, after we understand that previos and next's block's x.positions are the same, will will load verstical body)
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    #as in the previos case, but with y position, y remains the same of teh previos and next blocks, our snake's direction - horizontal and rotation of image is needed(self.body_horizontal was specified as rotate picture, for the block_rect we give teh image)
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    #we substitured from self.body block(current block position) and got values -1, 0 ,1 . With that setting conditions are much simpler and by manipulating
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

#as in the case with body turn graphics, we need to specify conditions for rotating our image(here refer to variable where we did this)
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down
        #funtion for moving the snake
    def move_snake(self):
        #moving snake with the archetecture of copying the next to you block and adding to your x/y posion 1. Also if statement for checking whether to add new block
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            #we need to retun false for stopping copying and placing new blocks till the snake eats apple(specified funtion when new_block becomes True)
            self.body = body_copy[:]
            self.new_block = False
            #moving snake with the archetecture of copying the next to you block and adding to your x/y posion 1.(we need to consider also the actuarl direction of our snake,specifically for head as it doesnt have the next to it property but can get a command. When the head direction changes , the direction of other will be also changed as it is like domino)
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    def add_block(self):
        self.new_block = True

    def play_following_sound(self):
        self.following_sound.play()

    def play_crunch_sound(self):
        self.crunch_sound.play()
        #class for fruit property
    def addition_to_loose(self):
        self.game_over_text = game_font.render("Game over", True, (170, 74, 68))
        self.score_text = game_font.render("This application will be closed automatically", True, (255, 255, 255))
        self.menu = game_font.render("For you, there other levels of game!", True, (200,200,200))
        screen.blit(LOOSE_SCREEN, (0, 0))
        screen.blit(self.game_over_text, (400 - (self.game_over_text.get_width()/2), (400 + self.menu.get_height()/2)))
        screen.blit(self.score_text, (400 - (self.score_text.get_width()/2), 400 + self.score_text.get_height()* 1.5))
        screen.blit(self.menu, (400 - (self.menu.get_width()/2), 400 + self.menu.get_height()* 2.5))
        pygame.display.update()
        
        time.sleep(5)
        pygame.quit()
        sys.exit()
    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.addition_to_loose()
    def addition_to_youwin(self):
        self.game_over_text = game_font.render("You completed the level. Congratulations", True, (127, 255, 212))
        self.score_text = game_font.render("Do you want to continue?", True, (255, 255, 255))
        self.menu = game_font.render("Press m for going to menu, Press r to try again", True, (200,200,200))

        screen.blit(LOOSE_SCREEN, (0, 0))
        screen.blit(self.game_over_text, (400 - (self.game_over_text.get_width()/2), (300 + self.menu.get_height()/2)))
        screen.blit(self.score_text, (400 - (self.score_text.get_width()/2), 300 + self.score_text.get_height()* 1.5))
        screen.blit(self.menu, (400 - (self.menu.get_width()/2), 300 + self.menu.get_height()* 2.5))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()
    def you_win(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.addition_to_youwin()
class BOMB:
    def __init__(self):
        self.randomize()
    def draw_bomb(self):
        bomb_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(bomb, bomb_rect)
    def randomize(self):
        self.x = random.randint(0, cell_number -1)
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x, self.y)
class FRUIT:
    def __init__(self):
        self.randomize()
        #create an x and y position
        #draw a squire
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        #creating our random x and y position and making them as the vector
    def randomize(self):
        self.x = random.randint(0, cell_number -1)
        self.y = random.randint(0, cell_number -1)
        self.pos = Vector2(self.x, self.y)
        #class where the functionas from other classes will be called. With that we do not repeat ourselves and follow DRY rule
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.obstacle = OBSTACLE()
        self.bomb = BOMB()
        #neccessary event that should be check every time
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.apple_near()
        self.check_explode()
        #drawing all our elemnts by calling the needed function where the style and rect(physical body) was given
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.obstacle.draw_obtacle()
        self.bomb.draw_bomb()
        #condition for sound effect
    def apple_near(self):
        if self.fruit.pos + pygame.math.Vector2(1) == self.snake.body[0] or self.fruit.pos + pygame.math.Vector2(-1) == self.snake.body[0]:
            self.snake.play_following_sound()
            #instruction for what to do if the snake eats an apple(loop of fruit functions)
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            #repostion the fruit
            #add another block to the snake
            self.bomb.randomize()
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            #apple can appear in the postion of block that gives bug, by rerandomizing the problems is fixed
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
        for unit in self.obstacle.body[0:]:
            if unit == self.fruit.pos:
                self.fruit.randomize()
    def check_explode(self):
        if self.bomb.pos == self.snake.body[0]:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.bomb.pos:
                self.fruit.randomize()
        for unit in self.obstacle.body[0:]:
            if unit == self.bomb.pos:
                self.bomb.randomize()
        if self.bomb.pos == self.fruit.pos:
            self.bomb.randomize()
    def check_fail(self):
        #check if snake is outside of the screen
        if self.snake.body[0].x <0:
            self.snake.body[0].x = cell_number -1
        if self.snake.body[0].x > cell_number:
            self.snake.body[0].x =1
        if self.snake.body[0].y < 0:
            self.snake.body[0].y= cell_number-1
        if self.snake.body[0].y > cell_number:
            self.snake.body[0].y =1
        #gamer over stay for self hit
        for block in self.snake.body[1: ]:
            if  block == self.snake.body[0]:
                self.game_over()
        for each in self.obstacle.body[0:]:
            if each == self.snake.body[0]:
                self.game_over()
        if int(len(self.snake.body) - 3) >= 10:
            self.you_win_local()
    def game_over(self):
        self.snake.reset()
    def you_win_local(self):
        self.snake.you_win()
    def draw_grass(self):
        grass_color = (167, 209,61)
        #for drawing grass, we need to two-colorign effect(bright green and dark green, for that every second frame)
        for row in range(cell_number):
            if row % 2 == 0:  
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    #drawing the score
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74,12))
        score_x = int(cell_size * cell_number -60)
        score_y = int(cell_size * cell_number -40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,apple_rect.width + score_rect.width + 10, apple_rect.height)
        
        pygame.draw.rect(screen,(167,209, 61),bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen,(56, 74, 12), bg_rect, 2)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74,12))
        score_x = int(cell_size * cell_number -60)
        score_y = int(cell_size * cell_number -40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,apple_rect.width + score_rect.width + 10, apple_rect.height)
        
        pygame.draw.rect(screen,(167,209, 61),bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen,(56, 74, 12), bg_rect, 2)
        #pre_init tool is needed, because the sound starts after the event happes, not in parallel. Setting the give frequency gives us affect of eating immediately when the snake's position is equal to apples
pygame.mixer.pre_init(44100, -16, 2, 512)

cell_size = 40
cell_number = 20
#Our screen 800 by 800 pixels that are divided to 20 squire blocks
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('images/apple.png').convert_alpha()
game_font = pygame.font.Font("fonts/Yeseva_One/YesevaOne-Regular.ttf", 25)
main_game = MAIN()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)
LOOSE_SCREEN = pygame.transform.scale(pygame.image.load('images/you_win.jpg'), (800,800))
score = SNAKE.scrore
Obstacle_image = pygame.transform.scale(pygame.image.load('images/obstacle.png'), (40, 40))
bomb = pygame.transform.scale(pygame.image.load('images/bomb.png'), (40, 40))
counter = 0
while True:
    for event in pygame.event.get():
       if  event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
       n = 90
       if int(score - 3) % 5 == 0:
        pygame.time.set_timer(SCREEN_UPDATE, n)
        n -=30
        #keydown event of the package gives us to handle direction when the user presses specific keys
       if event.type == SCREEN_UPDATE:
        main_game.update()
       if event.type ==  pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            if main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0,-1)
        if event.key == pygame.K_RIGHT:
             if main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1,0)
        if event.key == pygame.K_DOWN:
             if main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0,1)
        if event.key == pygame.K_LEFT:
             if main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1,0)
        
    #draw all out elements
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(90)