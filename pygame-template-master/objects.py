import pygame as pg
import random
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self):
        self.direction = 1
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\sprites\\player.gif")
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2
        self.vel_x = 0
        self.vel_y = 0
        self.jump_counter = 2
        self.can_jump = False
        self.reload_ticks = 0
        self.can_shoot = True

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel_x = -SPEED
            self.direction = -1
        if keys[pg.K_RIGHT]:
            self.vel_x = SPEED
            self.direction = 1
        if keys[pg.K_UP] and self.can_jump and self.jump_counter > 0:
            self.vel_y -= PLAYER_JUMP
            self.can_jump = False
            self.jump_counter -= 1
        if not keys[pg.K_UP]:
            self.can_jump = True
        self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_x = 0
        if keys[pg.K_SPACE]:
            event = pg.event.Event(SHOT_FIRED)
            pg.event.post(event)
            self.reload_ticks = pg.time.get_ticks()
            self.can_shoot = False
        if pg.time.get_ticks() - self.reload_ticks > self.weapon.reload_time:
            self.can_shoot = True

    def draw(self, canvas):
        canvas.blit(self.image, self.rect)

class Platform(pg.sprite.Sprite):
    def __init__(self, img_path, x, y, type):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.type = type

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        type = random.choice([True, False])
        self.speedIsNotIncreased = True
        if type:
            self.image = pg.image.load("img\\sprites\\gnome.png")
            self.image = pg.transform.scale(self.image, (45, 45))
            self.hp = 30
            self.speed = random.choice([4, 6])
        else:
            self.image = pg.image.load("img\\sprites\\ricardo.png")
            self.image = pg.transform.scale(self.image, (75, 75))
            self.hp = random.choice([60, 100])
            self.speed = random.choice([2, 3])
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, 30)
        self.direction = random.choice([-1, 1])
        self.vel_y = 0
    def update(self):
        self.vel_y += GRAVITY
        self.rect.x += self.speed * self.direction
        self.rect.y += self.vel_y
        if self.rect.bottom > HEIGHT:
            self.rect.top = 30
            if self.speedIsNotIncreased == True:
                self.speed *= 1.2
                self.speedIsNotIncreased = False

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, dir_x, dir_y, weapon):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img\\smallbullet.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.speed = weapon.bullet_speed
        self.damage = weapon.damage
    def update(self):
        self.rect.x += self.speed * self.dir_x
        self.rect.y += self.speed * self.dir_y

class Weapon:
    def __init__(self, bullet_speed, reload_time, damage, name):
        self.bullet_speed = bullet_speed
        self.reload_time = reload_time
        self.damage = damage
        self.name = name
