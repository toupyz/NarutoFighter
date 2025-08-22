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
round_time = 30000 #3 mins
round_time_left = round_time
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0,0] #Player scores: [player1, player2]
round_over = False
ROUND_OVER_COOLDOWN = 2000 #Time after death, 2 seconds
winner_text = ""

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
    draw_text(str(health) + "/" + str(max_health), score_font, BLACK, x, y)


#Create two instances of fighters
fighter_1 = Fighter("naruto", 1, 300, 620, False, punch_fx, kunai_fx)
fighter_2 = Fighter("sasuke", 2, 1100, 620, True, punch_fx, kunai_fx)

#Game loop
run = True
while run:
    #clock.tick(FPS)
    dt = clock.tick(FPS)  # milliseconds since last frame

    #Draw background
    draw_bg()
    #Show player's stats
    draw_health_bar(fighter_1.health, fighter_1.data["health"], 100, 50)
    draw_health_bar(fighter_2.health, fighter_2.data["health"], 900, 50)
    draw_text("Player 1: "+ str(score[0]), score_font, RED, 100, 100)
    draw_text("Player 2: "+ str(score[1]), score_font, RED, 900, 100)

    # Countdown intro
    if intro_count <= 0 and not round_over:
        #Move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        if intro_count > 0:  # show countdown before match
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

    # Update round timer only if round not finished
    if not round_over and intro_count <= 0:
        round_time_left -= dt
        if round_time_left <= 0:
            round_over = True
            round_time_left = 0
            if score[0] > score[1]:
                winner_text = "Player 1 Wins!"
            elif score[1] > score[0]:
                winner_text = "Player 2 Wins!"
            else:
                winner_text = "Draw!"

    # Draw round timer
    seconds_left = round_time_left // 1000
    minutes = seconds_left // 60
    seconds = seconds_left % 60
    draw_text(f"{minutes:01}:{seconds:02}", score_font, RED, SCREEN_WIDTH // 2 - 40, 50)

    #Update fighters
    fighter_1.update()
    fighter_2.update()
    fighter_1.update_projectiles(screen, fighter_2)
    fighter_2.update_projectiles(screen, fighter_1)

    #Draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #Check for player defeat
    if not round_over:
        if not fighter_1.alive: #If player 1 dies
            score[1] += 1
            fighter_2.is_winner = True
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif not fighter_2.alive: #If player 2 dies
            score[0] += 1
            fighter_1.is_winner = True
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # Respawn only if the round_time isn't over
        if round_time_left > 0 and pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter("naruto", 1, 300, 620, False, punch_fx, kunai_fx)
            fighter_2 = Fighter("sasuke", 2, 1100, 620, True, punch_fx, kunai_fx)

    # Show winner if round timer ended
    if round_time_left <= 0:
        draw_text(winner_text, count_font, RED, SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2)

    #Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Update display
        pygame.display.update()

#Exit pygame
pygame.quit()