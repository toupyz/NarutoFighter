import pygame

class Fighter():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x,y, 80, 180))
        self.vel_y = 0 #y velocity
        self.jump = False


    def move(self, screen_width, screen_height):
        SPEED = 10
        GRAVITY = 2
        dx = 0 #Change in x coordinate
        dy = 0 #Change in y coordinate
        key = pygame.key.get_pressed() #Get key presses

        #Movement
        if key[pygame.K_a]:
            dx = -SPEED
        if key[pygame.K_d]:
            dx = SPEED
        #Jumping
        if key[pygame.K_w] and self.jump == False:
            self.vel_y = -30 #Negative in y will go up
            self.jump = True
        self.vel_y += GRAVITY
        dy += self.vel_y

        #Ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 100:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 100 - self.rect.bottom

        #Update player position
        self.rect.x += dx
        self.rect.y += dy



    def draw(self, surface):
        pygame.draw.rect(surface, (255,0,0), self.rect)