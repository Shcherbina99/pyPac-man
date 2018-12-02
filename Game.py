import sys

import pygame

from Ghost import *
from Player import *


class CellChars(enum.Enum):
    """Текстовое представление клеток поля"""
    EMPTY = ' '
    WALL = '#'
    GHOST = 'G'
    PLAYER = 'P'
    POINT = '*'
    POWERPOINT = '0'


cellSize = 40
walkRight = [pygame.image.load('image/walkR2.png'), pygame.image.load('image/walkR3.png'),
             pygame.image.load('image/walkR2.png'), pygame.image.load('image/walkR1.png')]
noWalk = pygame.image.load("image/walkR2.png")
point = pygame.image.load("image/Point.png")


class Game:
    def __init__(self, name, frame_rate=10):
        self.countLife = 3
        self.score = 0
        self.ghosts = []
        self.chekings = []
        self.walls = []
        self.game_over = False
        self.speed = 1
        pygame.init()
        pygame.font.init()
        self.frame_rate = frame_rate
        self.background = pygame.image.load("image/bg.png")

        if name == "Test":
            cells = Test
        elif name == "Test1":
            cells = Test1
        else:
            AttributeError()
        self.height = len(cells)
        self.width = len(cells[0])

        self.cells = []
        for i in range(self.height):
            self.cells.append([])
            for j in range(self.width):
                self.cells[i].append(CellChars.EMPTY)

        self.surface = pygame.display.set_mode((self.width * cellSize, self.height * cellSize))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()

        for y in range(self.height):
            for x in range(self.width):
                if cells[y][x] == "P":
                    self.cells[y][x] = CellChars.PLAYER
                    self.player = Player(x, y)
                elif cells[y][x] == "G":
                    self.cells[y][x] = CellChars.GHOST
                    self.ghosts.append(Ghost(x, y))
                elif cells[y][x] == "*":
                    self.cells[y][x] = CellChars.POINT
                    self.chekings.append((x, y))
                elif cells[y][x] == "#":
                    self.cells[y][x] = CellChars.WALL
                    self.walls.append((x, y))

    def draw(self):
        self.surface.blit(self.background, (0, 0))
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.width * cellSize, self.height * cellSize))
        for wall in self.walls:
            pygame.draw.rect(self.surface, (255, 0, 0), (wall[0] * cellSize, wall[1] * cellSize, cellSize, cellSize))

        if self.player.direction == direction.RIGHT:
            self.surface.blit(walkRight[0], (self.player.x * cellSize, self.player.y * cellSize))
        else:
            self.surface.blit(noWalk, (self.player.x * cellSize, self.player.y * cellSize))


        self.check_cheking()
        for cheking in self.chekings:
            self.surface.blit(point, (cheking[0] * cellSize, cheking[1] * cellSize, cellSize, cellSize))
        for ghost in self.ghosts:
            pygame.draw.rect(self.surface, (0, 0, 0), (ghost.x * cellSize, ghost.y * cellSize, 40, 40))
        pygame.display.update()

    # def update(self):
    #    for object in self.objects:
    #        object.update()

    # def draw(self):
    #   for object in self.objects:
    #      object.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.player.x > 0 and \
                self.cells[self.player.y][self.player.x - self.speed] != CellChars.WALL:
            self.player.x -= self.speed
            self.player.direction = direction.LEFT
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.player.x < self.width - 1 and \
                self.cells[self.player.y][self.player.x + self.speed] != CellChars.WALL:
            self.player.x += self.speed
            self.player.direction = direction.RIGHT
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.player.y > 0 and \
                self.cells[self.player.y - self.speed][self.player.x] != CellChars.WALL:
            self.player.y -= self.speed
            self.player.direction = direction.UP
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.player.y < self.height - 1 and \
                self.cells[self.player.y + self.speed][self.player.x] != CellChars.WALL:
            self.player.y += self.speed
            self.player.direction = direction.DOWN

    def run(self):
        while not self.game_over:
            self.surface.blit(self.background, (0, 0))
            self.handle_events()


            for ghost in self.ghosts:
                ghost.go(self)

            self.draw()

            fontObj = pygame.font.Font(None, 35)
            textSurfaceObj = fontObj.render(
                " Life = " + str(self.countLife) + " " + "score = " + str(self.score),
                True, (255, 255, 0))
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (self.width * cellSize - 120, self.height * cellSize - 10)
            self.surface.blit(textSurfaceObj, textRectObj)
            pygame.display.flip()

            # self.update()
            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def check_cheking(self):
        for check in self.chekings:
            if check[0] == self.player.x and check[1] == self.player.y:
                self.chekings.remove(check)
                self.score += 1

    def inBounds(self, point):
        return point[0] > 0 and point[0] < self.width and point[1] > 0 and point[1] < self.height

    def FindPaths(self, start, finish):
        finish = (finish.x, finish.y)
        start = (start.x, start.y)
        if finish == start:
            return [start]
        track = {}
        track[start] = (start, None)
        queue = [start]
        while len(queue) != 0:
            point = queue.pop()
            for i in range(-1, 1):
                for j in range(-1, 1):
                    if i * i + j * j == 1:
                        newPoint = (point[0] + i, point[1] + j)
                        if not self.inBounds(newPoint) or (newPoint[0], newPoint[1]) in self.walls:
                            continue
                        if newPoint in track.keys():
                            continue
                        queue.append(newPoint)
                        track[newPoint] = (newPoint, track[point][0])
        arr = []
        point = finish
        while point is not start:
            arr.append(point)
            if point in track.keys():
                point = track[point][1]
            else:
                return arr
        return arr


Test = [
    "#################",
    "#P******#*******#",
    "#*##*##*#*##*##*#",
    "#*##*##*#*##*##*#",
    "#***************#",
    "#*##*#*###*#*##*#",
    "#****#**#**#****#",
    "####*##*#*##*####",
    "####*#     #*####",
    "####*  ###  *####",
    "####*#  G  #*####",
    "####*# ### #*####",
    "#*******#*******#",
    "#*##*##*#*##*##*#",
    "#**#*********#**#",
    "##*#*#*###*#*#*##",
    "#****#**#**#****#",
    "#*#####*#*#####*#",
    "#***************#",
    "#################"
]

Test1 = [
    "###########",
    "#P********#",
    "#*********#",
    "#*******G##",
    "###########"
]
