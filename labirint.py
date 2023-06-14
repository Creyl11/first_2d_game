from pygame import *
from time import sleep
BACK = (128,128,128)
GREEN = (0,255,0)
picture = transform.scale(image.load('galaxy_2.jpg'), (700,500))


window = display.set_mode((700,500))
display.set_caption('Лабиринт')


class Card(sprite.Sprite):
    def __init__(self,width,height,x,y,color):
        super().__init__()
        self.rect = Rect(x,y,width,height)
        self.fill_color = color
    
    def draw(self):
        draw.rect(window, self.fill_color, self.rect)

class Pic(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Enemy(Pic):
    def __init__(self, picture, w, h, x, y, left_b, right_b):
        super().__init__(picture, w, h, x, y)
        self.left_b = left_b
        self.right_b = right_b
        self.speed_x = 10
    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x > self.right_b and self.speed_x == 10:
            self.speed_x *= -1
        elif self.rect.x < self.left_b and self.speed_x == -10:
            self.speed_x *= -1

class Bullet(Pic):
    def __init__(self,picture,x,y):
        super().__init__(picture,20,30,x,y)
        self.speed = 20
        
    def update(self):
        self.rect.x += self.speed

class Player(Pic):
    def __init__(self, picture, w, h, x, y, speed_x, speed_y):
        super().__init__(picture, w, h, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y
        #self.speed = 10

    def update(self):
        if self.speed_x > 0 and self.rect.right < window.get_width()-10:
            self.rect.x += self.speed_x
        if self.speed_x < 0 and self.rect.left > 10:
            self.rect.x += self.speed_x
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_x > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speed_x < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        
        if self.speed_y > 0 and self.rect.bottom < 490:
            self.rect.y += self.speed_y
        if self.speed_y < 0 and self.rect.top > 10:
            self.rect.y += self.speed_y

        '''keys = key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed
        if keys[K_DOWN] or keys[K_s]:
            self.rect.y += self.speed
        if keys[K_UP] or keys[K_w]:
            self.rect.y -= self.speed'''
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_y > 0:
            for p in platforms_touched:
                self.speed_y = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.speed_y < 0:
            for p in platforms_touched:
                self.speed_y = 0
                if p.rect.bottom > self.rect.top:
                    self.rect.top = p.rect.bottom
    def fire(self):
        bullet = Bullet('bullets.png', self.rect.x, self.rect.centery)
        bullets.add(bullet)


bullets = sprite.Group()             
ghost = Player('pac-7.png', 80, 80, 250, 400, 0, 0)
wall = Pic('platform_v.png', 30, 130, 360, 350)
wall2 = Pic('platform_v.png', 160, 30, 230, 317)
wall3 = Pic('platform_v.png', 30, 230, 225, 100)
enemy = Enemy('enemy.png', 80, 80, 250, 235, wall3.rect.left + 20, 620)
enemy2 = Enemy('enemy.png', 80, 80, 570, 100, wall3.rect.left + 20, 620)
star = Pic('star.png', 50, 50, 600, 400)
you_win = Pic('you_win.png', 700, 500, 0, 0)
you_lost = Pic('you_lost.png', 700, 500, 0, 0)
restart = Player('restart.png', 75, 75, 300, 400,0,0)

barriers = sprite.Group()
barriers.add(wall)
barriers.add(wall2)
barriers.add(wall3)


enemies = sprite.Group()
enemies.add(enemy)
enemies.add(enemy2)

def start_pos():
    ghost.rect.x, ghost.rect.y = 250, 400

def enemies_start_pos():
    enemy.rect.x, enemy.rect.y = 250, 235
    enemy2.rect.x, enemy2.rect.y = 570, 100

def update_sprites():
    ghost.reset()
    bullets.update()
    bullets.draw(window)
    barriers.draw(window)
    star.reset()
    ghost.update()
    enemies.update()
    enemies.draw(window)
    display.update()

def key_up_action(e):
    if e.key == K_UP:
        ghost.speed_y = 0
    elif e.key == K_DOWN:
        ghost.speed_y = 0
    elif e.key == K_RIGHT:
        ghost.speed_x = 0
    elif e.key == K_LEFT:
      ghost.speed_x = 0

def key_down_action(e):
    if e.key == K_UP:
        ghost.speed_y = -10
    elif e.key == K_DOWN:
        ghost.speed_y = 10
    elif e.key == K_RIGHT:
        ghost.speed_x = 14
    elif e.key == K_LEFT:
        ghost.speed_x = -14
    elif e.key == K_SPACE:
        ghost.fire()

def game(BACK,GREEN):
    run_game = True
    run = False 
    check_win = ''
    while run_game:
        time.delay(100)
        if run:
            if check_win == 1:
                for p in event.get():
                    if p.type == MOUSEBUTTONDOWN and p.button == 1:
                        x, y = p.pos
                        if restart.rect.collidepoint(x,y):
                            enemies_start_pos()
                            start_pos()
                            run = False
                    elif p.type == QUIT:
                        exit()
                you_win.reset()
                restart.reset()
                restart.update()
                display.update()
            elif check_win == 0:
                for z in event.get():
                    if z.type == MOUSEBUTTONDOWN and z.button == 1:
                        x, y = z.pos
                        if restart.rect.collidepoint(x,y):
                            enemies_start_pos()
                            start_pos()
                            run = False
                    elif z.type == QUIT:
                        exit()
                you_lost.reset()
                restart.reset()
                restart.update()
                display.update()
        else:
            window.fill(BACK)
            for e in event.get():
                if e.type == QUIT:
                    exit()
                elif e.type == KEYDOWN:
                    key_down_action(e)
                elif e.type == KEYUP:
                    key_up_action(e)
            if sprite.spritecollide(ghost, enemies, False):
                check_win = 0
                run = True
            sprite.groupcollide(bullets,barriers,True,False)
            sprite.groupcollide(bullets,enemies,True,True)
            if ghost.rect.colliderect(star.rect):
                check_win = 1
                run = True
            update_sprites()
    x,y = 0,0
    window.fill(BACK)
    return False
game(BACK,GREEN)
