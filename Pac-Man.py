from Game import *
from pygame.locals import *

if sys.version_info < (3, 6):
    print("Use python >= 3.6", file=sys.stderr)
    sys.exit()
else:
    print("Version ok", file=sys.stderr)

try:
    import pygame, sys, os, random
except Exception as e:
    print('Game modules not found: "{}"'.format(e), file=sys.stderr)
    sys.exit()

windWidth = 1024
windHeight = 688
cellSize = 40
speed = 1

walkRight = [pygame.image.load('image/walkR2.png'), pygame.image.load('image/walkR3.png'),
             pygame.image.load('image/walkR2.png'), pygame.image.load('image/walkR1.png')]
noWalk = pygame.image.load("image/walkR2.png")
background = pygame.image.load("image/bg.png")
point = pygame.image.load("image/Point.png")

if __name__ == '__main__':
    currentMap = Game("Test")
    currentMap.run()
#  win = pygame.display.set_mode((currentMap.width * cellSize, currentMap.height * cellSize)
