import pygame
from fighter import Fighter

pygame.init()

#Create game window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Naruto Fighter") #Screen title

#Set frame rate
clock = pygame.time.Clock()
FPS = 60

#Define colours
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)

#Define fighter varibles
NARUTO_SIZE = 160
NARUTO_SCALE = 3
NARUTO_OFFSET = [70, 39]
NARUTO_DATA = [NARUTO_SIZE, NARUTO_SCALE, NARUTO_OFFSET]
SASUKE_SIZE = 50
SASUKE_SCALE = 3
SASUKE_OFFSET = [20, 0]
SASUKE_DATA = [SASUKE_SIZE, SASUKE_SCALE, SASUKE_OFFSET]

#Load background image
bg_image = pygame.image.load("assets/images/background/konoha.png").convert_alpha()

#Load spritesheets
naruto_sheet = pygame.image.load("assets/images/naruto/naruto.png").convert_alpha()
sasuke_sheet = pygame.image.load("assets/images/sasuke/sasuke.png").convert_alpha()

#Define number of steps in each animation
NARUTO_ANIMATED_STEPS = [4,6,4,5,3,3,14]
SASUKE_ANIMATED_STEPS = [4,6,6,10,5,3,3,14]

#Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#Funcions for drawing fighter's health bar
def draw_health_bar(health, x ,y):
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x-2, y-2, 404, 34)) #rectangle outline
    pygame.draw.rect(screen, WHITE, (x, y, 400, 30)) #rectangle bottom layer of health bar
    pygame.draw.rect(screen, RED, (x, y, 400 * ratio, 30)) #rectangle top layer of health bar

#Create two instances of fighters
fighter_1 = Fighter(300, 620, False, NARUTO_DATA, naruto_sheet, NARUTO_ANIMATED_STEPS)
fighter_2 = Fighter(1100, 620, True, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATED_STEPS)

#Game loop
run = True
while run:
    clock.tick(FPS)

    #Draw background
    draw_bg()
    #Show player's stats
    draw_health_bar(fighter_1.health, 100 , 50)
    draw_health_bar(fighter_2.health, 900 , 50)

    #Move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
    #fighter_2.move()

    #Update fighters
    fighter_1.update()
    fighter_2.update()

    #Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Update display
    pygame.display.update()


#Exit pygame
pygame.quit()