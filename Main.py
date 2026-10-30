import pygame
from sys import exit
from random import *
from time import time

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((600, 700))
bg_color = (20, 30, 60)
pygame.display.set_caption('Galaxy Shooter 2')
icon = pygame.transform.scale(pygame.image.load('UFO-GREEN.png'), (70, 70))
pygame.display.set_icon(icon)

show_hitbox = 0

# Игрок:
class Player(pygame.sprite.Sprite):
    def __init__(self, img, img_x, img_y, speed, hp, sprite_x, sprite_y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.transform.scale(pygame.image.load(img), (85, 85))
        self.speed = speed
        self.img_rect = self.img.get_rect()
        self.img_rect.x = img_x
        self.img_rect.y = img_y
        self.sprite_rect = pygame.Rect(0, 0, sprite_x, sprite_y)
        self.sprite_rect.center = self.img_rect.center
        self.health = hp
        self.explosion = pygame.transform.scale(pygame.image.load('Blow_up.png'), (85, 85))
        self.explosion_rect = self.explosion.get_rect()
        self.explosion_rect.center = self.img_rect.center
    def draw(self):
        window.blit(self.img, (self.img_rect.x, self.img_rect.y))
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.sprite_rect, 3)
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.img_rect, 3)
    def blow_up(self):
        window.blit(self.explosion, (self.explosion_rect.x, self.explosion_rect.y))

PLAYER = Player('Spaceship-RED.png', 257.5, 500, 10, 3, 55, 55)
mousemotion = False

# Пули:
class Bullet(pygame.sprite.Sprite):
    def __init__(self, img, img_x, img_y, speed, sprite_x, sprite_y, health):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.transform.scale(pygame.image.load(img), (85, 85))
        self.speed = speed
        self.img_rect = self.img.get_rect()
        self.img_rect.x = img_x
        self.img_rect.y = img_y
        self.sprite_rect = pygame.Rect(0, 0, sprite_x, sprite_y)
        self.sprite_rect.center = self.img_rect.center
        self.bullet_power = 1
        self.hp = health
    def draw(self):
        window.blit(self.img, (self.img_rect.x, self.img_rect.y))
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.sprite_rect, 3)
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.img_rect, 3)
    def shoot(self):
        self.img_rect.y -= self.speed
        self.sprite_rect.center = self.img_rect.center

BULLETS = pygame.sprite.Group()
amount_bullets = 1
shoot = True

# НЛО:
class UFO(pygame.sprite.Sprite):
    def __init__(self, img, img_x, img_y, speed1, speed2, sprite_x, sprite_y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.transform.scale(pygame.image.load(img), (85, 85))
        self.speed1 = speed1
        self.speed2 = speed2
        self.img_rect = self.img.get_rect()
        self.img_rect.x = img_x
        self.img_rect.y = img_y
        self.sprite_rect = pygame.Rect(0, 0, sprite_x, sprite_y)
        self.sprite_rect.center = self.img_rect.center
        self.health = hp
        self.bullet_img = pygame.transform.scale(pygame.image.load('Bullet-RED.png'), (85, 85))
        self.bullet_img_rect = self.bullet_img.get_rect()
        self.bullet_sprite_rect = pygame.Rect(0, 0, 20, 50)
        self.bullet_img_rect.center = self.img_rect.center
        self.bullet_sprite_rect.center = self.bullet_img_rect.center
        self.bullet_speed = 6
        self.bullet_power = 1
        self.explosion = pygame.transform.scale(pygame.image.load('Blow_up.png'), (85, 85))
        self.explosion_rect = self.explosion.get_rect()
        self.explosion_rect.center = self.img_rect.center
        self.explosion_time = pygame.Rect(0, 0, 10, 10)
        self.random_angle = [0, 90, 180, 270, 360]
        self.angle = choice(self.random_angle)
        self.image_to_know = img
    def draw(self):
        if self.image_to_know == 'UFO-BLUE.png' and self.health <= 3:
            self.img = pygame.transform.scale(pygame.image.load('UFO-GREEN.png'), (85, 85))
        window.blit(self.img, (self.img_rect.x, self.img_rect.y))
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.sprite_rect, 3)
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.img_rect, 3)
    def draw_bullet(self):
        if self.bullet_img_rect.y > self.img_rect.y + 20:
            window.blit(self.bullet_img, (self.bullet_img_rect.x, self.bullet_img_rect.y))
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.bullet_sprite_rect, 3)
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.bullet_img_rect, 3)
    def shoot(self):
        self.bullet_img_rect.y += self.bullet_speed
        self.bullet_sprite_rect.center = self.bullet_img_rect.center
    def bullet_return(self):
        self.bullet_img_rect.center = self.img_rect.center
        self.bullet_sprite_rect.center = self.bullet_img_rect.center
    def new_icon(self):
        random_icon = randint(1, 3)
        if random_icon == 2:
            self.img = pygame.transform.scale(pygame.image.load('UFO-BLUE.png'), (85, 85))
            self.bullet_img = pygame.transform.scale(pygame.image.load('Bullet-RED.png'), (85, 85))
            self.bullet_power = 1
            self.health = 5
            self.image_to_know = 'UFO-BLUE.png'
        elif random_icon == 3:
            self.img = pygame.transform.scale(pygame.image.load('UFO-ORANGE.png'), (85, 85))
            self.bullet_img = pygame.transform.scale(pygame.image.load('Bullet-BLUE.png'), (85, 85))
            self.bullet_power = 2
            self.health = 3
            self.image_to_know = 'UFO-ORANGE.png'
        else:
            self.img = pygame.transform.scale(pygame.image.load('UFO-GREEN.png'), (85, 85))
            self.bullet_img = pygame.transform.scale(pygame.image.load('Bullet-RED.png'), (85, 85))
            self.bullet_power = 1
            self.health = 3
            self.image_to_know = 'UFO-GREEN.png'
    def destroyed(self):
        self.img_rect.y -= 400
        self.sprite_rect.center = self.img_rect.center
        self.bullet_img_rect.center = self.img_rect.center
        self.bullet_sprite_rect.center = self.bullet_img_rect.center
    def blow_up(self):
        explosion = pygame.transform.rotate(self.explosion, self.angle)
        window.blit(explosion, (self.explosion_rect.x, self.explosion_rect.y))


# Звёзды(bg):
class Stars(pygame.sprite.Sprite):
    def __init__(self, img, img_x, img_y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.transform.scale(pygame.image.load(img), (800, 800))
        self.speed = speed
        self.img_rect = self.img.get_rect()
        self.img_rect.x = img_x
        self.img_rect.y = img_y
    def draw(self):
        window.blit(self.img, (self.img_rect.x, self.img_rect.y))
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.img_rect, 3)
    def return_stars(self):
        if self.img_rect.y == 720:
            self.img_rect.y = -830

Stars1 = Stars('Stars_bg.png', -30, 0, 1)
Stars2 = Stars('Stars_bg.png', -30, -830, 1)

# Предметы:
class Items(pygame.sprite.Sprite):
    def __init__(self, img, img_x, img_y, speed, sprite_x, sprite_y):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.transform.scale(pygame.image.load(img), (85, 85))
        self.speed = speed
        self.img_rect = self.img.get_rect()
        self.img_rect.x = img_x
        self.img_rect.y = img_y
        self.sprite_rect = pygame.Rect(0, 0, sprite_x, sprite_y)
        self.sprite_rect.center = self.img_rect.center
        self.image_for_know = None
    def draw(self):
        window.blit(self.img, (self.img_rect.x, self.img_rect.y))
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.sprite_rect, 3)
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.img_rect, 3)

ITEMS = pygame.sprite.Group()
super_power_time = pygame.Rect(0, 0, 10, 10)
power_time = False

# Метеориты:
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, img, img_x, img_y, speed, sprite_x, sprite_y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.transform.scale(pygame.image.load(img), (85, 85))
        self.random_angle = [0, 90, 180, 270, 360]
        self.angle = choice(self.random_angle)
        self.new_img = pygame.transform.rotate(self.img, self.angle)
        self.speed = speed
        self.img_rect = self.new_img.get_rect()
        self.img_rect.x = img_x
        self.img_rect.y = img_y
        self.sprite_rect = pygame.Rect(0, 0, sprite_x, sprite_y)
        self.sprite_rect.center = self.img_rect.center
        self.hp = hp
        self.explosion = pygame.transform.scale(pygame.image.load('Blow_up.png'), (85, 85))
        self.explosion_rect = self.explosion.get_rect()
        self.explosion_rect.center = self.img_rect.center
        self.explosion_time = pygame.Rect(0, 0, 10, 10)
        self.random_angle = [0, 90, 180, 270, 360]
        self.angle = choice(self.random_angle)
        self.image_to_know = img
    def draw(self):
        window.blit(self.new_img, (self.img_rect.x, self.img_rect.y))
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.sprite_rect, 3)
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.img_rect, 3)
    def blow_up(self):
        explosion = pygame.transform.rotate(self.explosion, self.angle)
        window.blit(explosion, (self.explosion_rect.x, self.explosion_rect.y))

# Боссы:
class Boss(pygame.sprite.Sprite):
    def __init__(self, img, img_x, img_y, speed, sprite_x, sprite_y, hp):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.transform.scale(pygame.image.load(img), (170, 170))
        self.speed = speed
        self.img_rect = self.img.get_rect()
        self.img_rect.x = img_x
        self.img_rect.y = img_y
        self.sprite_rect = pygame.Rect(0, 0, sprite_x, sprite_y)
        self.sprite_rect.center = self.img_rect.center
        self.hp = hp
        self.explosion1 = pygame.transform.scale(pygame.image.load('Boss-BLOWUP.png'), (170, 170))
        self.explosion1_rect = self.explosion1.get_rect()
        self.explosion1_rect.center = self.img_rect.center
        self.explosion1_time = pygame.Rect(0, 0, 10, 10)
        self.explosion2 = pygame.transform.scale(pygame.image.load('Blow_up.png'), (85, 85))
        self.explosion2_rect = self.explosion2.get_rect()
        self.explosion2_rect.center = self.img_rect.center
        self.explosion2_time = pygame.Rect(0, 0, 10, 10)
        self.explosion3 = pygame.transform.scale(pygame.image.load('Blow_up.png'), (85, 85))
        self.explosion3_rect = self.explosion2.get_rect()
        self.explosion3_rect.center = self.img_rect.center
        self.explosion3_time = pygame.Rect(0, 0, 10, 10)
        self.laser = pygame.transform.scale(pygame.image.load('Boss-2-laser.png'), (120, 500))
        self.laser_img_rect = self.laser.get_rect()
        self.laser_img_rect.center = self.sprite_rect.center
        self.laser_img_rect.y += 200
        self.laser_sprite_rect = pygame.Rect(0, 0, 30, 500)
        self.laser_sprite_rect.center = self.laser_img_rect.center
        self.claw1 = pygame.transform.scale(pygame.image.load('Boss-3_claw1.png'), (170, 170))
        self.claw1_img_rect = self.claw1.get_rect()
        self.claw1_img_rect.center = self.img_rect.center
        self.claw1_img_rect.x -= 50
        self.claw1_sprite_rect = pygame.Rect(0, 0, 170, 20)
        self.claw1_sprite_rect.center = self.claw1_img_rect.center
        self.claw2 = pygame.transform.scale(pygame.image.load('Boss-3_claw2.png'), (170, 170))
        self.claw2_img_rect = self.claw2.get_rect()
        self.claw2_img_rect.center = self.img_rect.center
        self.claw2_img_rect.x += 50
        self.claw2_sprite_rect = pygame.Rect(0, 0, 170, 20)
        self.claw2_sprite_rect.center = self.claw2_img_rect.center
    def draw(self):
        window.blit(self.img, (self.img_rect.x, self.img_rect.y))
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.sprite_rect, 3)
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.img_rect, 3)
    def laser_draw(self):
        window.blit(self.laser, (self.laser_img_rect.x, self.laser_img_rect.y))
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.laser_img_rect, 3)
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.laser_sprite_rect, 3)
    def claws_draw(self):
        window.blit(self.claw1, (self.claw1_img_rect.x, self.claw1_img_rect.y))
        window.blit(self.claw2, (self.claw2_img_rect.x, self.claw2_img_rect.y))
        if show_hitbox == 1:
            pygame.draw.rect(window, (0, 0, 255), self.claw1_img_rect, 3)
            pygame.draw.rect(window, (0, 0, 255), self.claw2_img_rect, 3)
        if show_hitbox >= 1:
            pygame.draw.rect(window, (255, 0, 0), self.claw1_sprite_rect, 3)
            pygame.draw.rect(window, (255, 0, 0), self.claw2_sprite_rect, 3)
    def blow_up1(self):
        window.blit(self.explosion1, (self.explosion1_rect.x, self.explosion1_rect.y))
    def blow_up2(self):
        window.blit(self.explosion2, (self.explosion2_rect.x, self.explosion2_rect.y))
    def blow_up3(self):
        window.blit(self.explosion3, (self.explosion3_rect.x, self.explosion3_rect.y))

# Тексты и счётчики:
font1 = pygame.font.Font("PixeloidSans.ttf", 25)
font2 = pygame.font.Font("PixeloidSans.ttf", 34)
font3 = pygame.font.Font("PixeloidSans.ttf", 40)
font4 = pygame.font.Font("PixeloidSans.ttf", 60)
font5 = pygame.font.Font("PixeloidSans.ttf", 100)
font6 = pygame.font.Font("PixeloidSans.ttf", 80)

game_name1 = font4.render("GALAXY", True, (255, 255, 0))
game_name2 = font4.render("SHOOTER", True, (0, 255, 0))
logo = pygame.transform.scale(pygame.image.load('Boss-BLOWUP.png'), (170, 170))
two = font5.render("2", True, (0, 0, 255))
boss_text = font2.render("BOSS", True, (255, 0, 0))

best_score = None

def load_best_score():
    try:
        with open('best_score.txt', 'r') as f:
            best_score_value = int(f.read().strip())
            return best_score_value
    except FileNotFoundError:
        return 0

def save_best_score(best_score_value):
    with open('best_score.txt', 'w') as f:
        f.write(str(best_score_value))

best_score = load_best_score()
best_score_text = font1.render('BEST SCORE - '+str(best_score), True, (255, 255, 255))

game_over_text = font6.render('GAME OVER', True, (100, 100, 255))

options_text = font4.render('OPTIONS', True, (255, 255, 255))
player_color_text = font2.render('PLAYER COLOR:', True, (255, 255, 255))
bg_color_text = font2.render('BACKGROUND COLOR:', True, (255, 255, 255))
music_text = font2.render('STARS:', True, (255, 255, 255))

info_text = font4.render('INFORMATION', True, (255, 255, 255))
ufo_green = pygame.transform.scale(pygame.image.load('UFO-GREEN.png'), (60, 60))
ufo_blue = pygame.transform.scale(pygame.image.load('UFO-BLUE.png'), (60, 60))
ufo_orange = pygame.transform.scale(pygame.image.load('UFO-ORANGE.png'), (60, 60))
ufo_green_info = font1.render('3 hp; 1 power; 1-3 score', True, (255, 255, 255))
ufo_blue_info = font1.render('3 hp (+ 2 armor); 1 power; 1-3 score', True, (255, 255, 255))
ufo_orange_info = font1.render('3 hp; 2 power; 1-3 score', True, (255, 255, 255))
health_item = pygame.transform.scale(pygame.image.load('Health_point.png'), (60, 60))
power_item = pygame.transform.scale(pygame.image.load('Power_point.png'), (60, 60))
health_item_info = font1.render('+ 1 hp', True, (255, 255, 255))
power_item_info = font1.render('+ 3 bullets (5 sec.)', True, (255, 255, 255))
about_health = font1.render('If your hp reaches 0, the game ends', True, (255, 255, 0))

# Кнопки:
button_play1 = pygame.transform.scale(pygame.image.load('invisible_square_50.png'), (150, 80))
button_play2 = pygame.Rect(225, 300, 150, 80)
play = font3.render("PLAY", True, (255, 255, 255))

button_info1 = pygame.transform.scale(pygame.image.load('invisible_square_50.png'), (150, 80))
button_info2 = pygame.Rect(225, 400, 150, 80)
info = font3.render("INFO", True, (255, 255, 255))

button_options1 = pygame.transform.scale(pygame.image.load('invisible_square_50.png'), (150, 80))
button_options2 = pygame.Rect(225, 500, 150, 80)
options = font2.render("OPTION", True, (255, 255, 255))

button_quit1 = pygame.transform.scale(pygame.image.load('invisible_square_50.png'), (150, 80))
button_quit2 = pygame.Rect(225, 600, 150, 80)
quit = font3.render("EXIT", True, (255, 255, 255))

button_main1 = pygame.transform.scale(pygame.image.load('invisible_square_50.png'), (150, 80))
button_main2 = pygame.Rect(225, 600, 150, 80)
main = font3.render("MAIN", True, (255, 255, 255))

button1_color = (100, 100, 255)
button2_color = (100, 100, 255)
button3_color = (100, 100, 255)
button4_color = (100, 100, 255)
button5_color = (100, 100, 255)
button6_color = (100, 100, 255)

d = 1

player_red = pygame.transform.scale(pygame.image.load('Spaceship-RED.png'), (40, 40))
color_button1 = player_red.get_rect()
color_button1.x = 300
color_button1.y = 150
red_choosed = True

player_green = pygame.transform.scale(pygame.image.load('Spaceship-GREEN.png'), (40, 40))
color_button2 = player_green.get_rect()
color_button2.x = 350
color_button2.y = 150
green_choosed = False

player_blue = pygame.transform.scale(pygame.image.load('Spaceship-BLUE.png'), (40, 40))
color_button3 = player_blue.get_rect()
color_button3.x = 400
color_button3.y = 150
blue_choosed = False

player_yellow = pygame.transform.scale(pygame.image.load('Spaceship-YELLOW.png'), (40, 40))
color_button4 = player_yellow.get_rect()
color_button4.x = 450
color_button4.y = 150
yellow_choosed = False

player_purple = pygame.transform.scale(pygame.image.load('Spaceship-PURPLE.png'), (40, 40))
color_button5 = player_purple.get_rect()
color_button5.x = 500
color_button5.y = 150
purple_choosed = False

bg_blue_button1 = pygame.Rect(400, 225, 40, 40)
bg_blue_button2 = pygame.Rect(400, 225, 40, 40)

bg_purple_button1 = pygame.Rect(450, 225, 40, 40)
bg_purple_button2 = pygame.Rect(450, 225, 40, 40)

bg_green_button1 = pygame.Rect(500, 225, 40, 40)
bg_green_button2 = pygame.Rect(500, 225, 40, 40)

bg_red_button1 = pygame.Rect(550, 225, 40, 40)
bg_red_button2 = pygame.Rect(550, 225, 40, 40)

button_offon_stars1 = pygame.transform.scale(pygame.image.load('invisible_square_50.png'), (150, 50))
button_offon_stars2 = pygame.Rect(150, 295, 150, 50)
offon_stars = font2.render("OFF/ON", True, (255, 255, 255))
hide_stars = 1
hide_stars1 = False

# Звуки:
button_click_sound = pygame.mixer.Sound('button_click.mp3')
player_shoot_sound = pygame.mixer.Sound('player_shoot.mp3')
player_supershoot_sound = pygame.mixer.Sound('player_supershoot.mp3')
ufo_destroyed_sound = pygame.mixer.Sound('UFO_destroyed.mp3')
ufo_heated_sound = pygame.mixer.Sound('UFO_heated.mp3')
health_plus_sound = pygame.mixer.Sound('health+.mp3')
super_power_sound = pygame.mixer.Sound('power+.mp3')
player_blowup_sound = pygame.mixer.Sound('player_blowup.mp3')
player_heated_sound = pygame.mixer.Sound('player_heated.mp3')
boss_shoots_sound = pygame.mixer.Sound('boss_shoots.mp3')
laser_sound = pygame.mixer.Sound('laser_attack.mp3')
boss_asteroids_sound = pygame.mixer.Sound('boss_asteroids.mp3')
boss_small_blowup_sound = pygame.mixer.Sound('boss_small_blowup.mp3')
boss_big_blowup_sound = pygame.mixer.Sound('boss_big_blowup.mp3')
game_music = pygame.mixer.Sound('game_music.mp3')
boss_music = pygame.mixer.Sound('boss_music.mp3')
boss_appear_sound = pygame.mixer.Sound('boss_appear.mp3')

channel0 = pygame.mixer.Channel(0)
channel0.set_volume(1)
channel1 = pygame.mixer.Channel(1)
channel1.set_volume(0.5)
channel2 = pygame.mixer.Channel(2)
channel2.set_volume(0.5)
channel3 = pygame.mixer.Channel(3)
channel3.set_volume(0.3)
channel4 = pygame.mixer.Channel(4)
channel4.set_volume(0.5)
channel5 = pygame.mixer.Channel(5)
channel5.set_volume(0.2)
channel6 = pygame.mixer.Channel(6)
channel6.set_volume(0.3)
channel7 = pygame.mixer.Channel(7)
channel7.set_volume(0.4)
e = 1
f = 1

# Игровой цикл:
clock = pygame.time.Clock()
game_over = False
start_game = True
options_list = False
info_list = False

while True:

    # Отрисовка объектов:
    window.fill(bg_color)

    if not hide_stars1:
        Stars1.draw()
        Stars2.draw()
        Stars1.return_stars()
        Stars2.return_stars()
        Stars1.img_rect.y += Stars1.speed
        Stars2.img_rect.y += Stars2.speed

    if not start_game:
        for bullet in BULLETS:
            if bullet.img_rect.y <= PLAYER.img_rect.y - 20:
                bullet.draw()
        if not game_over:
            PLAYER.draw()
        for ufo in ENEMIES:
            if destroyed != 10 and PLAYER.health != 0:
                ufo.draw_bullet()
            if ufo.health != 0:
                ufo.draw()

        for asteroid in ASTEROIDS:
            if asteroid.hp != 0:
                asteroid.draw()

        for asteroid in asteroid_boss_group:
            if asteroid.hp != 0:
                asteroid.draw()
        if BOSS_1.explosion3_time.x != 150:
            BOSS_1.draw()
        if BOSS_2.explosion3_time.x != 150:
            BOSS_2.draw()
            if laser_attack and BOSS_2.img_rect.y > 0:
                if e == 1:
                    channel6.play(laser_sound)
                    e = 0
                BOSS_2.laser_draw()
        if BOSS_3.explosion3_time.x != 150:
            for bullet in bullets_boss_group:
                if bullet.hp == 1:
                    bullet.draw()
            BOSS_3.claws_draw()
            BOSS_3.draw()

        window.blit(square_score, (35, 620))
        window.blit(score_text, (54, 620))
        window.blit(score_counter, (score_counter_x, 650))

        window.blit(square_hp, (445, 620))
        window.blit(health_text, (454, 620))
        window.blit(hp_counter, (495, 650))

        wave_counter_text = font3.render('WAVE-' + str(wave_counter), True, (255, 255, 255))
        if wave_counter_x >= -160:
            window.blit(wave_counter_text, (wave_counter_x, 350))
        window.blit(warning_text, (warning_x, 350))

        if wave_counter == 1 and UFO1.img_rect.y != 75:
            window.blit(ready_text, (235, 630))

    # Управление игрой (события):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEMOTION and not game_over and not start_game:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            PLAYER.img_rect.center = (mouse_x, mouse_y)
            PLAYER.sprite_rect.center = PLAYER.img_rect.center
            PLAYER.explosion_rect.center = PLAYER.img_rect.center

        if event.type == pygame.MOUSEBUTTONDOWN and shoot and not game_over and not start_game:
            if event.button == 1:
                if amount_bullets >= 1:
                    channel1.set_volume(0.5)
                    channel1.play(player_shoot_sound)
                    BULLET = Bullet('Bullet-YELLOW.png', 0, 0, 15, 20, 50, 0)
                    BULLET.img_rect.center = PLAYER.img_rect.center
                    BULLET.sprite_rect.center = BULLET.img_rect.center
                    BULLETS.add(BULLET)
                if amount_bullets == 3:
                    channel1.set_volume(0.3)
                    channel1.play(player_supershoot_sound)
                    BULLET1 = Bullet('Bullet-YELLOW.png', 0, 0, 15, 20, 50, 0)
                    BULLET1.img_rect.center = PLAYER.img_rect.center
                    BULLET1.img_rect.x -= 30
                    BULLET1.img_rect.y += 60
                    BULLET1.sprite_rect.center = BULLET1.img_rect.center
                    BULLETS.add(BULLET1)
                    BULLET2 = Bullet('Bullet-YELLOW.png', 0, 0, 15, 20, 50, 0)
                    BULLET2.img_rect.center = PLAYER.img_rect.center
                    BULLET2.img_rect.x += 30
                    BULLET2.img_rect.y += 60
                    BULLET2.sprite_rect.center = BULLET2.img_rect.center
                    BULLETS.add(BULLET2)

        if event.type == pygame.MOUSEBUTTONDOWN and start_game and not options_list and not info_list:
            x, y = event.pos
            channel0.set_volume(1)
            if button_play2.collidepoint(x,y):

                channel0.play(button_click_sound)

                PLAYER.img_rect.x = 257.5
                PLAYER.img_rect.y = 500
                PLAYER.sprite_rect.center = PLAYER.img_rect.center
                PLAYER.explosion_rect.center = PLAYER.img_rect.center
                PLAYER.health = 3

                UFO1 = UFO('UFO-GREEN.png', 25, 75 - 300, 1, 10, 55, 55, 3)
                UFO2 = UFO('UFO-GREEN.png', 140.5, 75 - 300, 1, 10, 55, 55, 3)
                UFO3 = UFO('UFO-GREEN.png', 257.5, 75 - 300, 1, 10, 55, 55, 3)
                UFO4 = UFO('UFO-GREEN.png', 375.5, 75 - 300, 1, 10, 55, 55, 3)
                UFO5 = UFO('UFO-GREEN.png', 495, 75 - 300, 1, 10, 55, 55, 3)
                UFO6 = UFO('UFO-GREEN.png', 25, 175 - 600, 1, 10, 55, 55, 3)
                UFO7 = UFO('UFO-GREEN.png', 140.5, 175 - 600, 1, 10, 55, 55, 3)
                UFO8 = UFO('UFO-GREEN.png', 257.5, 175 - 600, 1, 10, 55, 55, 3)
                UFO9 = UFO('UFO-GREEN.png', 375.5, 175 - 600, 1, 10, 55, 55, 3)
                UFO10 = UFO('UFO-GREEN.png', 495, 175 - 600, 1, 10, 55, 55, 3)

                ENEMIES = pygame.sprite.Group()
                ENEMIES.add(UFO1)
                ENEMIES.add(UFO2)
                ENEMIES.add(UFO3)
                ENEMIES.add(UFO4)
                ENEMIES.add(UFO5)
                ENEMIES.add(UFO6)
                ENEMIES.add(UFO7)
                ENEMIES.add(UFO8)
                ENEMIES.add(UFO9)
                ENEMIES.add(UFO10)
                for ufo in ENEMIES:
                    ufo.new_icon()

                ENEMIES_list = [UFO1, UFO2, UFO3, UFO4, UFO5, UFO6, UFO7, UFO8, UFO9, UFO10]
                UFO_TOP = [UFO1, UFO2, UFO3, UFO4, UFO5]
                UFO_DOWN = [UFO6, UFO7, UFO8, UFO9, UFO10]

                destroyed = 10

                UFO1_shoot = randint(1, 5)
                UFO2_shoot = randint(1, 5)
                UFO3_shoot = randint(1, 5)
                UFO4_shoot = randint(1, 5)
                UFO5_shoot = randint(1, 5)
                UFO6_shoot = randint(1, 5)
                UFO7_shoot = randint(1, 5)
                UFO8_shoot = randint(1, 5)
                UFO9_shoot = randint(1, 5)
                UFO10_shoot = randint(1, 5)

                asteroid_x = [0, 100, 200, 300, 400, 500]

                ASTEROID1 = Asteroid('Asteroid.png', choice(asteroid_x), -100, 3, 60, 60, 10)
                ASTEROID2 = Asteroid('Asteroid.png', choice(asteroid_x), -200, 3, 60, 60, 10)
                ASTEROID3 = Asteroid('Asteroid.png', choice(asteroid_x), -300, 3, 60, 60, 10)
                ASTEROID4 = Asteroid('Asteroid.png', choice(asteroid_x), -400, 3, 60, 60, 10)
                ASTEROID5 = Asteroid('Asteroid.png', choice(asteroid_x), -500, 3, 60, 60, 10)
                ASTEROID6 = Asteroid('Asteroid.png', choice(asteroid_x), -600, 3, 60, 60, 10)
                ASTEROID7 = Asteroid('Asteroid.png', choice(asteroid_x), -700, 3, 60, 60, 10)
                ASTEROID8 = Asteroid('Asteroid.png', choice(asteroid_x), -800, 3, 60, 60, 10)
                ASTEROID9 = Asteroid('Asteroid.png', choice(asteroid_x), -900, 3, 60, 60, 10)
                ASTEROID10 = Asteroid('Asteroid.png', choice(asteroid_x), -1000, 3, 60, 60, 10)

                asteroid_wave = False
                asteroid_wave_end = 0

                ASTEROIDS = pygame.sprite.Group()
                ASTEROIDS.add(ASTEROID1)
                ASTEROIDS.add(ASTEROID2)
                ASTEROIDS.add(ASTEROID3)
                ASTEROIDS.add(ASTEROID4)
                ASTEROIDS.add(ASTEROID5)
                ASTEROIDS.add(ASTEROID6)
                ASTEROIDS.add(ASTEROID7)
                ASTEROIDS.add(ASTEROID8)
                ASTEROIDS.add(ASTEROID9)
                ASTEROIDS.add(ASTEROID10)

                ASTEROIDS_list = [ASTEROID1, ASTEROID2, ASTEROID3, ASTEROID4, ASTEROID5, ASTEROID6, ASTEROID7,
                                  ASTEROID8, ASTEROID9, ASTEROID10]

                BOSS_1 = Boss('Boss-1.png', 215, -200, 5, 130, 120, 50)
                asteroid_boss_group = pygame.sprite.Group()
                boss_time = pygame.Rect(0, 0, 10, 10)
                a = 1
                b = 1
                c = 1

                BOSS_2 = Boss('Boss-2.png', 215, -200, 5, 130, 120, 50)
                BOSS_2_attack1 = False
                BOSS_2_attack2 = False
                BOSS_2_attack3 = False
                laser_attack = False
                laser_attack_time = pygame.Rect(0, 0, 10, 10)
                bullets_boss_group = pygame.sprite.Group()
                e = 1
                f = 1
                g = 1

                BOSS_3 = Boss('Boss-3.png', 215, -200, 5, 130, 120, 50)
                claws_random_y = [250, 300, 350, 400, 450, 500, 550, 600]

                boss_health_bar1 = pygame.Rect(150, 50, 300, 20)
                boss_health_bar2 = pygame.Rect(150, 50, 300, 20)
                boss_hp1 = pygame.Rect(150, 50, 60, 20)
                boss_hp2 = pygame.Rect(210, 50, 60, 20)
                boss_hp3 = pygame.Rect(270, 50, 60, 20)
                boss_hp4 = pygame.Rect(330, 50, 60, 20)
                boss_hp5 = pygame.Rect(390, 50, 60, 20)

                boss_wave = False

                score = 0
                score_text = font1.render("SCORE", True, (255, 255, 255))
                score_counter = font2.render(str(score), True, (255, 255, 0))
                score_counter_x = 86
                square_score = pygame.transform.scale(pygame.image.load('invisible_square_50.png'), (120, 70))

                health_text = font1.render('HEALTH', True, (255, 255, 255))
                hp_color = (0, 255, 0)
                hp_counter = font2.render(str(PLAYER.health), True, hp_color)
                square_hp = pygame.transform.scale(pygame.image.load('invisible_square_50.png'), (120, 70))

                wave_counter = 1
                wave_counter_text = font3.render('WAVE-' + str(wave_counter), True, (255, 255, 255))
                wave_counter_x = -200
                warning_text = font3.render('! WARNING !', True, (255, 0, 0))
                warning_x = -300

                ready_text = font3.render('READY', True, (255, 255, 0))

                super_power_text = font1.render("Super Power!", True, (255, 255, 0))
                plus_health_text = font1.render("+ 1HP!", True, (255, 255, 0))
                text_time = pygame.Rect(0, 0, 10, 10)
                time_for_text = False

                enemies_destroyed = 0
                bosses_destroyed = 0

                for item in ITEMS:
                    ITEMS.remove(item)
                super_power_time.x = 0
                power_time = False
                text_time.x = 0
                time_for_text = False

                game_over_rect = pygame.Rect(0, -900, 600, 700)

                start_time = time()
                cur_time = start_time

                music_play_time = 0
                channel0.set_volume(0.2)
                channel0.play(game_music)

                start_game = False
                game_over = False

            if button_quit2.collidepoint(x,y) and d == 1:
                channel0.play(button_click_sound)
                exit()

            if button_options2.collidepoint(x,y):
                channel0.play(button_click_sound)
                options_list = True
                d = 0
            if button_info2.collidepoint(x,y):
                channel0.play(button_click_sound)
                info_list = True

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            x, y = event.pos
            channel0.set_volume(1)
            if button_main2.collidepoint(x,y):
                channel0.play(button_click_sound)
                if score > best_score:
                    best_score = score
                    save_best_score(best_score)
                    best_score_text = font1.render('BEST SCORE - ' + str(best_score), True, (255, 255, 255))
                start_game = True

        if event.type == pygame.MOUSEBUTTONDOWN and options_list and d == 0 and not info_list:
            x, y = event.pos
            channel0.set_volume(1)
            if button_main2.collidepoint(x,y):
                channel0.play(button_click_sound)
                options_list = False
                d = 1
                
            if color_button1.collidepoint(x,y):
                channel0.play(button_click_sound)
                red_choosed = True
                green_choosed = False
                blue_choosed = False
                yellow_choosed = False
                purple_choosed = False
                PLAYER = Player('Spaceship-RED.png', 257.5, 500, 10, 3, 55, 55)
            if color_button2.collidepoint(x,y):
                channel0.play(button_click_sound)
                red_choosed = False
                green_choosed = True
                blue_choosed = False
                yellow_choosed = False
                purple_choosed = False
                PLAYER = Player('Spaceship-GREEN.png', 257.5, 500, 10, 3, 55, 55)
            if color_button3.collidepoint(x,y):
                channel0.play(button_click_sound)
                red_choosed = False
                green_choosed = False
                blue_choosed = True
                yellow_choosed = False
                purple_choosed = False
                PLAYER = Player('Spaceship-BLUE.png', 257.5, 500, 10, 3, 55, 55)
            if color_button4.collidepoint(x,y):
                channel0.play(button_click_sound)
                red_choosed = False
                green_choosed = False
                blue_choosed = False
                yellow_choosed = True
                purple_choosed = False
                PLAYER = Player('Spaceship-YELLOW.png', 257.5, 500, 10, 3, 55, 55)
            if color_button5.collidepoint(x,y):
                channel0.play(button_click_sound)
                red_choosed = False
                green_choosed = False
                blue_choosed = False
                yellow_choosed = False
                purple_choosed = True
                PLAYER = Player('Spaceship-PURPLE.png', 257.5, 500, 10, 3, 55, 55)
            if bg_blue_button1.collidepoint(x,y):
                channel0.play(button_click_sound)
                bg_color = (20, 30, 60)
            if bg_purple_button1.collidepoint(x,y):
                channel0.play(button_click_sound)
                bg_color = (40, 25, 40)
            if bg_green_button1.collidepoint(x,y):
                channel0.play(button_click_sound)
                bg_color = (30, 40, 30)
            if bg_red_button1.collidepoint(x,y):
                channel0.play(button_click_sound)
                bg_color = (60, 25, 40)
            if button_offon_stars2.collidepoint(x,y):
                channel0.play(button_click_sound)
                hide_stars += 1
                if hide_stars == 3:
                    hide_stars = 1
                if hide_stars == 2:
                    hide_stars1 = True
                else:
                    hide_stars1 = False

        if event.type == pygame.MOUSEBUTTONDOWN and info_list:
            x, y = event.pos
            channel0.set_volume(1)
            if button_main2.collidepoint(x,y):
                channel0.play(button_click_sound)
                info_list = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                show_hitbox += 1
                if show_hitbox == 3:
                    show_hitbox = 0
            if event.key == pygame.K_p:
                amount_bullets += 2
                if amount_bullets == 5:
                    amount_bullets = 1

    # Главное меню:
    if start_game and not options_list and not info_list:

        window.blit(logo, (70, 50))
        window.blit(two, (130, 80))
        window.blit(game_name1, (250, 70))
        window.blit(game_name2, (250, 130))

        window.blit(best_score_text, (255, 210))

        window.blit(button_play1, (225, 300))
        pygame.draw.rect(window, button1_color, button_play2, 5)
        window.blit(play, (248, 315))

        window.blit(button_info1, (225, 400))
        pygame.draw.rect(window, button2_color, button_info2, 5)
        window.blit(info, (249, 415))

        window.blit(button_options1, (225, 500))
        pygame.draw.rect(window, button3_color, button_options2, 5)
        window.blit(options, (235, 520))

        window.blit(button_quit1, (225, 600))
        pygame.draw.rect(window, button4_color, button_quit2, 5)
        window.blit(quit, (253, 615))

        mouse_pos = pygame.mouse.get_pos()
        if button_play2.collidepoint(mouse_pos):
            button1_color = (200, 200, 255)
        else:
            button1_color = (100, 100, 255)
        if button_info2.collidepoint(mouse_pos):
            button2_color = (200, 200, 255)
        else:
            button2_color = (100, 100, 255)
        if button_options2.collidepoint(mouse_pos):
            button3_color = (200, 200, 255)
        else:
            button3_color = (100, 100, 255)
        if button_quit2.collidepoint(mouse_pos):
            button4_color = (200, 200, 255)
        else:
            button4_color = (100, 100, 255)

    # Настройки:
    if options_list and not info_list:
        window.blit(options_text, (165, 20))

        window.blit(player_color_text, (10, 150))
        window.blit(player_red, (300, 150))
        if red_choosed:
            pygame.draw.rect(window, (255, 255, 0), color_button1, 2)
        window.blit(player_green, (350, 150))
        if green_choosed:
            pygame.draw.rect(window, (255, 255, 0), color_button2, 2)
        window.blit(player_blue, (400, 150))
        if blue_choosed:
            pygame.draw.rect(window, (255, 255, 0), color_button3, 2)
        window.blit(player_yellow, (450, 150))
        if yellow_choosed:
            pygame.draw.rect(window, (255, 255, 0), color_button4, 2)
        window.blit(player_purple, (500, 150))
        if purple_choosed:
            pygame.draw.rect(window, (255, 255, 0), color_button5, 2)

        window.blit(bg_color_text, (10, 225))
        pygame.draw.rect(window, (20, 30, 60), bg_blue_button1)
        pygame.draw.rect(window, (200, 200, 200), bg_blue_button2, 2)
        pygame.draw.rect(window, (40, 25, 40), bg_purple_button1)
        pygame.draw.rect(window, (200, 200, 200), bg_purple_button2, 2)
        pygame.draw.rect(window, (30, 40, 30), bg_green_button1)
        pygame.draw.rect(window, (200, 200, 200), bg_green_button2, 2)
        pygame.draw.rect(window, (60, 25, 40), bg_red_button1)
        pygame.draw.rect(window, (200, 200, 200), bg_red_button2, 2)

        window.blit(music_text, (10, 300))

        window.blit(button_offon_stars1, (150, 295))
        pygame.draw.rect(window, button6_color, button_offon_stars2, 5)
        window.blit(offon_stars, (155, 300))

        window.blit(button_main1, (225, 600))
        pygame.draw.rect(window, button5_color, button_main2, 5)
        window.blit(main, (246, 615))

        mouse_pos = pygame.mouse.get_pos()
        if button_main2.collidepoint(mouse_pos):
            button5_color = (200, 200, 255)
        else:
            button5_color = (100, 100, 255)
        if button_offon_stars2.collidepoint(mouse_pos):
            button6_color = (200, 200, 255)
        else:
            button6_color = (100, 100, 255)

    # Информация:
    if info_list:
        window.blit(info_text, (85, 20))

        window.blit(ufo_green, (10, 150))
        window.blit(ufo_green_info, (85, 160))
        window.blit(ufo_blue, (10, 215))
        window.blit(ufo_blue_info, (85, 225))
        window.blit(ufo_orange, (10, 280))
        window.blit(ufo_orange_info, (85, 290))

        window.blit(health_item, (10, 345))
        window.blit(health_item_info, (70, 355))
        window.blit(power_item, (10, 410))
        window.blit(power_item_info, (70, 420))

        window.blit(about_health, (50, 495))

        window.blit(button_main1, (225, 600))
        pygame.draw.rect(window, button5_color, button_main2, 5)
        window.blit(main, (246, 615))

        mouse_pos = pygame.mouse.get_pos()
        if button_main2.collidepoint(mouse_pos):
            button5_color = (200, 200, 255)
        else:
            button5_color = (100, 100, 255)

    # Сама игра (основные действия):
    if not game_over and not start_game:

        pygame.mouse.set_visible(False)

        # Игрок:
        if PLAYER.img_rect.x >= 515:
            PLAYER.img_rect.x = 515
            PLAYER.sprite_rect.center = PLAYER.img_rect.center
            PLAYER.explosion_rect.center = PLAYER.img_rect.center
        if PLAYER.img_rect.x <= 0:
            PLAYER.img_rect.x = 0
            PLAYER.sprite_rect.center = PLAYER.img_rect.center
            PLAYER.explosion_rect.center = PLAYER.img_rect.center
        if PLAYER.img_rect.y <= 100:
            PLAYER.img_rect.y = 100
            PLAYER.sprite_rect.center = PLAYER.img_rect.center
            PLAYER.explosion_rect.center = PLAYER.img_rect.center
        if PLAYER.img_rect.y >= 615:
            PLAYER.img_rect.y = 615
            PLAYER.sprite_rect.center = PLAYER.img_rect.center
            PLAYER.explosion_rect.center = PLAYER.img_rect.center

        for bullet in BULLETS:
            bullet.shoot()
            if bullet.img_rect.y <= -80:
                BULLETS.remove(bullet)

        if PLAYER.img_rect.colliderect(BOSS_1.sprite_rect):
            PLAYER.health = 0
        if PLAYER.img_rect.colliderect(BOSS_2.sprite_rect):
            PLAYER.health = 0

        # НЛО:
        for ufo in ENEMIES:
            for bullet in BULLETS:
                if bullet.sprite_rect.colliderect(ufo.sprite_rect):
                    channel3.play(ufo_heated_sound)
                    BULLETS.remove(bullet)
                    ufo.health -= 1
            if ufo.health <= 0:
                ufo.bullet_return()
                channel2.play(ufo_destroyed_sound)
                item_chance = randint(1, 10)
                if item_chance == 1:
                    random_item = randint(1, 2)
                    if random_item == 1:
                        ITEM = Items('Health_point.png', ufo.sprite_rect.x, ufo.sprite_rect.y, 2, 30, 30)
                        ITEM.image_for_know = 'Health_point.png'
                    else:
                        ITEM = Items('Power_point.png', ufo.sprite_rect.x, ufo.sprite_rect.y, 2, 30, 30)
                        ITEM.image_for_know = 'Power_point.png'
                    ITEMS.add(ITEM)
                ufo.destroyed()
                ufo.new_icon()
                ENEMIES.remove(ufo)
                destroyed += 1
                score += randint(1, 3)
                score_counter = font2.render(str(score), True, (255, 255, 0))
                enemies_destroyed += 1
            if ufo.bullet_img_rect.y >= 700:
                ufo.bullet_return()
            if ufo.bullet_sprite_rect.colliderect(PLAYER.sprite_rect):
                channel2.play(player_heated_sound)
                PLAYER.health -= ufo.bullet_power
                ufo.bullet_return()
            if PLAYER.sprite_rect.colliderect(ufo.sprite_rect):
                PLAYER.health = 0
                ufo.destroyed()
                ufo.new_icon()
                ufo.bullet_return()
                ENEMIES.remove(ufo)
                destroyed += 1
                enemies_destroyed += 1

        if destroyed != 10:
            if UFO1_shoot == 1 and UFO1.img_rect.y > 0:
                UFO1.shoot()
            if UFO2_shoot == 1 and UFO2.img_rect.y > 0:
                UFO2.shoot()
            if UFO3_shoot == 1 and UFO3.img_rect.y > 0:
                UFO3.shoot()
            if UFO4_shoot == 1 and UFO4.img_rect.y > 0:
                UFO4.shoot()
            if UFO5_shoot == 1 and UFO5.img_rect.y > 0:
                UFO5.shoot()
            if UFO6_shoot == 1 and UFO6.img_rect.y > 0:
                UFO6.shoot()
            if UFO7_shoot == 1 and UFO7.img_rect.y > 0:
                UFO7.shoot()
            if UFO8_shoot == 1 and UFO8.img_rect.y > 0:
                UFO8.shoot()
            if UFO9_shoot == 1 and UFO9.img_rect.y > 0:
                UFO9.shoot()
            if UFO10_shoot == 1 and UFO10.img_rect.y > 0:
                UFO10.shoot()

        for ufo in ENEMIES_list:
            ufo.img_rect.x -= ufo.speed1
            ufo.sprite_rect.center = ufo.img_rect.center
            if ufo.img_rect.y > 0:
                ufo.explosion_rect.x = ufo.img_rect.x

        if UFO1.img_rect.x == 5 or UFO5.img_rect.x == 515:
            for ufo in ENEMIES_list:
                ufo.speed1 *= -1

        for ufo in ENEMIES_list:
            if ufo.img_rect.y < 0 and ufo.explosion_time.x != 100:
                ufo.blow_up()
                ufo.explosion_time.x += 5

        # Метеориты:
        if asteroid_wave:
            for asteroid in ASTEROIDS:
                asteroid.img_rect.y += asteroid.speed
                asteroid.sprite_rect.center = asteroid.img_rect.center
                asteroid.explosion_rect.center = asteroid.img_rect.center
                if ASTEROID1.img_rect.y >= 700:
                    destroyed = 0
                if asteroid.img_rect.y >= 700 and asteroid_wave_end != 3:
                    if ASTEROID10.img_rect.y >= 700:
                        asteroid_wave_end += 1
                    asteroid.img_rect.y -= 900
                    asteroid.img_rect.x = choice(asteroid_x)
                    asteroid.sprite_rect.center = asteroid.img_rect.center
                    asteroid.hp = 10
                    asteroid.explosion_time.x = 0
                for bullet in BULLETS:
                    if bullet.sprite_rect.colliderect(asteroid.sprite_rect) and asteroid.hp > 0:
                        channel3.play(ufo_heated_sound)
                        asteroid.hp -= 1
                        BULLETS.remove(bullet)
                if asteroid.sprite_rect.colliderect(PLAYER.sprite_rect) and asteroid.hp != 0:
                    PLAYER.health = 0
                if asteroid_wave_end == 3 and ASTEROID10.img_rect.y >= 700:
                    asteroid_wave = False
                    destroyed = 10
                    wave_counter += 1
                    asteroid_wave_end = 0
                    ASTEROID1.img_rect.y = -100
                    ASTEROID2.img_rect.y = -200
                    ASTEROID3.img_rect.y = -300
                    ASTEROID4.img_rect.y = -400
                    ASTEROID5.img_rect.y = -500
                    ASTEROID6.img_rect.y = -600
                    ASTEROID7.img_rect.y = -700
                    ASTEROID8.img_rect.y = -800
                    ASTEROID9.img_rect.y = -900
                    ASTEROID10.img_rect.y = -1000
                    for asteroid in ASTEROIDS:
                        asteroid.sprite_rect.center = asteroid.img_rect.center
                        asteroid.explosion_rect.center = asteroid.img_rect.center
                    for ufo in ENEMIES_list:
                        ufo.bullet_speed += 0.2

        for asteroid in ASTEROIDS_list:
            if asteroid.hp == 0 and asteroid.explosion_time.x != 100:
                channel2.play(ufo_destroyed_sound)
                asteroid.blow_up()
                asteroid.explosion_time.x += 5

        # Боссы:
        if boss_wave:
            destroyed = 0
            if g == 1:
                channel0.play(boss_appear_sound)
                music_play_time = 0
                g = 0
            # Босс-1:
            if random_boss == 1:
                if BOSS_1.img_rect.y != 100:
                    BOSS_1.img_rect.y += 2
                    BOSS_1.sprite_rect.center = BOSS_1.img_rect.center
                    BOSS_1.explosion1_rect.center = BOSS_1.img_rect.center
                    BOSS_1.explosion2_rect.center = BOSS_1.img_rect.center
                    BOSS_1.explosion3_rect.center = BOSS_1.img_rect.center
                    BOSS_1.explosion2_rect.x = BOSS_1.img_rect.x
                    BOSS_1.explosion3_rect.x = BOSS_1.img_rect.x + 85
                    warning_x += 8
                else:
                    warning_x = -300
                    if boss_time.x != 50:
                        boss_time.x += 2
                    else:
                        window.blit(boss_text, (255, 5))
                        pygame.draw.rect(window, (0, 0, 0), boss_health_bar1)
                        if BOSS_1.hp >= 1:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp1)
                        if BOSS_1.hp >= 10:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp2)
                        if BOSS_1.hp >= 20:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp3)
                        if BOSS_1.hp >= 30:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp4)
                        if BOSS_1.hp >= 40:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp5)
                        pygame.draw.rect(window, (150, 150, 150), boss_health_bar2, 3)
                        if BOSS_1.hp >= 0:
                            shoot = True
                        if a == 1:
                            channel0.play(boss_music)
                            music_play_time = 0
                            ASTEROID = Asteroid('Asteroid.png', 0, 0, 5, 65, 65, 100)
                            ASTEROID.img_rect.center = BOSS_1.img_rect.center
                            ASTEROID.img_rect.y += 50
                            ASTEROID.sprite_rect.center = ASTEROID.img_rect.center
                            asteroid.explosion_rect.center = asteroid.img_rect.center
                            asteroid_boss_group.add(ASTEROID)
                            channel5.play(boss_asteroids_sound)
                            a = 0
                        if BOSS_1.img_rect.x == 10 or BOSS_1.img_rect.x == 420:
                            BOSS_1.speed *= -1
                        if BOSS_1.hp > 0:
                            BOSS_1.img_rect.x += BOSS_1.speed
                            BOSS_1.sprite_rect.center = BOSS_1.img_rect.center
                            BOSS_1.explosion1_rect.center = BOSS_1.img_rect.center
                            BOSS_1.explosion2_rect.center = BOSS_1.img_rect.center
                            BOSS_1.explosion2_rect.x = BOSS_1.img_rect.x
                            BOSS_1.explosion3_rect.center = BOSS_1.img_rect.center
                            BOSS_1.explosion3_rect.x = BOSS_1.img_rect.x + 85
                        if BOSS_1.hp < 0:
                            BOSS_1.hp = 0
                        for bullet in BULLETS:
                            if bullet.sprite_rect.colliderect(BOSS_1.sprite_rect):
                                channel3.play(ufo_heated_sound)
                                BOSS_1.hp -= 1
                                BULLETS.remove(bullet)
                        for asteroid in asteroid_boss_group:
                            if asteroid.img_rect.y == 358 and BOSS_1.hp > 0:
                                ASTEROID = Asteroid('Asteroid.png', 0, 0, 5, 65, 65, 100)
                                ASTEROID.img_rect.center = BOSS_1.img_rect.center
                                ASTEROID.img_rect.y += 50
                                ASTEROID.sprite_rect.center = ASTEROID.img_rect.center
                                asteroid.explosion_rect.center = asteroid.img_rect.center
                                asteroid_boss_group.add(ASTEROID)
                                channel5.play(boss_asteroids_sound)
                            asteroid.img_rect.y += asteroid.speed
                            asteroid.sprite_rect.center = asteroid.img_rect.center
                            if asteroid.sprite_rect.colliderect(PLAYER.sprite_rect) and asteroid.hp != 0:
                                channel2.play(player_heated_sound)
                                PLAYER.health -= 1
                                asteroid.hp = 0
                            for bullet in BULLETS:
                                if bullet.sprite_rect.colliderect(asteroid.sprite_rect):
                                    channel3.play(ufo_heated_sound)
                                    asteroid.hp -= 1
                                    BULLETS.remove(bullet)
                            if asteroid.img_rect.y >= 700:
                                asteroid_boss_group.remove(asteroid)
                        if BOSS_1.hp == 0:
                            shoot = False
                            asteroid_boss_group.empty()
                            if BOSS_1.explosion2_time.x != 150:
                                if b == 1:
                                    BOSS_1.img = pygame.transform.rotate(BOSS_1.img, 5)
                                    b = 0
                                BOSS_1.blow_up2()
                                BOSS_1.explosion2_time.x += 5
                                if f == 1:
                                    channel7.set_volume(1)
                                    channel7.play(boss_small_blowup_sound)
                                    f = 0
                            else:
                                if BOSS_1.explosion3_time.x != 150:
                                    if c == 1:
                                        BOSS_1.img = pygame.transform.rotate(BOSS_1.img, -10)
                                        c = 0
                                        f = 1
                                    BOSS_1.blow_up3()
                                    BOSS_1.explosion3_time.x += 5
                                    if f == 1:
                                        channel7.play(boss_small_blowup_sound)
                                        f = 0
                                else:
                                    if BOSS_1.explosion1_time.x != 200:
                                        BOSS_1.blow_up1()
                                        BOSS_1.explosion1_time.x += 5
                                        if f == 0:
                                            channel7.set_volume(0.4)
                                            channel7.play(boss_big_blowup_sound)
                                            f = 1
                                    else:
                                        ITEM1 = Items('Health_point.png', BOSS_1.sprite_rect.x - 20, BOSS_1.sprite_rect.y - 20, 2, 30, 30)
                                        ITEM1.image_for_know = 'Health_point.png'
                                        ITEMS.add(ITEM1)
                                        ITEM2 = Items('Health_point.png', BOSS_1.sprite_rect.x + 20, BOSS_1.sprite_rect.y, 2, 30, 30)
                                        ITEM2.image_for_know = 'Health_point.png'
                                        ITEMS.add(ITEM2)
                                        BOSS_1.img = pygame.transform.scale(pygame.image.load('Boss-1.png'), (170, 170))
                                        BOSS_1.img_rect.y -= 300
                                        BOSS_1.img_rect.x = 215
                                        BOSS_1.sprite_rect.center = BOSS_1.img_rect.center
                                        BOSS_1.explosion1_rect.center = BOSS_1.img_rect.center
                                        BOSS_1.explosion2_rect.center = BOSS_1.img_rect.center
                                        BOSS_1.explosion2_rect.x = BOSS_1.img_rect.x
                                        BOSS_1.explosion3_rect.center = BOSS_1.img_rect.center
                                        BOSS_1.explosion3_rect.x = BOSS_1.img_rect.x + 85
                                        boss_wave = False
                                        destroyed = 10
                                        wave_counter += 1
                                        BOSS_1.explosion1_time.x = 0
                                        BOSS_1.explosion2_time.x = 0
                                        BOSS_1.explosion3_time.x = 0
                                        score += 50
                                        a = 1
                                        b = 1
                                        c = 1
                                        BOSS_1.hp = 50
                                        boss_time.x = 0
                                        for ufo in ENEMIES_list:
                                            ufo.bullet_speed += 0.2
                                        random_boss = randint(1, 3)
                                        bosses_destroyed += 1
                                        channel0.play(game_music)
                                        music_play_time = 0
                                        g = 1
            # Босс-2:
            if random_boss == 2:
                if BOSS_2.img_rect.y != 100:
                    BOSS_2.img_rect.y += 2
                    BOSS_2.sprite_rect.center = BOSS_2.img_rect.center
                    BOSS_2.explosion1_rect.center = BOSS_2.img_rect.center
                    BOSS_2.explosion2_rect.center = BOSS_2.img_rect.center
                    BOSS_2.explosion3_rect.center = BOSS_2.img_rect.center
                    BOSS_2.explosion2_rect.x = BOSS_2.img_rect.x
                    BOSS_2.explosion3_rect.x = BOSS_2.img_rect.x + 85
                    BOSS_2.laser_img_rect.center = BOSS_2.sprite_rect.center
                    BOSS_2.laser_img_rect.y += 320
                    BOSS_2.laser_sprite_rect.center = BOSS_2.laser_img_rect.center
                    warning_x += 8
                    if PLAYER.img_rect.x < 200:
                        BOSS_2_attack1 = True
                        BOSS_2_attack2 = False
                        BOSS_2_attack3 = False
                    if PLAYER.img_rect.x >= 200 and PLAYER.img_rect.x <= 400:
                        BOSS_2_attack1 = False
                        BOSS_2_attack2 = True
                        BOSS_2_attack3 = False
                    if PLAYER.img_rect.x > 400:
                        BOSS_2_attack1 = False
                        BOSS_2_attack2 = False
                        BOSS_2_attack3 = True
                else:
                    warning_x = -300
                    if boss_time.x != 50:
                        boss_time.x += 2
                    else:
                        window.blit(boss_text, (255, 5))
                        pygame.draw.rect(window, (0, 0, 0), boss_health_bar1)
                        if BOSS_2.hp >= 1:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp1)
                        if BOSS_2.hp >= 10:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp2)
                        if BOSS_2.hp >= 20:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp3)
                        if BOSS_2.hp >= 30:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp4)
                        if BOSS_2.hp >= 40:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp5)
                        pygame.draw.rect(window, (150, 150, 150), boss_health_bar2, 3)
                        if BOSS_2_attack1:
                            if BOSS_2.img_rect.x != 15:
                                BOSS_2.img_rect.x -= 5
                                BOSS_2.sprite_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion1_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion2_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion3_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion2_rect.x = BOSS_2.img_rect.x
                                BOSS_2.explosion3_rect.x = BOSS_2.img_rect.x + 85
                                BOSS_2.laser_img_rect.center = BOSS_2.sprite_rect.center
                                BOSS_2.laser_img_rect.y += 320
                                BOSS_2.laser_sprite_rect.center = BOSS_2.laser_img_rect.center
                            else:
                                if laser_attack_time.x < 50:
                                    laser_attack_time.x += 1
                                else:
                                    if laser_attack_time.x < 200:
                                        laser_attack = True
                                        laser_attack_time.x += 2
                                    else:
                                        laser_attack_time.x = 0
                                        laser_attack = False
                                        e = 1
                                        BOSS_2_attack1 = False
                                        if PLAYER.img_rect.x < 200:
                                            BOSS_2_attack1 = True
                                            BOSS_2_attack2 = False
                                            BOSS_2_attack3 = False
                                        if PLAYER.img_rect.x >= 200 and PLAYER.img_rect.x <= 400:
                                            BOSS_2_attack1 = False
                                            BOSS_2_attack2 = True
                                            BOSS_2_attack3 = False
                                        if PLAYER.img_rect.x > 400:
                                            BOSS_2_attack1 = False
                                            BOSS_2_attack2 = False
                                            BOSS_2_attack3 = True
                        if BOSS_2_attack2:
                            if BOSS_2.img_rect.x != 215:
                                if BOSS_2.img_rect.x > 215:
                                    BOSS_2.img_rect.x -= 5
                                if BOSS_2.img_rect.x < 215:
                                    BOSS_2.img_rect.x += 5
                                BOSS_2.sprite_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion1_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion2_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion3_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion2_rect.x = BOSS_2.img_rect.x
                                BOSS_2.explosion3_rect.x = BOSS_2.img_rect.x + 85
                                BOSS_2.laser_img_rect.center = BOSS_2.sprite_rect.center
                                BOSS_2.laser_img_rect.y += 320
                                BOSS_2.laser_sprite_rect.center = BOSS_2.laser_img_rect.center
                            else:
                                if laser_attack_time.x < 50:
                                    laser_attack_time.x += 1
                                else:
                                    if laser_attack_time.x < 200:
                                        laser_attack = True
                                        laser_attack_time.x += 2
                                    else:
                                        laser_attack_time.x = 0
                                        laser_attack = False
                                        e = 1
                                        BOSS_2_attack2 = False
                                        if PLAYER.img_rect.x < 200:
                                            BOSS_2_attack1 = True
                                            BOSS_2_attack2 = False
                                            BOSS_2_attack3 = False
                                        if PLAYER.img_rect.x >= 200 and PLAYER.img_rect.x <= 400:
                                            BOSS_2_attack1 = False
                                            BOSS_2_attack2 = True
                                            BOSS_2_attack3 = False
                                        if PLAYER.img_rect.x > 400:
                                            BOSS_2_attack1 = False
                                            BOSS_2_attack2 = False
                                            BOSS_2_attack3 = True
                        if BOSS_2_attack3:
                            if BOSS_2.img_rect.x != 415:
                                BOSS_2.img_rect.x += 5
                                BOSS_2.sprite_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion1_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion2_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion3_rect.center = BOSS_2.img_rect.center
                                BOSS_2.explosion2_rect.x = BOSS_2.img_rect.x
                                BOSS_2.explosion3_rect.x = BOSS_2.img_rect.x + 85
                                BOSS_2.laser_img_rect.center = BOSS_2.sprite_rect.center
                                BOSS_2.laser_img_rect.y += 320
                                BOSS_2.laser_sprite_rect.center = BOSS_2.laser_img_rect.center
                            else:
                                if laser_attack_time.x < 50:
                                    laser_attack_time.x += 1
                                else:
                                    if laser_attack_time.x < 200:
                                        laser_attack = True
                                        laser_attack_time.x += 2
                                    else:
                                        laser_attack_time.x = 0
                                        laser_attack = False
                                        e = 1
                                        BOSS_2_attack3 = False
                                        if PLAYER.img_rect.x < 200:
                                            BOSS_2_attack1 = True
                                            BOSS_2_attack2 = False
                                            BOSS_2_attack3 = False
                                        if PLAYER.img_rect.x >= 200 and PLAYER.img_rect.x <= 400:
                                            BOSS_2_attack1 = False
                                            BOSS_2_attack2 = True
                                            BOSS_2_attack3 = False
                                        if PLAYER.img_rect.x > 400:
                                            BOSS_2_attack1 = False
                                            BOSS_2_attack2 = False
                                            BOSS_2_attack3 = True
                        if a == 1:
                            channel0.play(boss_music)
                            music_play_time = 0
                            BULLET1 = Bullet('Bullet-RED.png', 0, 0, 8, 20, 50, 1)
                            BULLET1.img_rect.center = BOSS_2.img_rect.center
                            BULLET1.img_rect.x -= 75
                            BULLET1.img_rect.y += 60
                            BULLET1.sprite_rect.center = BULLET1.img_rect.center
                            bullets_boss_group.add(BULLET1)
                            BULLET2 = Bullet('Bullet-RED.png', 0, 0, 8, 20, 50, 1)
                            BULLET2.img_rect.center = BOSS_2.img_rect.center
                            BULLET2.img_rect.x += 75
                            BULLET2.img_rect.y += 60
                            BULLET2.sprite_rect.center = BULLET2.img_rect.center
                            bullets_boss_group.add(BULLET2)
                            channel5.play(boss_shoots_sound)
                            a = 0
                        if BOSS_2.hp > 0:
                            shoot = True
                            for bullet in bullets_boss_group:
                                if bullet.hp == 1:
                                    bullet.draw()
                                bullet.img_rect.y += bullet.speed
                                bullet.sprite_rect.center = bullet.img_rect.center
                                if bullet.img_rect.y > 700:
                                    channel5.play(boss_shoots_sound)
                                    bullets_boss_group.empty()
                                    BULLET1 = Bullet('Bullet-RED.png', 0, 0, 8, 20, 50, 1)
                                    BULLET1.img_rect.center = BOSS_2.img_rect.center
                                    BULLET1.img_rect.x -= 75
                                    BULLET1.img_rect.y += 60
                                    BULLET1.sprite_rect.center = BULLET1.img_rect.center
                                    bullets_boss_group.add(BULLET1)
                                    BULLET2 = Bullet('Bullet-RED.png', 0, 0, 8, 20, 50, 1)
                                    BULLET2.img_rect.center = BOSS_2.img_rect.center
                                    BULLET2.img_rect.x += 75
                                    BULLET2.img_rect.y += 60
                                    BULLET2.sprite_rect.center = BULLET2.img_rect.center
                                    bullets_boss_group.add(BULLET2)
                                if bullet.sprite_rect.colliderect(PLAYER.sprite_rect) and bullet.hp == 1:
                                    channel2.play(player_heated_sound)
                                    PLAYER.health -= 1
                                    bullet.hp = 0
                        if BOSS_2.hp < 0:
                            BOSS_2.hp = 0
                        for bullet in BULLETS:
                            if bullet.sprite_rect.colliderect(BOSS_2.sprite_rect):
                                channel3.play(ufo_heated_sound)
                                BOSS_2.hp -= 1
                                BULLETS.remove(bullet)
                        if BOSS_2.sprite_rect.colliderect(PLAYER.sprite_rect):
                            PLAYER.health = 0
                        if PLAYER.sprite_rect.colliderect(BOSS_2.laser_sprite_rect) and laser_attack:
                            channel2.play(player_heated_sound)
                            PLAYER.health -= 1
                        if BOSS_2.hp == 0:
                            shoot = False
                            bullets_boss_group.empty()
                            laser_attack = False
                            BOSS_2_attack1 = False
                            BOSS_2_attack2 = False
                            BOSS_2_attack3 = False
                            if BOSS_2.explosion2_time.x != 150:
                                if b == 1:
                                    BOSS_2.img = pygame.transform.rotate(BOSS_2.img, 5)
                                    b = 0
                                BOSS_2.blow_up2()
                                BOSS_2.explosion2_time.x += 5
                                if f == 1:
                                    channel7.set_volume(1)
                                    channel7.play(boss_small_blowup_sound)
                                    f = 0
                            else:
                                if BOSS_2.explosion3_time.x != 150:
                                    if c == 1:
                                        f = 1
                                        BOSS_2.img = pygame.transform.rotate(BOSS_2.img, -10)
                                        c = 0
                                    BOSS_2.blow_up3()
                                    BOSS_2.explosion3_time.x += 5
                                    if f == 1:
                                        channel7.play(boss_small_blowup_sound)
                                        f = 0
                                else:
                                    if BOSS_2.explosion1_time.x != 200:
                                        BOSS_2.blow_up1()
                                        BOSS_2.explosion1_time.x += 5
                                        if f == 0:
                                            channel7.set_volume(0.4)
                                            channel7.play(boss_big_blowup_sound)
                                            f = 1
                                    else:
                                        ITEM1 = Items('Health_point.png', BOSS_2.sprite_rect.x - 20, BOSS_2.sprite_rect.y - 20, 2, 30, 30)
                                        ITEM1.image_for_know = 'Health_point.png'
                                        ITEMS.add(ITEM1)
                                        ITEM2 = Items('Health_point.png', BOSS_2.sprite_rect.x + 20, BOSS_2.sprite_rect.y, 2, 30, 30)
                                        ITEM2.image_for_know = 'Health_point.png'
                                        ITEMS.add(ITEM2)
                                        BOSS_2.img = pygame.transform.scale(pygame.image.load('Boss-2.png'), (170, 170))
                                        BOSS_2.img_rect.y -= 300
                                        BOSS_2.img_rect.x = 215
                                        BOSS_2.sprite_rect.center = BOSS_2.img_rect.center
                                        BOSS_2.explosion1_rect.center = BOSS_2.img_rect.center
                                        BOSS_2.explosion2_rect.center = BOSS_2.img_rect.center
                                        BOSS_2.explosion2_rect.x = BOSS_2.img_rect.x
                                        BOSS_2.explosion3_rect.center = BOSS_2.img_rect.center
                                        BOSS_2.explosion3_rect.x = BOSS_2.img_rect.x + 85
                                        BOSS_2.laser_img_rect.center = BOSS_2.sprite_rect.center
                                        BOSS_2.laser_img_rect.y += 320
                                        BOSS_2.laser_sprite_rect.center = BOSS_2.laser_img_rect.center
                                        boss_wave = False
                                        destroyed = 10
                                        wave_counter += 1
                                        BOSS_2.explosion1_time.x = 0
                                        BOSS_2.explosion2_time.x = 0
                                        BOSS_2.explosion3_time.x = 0
                                        score += 50
                                        a = 1
                                        b = 1
                                        c = 1
                                        BOSS_2.hp = 50
                                        boss_time.x = 0
                                        for ufo in ENEMIES_list:
                                            ufo.bullet_speed += 0.2
                                        random_boss = randint(1, 3)
                                        bosses_destroyed += 1
                                        channel0.play(game_music)
                                        music_play_time = 0
                                        g = 1
            # Босс-3:
            if random_boss == 3:
                if BOSS_3.img_rect.y != 100:
                    BOSS_3.img_rect.y += 2
                    BOSS_3.sprite_rect.center = BOSS_3.img_rect.center
                    BOSS_3.explosion1_rect.center = BOSS_3.img_rect.center
                    BOSS_3.explosion2_rect.center = BOSS_3.img_rect.center
                    BOSS_3.explosion3_rect.center = BOSS_3.img_rect.center
                    BOSS_3.explosion2_rect.x = BOSS_3.img_rect.x
                    BOSS_3.explosion3_rect.x = BOSS_3.img_rect.x + 85
                    BOSS_3.claw1_img_rect.center = BOSS_3.img_rect.center
                    BOSS_3.claw1_img_rect.x -= 50
                    BOSS_3.claw1_img_rect.y += 30
                    BOSS_3.claw1_sprite_rect.center = BOSS_3.claw1_img_rect.center
                    BOSS_3.claw2_img_rect.center = BOSS_3.img_rect.center
                    BOSS_3.claw2_img_rect.x += 50
                    BOSS_3.claw2_img_rect.y += 25
                    BOSS_3.claw2_sprite_rect.center = BOSS_3.claw2_img_rect.center
                    warning_x += 8
                else:
                    warning_x = -300
                    if boss_time.x != 80:
                        boss_time.x += 2
                        BOSS_3.claw1_img_rect.x -= 10
                        BOSS_3.claw2_img_rect.x += 10
                    else:
                        window.blit(boss_text, (255, 5))
                        pygame.draw.rect(window, (0, 0, 0), boss_health_bar1)
                        if BOSS_3.hp >= 1:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp1)
                        if BOSS_3.hp >= 10:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp2)
                        if BOSS_3.hp >= 20:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp3)
                        if BOSS_3.hp >= 30:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp4)
                        if BOSS_3.hp >= 40:
                            pygame.draw.rect(window, (255, 0, 0), boss_hp5)
                        pygame.draw.rect(window, (150, 150, 150), boss_health_bar2, 3)
                        if BOSS_3.hp >= 0:
                            shoot = True
                        if BOSS_3.img_rect.x == 10 or BOSS_3.img_rect.x == 420:
                            BOSS_3.speed *= -1
                        if BOSS_3.hp > 0:
                            BOSS_3.img_rect.x += BOSS_3.speed
                            BOSS_3.sprite_rect.center = BOSS_3.img_rect.center
                            BOSS_3.explosion1_rect.center = BOSS_3.img_rect.center
                            BOSS_3.explosion2_rect.center = BOSS_3.img_rect.center
                            BOSS_3.explosion3_rect.center = BOSS_3.img_rect.center
                            BOSS_3.explosion2_rect.x = BOSS_3.img_rect.x
                            BOSS_3.explosion3_rect.x = BOSS_3.img_rect.x + 85
                        if BOSS_3.hp < 0:
                            BOSS_3.hp = 0
                        for bullet in BULLETS:
                            if bullet.sprite_rect.colliderect(BOSS_3.sprite_rect):
                                channel3.play(ufo_heated_sound)
                                BOSS_3.hp -= 1
                                BULLETS.remove(bullet)
                        if BOSS_3.sprite_rect.colliderect(PLAYER.sprite_rect):
                            PLAYER.health = 0
                        if a == 1:
                            channel0.play(boss_music)
                            music_play_time = 0
                            BULLET1 = Bullet('Bullet-RED.png', 0, 0, 8, 20, 50, 1)
                            BULLET1.img_rect.center = BOSS_3.img_rect.center
                            BULLET1.img_rect.y += 60
                            BULLET1.sprite_rect.center = BULLET1.img_rect.center
                            bullets_boss_group.add(BULLET1)
                            channel5.play(boss_shoots_sound)
                            a = 0
                        if BOSS_3.hp > 0:
                            shoot = True
                            for bullet in bullets_boss_group:
                                bullet.img_rect.y += bullet.speed
                                bullet.sprite_rect.center = bullet.img_rect.center
                                if bullet.img_rect.y == 603:
                                    channel5.play(boss_shoots_sound)
                                    BULLET = Bullet('Bullet-RED.png', 0, 0, 8, 20, 50, 1)
                                    BULLET.img_rect.center = BOSS_3.img_rect.center
                                    BULLET.img_rect.y += 60
                                    BULLET.sprite_rect.center = BULLET.img_rect.center
                                    bullets_boss_group.add(BULLET)
                                if bullet.sprite_rect.colliderect(PLAYER.sprite_rect) and bullet.hp == 1:
                                    channel2.play(player_heated_sound)
                                    PLAYER.health -= 1
                                    bullet.hp = 0
                            if BOSS_3.claw1_img_rect.y < 300 or BOSS_3.claw1_img_rect.x < -300:
                                BOSS_3.claw1_img_rect.y = choice(claws_random_y)
                                BOSS_3.claw1_img_rect.x = 750
                            BOSS_3.claw1_img_rect.x -= 8
                            BOSS_3.claw1_sprite_rect.center = BOSS_3.claw1_img_rect.center
                            if BOSS_3.claw2_img_rect.y < 300 or BOSS_3.claw2_img_rect.x > 900:
                                BOSS_3.claw2_img_rect.y = choice(claws_random_y)
                                BOSS_3.claw2_img_rect.x = -300
                            BOSS_3.claw2_img_rect.x += 8
                            BOSS_3.claw2_sprite_rect.center = BOSS_3.claw2_img_rect.center
                            for bullet in BULLETS:
                                if bullet.sprite_rect.colliderect(BOSS_3.claw1_sprite_rect) or bullet.sprite_rect.colliderect(BOSS_3.claw2_sprite_rect):
                                    channel3.play(ufo_heated_sound)
                                    BULLETS.remove(bullet)
                            if PLAYER.sprite_rect.colliderect(BOSS_3.claw1_sprite_rect) or PLAYER.sprite_rect.colliderect(BOSS_3.claw2_sprite_rect):
                                channel2.play(player_heated_sound)
                                PLAYER.health -= 1
                        if BOSS_3.hp == 0:
                            shoot = False
                            bullets_boss_group.empty()
                            BOSS_3.claw1_img_rect.x = -500
                            BOSS_3.claw1_sprite_rect.center = BOSS_3.claw1_img_rect.center
                            BOSS_3.claw2_img_rect.x = 1000
                            BOSS_3.claw2_sprite_rect.center = BOSS_3.claw2_img_rect.center
                            if BOSS_3.explosion2_time.x != 150:
                                if b == 1:
                                    BOSS_3.img = pygame.transform.rotate(BOSS_3.img, 5)
                                    b = 0
                                BOSS_3.blow_up2()
                                BOSS_3.explosion2_time.x += 5
                                if f == 1:
                                    channel7.set_volume(1)
                                    channel7.play(boss_small_blowup_sound)
                                    f = 0
                            else:
                                if BOSS_3.explosion3_time.x != 150:
                                    if c == 1:
                                        f = 1
                                        BOSS_3.img = pygame.transform.rotate(BOSS_3.img, -10)
                                        c = 0
                                    BOSS_3.blow_up3()
                                    BOSS_3.explosion3_time.x += 5
                                    if f == 1:
                                        channel7.play(boss_small_blowup_sound)
                                        f = 0
                                else:
                                    if BOSS_3.explosion1_time.x != 200:
                                        BOSS_3.blow_up1()
                                        BOSS_3.explosion1_time.x += 5
                                        if f == 0:
                                            channel7.set_volume(0.4)
                                            channel7.play(boss_big_blowup_sound)
                                            f = 1
                                    else:
                                        ITEM1 = Items('Health_point.png', BOSS_3.sprite_rect.x - 20, BOSS_3.sprite_rect.y - 20, 2, 30, 30)
                                        ITEM1.image_for_know = 'Health_point.png'
                                        ITEMS.add(ITEM1)
                                        ITEM2 = Items('Health_point.png', BOSS_3.sprite_rect.x + 20, BOSS_3.sprite_rect.y, 2, 30, 30)
                                        ITEM2.image_for_know = 'Health_point.png'
                                        ITEMS.add(ITEM2)
                                        BOSS_3.img = pygame.transform.scale(pygame.image.load('Boss-3.png'), (170, 170))
                                        BOSS_3.img_rect.y -= 300
                                        BOSS_3.img_rect.x = 215
                                        BOSS_3.sprite_rect.center = BOSS_3.img_rect.center
                                        BOSS_3.explosion1_rect.center = BOSS_3.img_rect.center
                                        BOSS_3.explosion2_rect.center = BOSS_3.img_rect.center
                                        BOSS_3.explosion3_rect.center = BOSS_3.img_rect.center
                                        BOSS_3.explosion2_rect.x = BOSS_3.img_rect.x
                                        BOSS_3.explosion3_rect.x = BOSS_3.img_rect.x + 85
                                        BOSS_3.claw1_img_rect.center = BOSS_3.img_rect.center
                                        BOSS_3.claw1_img_rect.x -= 50
                                        BOSS_3.claw1_img_rect.y += 30
                                        BOSS_3.claw1_sprite_rect.center = BOSS_3.claw1_img_rect.center
                                        BOSS_3.claw2_img_rect.center = BOSS_3.img_rect.center
                                        BOSS_3.claw2_img_rect.x += 50
                                        BOSS_3.claw2_img_rect.y += 25
                                        BOSS_3.claw2_sprite_rect.center = BOSS_3.claw2_img_rect.center
                                        boss_wave = False
                                        destroyed = 10
                                        wave_counter += 1
                                        BOSS_3.explosion1_time.x = 0
                                        BOSS_3.explosion2_time.x = 0
                                        BOSS_3.explosion3_time.x = 0
                                        score += 50
                                        a = 1
                                        b = 1
                                        c = 1
                                        BOSS_3.hp = 50
                                        boss_time.x = 0
                                        for ufo in ENEMIES_list:
                                            ufo.bullet_speed += 0.2
                                        random_boss = randint(1, 3)
                                        bosses_destroyed += 1
                                        channel0.play(game_music)
                                        music_play_time = 0
                                        g = 1
        # Новая волна:
        if destroyed == 10:
            shoot = False
            if wave_counter % 10 != 0:
                if wave_counter % 5 != 0:
                    for bullet in BULLETS:
                        BULLETS.remove(bullet)
                    for ufo_down in UFO_DOWN:
                        if UFO6.img_rect.y != 175:
                            ufo_down.img_rect.y += 5
                            ufo_down.sprite_rect.center = ufo_down.img_rect.center
                            ENEMIES.add(ufo_down)
                    if UFO6.img_rect.y == 175:
                        UFO6.img_rect.y = UFO10.img_rect.y
                    for ufo_top in UFO_TOP:
                        if UFO6.img_rect.y >= 75 and UFO1.img_rect.y != 75:
                            ufo_top.img_rect.y += 5
                            ufo_top.sprite_rect.center = ufo_top.img_rect.center
                            ENEMIES.add(ufo_top)
                    if UFO1.img_rect.y == 75:
                        UFO1.img_rect.y = UFO5.img_rect.y
                        destroyed = 0
                        shoot = True
                        wave_counter += 1
                        for ufo in ENEMIES:
                            ufo.bullet_return()
                        UFO1_shoot = randint(1, 3)
                        UFO2_shoot = randint(1, 3)
                        UFO3_shoot = randint(1, 3)
                        UFO4_shoot = randint(1, 3)
                        UFO5_shoot = randint(1, 3)
                        UFO6_shoot = randint(1, 3)
                        UFO7_shoot = randint(1, 3)
                        UFO8_shoot = randint(1, 3)
                        UFO9_shoot = randint(1, 3)
                        UFO10_shoot = randint(1, 3)
                        for ufo in ENEMIES:
                            ufo.explosion_rect.y = ufo.img_rect.y
                            ufo.explosion_time.x = 0
                            ufo.random_angle = [0, 90, 180, 270, 360]
                else:
                    asteroid_wave = True
                    shoot = True
            else:
                boss_wave = True
                random_boss = randint(1, 3)

        # Усиления и улучшения:
        for item in ITEMS:
            item.draw()
            item.img_rect.y += item.speed
            item.sprite_rect.center = item.img_rect.center
            if item.sprite_rect.colliderect(PLAYER.sprite_rect):
                if item.image_for_know == 'Health_point.png':
                    channel4.play(health_plus_sound)
                    time_for_text = True
                    PLAYER.health += 1
                    if PLAYER.health > 3:
                        PLAYER.health = 3
                if item.image_for_know == 'Power_point.png':
                    channel4.play(super_power_sound)
                    super_power_time.x = 0
                    power_time = True
                ITEMS.remove(item)
            if item.img_rect.y > 700:
                ITEMS.remove(item)

        if power_time:
            super_power_time.x += 2
            window.blit(super_power_text, (205, 650))
        if super_power_time.x >= 2 and super_power_time.x != 500:
            amount_bullets = 3
        else:
            amount_bullets = 1
            super_power_time.x = 0
            power_time = False

        if time_for_text:
            if text_time.x != 150:
                text_time.x += 2
                window.blit(plus_health_text, (255, 620))
            else:
                text_time.x = 0
                time_for_text = False

        # Тескты и счётчики:
        score_counter = font2.render(str(score), True, (255, 255, 0))
        if score >= 10:
            score_counter_x = 75
        if score >= 100:
            score_counter_x = 64
        if score >= 1000:
            score_counter_x = 53

        if PLAYER.health == 3:
            hp_color = (0, 255, 0)
        if PLAYER.health == 2:
            hp_color = (255, 255, 0)
        if PLAYER.health == 1:
            hp_color = (255, 0, 0)
        if PLAYER.health <= 0:
            PLAYER.health = 0
            hp_color = (255, 255, 255)
        hp_counter = font2.render(str(PLAYER.health), True, hp_color)

        if destroyed == 10:
            wave_counter_x += 8
        else:
            wave_counter_x = -230

        music_play_time += 1
        if music_play_time == 6780 and not boss_wave:
            channel0.play(game_music)
            music_play_time = 0
        if music_play_time == 6780 and boss_wave:
            channel0.play(boss_music)
            music_play_time = 0

        new_time = time()
        if int(new_time) - int(cur_time) == 1:
            time_text = font2.render('• TIME: ' + str(int(new_time - start_time)) + ' sec.', True, (100, 100, 255))
            cur_time = new_time

        your_score = font2.render('• SCORE: ' + str(score), True, (100, 100, 255))

        enemies_destroyed_text = font2.render('• ENEMIES DESTROYED: ' + str(enemies_destroyed), True, (100, 100, 255))

        bosses_destroyed_text = font2.render('• BOSSES DESTROYED: ' + str(bosses_destroyed), True, (100, 100, 255))

        if PLAYER.health == 0:
            channel0.set_volume(0.5)
            channel0.play(player_blowup_sound)
            game_over = True

    # Конец игры:
    if game_over and not start_game:
        PLAYER.blow_up()
        pygame.draw.rect(window, (0, 0, 0), game_over_rect)
        if game_over_rect.y != 0:
            game_over_rect.y += 10
        else:
            pygame.mouse.set_visible(True)
            window.blit(game_over_text, (70, 40))
            window.blit(your_score, (10, 200))
            window.blit(enemies_destroyed_text, (10, 275))
            window.blit(bosses_destroyed_text, (10, 350))
            window.blit(time_text, (10, 425))
            window.blit(button_main1, (225, 600))
            pygame.draw.rect(window, button5_color, button_main2, 5)
            window.blit(main, (246, 615))
            mouse_pos = pygame.mouse.get_pos()
            if button_main2.collidepoint(mouse_pos):
                button5_color = (200, 200, 255)
            else:
                button5_color = (100, 100, 255)

    pygame.display.update()
    clock.tick(60)