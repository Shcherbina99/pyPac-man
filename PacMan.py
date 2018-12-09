import sys,enum

if sys.version_info < (3, 6):
    print("Use python >= 3.6", file=sys.stderr)
    sys.exit()
else:
    print("Version ok", file=sys.stderr)

try:
    import pygame, sys, os, random
    from pygame.locals import *
except Exception as e:
    print('Game modules not found: "{}"'.format(e), file=sys.stderr)
    sys.exit()
pygame.mixer.pre_init(22050,16,2,512)
pygame.mixer.init()
SCRIPT_PATH = sys.path[0]
clock = pygame.time.Clock()
pygame.init()

window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Pacman")
screen = pygame.display.get_surface()
img_Background = pygame.image.load(os.path.join(SCRIPT_PATH, "res", "backgrounds", "1.gif")).convert()

ghostcolor = {}
ghostcolor[0] = (255, 0, 0, 255)
ghostcolor[1] = (255, 128, 255, 255)
ghostcolor[2] = (128, 255, 255, 255)
ghostcolor[3] = (255, 128, 0, 255)
ghostcolor[4] = (50, 50, 255, 255)  # blue
ghostcolor[5] = (255, 255, 255, 255)  # white

snd_pellet = {}

snd_pellet[0] = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","pellet1.wav"))
snd_pellet[1] = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","pellet2.wav"))
snd_powerpellet = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","powerpellet.wav"))
snd_eatgh = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatgh2.wav"))
snd_fruitbounce = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","fruitbounce.wav"))
snd_eatfruit = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","eatfruit.wav"))
snd_extralife = pygame.mixer.Sound(os.path.join(SCRIPT_PATH,"res","sounds","extralife.wav"))

class direction(enum.Enum):
    RIGHT = "Right"
    LEFT = "Left"
    UP = "Up"
    DOWN = "Down"


class Game:
    def __init__(self):
        self.levelNum = 1
        self.score = 0
        self.lives = 3

        # game "mode" variable
        # 1 = normal
        # 2 = hit ghost
        # 3 = game over
        # 4 = wait to start
        self.mode = 1
        self.modeTimer = 0

        self.SetMode(3)

        self.screenTileSize = (25, 20)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)
        self.name = self.getplayername()
        self.digit = {}
        for i in range(10):
            self.digit[i] = pygame.image.load(os.path.join(SCRIPT_PATH, "res", "text", str(i) + ".gif")).convert()
        self.imLife = pygame.image.load(os.path.join(SCRIPT_PATH, "res", "text", "life.gif")).convert()
        self.imGameOver = pygame.image.load(os.path.join(SCRIPT_PATH, "res", "text", "gameover.gif")).convert()
        self.imReady = pygame.image.load(os.path.join(SCRIPT_PATH, "res", "text", "ready.gif")).convert()
        self.imLogo = pygame.image.load(os.path.join(SCRIPT_PATH, "res", "text", "logo.gif")).convert()

    def StartNewGame(self):
        self.levelNum = 1
        self.score = 0
        self.lives = 3
        self.SetMode(4)
        thisLevel.LoadLevel(thisGame.GetLevelNum())
        player.x = player.homeX
        player.y = player.homeY

    def SetNextLevel(self):
        self.levelNum += 1
        self.SetMode(4)
        thisLevel.LoadLevel(thisGame.GetLevelNum())
        player.velX = 0
        player.velY = 0
        player.anim_pacmanCurrent = player.anim_pacmanS

    def defaulthiscorelist(self):
        return [(100000, "Clyde"), (80000, "Inky"), (60000, "Pinky"), (40000, "Pac-man"), (
            20000, "Blinky"),(0, self.name)]

    def gethiscores(self):
        try:
            f = open(os.path.join(SCRIPT_PATH, "res", "hiscore.txt"))
            hs = []
            for line in f:
                line = line.replace("\n", "")
                line = line.replace("\r", "")
                line = line.split(" ")
                score = int(line[0])
                name = line[1]
                if score > 99999999:
                    score = 99999999
                if len(name) > 22:
                    name = name[:22]
                hs.append((score, name))
            f.close()
            if len(hs) > 6:
                hs = hs[:6]
            while len(hs) < 6:
                hs.append((0, ""))
            return hs
        except IOError:
            return self.defaulthiscorelist()

    def writehiscores(self, hs):
        fname = os.path.join(SCRIPT_PATH, "res", "hiscore.txt")
        f = open(fname, "w")
        for line in hs:
            f.write(str(line[0]) + " " + line[1] + "\n")
        f.close()

    def updatehiscores(self, newscore):
        hs = self.gethiscores()
        for line in hs:
            if newscore >= line[0]:
                hs.insert(hs.index(line), (newscore, self.name))
                hs.pop(-1)
                self.writehiscores(hs)
                break

    def drawmidgamehiscores(self):
        f = pygame.font.Font(None, 50)
        color = thisLevel.edgeLightColor
        hs = self.gethiscores()
        i = 1
        text = f.render("Score List:", True, color)
        screen.blit(text, (80, 0))
        for line in hs:
            text = f.render("{}".format(line[1] + " : " + str(line[0])), True, color)
            screen.blit(text, (80, i * 50))
            i += 1

    def getplayername(self):
        fontAns = pygame.font.Font(None, 32)
        input_box = pygame.Rect(100, 100, 140, 32)
        color = pygame.Color('lightskyblue3')
        text = ''
        fontQues = pygame.font.SysFont(None, 25)
        text1 = fontQues.render("{}".format("What is your name ?"), True, color)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

            window.fill((30, 30, 30))
            screen.blit(text1, (100, 80))
            txt_surface = fontAns.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(window, color, input_box, 2)

            pygame.display.flip()
            clock.tick(30)

    def SetMode(self, newMode):
        self.mode = newMode
        self.modeTimer = 0

    def GetLevelNum(self):
        return self.levelNum

    def DrawScore(self):
        self.DrawNumber(self.score, (24 + 16, self.screenSize[1] - 24))
        for i in range(0, self.lives, 1):
            screen.blit(self.imLife, (24 + i * 10 + 16, self.screenSize[1] - 12))
        if self.mode == 3:
            screen.blit(self.imGameOver, (self.screenSize[0] / 2, self.screenSize[1] - 20))
            self.drawmidgamehiscores()
        elif self.mode == 4:
            screen.blit(self.imReady, (self.screenSize[0] / 2 - 20, self.screenSize[1] / 2 + 12))
        self.DrawNumber(self.levelNum, (0, self.screenSize[1] - 12))

    def DrawNumber(self, number, point):
        strNumber = str(number)
        for i in range(0, len(str(number)), 1):
            iDigit = int(strNumber[i])
            screen.blit(self.digit[iDigit], (point[0] + i * 9, point[1]))

    def AddToScore(self, score):
        extraLifeSet = [25000, 50000, 100000, 150000]
        for specialScore in extraLifeSet:
            if self.score < specialScore and self.score + score >= specialScore:
                snd_extralife.play()
                thisGame.lives += 1
        self.score += score


class Level:
    def __init__(self):
        self.lvlWidth = 0
        self.lvlHeight = 0
        self.edgeLightColor = (255, 255, 0, 255)
        self.edgeShadowColor = (255, 150, 0, 255)
        self.fillColor = (0, 255, 255, 255)
        self.pelletColor = (255, 255, 255, 255)

        self.map = {}

        self.pellets = 0
        self.powerPelletBlinkTimer = 0

    def LoadLevel(self, levelNum):

        self.map = {}

        self.pellets = 0
        try:
            f = open(os.path.join(SCRIPT_PATH, "res", "levels", str(levelNum) + ".txt"), 'r')
        except IOError:
            return
        rowNum = 0
        isReadingLevelData = False

        for line in f:
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            str_splitBySpace = line.split(' ')
            j = str_splitBySpace[0]
            if j == "'" or j == "":
                continue
            elif j == "#":
                firstWord = str_splitBySpace[1]
                if firstWord == "lives":
                    thisGame.lives = int(str_splitBySpace[2])

                elif firstWord == "score":
                    thisGame.score = int(str_splitBySpace[2])

                elif firstWord == "player":
                    player.x = int(str_splitBySpace[2])
                    player.y = int(str_splitBySpace[3])

                elif firstWord == "lvlwidth":
                    self.lvlWidth = int(str_splitBySpace[2])

                elif firstWord == "lvlheight":
                    self.lvlHeight = int(str_splitBySpace[2])

                elif firstWord == "edgecolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "edgelightcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)

                elif firstWord == "edgeshadowcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "fillcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.fillColor = (red, green, blue, 255)

                elif firstWord == "pelletcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.pelletColor = (red, green, blue, 255)

                elif firstWord == "fruittype":
                    pass

                elif firstWord == "startleveldata":
                    isReadingLevelData = True
                    rowNum = 0

                elif firstWord == "endleveldata":
                    isReadingLevelData = False

            else:
                if isReadingLevelData == True:
                    for k in range(self.lvlWidth):
                        self.SetMapTile((rowNum, k), int(str_splitBySpace[k]))

                        thisID = int(str_splitBySpace[k])
                        if thisID == 4:
                            player.homeX = k * 16
                            player.homeY = rowNum * 16
                            self.SetMapTile((rowNum, k), 0)

                        elif thisID >= 10 and thisID <= 13:
                            ghosts[thisID - 10].homeX = k * 16
                            ghosts[thisID - 10].homeY = rowNum * 16
                            self.SetMapTile((rowNum, k), 0)

                        elif thisID == 2:
                            self.pellets += 1

                    rowNum += 1
        GetCrossRef()

    def SaveLevel(self):
        f = open(os.path.join(SCRIPT_PATH, "res", "levels", "Save.txt"), 'w')
        f.writelines(["# lives " + str(thisGame.lives), "\n",
                      "# score " + str(thisGame.score), "\n",
                      "# player " + str(player.x) + " " + str(player.y), "\n",
                      "# lvlwidth" + str(self.lvlWidth), "\n",
                      "# lvlheight" + str(self.lvlHeight), "\n",
                      "# edgelightcolor" + str(self.edgeLightColor), "\n",
                      "# edgeshadowcolor" + str(self.edgeShadowColor), "\n",
                      "# fillcolor" + str(self.fillColor), "\n",
                      "# pelletcolor" + str(self.pelletColor), "\n",
                      "# fruittype", "\n",
                      "# startleveldata", "\n"])
        for k in range(self.lvlHeight):
            for i in range(self.lvlWidth):
                f.write(str(self.GetMapTile((k, i))) + " ")
            f.write("\n")
        f.writelines("# endleveldata")

    def SetMapTile(self, point, newValue):
        self.map[(point[0] * self.lvlWidth) + point[1]] = newValue

    def GetMapTile(self, point):
        if point[0] >= 0 and point[0] < self.lvlHeight and point[1] >= 0 and point[1] < self.lvlWidth:
            return self.map[(point[0] * self.lvlWidth) + point[1]]
        else:
            return 0

    def IsWall(self, point):
        if point[0] > thisLevel.lvlHeight - 1 or point[0] < 0:
            return True
        if point[1] > thisLevel.lvlWidth - 1 or point[1] < 0:
            return True
        result = thisLevel.GetMapTile(point)
        return (result >= 100 and result <= 199) or result == 1

    def CheckIfHitWall(self, possiblePlayer, point):
        numCollisions = 0
        for iRow in range(point[0] - 1, point[0] + 2):
            for iCol in range(point[1] - 1, point[1] + 2):
                if (possiblePlayer[0] - (iCol * 16) < 16) and (possiblePlayer[0] - (iCol * 16) > -16) and (
                        possiblePlayer[1] - (iRow * 16) < 16) and (possiblePlayer[1] - (iRow * 16) > -16):
                    if self.IsWall((iRow, iCol)):
                        numCollisions += 1
        return numCollisions > 0

    def CheckIfHitSomething(self, playerPoint, point):
        for iRow in range(point[0] - 1, point[0] + 2):
            for iCol in range(point[1] - 1, point[1] + 2):
                if (playerPoint[0] - (iCol * 16) < 16) and (playerPoint[0] - (iCol * 16) > -16) and (
                        playerPoint[1] - (iRow * 16) < 16) and (
                        playerPoint[1] - (iRow * 16) > -16):
                    result = thisLevel.GetMapTile((iRow, iCol))
                    if result == tileID['pellet']:
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        thisLevel.pellets -= 1
                        thisGame.AddToScore(10)
                        snd_pellet[player.pelletSndNum].play()
                        player.pelletSndNum = 1 - player.pelletSndNum
                        if thisLevel.pellets == 0:
                            thisGame.levelNum += 1
                            thisLevel.LoadLevel(thisGame.GetLevelNum())
                            player.x = player.homeX
                            player.y = player.homeY
                            # WON THE LEVEL
                            # thisGame.SetMode(6)

                    elif result == tileID['pellet-power']:
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        thisGame.AddToScore(100)
                        snd_powerpellet.play()
                    elif result == tileID['door-h']:
                        for i in range(0, thisLevel.lvlWidth, 1):
                            if not i == iCol:
                                if thisLevel.GetMapTile((iRow, i)) == tileID['door-h']:
                                    player.x = i * 16
                                    if player.velX > 0:
                                        player.x += 16
                                    else:
                                        player.x -= 16

                    elif result == tileID['door-v']:
                        for i in range(0, thisLevel.lvlHeight, 1):
                            if not i == iRow:
                                if thisLevel.GetMapTile((i, iCol)) == tileID['door-v']:
                                    player.y = i * 16
                                    if player.velY > 0:
                                        player.y += 16
                                    else:
                                        player.y -= 16

    def DrawMap(self):
        self.powerPelletBlinkTimer += 1
        if self.powerPelletBlinkTimer == 60:
            self.powerPelletBlinkTimer = 0

        for row in range(-1, thisGame.screenTileSize[0] + 1, 1):
            for col in range(-1, thisGame.screenTileSize[1] + 1, 1):
                actualRow = row
                actualCol = col
                useTile = self.GetMapTile((actualRow, actualCol))
                if not useTile == 0 and not useTile == tileID['door-h'] and not useTile == tileID['door-v']:
                    if useTile == tileID['pellet-power']:
                        if self.powerPelletBlinkTimer < 30:
                            screen.blit(tileIDImage[useTile], (
                                col * 16, row * 16))
                    elif useTile == tileID['showlogo']:
                        screen.blit(thisGame.imLogo, (
                            col * 16, row * 16))
                    else:
                        screen.blit(tileIDImage[useTile], (
                            col * 16, row * 16))


def GetCrossRef():
    f = open(os.path.join(SCRIPT_PATH, "res", "crossref.txt"), 'r')
    for i in f.readlines():
        i = i.replace("\n", "")
        i = i.replace("\r", "")
        str_splitBySpace = i.split(' ')
        j = str_splitBySpace[0]
        if not (j == "'" or j == "" or j == "#"):
            tileIDName[int(str_splitBySpace[0])] = str_splitBySpace[1]
            tileID[str_splitBySpace[1]] = int(str_splitBySpace[0])
            thisID = int(str_splitBySpace[0])
            tileIDImage[thisID] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "tiles", str_splitBySpace[1] + ".gif")).convert()
            for y in range(16):
                for x in range(16):
                    if tileIDImage[thisID].get_at((x, y)) == (255, 206, 255, 255):
                        tileIDImage[thisID].set_at((x, y), thisLevel.edgeLightColor)

                    elif tileIDImage[thisID].get_at((x, y)) == (132, 0, 132, 255):
                        tileIDImage[thisID].set_at((x, y), thisLevel.fillColor)

                    elif tileIDImage[thisID].get_at((x, y)) == (255, 0, 255, 255):
                        tileIDImage[thisID].set_at((x, y), thisLevel.edgeShadowColor)

                    elif tileIDImage[thisID].get_at((x, y)) == (128, 0, 128, 255):
                        tileIDImage[thisID].set_at((x, y), thisLevel.pelletColor)


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
        self.direction = None

        for i in range(1, 9):
            self.anim_pacmanL[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-l " + str(i) + ".gif")).convert()
            self.anim_pacmanR[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-r " + str(i) + ".gif")).convert()
            self.anim_pacmanU[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-u " + str(i) + ".gif")).convert()
            self.anim_pacmanD[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-d " + str(i) + ".gif")).convert()
            self.anim_pacmanS[i] = pygame.image.load(os.path.join(SCRIPT_PATH, "res", "sprite", "pacman.gif")).convert()

        self.animFrame = 3
        self.anim_pacmanCurrent = self.anim_pacmanS
        self.pelletSndNum = 0

    def move(self):
        self.nearestRow = int(((self.y + 8) / 16))
        self.nearestCol = int(((self.x + 8) / 16))
        if self.direction == direction.RIGHT:
            if not thisLevel.CheckIfHitWall((player.x + player.speed, player.y), (player.nearestRow, player.nearestCol)):
                player.velX = player.speed
                player.velY = 0
        elif self.direction == direction.LEFT:
            if not thisLevel.CheckIfHitWall((player.x - player.speed, player.y), (player.nearestRow, player.nearestCol)):
                player.velX = -player.speed
                player.velY = 0
        elif self.direction == direction.DOWN:
            if not thisLevel.CheckIfHitWall((player.x , player.y + player.speed), (player.nearestRow, player.nearestCol)):
                player.velX = 0
                player.velY = player.speed
        elif self.direction == direction.UP:
            if not thisLevel.CheckIfHitWall((player.x , player.y - player.speed), (player.nearestRow, player.nearestCol)):
                player.velX = 0
                player.velY = -player.speed
        if not thisLevel.CheckIfHitWall((self.x + self.velX, self.y + self.velY), (self.nearestRow, self.nearestCol)):
            self.x += self.velX
            self.y += self.velY
            thisLevel.CheckIfHitSomething((self.x, self.y), (self.nearestRow, self.nearestCol))
        else:
            self.velX = 0
            self.velY = 0

    def draw(self):
        if thisGame.mode == 3:
            return False
        if self.velX > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velX < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.velY > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.velY < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU
        screen.blit(self.anim_pacmanCurrent[self.animFrame], (self.x, self.y))
        if thisGame.mode == 1:
            if not self.velX == 0 or not self.velY == 0:
                self.animFrame += 1
            if self.animFrame == 9:
                self.animFrame = 1


class ghost():

    def __init__(self, ghostID):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 1
        self.nearestRow = 0
        self.nearestCol = 0
        self.id = ghostID

        # ghost "state" variable
        # 1 = normal
        # 2 = vulnerable
        # 3 = spectacles
        self.state = 1
        self.homeX = 0
        self.homeY = 0
        self.currentPath = ""
        self.anim = {}

        for i in range(1, 7, 1):
            self.anim[i] = pygame.image.load(
                os.path.join(SCRIPT_PATH, "res", "sprite", "ghost " + str(i) + ".gif")).convert()
            # change the ghost color in this frame
            for y in range(0, 16, 1):
                for x in range(0, 16, 1):
                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        # default, red ghost body color
                        self.anim[i].set_at((x, y), ghostcolor[self.id])
        self.animFrame = 1
        self.animDelay = 0


def CheckInputs(events):
    for event in events:
        if event.type == pygame.QUIT or event.key == pygame.K_ESCAPE:
            thisLevel.SaveLevel()
            thisGame.updatehiscores(thisGame.score)
            sys.exit(0)
        if thisGame.mode == 1:
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]:
                    player.direction = direction.RIGHT
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.direction = direction.LEFT
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.direction = direction.UP
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.direction = direction.DOWN
                elif event.key == pygame.K_l:
                    thisLevel.LoadLevel("Save")
        if thisGame.mode == 3:
            if event.key == pygame.K_RETURN:
                sys.exit(0)
                # thisGame.StartNewGame()




if __name__ == '__main__':
    tileIDName = {}
    tileID = {}
    tileIDImage = {}
    window = pygame.display.set_mode((400, 400), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN)
    thisGame = Game()
    thisLevel = Level()
    player = Player()
    thisGame.StartNewGame()
    ghosts = {}
    for i in range(6):
        ghosts[i] = ghost(i)
    while True:
        CheckInputs(pygame.event.get())
        if thisGame.mode == 4:
            thisGame.modeTimer += 1
            if thisGame.modeTimer == 90:
                thisGame.SetMode(1)
                player.direction = direction.LEFT
        player.move()
        screen.blit(img_Background, (0, 0))
        thisLevel.DrawMap()
        thisGame.DrawScore()
        player.draw()

        pygame.display.flip()
        clock.tick(60)
