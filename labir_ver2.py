import pygame

import os
import sys

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
left, top, cell_size = 50, 50, 0
width, height = 0, 0
walls = []
board = []


def open_file():
    global cell_size, width, height
    with open('moard_ver2.txt', mode='r', encoding='utf8') as f:
        lab = f.readlines()
    width, height, cell_size = map(int, lab[0].split())
    lab = lab[1:]
    for i in range(len(lab)):
        if i != len(lab) - 1:
            side = lab[i][:-1].split(';')
        else:
            side = lab[i].split(';')
        for j in range(len(side)):
            side[j] = list(map(int, side[j].split(', ')))
        board.append(side)


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
        running = True
        self.make_board()
        self.draw_board()
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
            self.screen.fill('black')
            # if self.move_timer == fps // 8:
            #     self.move_timer = 0
            #     sprites.update(pygame.key.get_pressed())
            sprites.draw(self.screen)
            self.draw_board()
            pygame.display.flip()
            clock.tick(fps)
            self.move_timer += 1

    def make_board(self):
        global width, height, board, walls
        for i in range(len(board)):
            r, b, l, t = True, True, True, True
            for j in range(len(board[i])):

                if board[i][j][0] == i % width and board[i][j][1] == i // width + 1:
                    b = False
                elif board[i][j][0] == i % width + 1 and board[i][j][1] == i // width:
                    r = False
                elif board[i][j][0] == i % width and board[i][j][1] == i // width - 1:
                    t = False
                elif board[i][j][0] == i % width - 1 and board[i][j][1] == i // width:
                    l = False
            print(r, b, l, t)
            walls.append([r, b, l, t])

    def draw_board(self):
        global walls, width, height, left, top, cell_size
        for i in range(len(walls)):
            if walls[i][0]:
                pygame.draw.line(self.screen, 'white', (left + (i % width + 1) * cell_size,
                                top + (i // width) * cell_size), (left + (i % width + 1) * cell_size,
                                                                  top + ((i // width) + 1) * cell_size), 2)
            if walls[i][1]:
                pygame.draw.line(self.screen, 'white', (left + (i % width) * cell_size,
                                                        top + (i // width + 1) * cell_size),
                                 (left + (i % width + 1) * cell_size,
                                  top + ((i // width) + 1) * cell_size), 2)

            if walls[i][2]:
                pygame.draw.line(self.screen, 'white', (left + (i % width) * cell_size,
                                                        top + (i // width) * cell_size),
                                 (left + (i % width) * cell_size,
                                  top + (i // width + 1) * cell_size), 2)

            if walls[i][3]:
                pygame.draw.line(self.screen, 'white', (left + (i % width) * cell_size,
                                                        top + (i // width) * cell_size),
                                 (left + (i % width + 1) * cell_size,
                                  top + (i // width) * cell_size), 2)


class Player(pygame.sprite.Sprite):
    global cell_size
    open_file()
    image = load_image("upg_rabbit.png")
    image = pygame.transform.scale(image, (cell_size, cell_size))
    image_cat = load_image("cat_run.jpg")
    image_cat = pygame.transform.scale(image_cat, (cell_size, cell_size))

    def __init__(self, *group):
        super().__init__(*group)
        self.image_rabbit = Player.image
        self.rect = self.image_rabbit.get_rect()
        self.image_cat = Player.image_cat

        self.rect.x = 10
        self.rect.y = 50
        self.location = [-1, 0]

    def update(self, keys):
        global width
        if keys[pygame.K_UP]:
            if ([self.location[0], self.location[1] - 1] in board[self.location[1] * width + self.location[0]]
                    and self.location != [-1, 0]):
                self.location[1] -= 1
                self.rect.y -= cell_size
        elif keys[pygame.K_DOWN]:
            if ([self.location[0], self.location[1] + 1] in board[self.location[1] * width + self.location[0]]
                    and self.location != [-1, 0]):
                self.location[1] += 1
                self.rect.y += cell_size
        elif keys[pygame.K_LEFT]:
            if ([self.location[0] - 1, self.location[1]] in board[self.location[1] * width + self.location[0]]
                    and self.location != [-1, 0]):
                self.location[0] -= 1
                self.rect.x -= cell_size
        elif keys[pygame.K_RIGHT]:
            if [self.location[0] + 1, self.location[1]] in board[self.location[1] * width + self.location[0]] \
               or self.location == [-1, 0]:
                self.location[0] += 1
                self.rect.x += cell_size

    def chase(self, clock):
        pass

if __name__ == '__main__':
    Main(screen)


