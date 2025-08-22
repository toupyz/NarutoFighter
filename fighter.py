import pygame
import json

kunai_img = pygame.image.load("assets/images/kunai.png")
kunai_img = pygame.transform.scale(kunai_img, (50, 20))  # resize to fit your game

with open("characters.json", "r") as file:
    character_data = json.load(file)

class Fighter():
    def __init__(self, char_id, player, x, y, flip, punch_sound, kunai_sound):
        self.char_id = char_id
        self.data = character_data[char_id]

        self.alive = True
        self.action = 0  # 0=idle, 1=run, 2=jump, 3=phyical(punch,kick), 4=throwing, 5=hit, 6=death, 7=winning
        self.attack_cooldown = 0
        self.attacking = False
        self.attack_type = 0
        self.flip = flip
        self.frame_index = 0
        self.health = self.data["health"]
        self.hit = False
        self.size = self.data["size"]
        self.image_scale = self.data["scale"]
        self.offset = self.data["offset"]
        sprite_sheet = pygame.image.load(self.data["sprite_sheet"]).convert_alpha()
        self.animation_list = self.load_images(sprite_sheet, self.data["animation_steps"])
        self.image = self.animation_list[self.action][self.frame_index]
        self.jump = False
        self.kunai_sound = kunai_sound
        self.player = player 
        self.projectiles = []
        self.punch_sound = punch_sound
        self.punch_damage = self.data["punch_damage"]
        self.throw_damage = self.data["throw_damage"]
        self.rect = pygame.Rect((x, y, 80, 180))
        self.running = False
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0  # y velocity


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

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0 #Change in x coordinate
        dy = 0 #Change in y coordinate
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed() #Get key presses
        #Will attack when the following is not performed
        if self.attacking == False and self.alive == True and round_over == False:
            #Checks player 1 controls
            if self.player == 1: #Player 1 
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
                if key[pygame.K_e] or key[pygame.K_f]:
                    #Determine what attack is used
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_f]:
                        self.attack_type = 2
                    self.attack(surface, target, kunai_img)

            if self.player == 2: #Player 2
                #Movement
                if key[pygame.K_j]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_l]:
                    dx = SPEED
                    self.running = True
                #Jumping
                if key[pygame.K_i] and self.jump == False:
                    self.vel_y = -30 #Negative in y will go up
                    self.jump = True
                #Attack
                if key[pygame.K_u] or key[pygame.K_h]:
                    self.attack(surface, target)
                    #Determine what attack is used
                    if key[pygame.K_u]:
                        self.attack_type = 1
                    if key[pygame.K_h]:
                        self.attack_type = 2
                    self.attack(surface, target, kunai_img)

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
            self.update_action(6)  # death
        elif self.hit:
            self.update_action(5)  # hit
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)  # punch
            elif self.attack_type == 2:
                self.update_action(4)  # throw
        elif self.jump:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else:
            # default to idle unless round_over happened
            if getattr(self, "is_winner", False):
                self.update_action(7)  # win pose
            else:
                self.update_action(0)  # idle


        animation_cooldown = 110 #miliseconds
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
                    self.attack_cooldown = 25
                #Check if damage was taken
                if self.action == 5:
                    self.hit = False
                    #If the player was in a middle in an attack, then the action is stopped
                    self.attacking = False
                    self.attack_cooldown = 25


    def attack(self, surface, target, kunai_img=None):
        if self.attack_cooldown == 0:
            self.attacking = True

            if self.attack_type == 1:  # Punch
                self.punch_sound.play()
                attack_width = self.rect.width // 2
                attack_height = self.rect.height
                if self.flip:  # Facing left
                    attack_x = self.rect.left - attack_width
                else:          # Facing right
                    attack_x = self.rect.right
                attack_y = self.rect.y
                attacking_rect = pygame.Rect(attack_x, attack_y, attack_width, attack_height)
                if attacking_rect.colliderect(target.rect):
                    target.health -= self.punch_damage
                    target.hit = True

            elif self.attack_type == 2 and kunai_img:
                self.kunai_sound.play()
                direction = -1 if self.flip else 1
                start_x = self.rect.centerx + (30 * direction)
                start_y = self.rect.centery
                kunai = Projectile(start_x, start_y, direction, kunai_img, self.throw_damage)
                self.projectiles.append(kunai)


            #pygame.draw.rect(surface, (0, 255, 255), attacking_rect) #Attack hitbox
        
    def update_projectiles(self, screen, target):
        for kunai in self.projectiles:
            kunai.update(screen, target)
        # Keep only alive kunai
        self.projectiles = [k for k in self.projectiles if k.alive]



    def update_action(self, new_action):
        #Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, (255,0,0), self.rect) #Red rectangle/hit box
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))



class Projectile():
    def __init__(self, x, y, direction, image, throw_damage):
        self.image_original = image
        # Flip image if direction is left
        if direction == -1:
            self.image = pygame.transform.flip(image, True, False)
        else:
            self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        # Physics
        self.vel_x = 12 * direction
        self.vel_y = -10   # initial upward arc -10
        self.gravity = 0.5
        self.alive = True
        self.throw_damage = throw_damage

    def update(self, screen, target):
        # Apply physics
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += self.gravity
        # Draw
        screen.blit(self.image, self.rect)
        # Check hit
        if self.rect.colliderect(target.rect):
            target.health -= self.throw_damage #Damage
            target.hit = True
            self.alive = False
        # Remove if off-screen
        if (self.rect.top > screen.get_height() or 
            self.rect.right < 0 or 
            self.rect.left > screen.get_width()):
            self.alive = False
