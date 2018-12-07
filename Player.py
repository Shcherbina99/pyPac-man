import enum
from PacMan import *
class direction(enum.Enum):
    RIGHT = "Right"
    LEFT = "Left"
    UP = "Up"
    DOWN = "Down"


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 2

        self.nearestRow = 0
        self.nearestCol = 0

        self.homeX = 0
        self.homeY = 0

        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        self.anim_pacmanCurrent = {}

        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-l " + str(i) + ".gif")).convert()
            self.anim_pacmanR[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-r " + str(i) + ".gif")).convert()
            self.anim_pacmanU[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-u " + str(i) + ".gif")).convert()
            self.anim_pacmanD[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-d " + str(i) + ".gif")).convert()
            self.anim_pacmanS[i] = pygame.image.load(os.path.join(SCRIPT_PATH, "res", "sprite", "pacman.gif")).convert()

        self.pelletSndNum = 0

    def Draw(self):

        if thisGame.mode == 3:
            return False

        # set the current frame array to match the direction pacman is facing
        if self.velX > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velX < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.velY > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.velY < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU

        screen.blit(self.anim_pacmanCurrent[self.animFrame],
                    (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))

        if thisGame.mode == 1:
            if not self.velX == 0 or not self.velY == 0:
                # only Move mouth when pacman is moving
                self.animFrame += 1

            if self.animFrame == 9:
                # wrap to beginning
                self.animFrame = 1
