import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
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

#Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0] #Player scores: [player1, player2
round_over = False
ROUND_OVER_COOLDOWN = 2000 #2 seconds

#Define fighter varibles
NARUTO_SIZE = 162
NARUTO_SCALE = 3
NARUTO_OFFSET = [70, 39]
NARUTO_DATA = [NARUTO_SIZE, NARUTO_SCALE, NARUTO_OFFSET]
SASUKE_SIZE = 162
SASUKE_SCALE = 3
SASUKE_OFFSET = [70, 39]
SASUKE_DATA = [SASUKE_SIZE, SASUKE_SCALE, SASUKE_OFFSET]

#Load music/sounds
pygame.mixer.music.load("assets/audio/silhouette.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
punch_fx = pygame.mixer.Sound("assets/audio/punch.wav")
punch_fx.set_volume(0.5)

#Load background image
bg_image = pygame.image.load("assets/images/background/konoha.png").convert_alpha()
#Load spritesheets
naruto_sheet = pygame.image.load("assets/images/naruto/naruto.png").convert_alpha()
sasuke_sheet = pygame.image.load("assets/images/sasuke/sasuke.png").convert_alpha()
#Define number of steps in each animation
NARUTO_ANIMATED_STEPS = [4,6,4,3,3,3,14]
SASUKE_ANIMATED_STEPS = [4,6,4,3,3,2,12]
#Define fonts
count_font = pygame.font.Font("assets/fonts/pixelifySans.ttf", 80)
score_font = pygame.font.Font("assets/fonts/pixelifySans.ttf", 30)

#Function for drawing text
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x,y))

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
fighter_1 = Fighter(1, 300, 620, False, NARUTO_DATA, naruto_sheet, NARUTO_ANIMATED_STEPS, punch_fx)
fighter_2 = Fighter(2, 1100, 620, True, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATED_STEPS, punch_fx)

#Game loop
run = True
while run:
    clock.tick(FPS)

    #Draw background
    draw_bg()
    #Show player's stats
    draw_health_bar(fighter_1.health, 100 , 50)
    draw_health_bar(fighter_2.health, 900 , 50)
    draw_text("Player 1: "+ str(score[0]), score_font, RED, 100, 100)
    draw_text("Player 2: "+ str(score[1]), score_font, RED, 900, 100)

    #Update count down
    if intro_count <= 0:
        #Move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        #Display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        #Update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    #Update fighters
    fighter_1.update()
    fighter_2.update()

    #Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #Check for player defeat
    if round_over == False:
        if fighter_1.alive == False: #If player 1 dies
            score[1] += 1 #Player 2 points increase
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False: #If player 2 dies
            score[0] += 1 #Player 1 points increase
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 300, 620, False, NARUTO_DATA, naruto_sheet, NARUTO_ANIMATED_STEPS, punch_fx)
            fighter_2 = Fighter(2, 1100, 620, True, SASUKE_DATA, sasuke_sheet, SASUKE_ANIMATED_STEPS, punch_fx)

    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Update display
    pygame.display.update()


#Exit pygame
pygame.quit()