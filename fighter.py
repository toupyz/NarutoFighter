import pygame

class Fighter():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0=idle, 1=run, 2=jump, 3=punch, 4=throwing, 5=hit, 6=death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect((x,y, 80, 180))
        self.vel_y = 0 #y velocity
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100

    def load_images(self, sprite_sheet, animation_steps):
        #Extract images from spritesheets
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range (animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0 #Change in x coordinate
        dy = 0 #Change in y coordinate
        key = pygame.key.get_pressed() #Get key presses

        #Will attack when the following is not performed
        if self.attacking == False:
            #Movement
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED

            #Jumping
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30 #Negative in y will go up
                self.jump = True

            #Attack
            if key[pygame.K_e] or key[pygame.K_r]:
                self.attack(surface, target)
                #Determine what attack is used
                if key[pygame.K_e]:
                    self.attack_type = 1
                if key[pygame.K_r]:
                    self.attack_type = 2


        #Apply gravity
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

        #Ensures players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #Update player position
        self.rect.x += dx
        self.rect.y += dy



    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
            print("Attacking")

        pygame.draw.rect(surface, (0,255,255), attacking_rect)




    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255,0,0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))



