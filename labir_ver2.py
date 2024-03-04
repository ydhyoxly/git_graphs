import pygame
import collections
import os
import sys

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
left, top, cell_size = 50, 50, 0
width, height = 0, 0
walls = []
board = []
path = ''
directory = ''


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
        enemy = Enemy()
        sprites = pygame.sprite.Group()
        sprites.add(player)
        sprites.add(enemy)
        self.move_timer = 0
        MYEVENTTYPE = pygame.USEREVENT + 1
        start = False
        pygame.time.set_timer(MYEVENTTYPE, 3000)

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
                    player.update(pygame.key.get_pressed())
                    rer = player.get_location()
                    Enemy().update([0, 0], rer)

                if event.type == MYEVENTTYPE:
                    print(start)
                    start = True
            if start:
                enemy.move()
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

    def __init__(self, *group):
        super().__init__(*group)
        self.image_rabbit = Player.image
        self.rect = self.image_rabbit.get_rect()

        self.rect.x = 10
        self.rect.y = 50
        self.location = [-1, 0]
        self.start = ''

    def get_location(self):
        return self.location

    def update(self, keys):
        global width
        self.start = 'start'
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



class Enemy(pygame.sprite.Sprite):
    image = load_image("cat_run_upg.png")
    image = pygame.transform.scale(image, (cell_size, cell_size))

    def __init__(self, *group):
        super().__init__(*group)
        global width, height, left, top, cell_size
        self.width = width
        self.cell_size = cell_size
        self.left, self.top = left, top
        self.image = Enemy.image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.location = [0, 0]
        self.used = ['' for _ in range(width * height)]

    def update(self, location, end):
        global board, path
        self.used = ['' for _ in range(width * height)]
        location = location[1] * self.width + location[0]
        end = end[1] * self.width + end[0]
        queue = collections.deque([location])
        self.used[location] = str(location)
        while queue:
            vertex = queue.popleft()
            for neighbour in board[vertex]:
                if neighbour != [-1, 0]:
                    neighbour = neighbour[1] * self.width + neighbour[0]
                    if self.used[neighbour] == '':
                        self.used[neighbour] = str(self.used[vertex]) + " " + str(neighbour)
                        queue.append(neighbour)

                        if neighbour == end:
                            break
        path = self.used[end]
        path = list(map(int, path.split()))
        for i in range(len(path)):
            path[i] = [path[i] % self.width, path[i] // self.width]

    def move(self):
        global directory
        if len(path) == 1:

            print('end')
        else:
            r = path[1]
            if self.location == r:
                del path[1]

            elif r[0] == self.location[0] and r[1] == self.location[1] + 1:
                directory = 'down'

            elif r[0] == self.location[0] and r[1] == self.location[1] - 1:
                directory = 'up'

            elif r[0] == self.location[0] + 1 and r[1] == self.location[1]:
                directory = 'right'

            elif r[0] == self.location[0] - 1 and r[1] == self.location[1]:
                directory = 'left'

            self.location = [(self.rect.x - self.left) // self.cell_size,
                             (self.rect.y - self.top) // self.cell_size]
            self.run_cat()

    def run_cat(self):
        if directory == 'right':
            self.rect.x += self.cell_size // 20
        elif directory == 'left':
            self.rect.x -= self.cell_size // 20
        elif directory == 'top':
            self.rect.y -= self.cell_size // 20
        elif directory == 'down':
            self.rect.y += self.cell_size // 20






if __name__ == '__main__':
    Main(screen)


