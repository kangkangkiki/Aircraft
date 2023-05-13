import random
import time
import pygame
from pygame import *


class HeroPlane(pygame.sprite.Sprite):
    # group to store all aircraft bullets
    bullets = pygame.sprite.Group()

    def __init__(self, screen):
        # The initialization method of this sprite must be called:
        pygame.sprite.Sprite.__init__(self)

        # Create a picture as a player's plane
        self.player = pygame.image.load("./photo/hero1.png")
        # getting a rectangle object based on the image
        self.rect = self.player.get_rect()
        self.rect.topleft = [Manager.bg_size[0]/ 2 - 134 / 2 , 580]
        # aircraft speed
        self.speed = 4
        self.screen = screen
        # list of loaded bullets
        self.bullets = pygame.sprite.Group()

    def key_control(self):
        # Listen for keyboard events
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            self.rect.top -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.rect.bottom += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.rect.left -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.rect.right += self.speed
        if key_pressed[K_SPACE]:
            # Create a new bullet
            bullet = Bullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)
            HeroPlane.bullets.add(bullet)

    def display(self):
        # 3.Paste the player picture into the window
        self.screen.blit(self.player, self.rect)
        # updating the coordinates of the bullet
        self.bullets.update()
        # adding all bullets to the screen
        self.bullets.draw(self.screen)

    def update(self):
        self.key_control()
        self.display()

    @classmethod
    def clear_bullets(cls):
        # clearing bullets
        cls.bullets.empty()


class EnemyPlane(pygame.sprite.Sprite):
    # all enemy bullets
    enemy_bullets = pygame.sprite.Group()

    def __init__(self, screen):
        # The initialization method of this sprite must be called:
        pygame.sprite.Sprite.__init__(self)
        # Create a picture as a player's plane
        self.player = pygame.image.load("./photo/enemy0.png")
        # getting a rectangle object based on the image
        self.rect = self.player.get_rect()
        x = random.randrange(1, Manager.bg_size[0], 50)
        self.rect.topleft = [x, 0]
        # aircraft speed
        self.speed = 4
        self.screen = screen
        # list of loaded bullets
        self.bullets = pygame.sprite.Group()
        # direction of enemy aircraft movement
        self.direction = 'right'

    def display(self):
        # Paste the player picture into the window
        self.screen.blit(self.player, self.rect)
        # updating the coordinates of the bullet
        self.bullets.update()
        # adding all bullets to the screen
        self.bullets.draw(self.screen)

    def update(self):
        self.auto_move()
        self.auto_fire()
        self.display()

    def auto_move(self):
        if self.direction == 'right':
            self.rect.right += self.speed
        elif self.direction == 'left':
            self.rect.right -= self.speed

        if self.rect.right > Manager.bg_size[0] - 51:
            self.direction = 'left'
        elif self.rect.right < 0 :
            self.direction = 'right'

        self.rect.bottom += self.speed

    def auto_fire(self):
        """automatic firing,creating a bullet object,and adding it to the list"""
        random_num = random.randint(1, 40)
        if random_num == 8 :
            bullet = EnemyBullet(self.screen,self.rect.left,self.rect.top)
            self.bullets.add(bullet)
            # adding bullets to the bullet group of the class property
            EnemyPlane.enemy_bullets.add(bullet)

    @classmethod
    def clear_bullets(cls):
        # clearing bullets
        cls.enemy_bullets.empty()


# bullet class
# attribute
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        # sprite class initialization
        pygame.sprite.Sprite.__init__(self)

        # creating an image
        self.image = pygame.image.load('./photo/bullet.png')

        # getting a rectangle object
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 100/2 - 22/2 , y - 22]

        # screen
        self.screen = screen
        # speed
        self.speed = 30

    def update(self):
        # modifying the bullet's coordinates
        self.rect.top -= self.speed
        # if the bullet moves above the screen , destroy the bullet
        if self.rect.top < -22:
            self.kill()


# enemy bullet class
# attribute
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        # sprite class initialization
        pygame.sprite.Sprite.__init__(self)

        # creating an image
        self.image = pygame.image.load('./photo/bullet1.png')

        # getting a rectangle object
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 50/2 - 8/2, y + 39 ]

        # screen
        self.screen = screen
        # speed
        self.speed = 6

    def update(self):
        # modifying the bullet's coordinates
        self.rect.top += self.speed
        # if the bullet moves above the screen , destroy the bullet
        if self.rect.top > Manager.bg_size[1]:
         self.kill()


class GameSound(object):
    def __init__(self):
        pygame.mixer.init() # music module initialization
        pygame.mixer.music.load('./photo/bg2.ogg')
        pygame.mixer.music.set_volume(0.5) # sound level

        self.__bomb = pygame.mixer.Sound('./photo/bomb.wav')

    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1) # begin playing music

    def playBombSound(self):
        pygame.mixer.Sound.play(self.__bomb)


class Bomb(object):
    # initializing collision
    def __init__(self,screen , type):
        self.screen = screen
        if type == "enemy":
            # loading explosion resources
            self.mImages = [pygame.image.load("./photo/enemy0_down" + str(v) + ".png") for v in range(1, 5)]
        else:
            self.mImages = [pygame.image.load("./photo/hero_blowup_n" + str(v) + ".png") for v in range(1, 5)]
        # setting the current explosion playback index
        self.mIndex = 0
        # explosing settings
        self.mPos = [0, 0]
        self.mVisible = False

    # setting the position
    def action(self,rect):
        # triggering the explosing method draw
        # explosing coordinates
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        # turning on the explosing switch
        self.mVisible = True

    # drawing the explosing
    def draw(self):
        if not self.mVisible :
            return
        self.screen.blit(self.mImages[self.mIndex],(self.mPos[0], self.mPos[1]))
        self.mIndex += 1
        if self.mIndex >= len(self.mImages):
            self.mIndex = 0
            self.mVisible = False


class GameBackground(object):
    # map initialization
    def __init__(self, screen):
        self.mImage1 = pygame.image.load("./photo/background.jpg")
        self.mImage2 = pygame.image.load("./photo/background.jpg")
        # window
        self.screen = screen
        # assist in moving the map
        self.y1 = 0
        self.y2 = -Manager.bg_size[1] # -768

    # moving the map
    def move(self):
        self.y1 += 2
        self.y2 += 2
        if self.y1 >= Manager.bg_size[1]:
            self.y1 = 0
        if self.y2 >= 0:
            self.y2 = -Manager.bg_size[1]

    # drawing the map
    def draw(self):
        self.screen.blit(self.mImage1, (0, self.y1))
        self.screen.blit(self.mImage2, (0, self.y2))


class Manager:
    bg_size = (512, 768)
    # ID of the timer for creating enemy aircraft
    create_enemy_id = 10
    # countdown ID when the game ends
    game_over_id = 11
    # if the game is over
    is_game_over = False
    # countdown time
    over_time = 2

    def __init__(self):
        pygame.init()
        # 1.Create a window
        self.screen = pygame.display.set_mode(Manager.bg_size, 0, 32)
        # 2.Create a picture as a background
        # self.background = pygame.image.load("./photo/background.jpg")
        self.map = GameBackground(self.screen)

        # initializing a group to hold the player sprite
        self.players = pygame.sprite.Group()
        # initializing a group to hold the enemy sprite
        self.enemys = pygame.sprite.Group()
        # initializing an object for player explosion
        self.player_bomb = Bomb(self.screen, 'player')
        # initializing an object for enemy explosion
        self.enemy_bomb = Bomb(self.screen, 'enemy')
        # initializing an object for sound playback
        self.sound = GameSound()

    def exit(self):
        print('exit')
        pygame.quit()
        exit()

    def show_over_text(self):
        # game over, restarting the game after the countdown
        self.drawText('gameover %d'% Manager.over_time, 100, Manager.bg_size[1]/2, textHeight=50, fontColor=[255,0,0])

    def game_over_timer(self):
        self.show_over_text()
        # decrementing the countdown by 1
        Manager.over_time -= 1
        if Manager.over_time == 0 :
            # halting the timer
            pygame.time.set_timer(Manager.game_over_id, 0)
            # restarting the game after the countdown
            Manager.over_time = 3
            Manager.is_game_over = False
            self.start_game()

    def start_game(self):
        # restarting game, some class properties need to be cleared
        EnemyPlane.clear_bullets()
        HeroPlane.clear_bullets()
        manager = Manager()
        manager.main()

    def new_player(self):
        # creating an aircraft object and adding it to the player's group
        player = HeroPlane(self.screen)
        self.players.add(player)

    def new_enemy(self):
        # creating an enemy aircraft object and adding it to the player's group
        enemy = EnemyPlane(self.screen)
        self.enemys.add(enemy)

    # drawing text
    def drawText(self,text,x,y, textHeight=30, fontColor=(255,0,0), backgroundColor=None):
        # getting a font object from a text file
        font_obj = pygame.font.Font('./photo/baddf.ttf', textHeight)
        # configuring the text to be displayed
        text_obj = font_obj.render(text,True,fontColor,backgroundColor)
        # getting the rect of the object to be displayed
        text_rect = text_obj.get_rect()
        # setting the coordinates of the display object
        text_rect.topleft = (x, y)
        # drawing text to a specified area
        self.screen.blit(text_obj, text_rect)

    def main(self):
        # playing background music
        self.sound.playBackgroundMusic()
        # creating a player aircraft
        self.new_player()
        # starting the timer to creat enemy aircraft
        pygame.time.set_timer(Manager.create_enemy_id, 1000)
        while True:
            # 3.Paste the background picture into the window
            # self.screen.blit(self.background, (0, 0))
            # moving the map
            self.map.move()
            # attaching the map to the window
            self.map.draw()

            # drawing text
            self.drawText('hp: 1000', 0, 0)
            if Manager.is_game_over:
                # displaying the game over text only when the game is over
                self.show_over_text()

            # Get the event
            for event in pygame.event.get():
                # Determine the even type
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == Manager.create_enemy_id:
                    # creating an enemy aircraft
                    self.new_enemy()
                elif event.type == Manager.game_over_id:
                    # the event that is triggered by the timer
                    self.game_over_timer()

            # calling the explosion object
            self.player_bomb.draw()
            self.enemy_bomb.draw()

            # collision detection between player aircraft and enemy bullets
            if self.players.sprites():
                isover = pygame.sprite.spritecollide(self.players.sprites()[0], EnemyPlane.enemy_bullets, True)
                if isover:
                    Manager.is_game_over = True
                    pygame.time.set_timer(Manager.game_over_id, 1000)
                    print('being hit')
                    self.player_bomb.action(self.players.sprites()[0].rect)
                    # removing the player aircraft from the sprite group
                    self.players.remove(self.players.sprites()[0])
                    # explosion sound
                    self.sound.playBombSound()

            # detecting collision
            iscollide = pygame.sprite.groupcollide(self.players, self.enemys, True, True)

            if iscollide:
                Manager.is_game_over = True # indicates that the game is over
                pygame.time.set_timer(Manager.game_over_id, 1000) # starting the game countdown

                items = list(iscollide.items())[0]
                print(items)
                x = items[0]
                y = items[1][0]
                # player aircraft explosion image
                self.player_bomb.action(x.rect)
                # enemy aircraft explosion image
                self.enemy_bomb.action(y.rect)
                # explosion sound
                self.sound.playBombSound()

            # collision detection between player bullets and all enemy aircraft
            is_enemy = pygame.sprite.groupcollide(HeroPlane.bullets,self.enemys,True,True)
            if is_enemy:
                items = list(is_enemy.items())[0]
                y = items[1][0]
                # enemy aircraft explosion image
                self.enemy_bomb.action(y.rect)
                # explosion sound
                self.sound.playBombSound()

            # display of the player aircraft and bullets
            self.players.update()
            # display of the enemy aircraft and bullets
            self.enemys.update()

            # refreshing the window content
            pygame.display.update()
            time.delay(15)


if __name__ == '__main__':
    manager = Manager()
    manager.main()





