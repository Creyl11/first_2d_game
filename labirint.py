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
    def __init__(self,picture,w,h,x,y,):
        super().__init__()
        self.pic = transform.scale(image.load(picture), (w,h))
        self.rect = self.pic.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.pic,(self.rect.x, self.rect.y))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Player(Pic):
    def __init__(self, picture, w, h, x, y, speed_x, speed_y):
        super().__init__(picture, w, h, x, y)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

ghost = Player('pac-7.png', 80, 80, 250, 400, 0, 0)
wall = Pic('platform_v.png', 30, 160, 330, 350)
wall2 = Pic('platform_v.png', 160, 30, 210, 350)
wall3 = Pic('platform_v.png', 30, 290, 210, 80)
enemy = Player('enemy.png', 80, 80, 225, 240, 10, 0)
star = Pic('star.png', 50, 50, 600, 400)
bullet = Pic('bullets.png', 30, 30, 150, 300)
you_win = Pic('you_win.png', 700, 500, 0, 0)
you_lost = Pic('you_lost.png', 700, 500, 0, 0)
restart = Player('restart.png', 75, 75, 300, 400,0,0)

def game(BACK,GREEN):
    run_game = True
    check_win = ''
    while run_game:
        time.delay(100)
        window.fill(BACK)
        for e in event.get():
            if e.type == QUIT:
                run_game = False
            elif e.type == KEYDOWN:
                if e.key == K_UP:
                    ghost.speed_y = -10
                elif e.key == K_DOWN:
                    ghost.speed_y = 10
                elif e.key == K_RIGHT:
                    ghost.speed_x = 14
                elif e.key == K_LEFT:
                    ghost.speed_x = -14
            elif e.type == KEYUP:
                if e.key == K_UP:
                    ghost.speed_y = 0
                elif e.key == K_DOWN:
                    ghost.speed_y = 0
                elif e.key == K_RIGHT:
                    ghost.speed_x = 0
                elif e.key == K_LEFT:
                    ghost.speed_x = 0
        if enemy.rect.right >= window.get_width():
            enemy.speed_x *= -1
        if enemy.rect.colliderect(wall3.rect):
            enemy.speed_x = 10
        if ghost.rect.colliderect(enemy.rect):
            check_win = 0
            break
        if ghost.rect.colliderect(star.rect):
            check_win = 1
            break
        ghost.reset()
        wall.reset()
        wall2.reset()
        wall3.reset()
        enemy.reset()
        star.reset()
        ghost.update()
        enemy.update()
        display.update()
    x,y = 0,0
    run = True
    window.fill(BACK)
    while run:
        if check_win == 1:
            for p in event.get():
                if p.type == MOUSEBUTTONDOWN and p.button == 1:
                    x, y = p.pos
                elif p.type == QUIT:
                    run = False
            if restart.rect.collidepoint(x,y):
                game(BACK,GREEN)
            you_win.reset()
            restart.reset()
            restart.update()
            display.update()
        elif check_win == 0:
            for z in event.get():
                if z.type == MOUSEBUTTONDOWN and z.button == 1:
                    x, y = z.pos
                elif z.type == QUIT:
                    run = False
            if restart.rect.collidepoint(x,y):
                game(BACK,GREEN)
            restart.reset()
            restart.update()
            you_lost.reset()
            display.update()
        else:
            run = False
    return False
a = game(BACK,GREEN)
while True:
    game(BACK,GREEN)