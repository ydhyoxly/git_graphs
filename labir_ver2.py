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
end = [0, 0]



location = [-1, 0]
directory = ''
flag_run = 0
number = 0
end_game = False
enemy_loc = [0, 0]


def open_file():
    global number
    global cell_size, width, height, board
    board = [[] for _ in range(5)]
    with open('moard_ver2.txt', mode='r', encoding='utf8') as f:
        lab = f.readlines()
    width, height, cell_size = map(int, lab[0].split())
    new = 1
    curr_num = 0
    for i in range(len(lab)):
        ar = True
        if new:
            side = lab[i].split()
            new = 0
        else:

            if lab[i][0] == '*':
                curr_num += 1
                new = 1
                ar = False
            else:
                if i != len(lab) - 1:
                    side = lab[i][:-1].split(';')
                else:
                    side = lab[i].split(';')
                for j in range(len(side)):
                    side[j] = list(map(int, side[j].split(', ')))
        if ar:
            board[curr_num].append(side)



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
        global flag_run, new_game, enemy_loc, end_game

        self.screen = screen
        running = True
        player = Player()
        enemy = Enemy()
        self.sprites = pygame.sprite.Group()
        self.sprites.add(player)
        self.move_timer = 0
        MYEVENTTYPE = pygame.USEREVENT + 1
        start = False
        flag_run = 0

        fps = 60
        clock = pygame.time.Clock()
        self.screen.fill('black')
        pygame.display.set_caption('Лабиринт')
        self.move_timer = 0
        self.flag = False
        while running:
            if end_game:
                enemy.update([0, 0])
                player.update()
                end_game = False

            if flag_run == 0:
                Start(self.screen).draw_screen()
                Start(self.screen).events()
                flag_run = Start(self.screen).get_flag()
                self.screen.fill('black')

            elif flag_run == 3:
                new_game = True
                Levels(self.screen).draw_screen()
                Levels(self.screen).events()
                flag_run = Levels(self.screen).get_flag()

            elif flag_run == 4:
                new_game = True
                Win(self.screen).draw_screen()
                Win(self.screen).events()
                flag_run = Win(self.screen).get_flag()
                start = False

            elif flag_run == 1:
                self.sprites.add(player)
                for event in pygame.event.get():
                    if new_game:
                        pygame.time.set_timer(MYEVENTTYPE, 1000)
                        enemy_loc = [0, 0]
                        self.make_board()
                        new_game = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        self.move_timer = 0
                        player.update(pygame.key.get_pressed())
                        rer = player.get_location()
                        Enemy().update(rer)

                    if event.type == MYEVENTTYPE:
                        start = True
                        self.sprites.add(enemy)
                if start:
                    enemy.move()
                # if self.move_timer == fps // 8:
                #     self.move_timer = 0
                #     sprites.update(pygame.key.get_pressed())
                self.draw_board()
                player.update()
                self.sprites.draw(self.screen)
                pygame.display.flip()
                clock.tick(fps)
                self.move_timer += 1
                flag_run = player.get_flag()

            elif flag_run == 2:
                new_game = True

                EndGame(self.screen).draw_screen()
                EndGame(self.screen).events()
                flag_run = EndGame(self.screen).get_flag()
                start = False



    def make_board(self):
        f = ''
        global width, height, board, walls, end, number
        walls = []
        open_file()
        for i in range(len(board[number][1:])):
            r, b, l, t = True, True, True, True
            for j in range(len(board[number][1:][i])):
                if board[number][1:][i][j][0] == width:
                    end = [i % width + 1, i // width]
                    f = [i, j]
                    r = False


                if board[number][1:][i][j][0] == i % width + 1 and board[number][1:][i][j][1] == i // width:
                    r = False
                elif board[number][1:][i][j][0] == i % width and board[number][1:][i][j][1] == i // width + 1:
                    b = False
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
        self.screen.fill('black')
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
        global new_game, location
        self.image_rabbit = Player.image
        self.rect = self.image_rabbit.get_rect()

        self.rect.x = 10
        self.rect.y = 50
        location = [-1, 0]
        self.start = ''


    def get_location(self):
        global location
        return location

    def get_flag(self):
        global flag_run
        return flag_run



    def update(self, keys=None):
        global width, flag_run, end, new_game, location, end_game
        if end_game:
            self.kill()
        self.start = 'start'
        if new_game:
            location = [-1, 0]
            self.rect.x = 10
            self.rect.y = 50
        if not keys:
            pass
        elif keys[pygame.K_w]:
            if ([location[0], location[1] - 1] in board[number][1:][location[1] * width + location[0]]
                    and location != [-1, 0]):
                location[1] -= 1
                self.rect.y -= cell_size
        elif keys[pygame.K_s]:
            if ([location[0], location[1] + 1] in board[number][1:][location[1] * width + location[0]]
                    and location != [-1, 0]):
                location[1] += 1
                self.rect.y += cell_size
        elif keys[pygame.K_a]:
            if ([location[0] - 1, location[1]] in board[number][1:][location[1] * width + location[0]]
                    and location != [-1, 0]):
                location[0] -= 1
                self.rect.x -= cell_size
        elif keys[pygame.K_d]:
            if location[0] + 1 == end[0] and location[1] == end[1]:
                flag_run = 4
                end_game = True
            elif [location[0] + 1, location[1]] in board[number][1:][location[1] * width + location[0]] \
               or location == [-1, 0]:
                location[0] += 1
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

    def update(self, end):
        global board, path, number, enemy_loc, end_game
        if end_game:
            self.rect.x = 50
            self.rect.y = 50
            enemy_loc = [0, 0]
            self.kill()
        path = []
        self.used = ['' for _ in range(width * height)]
        enemy_loc_1 = enemy_loc[1] * self.width + enemy_loc[0]
        end = end[1] * self.width + end[0]
        queue = collections.deque([enemy_loc_1])
        self.used[enemy_loc_1] = str(enemy_loc_1)
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
        global directory, flag_run, enemy_loc, end_game
        print(path)
        if len(path) == 1:
            pass
            flag_run = 2
            end_game = True
        else:
            r = path[0]
            if enemy_loc == r:
                del path[0]

            elif r[0] == enemy_loc[0] and r[1] == enemy_loc[1] + 1:
                directory = 'down'

            elif r[0] == enemy_loc[0] and r[1] == enemy_loc[1] - 1:
                directory = 'up'

            elif r[0] == enemy_loc[0] + 1 and r[1] == enemy_loc[1]:
                directory = 'right'

            elif r[0] == enemy_loc[0] - 1 and r[1] == enemy_loc[1]:
                directory = 'left'
            if (self.rect.x - self.left) % (self.cell_size) == 0:
                enemy_loc[0] = (self.rect.x - self.left) // (self.cell_size)
            if (self.rect.y - self.top) % (self.cell_size) == 0:
                enemy_loc[1] = (self.rect.y - self.top) // (self.cell_size)
            self.run_cat()

    def run_cat(self):
        if directory == 'right':
            self.rect.x += self.cell_size // 15
        elif directory == 'left':
            self.rect.x -= self.cell_size // 15
        elif directory == 'up':
            self.rect.y -= self.cell_size // 15
        elif directory == 'down':
            self.rect.y += self.cell_size // 15


class Start:
    def __init__(self, screen):
        global flag_run

        self.screen = screen
        self.running = True

    def events(self):
        global flag_run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        text = font.render('Levels', True, 'red')
        self.screen.blit(text, (250, 415))
        pygame.draw.rect(self.screen, 'red', (200, 400, 200, 50), 3)

        # pygame.draw.rect(self.screen, 'red', (350, 400, 200, 50), 3)
        pygame.display.flip()

    def events(self):
        global flag_run
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if 200 <= self.mouse_x <= 400 and 400 <= self.mouse_y <= 450:
                    self.screen.fill('black')

                    flag_run = 3

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
        global flag_run, number, new_game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                for i in range(3):
                    if 50 + i * 200 <= self.mouse_x <= 150 + i * 200 and 275 <= self.mouse_y <= 325:
                        new_game = True
                        flag_run = 1
                        number = i



    def draw_screen(self):
        for i in range(5):
            pygame.draw.rect(self.screen, 'white', (50 + 200 * i, 275, 50, 50), 3)


            font = pygame.font.Font(None, 55)
            text = font.render(str(i + 1), True, 'white')
            self.screen.blit(text, (65 + 200 * i, 280))
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
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                if 200 <= self.mouse_x <= 400 and 400 <= self.mouse_y <= 450:
                    flag_run = 3

    def get_flag(self):
        global flag_run
        return flag_run



if __name__ == '__main__':
    Main(screen)