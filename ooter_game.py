#Создай собственный Шутер!

from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption('Шутер')
clock = time.Clock()
score_n = 0
skip_n = 0

class GameSprite(sprite.Sprite):
    def __init__(self, name_image, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(name_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 15, 20, 4)
        bullets.add(bullet)

class Enemy(GameSprite):
    def auto_move(self):
        global skip_n
        if self.rect.y < 510:
            self.rect.y += self.speed
        elif self.rect.y > 509:
            self.rect.y = 0
            self.rect.x = randint(0, 600)
            skip_n += 1

class Bullet(GameSprite):
    def bullet_move(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

font.init()
white = (255, 255, 255)
score = font.Font(None, 40).render('Счет:', True, white)
skip = font.Font(None, 40).render('Пропущенно:', True, white)
lose = font.Font(None, 70).render('You lose!', True, (250, 0, 0))
win = font.Font(None, 70).render('You win!', True, (0, 255, 0))
galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))
player = Player('rocket.png', 350, 400, 70, 100, 5)
enemy = sprite.Group()
for i in range(5):
    ufo = Enemy('ufo.png', randint(0, 600), 0, 85, 55, randint(1, 2))
    enemy.add(ufo)
run = True
finish = False
fire = False
bullets = sprite.Group()
while run == True:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    player.fire()
    if finish != True:
        score_t = font.Font(None, 40).render(str(score_n), True, white)
        skip_t = font.Font(None, 40).render(str(skip_n), True, white)
        window.blit(galaxy, (0, 0))
        player.reset()
        player.move()
        window.blit(score, (10, 25))
        window.blit(skip, (10, 60))
        window.blit(score_t, (95, 25))
        window.blit(skip_t, (210, 60))
        for i in enemy:
            i.reset()
            i.auto_move()
        for i in bullets:
            i.reset()
            i.bullet_move()
        colides = sprite.groupcollide(bullets, enemy, True, True)
        for i in colides:
            ufo = Enemy('ufo.png', randint(0, 600), 0, 85, 55, randint(1, 3))
            enemy.add(ufo)
            score_n += 1
        if score_n >= 10:
            window.blit(win, (250, 250))
            finish = True
        if skip_n >= 3:
            window.blit(lose, (250, 250))
            finish = True
    display.update()
    clock.tick(60)