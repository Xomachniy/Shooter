#Создай собственный Шутер!
from pygame import *
from random import randint
init()
mixer.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, playerWidght, playerHeight, playerX, playerY, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (playerWidght, playerHeight))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = playerX
        self.rect.y = playerY
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_d] and self.rect.x <= 635) or (keys[K_RIGHT] and self.rect.x <= 635):
            self.rect.x += self.speed
        if (keys[K_a] and self.rect.x >= 0) or keys[K_LEFT] and (self.rect.x >= 0):
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', 15, 20, self.rect.centerx, self.rect.y, 15)
        Bullets.add(bullet)
        global ammo
        ammo -= 1

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 580:
            self.rect.x = randint(0, 600)
            self.rect.y = -80
            self.speed = randint(1, 7)
            global lost
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -10:
            self.kill()
Bullets = sprite.Group()

UFO = sprite.Group()
for i in range(5):
    Ufo = Enemy('ufo.png', 100, 65, randint(0, 600), -80, randint(1, 7))
    UFO.add(Ufo)

Meteors = sprite.Group()
for m in range(3):
    Meteor = Enemy('asteroid.png', 65, 65, randint(0, 600), -80, randint(2, 5))
    Meteors.add(Meteor)

window = display.set_mode((700, 500))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

ammo = 5
cooldown = 0
cooldownhp = 0
life = 3
kills = 0
lost = 0
fontresult = font.SysFont('Arial', 60)
fontTXT = font.SysFont('Arial', 30)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shoot = mixer.Sound('fire.ogg')

rocket = Player('rocket.png', 65, 100, 335, 400, 5)

clock = time.Clock()
fps = 60

game = True
finish = False
while game == True:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if finish != True:
                    if ammo >= 1:
                        rocket.fire()
                        shoot.play()

    if finish != True:
        window.blit(background, (0, 0))
        Bullets.update()
        for bullet in Bullets:
            bullet.reset()
        rocket.update()
        rocket.reset()
        UFO.update()
        for Ufo in UFO:
            Ufo.reset()
        Meteors.update()
        for Meteor in Meteors:
            Meteor.reset()
        
        colliderufo = sprite.groupcollide(UFO, Bullets, True, True)
        collidermeteor = sprite.groupcollide(Meteors, Bullets, False, True)
        for c in colliderufo:
            kills += 1
            Ufo = Enemy('ufo.png', 100, 65, randint(0, 600), -80, randint(1, 7))
            UFO.add(Ufo)
        if sprite.spritecollide(rocket, UFO, False):
            if life <= 0:
                finish = True
                mixer.music.stop()
                window.blit(fontresult.render('Поражение!',True,(227, 15, 0)), (230, 230))
            elif cooldownhp <= 0:
                life -= 1
                cooldownhp = 30
        if lost >= 10:
            finish = True
            mixer.music.stop()
            window.blit(fontresult.render('Поражение!',True,(227, 15, 0)), (230, 230))
        if kills >= 10:
            finish = True
            mixer.music.stop()
            window.blit(fontresult.render('Победа!',True,(38, 227, 0)), (270, 230))

        if cooldown < 180 and ammo <= 0:
            cooldown += 1
        if ammo <= 0 and cooldown >= 180:
            ammo = 5
            cooldown = 0
        if cooldownhp <= 120:
            cooldownhp -= 1

        window.blit(fontTXT.render('Пропущено: '+str(lost),True,(255, 255, 255)), (0, 0))
        window.blit(fontTXT.render('Убито: '+str(kills),True,(255, 255, 255)), (0, 25))
        window.blit(fontTXT.render('Здоровье: '+str(life),True,(255, 255, 255)), (550, 0))
        window.blit(fontTXT.render('Патроны: '+str(ammo),True,(255, 255, 255)), (0, 470))

        clock.tick(fps)
        display.update()