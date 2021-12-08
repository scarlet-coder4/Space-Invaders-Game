import pygame
import random
import math
from pygame import mixer

pygame.init()  #to initialize mixer for bg music

# colors
white = (255, 255, 255)
black = (0, 0, 0)
l_blue = (0, 0, 150)

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

class Game:
    def __init__(self):
        # creating game window
        self.screen = pygame.display.set_mode((800, 600))
        # title and logo
        pygame.display.set_caption("Space Invaders")
        self.icon = pygame.image.load("ufo.png")
        pygame.display.set_icon(self.icon)
        # background
        self.bg_img = pygame.image.load("background.jpg")
        # quit button
        self.close_button = pygame.image.load("close_button.png")
        # font
        self.myfont = pygame.font.SysFont('msgothic', 32)
        # score
        self.score = 0

        self.f=open("high score.txt","a+")
        self.f.seek(0)

        self.running = True
        self.playing = False

    def disp_score(self, x, y):
        self.score_value = self.myfont.render("score: {}".format(self.score), True, white)
        self.screen.blit(self.score_value, (x, y))

    def disp_highscore(self, k, x, y):
        self.highscore_value = self.myfont.render("high score: {}".format(k), True, white)
        self.screen.blit(self.highscore_value, (x, y))

    def click(self, x1, x2, y1, y2):
        self.pos = pygame.mouse.get_pos()
        if self.pos[0] >= x1 and self.pos[0] <= x2:
            if self.pos[1] >= y1 and self.pos[1] <= y2:
                return True

class Player(Game):
    def __init__(self):
        self.player_img = pygame.image.load("player.png")
        self.player_x = 390
        self.player_y = 480
        self.playerx_change = 0
        super().__init__()

    def player(self, x, y):
        self.screen.blit(self.player_img, (x, y))

    def player_move(self):
        self.player_x += self.playerx_change
        if self.player_x <= 0:
            self.player_x = 0
        elif self.player_x >= 736:
            self.player_x = 736

class Enemy(Player):
    def __init__(self):
        self.enemy_img = pygame.image.load("enemy.png")
        self.enemy_x = random.randint(0, 736)
        self.enemy_y = random.randint(50, 200)
        self.enemyx_change = 0.2
        self.enemyy_change = 30
        super().__init__()

    def enemy(self, x, y):
        self.screen.blit(self.enemy_img, (x, y))

    def enemy_move(self):
        self.enemy_x += self.enemyx_change
        if self.enemy_x >= 736:
            self.enemy_x = 736
            self.enemyx_change = -0.2
            self.enemy_y += self.enemyy_change
        elif self.enemy_x <= 0:
            self.enemy_x = 0
            self.enemyx_change = 0.2
            self.enemy_y += self.enemyy_change

class Bullet(Enemy):
    def __init__(self):
        self.bullet_img = pygame.image.load("bullet2.png")
        self.bullet_x = 0
        self.bullet_y = 480
        self.bullety_change = 0.7
        self.bullet_state = "ready"
        super().__init__()

    def fire_bullet(self):
        if self.bullet_state == "fire":
            self.screen.blit(self.bullet_img, (self.bullet_x + 16, self.bullet_y - 20))
            self.bullet_y -= self.bullety_change

        if self.bullet_y <= 0:
            self.bullet_state = "ready"
            self.bullet_y = 480

    def iscollision(self):
        self.dist_x = math.pow(self.enemy_x - self.bullet_x, 2)
        self.dist_y = math.pow(self.enemy_y - self.bullet_y, 2)
        self.distance = math.sqrt(self.dist_x + self.dist_y)
        if self.distance < 27:
            return True
        else:
            return False

class Play(Bullet):
    def __init__(self):
        super().__init__()

    def start_screen(self):
        self.start_bg = pygame.image.load("start_bg.jpg")
        self.start_button = pygame.image.load("start_button.png")

        while self.running:
            self.screen.blit(self.start_bg, (0, 0))
            self.screen.blit(self.start_button, (300, 400))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.click(300, 428, 400, 528):  # if user click on start button
                        self.running = False

            pygame.display.update()

    def game_screen(self):
        self.playing=True
        while self.playing:
            self.screen.blit(self.bg_img, (0, 0))
            self.screen.blit(self.close_button, (736, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.playerx_change = -0.5
                    if event.key == pygame.K_RIGHT:
                        self.playerx_change = 0.5
                    if event.key == pygame.K_SPACE and self.bullet_y == 480:
                        self.bullet_state = "fire"
                        self.bullet_x = self.player_x
                        self.bullet_sound = mixer.Sound("laser.wav")
                        self.bullet_sound.play()
                if event.type == pygame.KEYUP:
                    self.playerx_change = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.click(736, 800, 0, 64):    #if user click on cross button
                        self.playing = False

            self.player_move()
            self.enemy_move()
            self.fire_bullet()

            # collision
            self.collision = self.iscollision()
            if self.collision == True:
                collision_sound = mixer.Sound("explosion.wav")
                collision_sound.play()
                self.enemy_x = random.randint(0, 736)
                self.enemy_y = random.randint(50, 200)
                self.score += 100

            self.disp_score(10,10)

            # game over when enemy touches spaceship
            if (self.enemy_y >= 410):
                self.playing = False
                self.enemy_x = random.randint(0, 736)
                self.enemy_y = random.randint(50, 200)

            self.player(self.player_x, self.player_y)
            self.enemy(self.enemy_x, self.enemy_y)
            pygame.display.update()

    def end_screen(self):
        self.running = True
        self.exit_screen = pygame.image.load("end screen.jpg")
        self.play_again = pygame.image.load("replay.png")

        # highscore
        self.f.seek(0)
        h = self.f.read()

        if self.score> int(h):   #update highscore
            self.f.seek(0)
            self.f.truncate()
            self.f.seek(0)
            self.f.write(str(self.score))
            h=str(self.score)

        while self.running:
            self.screen.blit(self.exit_screen, (0, 0))
            self.disp_score(300, 500)
            self.screen.blit(self.play_again, (550, 480))
            self.disp_highscore(h,300,550)
            self.screen.blit(self.close_button, (736, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.click(736, 800, 0, 64):  # if user click on cross button
                        self.running = False
                    if self.click(550, 614, 480, 544):  # if user click on replay button
                        self.score=0
                        self.game_screen()
                        if self.score > int(h):  # update highscore in replay also
                            self.f.seek(0)
                            self.f.truncate()
                            self.f.seek(0)
                            self.f.write(str(self.score))
                            h = str(self.score)

            pygame.display.update()


# end of classes
# driver code

p=Play()
p.start_screen()
p.game_screen()
p.end_screen()