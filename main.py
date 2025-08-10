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

#Load background image
bg_image = pygame.image.load("assets/images/background/konoha.png").convert_alpha()

#Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#Create two instances of fighters
fighter_1 = Fighter(300,620)
fighter_2 = Fighter(1100, 620)



#Game loop
run = True
while run:
    clock.tick(FPS)

    #Draw background
    draw_bg()

    #Move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT)
    #fighter_2.move()

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