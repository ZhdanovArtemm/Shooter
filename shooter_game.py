from pygame import *
from random import *
from time import time as timer



init()
window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))


player_speed = 3.5
player_x = 325
player_y = 425
window.blit(background, (0, 0))
lost = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()


        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 0, 40, 60)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 530:
            self.rect.y = -70
            self.rect.x = randint(30, 660)
            self.speed = randint(1, 2)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= 7
        if self.rect.y <= -5:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 530:
            self.rect.y = -70
            self.rect.x = randint(30, 660)
            self.speed = randint(1, 2)
            

hero = Player("rocket.png", player_x, player_y, player_speed, 60, 60)
villian1 = Enemy("ufo.png", randint(30, 660), -70, randint(1, 2), 65, 50 )
villian2 = Enemy("ufo.png", randint(30, 660), -70, randint(1, 2), 65, 50 )
villian3 = Enemy("ufo.png", randint(30, 660), -70, randint(1, 2), 65, 50 )
villian4 = Enemy("ufo.png", randint(30, 660), -70, randint(1, 2), 65, 50 )
villian5 = Enemy("ufo.png", randint(30, 660), -70, randint(1, 2), 65, 50 )
villians = sprite.Group()
bullets = sprite.Group()
villians.add(villian1)
villians.add(villian2)
villians.add(villian3)
villians.add(villian4)
villians.add(villian5)
asteroid1 = Asteroid("asteroid.png", randint(30, 660), -70, randint(1, 2), 65, 50)
asteroid2 = Asteroid("asteroid.png", randint(30, 660), -70, randint(1, 2), 65, 50)
asteroid3 = Asteroid("asteroid.png", randint(30, 660), -70, randint(1, 2), 65, 50)
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
mixer.music.set_volume(1)
FPS = 240
clock = time.Clock()
game = True
font1 = font.SysFont("Arial", 36)
num_kill = 0
finish = False
lifes = 3
#! text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
#? еще один коментарий
#* еще один коментарий 2
#todo text_win = font1.render("Счет: " + str(win), 1, (255, 255,255))
win = font1.render("Победа", 1, (255, 255,255))
lose = font1.render("Проигрыш", 1, (255, 255,255))
num_fire = 0
reload_time = False
perezaradka = font1.render("Перезарядка", 1, (255, 255,255))
while game:
    if finish != True:


        window.blit(background, (0, 0))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_win = font1.render("Счет: " + str(num_kill), 1, (255, 255,255))
        text_lifes = font1.render("Жизни: " + str(lifes), 1, (255, 255,255))
        window.blit(text_lose, (20, 35))
        window.blit(text_win, (20, 7))
        window.blit(text_lifes, (20, 62))

        villians.draw(window)
        villians.update()
        asteroids.draw(window)
        asteroids.update()
        hero.reset()
        hero.update()
        bullets.draw(window)
        bullets.update()
        if reload_time == True:
            now_time = timer()
            if now_time - last_time <= 2:
               window.blit(perezaradka, (200, 250)) 
            else:
                num_fire = 0
                reload_time = False    

        sprites_list = sprite.groupcollide(villians, bullets, True, True)
        asteroids_list = sprite.spritecollide(hero, asteroids, True)
        
        for villian in sprites_list:
            num_kill += 1
            ufo = Enemy("ufo.png", randint(30, 660), -70, randint(1, 2), 65, 50 )  
            villians.add(ufo)
        for asteroid in asteroids_list:
            lifes -= 1
            asteroid = Asteroid("asteroid.png", randint(30, 660), -70, randint(1, 2), 65, 50 )
            asteroids.add(asteroid)
        if lifes <= 0:
            finish = True
            window.blit(lose, (200, 200))
            mixer.music.stop()
           

        if num_kill >= 15:
            window.blit(win, (200, 200))
            finish = True
            mixer.music.stop()
     
        
        if lost >= 5:
            finish = True
            window.blit(lose, (200, 200))
            mixer.music.stop()
      

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 7 and reload_time == False:
                    hero.fire()
                    fire.play()
                    num_fire += 1
                if num_fire >= 7 and reload_time == False:
                    reload_time = True
                    last_time = timer()


                

    clock.tick(FPS)
    display.update()