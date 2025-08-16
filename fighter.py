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
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x,y, 80, 180))
        self.vel_y = 0 #y velocity
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

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
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed() #Get key presses
        #Will attack when the following is not performed
        if self.attacking == False:
            #Movement
            if key[pygame.K_a]:
                dx = -SPEED
                self.running = True
            if key[pygame.K_d]:
                dx = SPEED
                self.running = True

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
        
        #Apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #Update player position
        self.rect.x += dx
        self.rect.y += dy

    #Define animation updates
    def update(self):
        #Check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) #death
        elif self.hit == True:
            self.update_action(5) #hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) #punch
            elif self.attack_type == 2:
                self.update_action(4) #throwing
        elif self.jump == True:
            self.update_action(2) #jumping
        elif self.running == True:
            self.update_action(1) #running
        else:
            self.update_action(0) #idle

        animation_cooldown = 50 #miliseconds
        self.image = self.animation_list[self.action][self.frame_index]
        #Check if enough time has passes since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #Check if the animtion if finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #Check if the player is dead, then stop the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0
                #Checks if an attack has been executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 30
                #Check if damage was taken
                if self.action == 5:
                    self.hit = False
                    #If the player was in a middle in an attack, then the action is stopped
                    self.attacking = False
                    self.attack_cooldown = 30


    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
                print("Attacking")
            pygame.draw.rect(surface, (0,255,255), attacking_rect)


    def update_action(self, new_action):
        #Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255,0,0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))



