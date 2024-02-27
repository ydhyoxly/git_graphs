import pygame

import os
import sys


pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
left, top, cell_size = 0, 0, 0
horizont, vertical = [], []



def open_file():
    global left, top, cell_size, vertical, horizont
    flag = 0
    with open('board.txt', mode='r', encoding='utf8') as f:
        lab = f.readlines()
    for i in range(len(lab)):
        side = lab[i][:-1]
        side = list(side)
        if side == []:
            flag = 1
        elif i == 0:
            left, top, cell_size = map(int, lab[i].split())
        elif not flag:
            horizont.append(side)

        elif flag:
            vertical.append(side)



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image



class Main:
    def __init__(self, screen):

        self.screen = screen
        pygame.display.set_caption('Герой двигается!')
        running = True
        self.draw()
        player = Player()
        sprites = pygame.sprite.Group()
        sprites.add(player)
        self.move_timer = 0

        fps = 60
        clock = pygame.time.Clock()
        self.screen.fill('black')
        pygame.display.set_caption('Лабиринт')
        self.height = 7
        self.move_timer = 0
        self.flag = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.move_timer = 0
                    sprites.update(pygame.key.get_pressed())
            if self.move_timer == fps // 8:
                self.move_timer = 0
                sprites.update(pygame.key.get_pressed())
            self.draw()
            sprites.draw(self.screen)
            pygame.display.flip()
            clock.tick(fps)
            self.move_timer += 1

    def draw(self):
        global left, top, cell_size, vertical, horizont
        self.screen.fill('black')
        for i in range(len(horizont)):
            for j in range(len(horizont[i])):
                if horizont[i][j] == '*':
                    pygame.draw.line(self.screen, 'white',
                                     (left + j * cell_size, top + i * cell_size),
                                     (left + (j + 1) * cell_size, top + i * cell_size), width=2)
            for i in range(len(vertical)):
                for j in range(len(vertical[i])):
                    if vertical[i][j] == '*':
                        pygame.draw.line(self.screen, 'white',
                                         (left + j * cell_size, top + i * cell_size),
                                         (left + j * cell_size, top + (i + 1) * cell_size), width=2)


class Player(pygame.sprite.Sprite):
    global cell_size
    open_file()
    image = load_image("upg_rabbit.png")
    image = pygame.transform.scale(image, (cell_size, cell_size))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 50

    def update(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= cell_size
        if keys[pygame.K_DOWN]:
            self.rect.y += cell_size
        if keys[pygame.K_LEFT]:
            self.rect.x -= cell_size
        if keys[pygame.K_RIGHT]:
            self.rect.x += cell_size

if __name__ == '__main__':
    Main(screen)

