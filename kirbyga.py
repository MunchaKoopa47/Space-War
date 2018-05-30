# Imports
import pygame
import random

# Initialize game engine
pygame.init()

# Window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
x, y = screen.get_size()
WIDTH = x
HEIGHT = y
TITLE = "Chef Kawasaki destroys Evil Kirby"
pygame.display.set_caption(TITLE)

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/SPACEBOY.ttf", 96)

# Images
background = pygame.image.load('assets/images/background.jpg')
background = pygame.transform.scale(background,(WIDTH, HEIGHT))
ship_img = pygame.image.load('assets/images/player.png')
laser_img = pygame.image.load('assets/images/laser.png')
mob_img = pygame.image.load('assets/images/alien1.png')
bomb_img = pygame.image.load('assets/images/bomb.png')
sprite_0 = pygame.image.load('assets/images/bomb.png')

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
INTRO = pygame.mixer.Sound("assets/sounds/intro.ogg")
SONG = pygame.mixer.Sound("assets/sounds/playing.ogg")
CREDITS = pygame.mixer.Sound("assets/sounds/credits.ogg")

# Stages
START = 0
PLAYING = 1
END = 2

# Game classes
#class Background(pygame.sprite.Sprite):
    #def __init__(self, x, y, image, image2, image3, image4):
        #super().__init__()
        #self.ticks = 0
        #self.image = image
        #self.image2 = image2
        #self.image3 = image3
        #self.image4 = image4
        #self.image5 = image5
        #self.rect = self.image.get_rect()
        #self.rect.x = x
        #self.rect.y = y
        

    #def update(self):
        #self.ticks += 1
        #if self.ticks %98 == 0:
            #self.image, self.image2, self.image3, self.image4, self.image5 = self.image2, self.image3, self.image4, self.image5, self.image

class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.shield = 1

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield = 0

        if self.shield == 0:
            #EXPLOSION.play()
            self.kill()
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            #EXPLOSION.play()
            player.score += 1
            self.kill()


class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 1
        self.bomb_rate = 60

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
            bomber.drop_bomb()

    
# Make game objects


# Game helper functions
def show_title_screen():
    title_text = FONT_XL.render("War on Kirb", 1, WHITE)
    screen.blit(title_text, [100, 204])

def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])

def show_credits():
    credit_text = FONT_XL.render("Game Over", 1, WHITE)
    screen.blit(credit_text, [100, 204])

def setup():
    global ship, player, lasers, mobs, bombs, fleet, stage
    
    #Make game objects
    ship = Ship(384, 536, ship_img)
    mob1 = Mob(100, 64, mob_img)
    mob2 = Mob(200, 64, mob_img)
    mob3 = Mob(300, 64, mob_img)
    mob4 = Mob(400, 64, mob_img)
    mob5 = Mob(500, 64, mob_img)
    mob6 = Mob(600, 64, mob_img)
    mob7 = Mob(700, 64, mob_img)
    mob8 = Mob(800, 64, mob_img)
    mob9 = Mob(900, 64, mob_img)
    mob10 = Mob(1000, 64, mob_img)
    mob11 = Mob(1100, 64, mob_img)
    mob12 = Mob(100, 128, mob_img)
    mob13 = Mob(200, 128, mob_img)
    mob14 = Mob(300, 128, mob_img)
    mob15 = Mob(400, 128, mob_img)
    mob16 = Mob(500, 128, mob_img)
    mob17 = Mob(600, 128, mob_img)
    mob18 = Mob(700, 128, mob_img)
    mob19 = Mob(800, 128, mob_img)
    mob20 = Mob(900, 128, mob_img)
    mob21 = Mob(1000, 128, mob_img)
    mob22 = Mob(1100, 128, mob_img)
    mob23 = Mob(100, 192, mob_img)
    mob24 = Mob(200, 192, mob_img)
    mob25 = Mob(300, 192, mob_img)
    mob26 = Mob(400, 192, mob_img)
    mob27 = Mob(500, 192, mob_img)
    mob28 = Mob(600, 192, mob_img)
    mob29 = Mob(700, 192, mob_img)
    mob30 = Mob(800, 192, mob_img)
    mob31 = Mob(900, 192, mob_img)
    mob32 = Mob(1000, 192, mob_img)
    mob33 = Mob(1100, 192, mob_img)

    #intro = Background(0, 0, sprite_0, sprite_1, sprite_2, sprite_3, sprite_4, sprite_5)

    # Make sprite groups
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10, mob11
            , mob12, mob13, mob14, mob15, mob16, mob17, mob18, mob19, mob20, mob21
            , mob22, mob23, mob24, mob25, mob26, mob27, mob28, mob29, mob30, mob31
            , mob32, mob33)

    bombs = pygame.sprite.Group()

    fleet = Fleet(mobs)

    # set stage
    stage = START

def level_up():
    mob1 = Mob(100, 64, mob_img)
    mob2 = Mob(200, 64, mob_img)
    mob3 = Mob(300, 64, mob_img)
    mob4 = Mob(400, 64, mob_img)
    mob5 = Mob(500, 64, mob_img)
    mob6 = Mob(600, 64, mob_img)
    mob7 = Mob(700, 64, mob_img)
    mob8 = Mob(800, 64, mob_img)
    mob9 = Mob(900, 64, mob_img)
    mob10 = Mob(1000, 64, mob_img)
    mob11 = Mob(1100, 64, mob_img)
    mob12 = Mob(100, 128, mob_img)
    mob13 = Mob(200, 128, mob_img)
    mob14 = Mob(300, 128, mob_img)
    mob15 = Mob(400, 128, mob_img)
    mob16 = Mob(500, 128, mob_img)
    mob17 = Mob(600, 128, mob_img)
    mob18 = Mob(700, 128, mob_img)
    mob19 = Mob(800, 128, mob_img)
    mob20 = Mob(900, 128, mob_img)
    mob21 = Mob(1000, 128, mob_img)
    mob22 = Mob(1100, 128, mob_img)
    mob23 = Mob(100, 192, mob_img)
    mob24 = Mob(200, 192, mob_img)
    mob25 = Mob(300, 192, mob_img)
    mob26 = Mob(400, 192, mob_img)
    mob27 = Mob(500, 192, mob_img)
    mob28 = Mob(600, 192, mob_img)
    mob29 = Mob(700, 192, mob_img)
    mob30 = Mob(800, 192, mob_img)
    mob31 = Mob(900, 192, mob_img)
    mob32 = Mob(1000, 192, mob_img)
    mob33 = Mob(1100, 192, mob_img)

    lasers = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10, mob11
            , mob12, mob13, mob14, mob15, mob16, mob17, mob18, mob19, mob20, mob21
            , mob22, mob23, mob24, mob25, mob26, mob27, mob28, mob29, mob30, mob31
            , mob32, mob33)

    bombs = pygame.sprite.Group()


    fleet = Fleet(mobs)

    # set stage
    stage = PLAYING

# Game loop
setup()
level_up()

done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.type == pygame.KEYDOWN:
                if stage == START:
                    if event.key == pygame.K_SPACE:
                        stage = PLAYING
                elif stage == PLAYING:
                    if event.key == pygame.K_SPACE:
                        ship.shoot()
                elif stage == END:
                    if event.key == pygame.K_r:
                        setup()

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()

        elif len(player) == 0:
            stage = END
            CREDITS.play()
        elif len(mobs) == 0:
            stage = END
            CREDITS.play()

    if stage == START:
        INTRO.play()

    if stage == PLAYING:
        SONG.play()

    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()
     
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.blit(background, (0, 0))
    lasers.draw(screen)
    player.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    show_stats(player)

    if stage == START:
        show_title_screen()
    if stage == END:
        show_credits()
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
