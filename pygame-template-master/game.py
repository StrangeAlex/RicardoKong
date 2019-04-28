import pygame as pg
from settings import *
from objects import *

"""
Основной класс игры
Состояние игры описывается двумя функциями: running и playing. Если игра
running, то это означает, что приложение работает и игрок будет начинать новую
игру - new() снова и снова. Если игра playing, то в данный момент крутится основной игровой
цикл run() - это происходит внутри new()
"""

class Game:
    """
    Инициализируем pygame, создаем дисплей, название игры, часы и задаем изнчальное
    состояние игры: running = True, загружаем шрифт
    """
    def __init__(self):
        pg.init()
        self.canvas = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Random game")
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.BG = pg.image.load("img\\bg.png")
        self.BG = pg.transform.scale(self.BG, (720, 480))

    """
    В этом методе реализуется логика новый игры, обнуляем счет, задаем начальные
    положения врагов, игрока и др.
    """
    def new(self):
        self.bullets = pg.sprite.Group()
        self.player = Player()
        self.weapons = []
        self.weapons.append(Weapon(5, 1000, 10, "pistol"))
        self.player.weapon = self.weapons[0]
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.enemies.add(Enemy())
        self.enemy_spawn_time = 2000
        self.enemy_counter = 1
        pg.time.set_timer(SPAWN_ENEMY, self.enemy_spawn_time)
        self.create_level()
        self.playing = True
        while self.playing:
            self.run()

    """
    Основная функция, в которой реализуется цикл анимации:
    1.Проверяем события
    2.Обновляем положение игровых объектов
    3.Закрашиваем экран цветом заднего фона
    4.Отрисовываем объекты заново
    """
    def run(self):
        self.clock.tick(60)
        self.events()
        self.update()
        self.fill()
        self.draw()

    """
    В этой функции проверям события, проверяем не закрыл ли игрок окно
    """
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == SHOT_FIRED:
                self.on_shot_fired()
            if event.type == SPAWN_ENEMY:
                if self.enemy_counter % 10 == 0 and self.enemy_spawn_time > 500:
                    pg.time.set_timer(SPAWN_ENEMY, 0)
                    self.enemy_spawn_time -= 500
                    pg.time.set_timer(SPAWN_ENEMY, self.enemy_spawn_time)
                self.enemies.add(Enemy())
                self.enemy_counter += 1
    """
    Обновляем положение игровых объеков
    """
    def update(self):
        self.bullets.update()
        self.player.update()
        self.platforms.update()
        self.enemies.update()
        self.check_collision()
    """
    Закрашиваем экран цветом фона
    """
    def fill(self):
        self.canvas.blit(self.BG, (0, 0))

    """
    Отрисовываем положение объектов заново
    """
    def draw(self):
        self.player.draw(self.canvas)
        self.platforms.draw(self.canvas)
        self.enemies.draw(self.canvas)
        self.bullets.draw(self.canvas)
        pg.display.flip()
    """
    Вспомогательная функция для отрисовки текста
    """
    def draw_text(self, text, size, text_color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.rendern(text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.canvas.blit(text_surface, text_rect)

    def check_collision(self):
        if self.player.rect.bottom > HEIGHT:
            self.player.rect.bottom = 0
            self.player.rect.right = WIDTH / 2
        for platform in self.platforms:
            if pg.sprite.collide_rect(self.player, platform):
                if self.player.rect.top < platform.rect.bottom and self.player.rect.top > platform.rect.top and platform.type == "platform":
                    self.player.rect.top = platform.rect.bottom
                    self.player.vel_y *= -1
                elif self.player.rect.bottom >= platform.rect.top and self.player.rect.top <= platform.rect.bottom and platform.type == "platform":
                    self.player.rect.bottom = platform.rect.top
                    self.player.vel_y = 0
                    self.player.jump_counter = 2
                    self.player.can_jump = True
                elif self.player.rect.right > platform.rect.left and self.player.rect.left < platform.rect.left and platform.type == "platform":
                    self.player.rect.right = platform.rect.left
                elif self.player.rect.left < platform.rect.right and self.player.rect.right > platform.rect.right and platform.type == "platform":
                    self.player.rect.left = platform.rect.right
                if self.player.rect.right >= platform.rect.left and self.player.rect.right <= platform.rect.right and platform.type == "wall":
                    self.player.rect.right = platform.rect.left
                if self.player.rect.left <= platform.rect.right and self.player.rect.left >= platform.rect.left and platform.type == "wall":
                    self.player.rect.left = platform.rect.right
            for enemy in self.enemies:
                if pg.sprite.collide_rect(enemy, self.player):
                    self.playing = False
                if pg.sprite.collide_rect(platform, enemy):
                    if enemy.rect.top < platform.rect.bottom and enemy.rect.top > platform.rect.top and platform.type == "platform":
                        enemy.rect.top = platform.rect.bottom
                        enemy.vel_y *= -1
                    elif enemy.rect.bottom >= platform.rect.top and enemy.rect.top <= platform.rect.bottom and platform.type == "platform":
                        enemy.rect.bottom = platform.rect.top
                        enemy.vel_y = 0
                        enemy.jump_counter = 2
                        enemy.can_jump = True
                    elif enemy.rect.right > platform.rect.left and enemy.rect.left < platform.rect.left and platform.type == "platform":
                        enemy.rect.right = platform.rect.left
                        enemy.direction *= -1
                    elif enemy.rect.left < platform.rect.right and enemy.rect.right > platform.rect.right and platform.type == "platform":
                        enemy.rect.left = platform.rect.right
                        enemy.direction *= -1
                    if enemy.rect.right >= platform.rect.left and enemy.rect.right <= platform.rect.right and platform.type == "wall":
                        enemy.rect.right = platform.rect.left
                        enemy.direction *= -1
                    if enemy.rect.left <= platform.rect.right and enemy.rect.left >= platform.rect.left and platform.type == "wall":
                        enemy.rect.left = platform.rect.right
                        enemy.direction *= -1
    def create_level(self):
        self.platforms.add(Platform("img\\bigplatform.png", WIDTH/2, HEIGHT/4, "platform"))
        self.platforms.add(Platform("img\\bigplatform.png", WIDTH/2, 330, "platform"))
        self.platforms.add(Platform("img\\smallplatform.png", 80, HEIGHT/2, "platform"))
        self.platforms.add(Platform("img\\smallplatform.png", WIDTH - 80, HEIGHT/2, "platform"))
        self.platforms.add(Platform("img\\rightwall.png", 10, HEIGHT/2, "wall"))
        self.platforms.add(Platform("img\\leftwall.png", WIDTH - 10, HEIGHT/2, "wall"))
        self.platforms.add(Platform("img\\bigplatform.png", 130, HEIGHT - 15, "platform"))
        self.platforms.add(Platform("img\\bigplatform.png", WIDTH - 130, HEIGHT - 15, "platform"))
        self.platforms.add(Platform("img\\bigplatform.png", 140, 15, "platform"))
        self.platforms.add(Platform("img\\bigplatform.png", WIDTH - 140, 15, "platform"))

    def on_shot_fired(self):
        self.bullets.add(Bullet(self.player.rect.centerx, self.player.rect.centery, self.player.direction, 0, self.player.weapon))

game = Game()
while game.running:
    game.new()
pg.quit()
