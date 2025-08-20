import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#Create game window
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Ninja Clash") #Screen title

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

#Load music/sounds
pygame.mixer.music.load("assets/audio/silhouette.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0, 5000)
punch_fx = pygame.mixer.Sound("assets/audio/punch.wav")
punch_fx.set_volume(0.2)
kunai_fx = pygame.mixer.Sound("assets/audio/kunai.wav")
kunai_fx.set_volume(0.2)

#Load background image
bg_image = pygame.image.load("assets/images/background/konoha.png").convert_alpha()

#Define fonts
count_font = pygame.font.Font("assets/fonts/squbitzplus.ttf", 100)
score_font = pygame.font.Font("assets/fonts/squbitzplus.ttf", 40)

#Function for drawing text
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x,y))

#Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#Funcions for drawing fighter's health bar
def draw_health_bar(health, max_health, x, y):
    ratio = health / max_health
    pygame.draw.rect(screen, BLACK, (x-2, y-2, 404, 34))  # outline
    pygame.draw.rect(screen, WHITE, (x, y, 400, 30))      # background
    pygame.draw.rect(screen, RED, (x, y, 400 * ratio, 30)) # fill


#Create two instances of fighters
fighter_1 = Fighter("naruto", 1, 300, 620, False, punch_fx, kunai_fx)
fighter_2 = Fighter("sasuke", 2, 1100, 620, True, punch_fx, kunai_fx)

#Game loop
run = True
while run:
    clock.tick(FPS)

    #Draw background
    draw_bg()
    #Show player's stats
    draw_health_bar(fighter_1.health, fighter_1.data["health"], 100, 50)
    draw_health_bar(fighter_2.health, fighter_2.data["health"], 900, 50)
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
    fighter_1.update_projectiles(screen, fighter_2)
    fighter_2.update_projectiles(screen, fighter_1)

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
            fighter_1 = Fighter("naruto", 1, 300, 620, False, punch_fx, kunai_fx)
            fighter_2 = Fighter("sasuke", 2, 1100, 620, True, punch_fx, kunai_fx)

    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Update display
    pygame.display.update()


#Exit pygame
pygame.quit()