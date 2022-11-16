#notice: if using VS code IDE, firstly open the folder inside it and run the code
import pygame
import sys
import subprocess
import os
pygame.init()
#basic variables
screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/Yeseva_One/YesevaOne-Regular.ttf', 30)
background_image = pygame.image.load("images/menu_background.png")
pygame.display.set_caption('Snake Game')
#main class for drawing all needed elements
class MAIN():
    def draw_elements(self):
        self.game_over_text = game_font.render("Welcome to the pygame", True, (255, 255, 255))
        self.score_text = game_font.render("There are 3 levels: press 1 for easy level, 2 for hard, 3 for infinite", True, (255, 255, 255))
        self.menu = game_font.render("Press q char or Q char for closing the application",  True, (255, 255, 255))

        screen.blit(self.game_over_text, (400 - (self.game_over_text.get_width()/2), (400 + self.menu.get_height()/2)))
        screen.blit(self.score_text, (500 - (self.score_text.get_width()/2), 400 + self.score_text.get_height()* 1.5))
        screen.blit(self.menu, (400 - (self.menu.get_width()/2), 400 + self.menu.get_height()* 2.5))
        pygame.display.update()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)
main_game = MAIN()
while True:
    
    for event in pygame.event.get():
       if  event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
        #keydown event of the package gives us to handle direction when the user presses specific keys
        #as buttons are not flexible and effective in pygame package, the menu can be simplified with keypress funcions
       if event.type ==  pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_1:
                #calling external script
                subprocess.call(["python", "scripts/level1.py"])
            if event.key == pygame.K_2:
                subprocess.call(["python","scripts/level2.py"])
            if event.key == pygame.K_3:
                subprocess.call(["python", "scripts/infinite_level.py"])
    screen.fill((175, 215, 70))
    screen.blit(background_image, (0, 0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(90)