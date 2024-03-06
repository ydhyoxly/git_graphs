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
board = [[] for i in range(5)]
path = ''
end = []
directory = ''
flag_run = 0
number = 0


def open_file():
    global number
    global cell_size, width, height
    with open('moard_ver2.txt', mode='r', encoding='utf8') as f:
        lab = f.readlines()
    width, height, cell_size = map(int, lab[0].split())
    new = 1
    for i in range(len(lab)):
        if new:
            side = lab[i].split()
            new = 0
        else:

            if lab[i][0] == '*':
                number += 1
                new = 1
            else:
                if i != len(lab) - 1:
                    side = lab[i][:-1].split(';')
                else:
                    side = lab[i].split(';')
                for j in range(len(side)):
                    side[j] = list(map(int, side[j].split(', ')))
        board[number].append(side)
    print(board[0])
    number = 0


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
        global flag_run

        self.screen = screen
        running = True
        player = Player()
        enemy = Enemy()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(player)
        self.sprites.add(enemy)
        self.move_timer = 0
        MYEVENTTYPE = pygame.USEREVENT + 1
        start = False
        flag_run = 0
        pygame.time.set_timer(MYEVENTTYPE, 3000)

        fps = 60
        clock = pygame.time.Clock()
        self.screen.fill('black')
        pygame.display.set_caption('Лабиринт')
        self.move_timer = 0
        self.flag = False
        self.make_board()
        while running:
            if flag_run == 0:
                Start(self.screen).draw_screen()
                Start(self.screen).events()
                flag_run = Start(self.screen).get_flag()
                self.screen.fill('black')
            elif flag_run == 3:
                Levels(self.screen).draw_screen()
                Levels(self.screen).events()
                flag_run = Levels(self.screen).get_flag()

            elif flag_run == 4:
                    Win(self.screen).draw_screen()
                    Win(self.screen).events()
                    flag_run = Win(self.screen).get_flag()

            elif flag_run == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        self.move_timer = 0
                        player.update(pygame.key.get_pressed())
                        rer = player.get_location()
                        Enemy().update([0, 0], rer)

                    # if event.type == MYEVENTTYPE:
                    #     start = True
                if start:
                    enemy.move()
                # if self.move_timer == fps // 8:
                #     self.move_timer = 0
                #     sprites.update(pygame.key.get_pressed())
                self.draw_screen()
                pygame.display.flip()
                clock.tick(fps)
                self.move_timer += 1
                flag_run = player.get_flag()
            elif flag_run == 2:
                EndGame(self.screen).draw_screen()
                EndGame(self.screen).events()
                flag_run = EndGame(self.screen).get_flag()


    def make_board(self):
        global width, height, board, walls, end, number
        for i in range(len(board[number][1:])):
            r, b, l, t = True, True, True, True
            for j in range(len(board[number][1:][i])):
                print(i, j, board[number][1:][i][j])
                if board[number][1:][i][j][0] == width:
                    end = [i % width + 1, i // width]
                    f = [i, j]

                if board[number][1:][i][j][0] == i % width and board[number][1:][i][j][1] == i // width + 1:
                    b = False
                elif board[number][1:][i][j][0] == i % width + 1 and board[number][1:][i][j][1] == i // width:
                    r = False
                elif board[number][1:][i][j][0] == i % width and board[number][1:][i][j][1] == i // width - 1:
                    t = False
                elif board[number][1:][i][j][0] == i % width - 1 and board[number][1:][i][j][1] == i // width:
                    l = False
            walls.append([r, b, l, t])
        del board[number][1:][f[0]][f[1]]

    def draw_screen(self):
        self.screen.fill('black')
        self.sprites.draw(self.screen)
        self.draw_board()

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

    def get_flag(self):
        global flag_run
        return flag_run

    def update(self, keys):
        global width, flag_run, end
        self.start = 'start'
        if keys[pygame.K_UP]:
            if ([self.location[0], self.location[1] - 1] in board[number][1:][self.location[1] * width + self.location[0]]
                    and self.location != [-1, 0]):
                self.location[1] -= 1
                self.rect.y -= cell_size
        elif keys[pygame.K_DOWN]:
            if ([self.location[0], self.location[1] + 1] in board[number][1:][self.location[1] * width + self.location[0]]
                    and self.location != [-1, 0]):
                self.location[1] += 1
                self.rect.y += cell_size
        elif keys[pygame.K_LEFT]:
            if ([self.location[0] - 1, self.location[1]] in board[number][1:][self.location[1] * width + self.location[0]]
                    and self.location != [-1, 0]):
                self.location[0] -= 1
                self.rect.x -= cell_size
        elif keys[pygame.K_RIGHT]:
            if self.location[0] + 1 == end[0] and self.location[1] == end[1]:
                flag_run = 4
            elif [self.location[0] + 1, self.location[1]] in board[number][1:][self.location[1] * width + self.location[0]] \
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
            for neighbour in board[number][1:][vertex]:
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
        global directory, flag_run
        if len(path) == 1:
            flag_run = 2
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
            self.location = [(self.rect.x - self.left) // (self.cell_size),
                             (self.rect.centery - self.top) // (self.cell_size)]
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

class Start:
    def __init__(self, screen):
        global flag_run

        self.screen = screen
        self.running = True

    def events(self):
        global flag_run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if 169 <= self.mouse_x <= 411 and 278 <= self.mouse_y <= 322:
                    flag_run = 3

            pygame.display.flip()

    def get_flag(self):
        global flag_run

        return flag_run

    def draw_screen(self):
        words = "Start Game"

        font = pygame.font.Font(None, 64)
        text = font.render(words, True, (255, 255, 255))
        w = text.get_rect().width
        h = text.get_rect().height
        self.screen.blit(text, (300 - w // 2, 300 - h // 2))
        pygame.draw.rect(self.screen, 'white', (300 - w // 2 - 10, 300 - h // 2 - 10, w + 20, h + 20), 4)


class EndGame:
    def __init__(self, screen):
        self.screen = screen

    def draw_screen(self):
        font = pygame.font.Font(None, 70)
        self.screen.fill('black')

        text = font.render('GAME OVER', True, 'red')
        w = text.get_rect().width
        h = text.get_rect().height
        self.screen.blit(text, (300 - w // 2, 300 - h // 2))
        font = pygame.font.Font(None, 36)
        text = font.render('Try again', True, 'red')
        self.screen.blit(text, (120, 415))
        text = font.render('Levels', True, 'red')
        self.screen.blit(text, (380, 415))
        pygame.draw.rect(self.screen, 'red', (100, 400, 150, 50), 3)
        pygame.draw.rect(self.screen, 'red', (350, 400, 150, 50), 3)
        pygame.display.flip()

    def events(self):
        global flag_run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if 100 <= self.mouse_x <= 250 and 400 <= self.mouse_y <= 450:
                    flag_run = 1

    def get_flag(self):
        global flag_run
        return flag_run

class Levels:
    def __init__(self, screen):
        self.screen = screen

    def get_flag(self):
        global flag_run
        return flag_run
    def events(self):
        global flag_run, number

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                for i in range(5):
                    if 50 + i * 100 <= self.mouse_x <= 150 + i * 50 and 275 <= self.mouse_y <= 325:
                        flag_run = 1
                        number = i



    def draw_screen(self):
        for i in range(5):
            pygame.draw.rect(self.screen, 'white', (50 + 100 * i, 275, 50, 50), 3)


            font = pygame.font.Font(None, 55)
            text = font.render(str(i + 1), True, 'white')
            self.screen.blit(text, (60 + 100 * i, 280))
            pygame.display.flip()


class Win:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill('black')

    def draw_screen(self):
        font = pygame.font.Font(None, 56)
        text = font.render('You won!', True, 'yellow')
        w = text.get_rect().width
        h = text.get_rect().height

        self.screen.blit(text, (300 - w // 2, 250 - h // 2))
        pygame.draw.rect(self.screen, 'yellow', (200, 400, 200, 50), 3)
        font = pygame.font.Font(None, 40)
        text = font.render('Levels', True, 'yellow')
        self.screen.blit(text, (245, 415))
        pygame.display.flip()

    def events(self):
        global flag_run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if 200 <= self.mouse_x <= 400 and 400 <= self.mouse_y <= 450:
                    flag_run = 3
                # if 50 + i * 100 <= self.mouse_x <= 150 + i * 50 and 275 <= self.mouse_y <= 325:

    def get_flag(self):
        global flag_run
        return flag_run



if __name__ == '__main__':
    Main(screen)



