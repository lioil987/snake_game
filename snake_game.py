import time
import colour
import pygame
import random

sizeOfWindow = [2000,1000]
window = pygame.display.set_mode(sizeOfWindow)
pygame.init()


class ManagementWin:
    pass


class Color:
    colorRGB = None
    nameOfSomeColor = ['DarkGreen', 'Green', 'DarkCyan', 'DeepSkyBlue', 'DarkTurquoise', 'MediumSpringGreen', 'Lime',
                       'SpringGreen', 'Cyan', 'Aqua', 'MidnightBlue', 'DodgerBlue', 'LightSeaGreen', 'ForestGreen',
                       'SeaGreen', 'DarkSlateGray', 'DarkSlateGrey', 'LimeGreen', 'MediumSeaGreen', 'Turquoise',
                       'RoyalBlue', 'SteelBlue', 'DarkSlateBlue', 'MediumTurquoise']

    def __init__(self, color="white"):
        self.getRGB(color)

    def getRGB(self, color):
        c = list(colour.Color(color).get_rgb())
        c[0] = int(c[0] * 255)
        c[1] = int(c[1] * 255)
        c[2] = int(c[2] * 255)
        self.colorRGB = tuple(c)

    def getColor(self):
        return self.colorRGB

    def getRandomColor(self):
        self.getRGB(random.choice(self.nameOfSomeColor))


class ManagementWindow:
    score = 0

    @staticmethod
    def showTitleScore():
        textScore = pygame.font.Font(None, 80)
        window.blit(textScore.render(f"Score: {ManagementWindow.score}", False, (255, 255, 255)), (0, 0))


class Object:
    x = None
    y = None
    w = None
    h = None
    color = None
    spead = None
    border = None
    destroyer = None
    _moving = None
    _lastMoveOrder = None

    def __init__(self, w=0, h=0, x=0, y=0, color="white", spead=5, border=5, destroyer=False,
                 listForAppend=None):
        self.x = x
        self.y = y
        self.spead = spead
        self.color = color
        self.border = border
        self.w = w
        self.h = h
        self._moveOrder = []
        self.destroyer = destroyer
        if listForAppend is not None:
            listForAppend.append(self)

    def appendMoveOrder(self, count, direction):
        if direction == "up-right":
            self._moveOrder.append([True, count, 0, (("|", False), ("-", True))])
        if direction == "up-left":
            self._moveOrder.append([True, count, 0, (("|", False), ("-", False))])
        if direction == "bottom-right":
            self._moveOrder.append([True, count, 0, (("|", True), ("-", True))])
        if direction == "bottom-left":
            self._moveOrder.append([True, count, 0, (("|", True), ("-", False))])

        if direction == "up":
            self._moveOrder.append([False, count, 0, "|", False])
        elif direction == "bottom":
            self._moveOrder.append([False, count, 0, "|", True])
        elif direction == "right":
            self._moveOrder.append([False, count, 0, "-", True])
        elif direction == "left":
            self._moveOrder.append([False, count, 0, "-", False])

    def changeOrder(self, count, direction, index):
        if -1 < index < len(self._moveOrder):
            if direction == "up-right":
                self._moveOrder[index] = [True, count, 0, (("|", False), ("-", True))]
            if direction == "up-left":
                self._moveOrder[index] = [True, count, 0, (("|", False), ("-", False))]
            if direction == "bottom-right":
                self._moveOrder[index] = [True, count, 0, (("|", True), ("-", True))]
            if direction == "bottom-left":
                self._moveOrder[index] = [True, count, 0, (("|", True), ("-", False))]

            if direction == "up":
                self._moveOrder[index] = [False, count, 0, "|", False]
            elif direction == "bottom":
                self._moveOrder[index] = [False, count, 0, "|", True]
            elif direction == "right":
                self._moveOrder[index] = [False, count, 0, "-", True]
            elif direction == "left":
                self._moveOrder[index] = [False, count, 0, "-", False]

    def move(self):
        self._mirror()
        if self._moveOrder and self._moveOrder[0][3]:

            if self._moveOrder[0][2] != self._moveOrder[0][1]:
                if self._moveOrder[0][0]:
                    for item in self._moveOrder[0][3]:
                        if item[0] == "|":
                            self.moveY(item[1])
                        else:
                            self.moveX(item[1])
                else:
                    if self._moveOrder[0][3] == "|":
                        self.moveY(self._moveOrder[0][4])
                    else:
                        self.moveX(self._moveOrder[0][4])

                self._moveOrder[0][2] += 1
            else:
                self._moveOrder.pop(0)

    def moveX(self, direction=True, count=1):
        if direction:
            self.x += self.spead
        else:
            self.x -= self.spead

    def moveY(self, direction=True, count=1):
        if direction:
            self.y += self.spead
        else:
            self.y -= self.spead

    def _show(self, win):
        raise NotImplementedError()

    def _mirror(self):
        if self.x == - self.w:
            self.x = sizeOfWindow[0]
        if self.y == -self.h:
            self.y = sizeOfWindow[1]
        if sizeOfWindow[0] + self.w == self.x:
            self.x = -self.w
        if sizeOfWindow[1] + self.h == self.y:
            self.y = -self.h



    def check(self, objects, type):
        if type == "prize":
            for item in objects:
                if (self.x < item.x < self.x + self.w) or (item.x < self.x < item.x + item.w) or (
                        item.x == self.x):
                    if (self.y < item.y < self.y + self.h) or (item.y < self.y < item.y + item.h):
                        ManagementWindow.score += item.value
                        sneak.creatCubes()
                        item.destroy()
        elif type == "snake":
            for item in objects:
                if self.x == item.x:
                    if self.y == item.y:
                        exit()




class Rect(Object):
    firstCube = None

    def __init__(self, w=0, h=0, x=0, y=0, color="white", spead=5, border=5, destroyer=False,
                 listForAppend=None):
        super().__init__(w, h, x, y, color, spead, border, destroyer, listForAppend)

    def _show(self, win):
        pygame.draw.rect(win, self.color, ((self.x - self.w // 2, self.y - self.h // 2), (self.w, self.h)), self.border)


class Sneak:
    size = 50

    _lastCubes = None
    _directionOfCubes = []
    _lastDirection = None
    _whatCube = 0
    _changeDir = False
    _sneakDir = 0
    _moveOrder = None
    listOfCubes = []

    def __init__(self, firsCubePosition):
        self._moveOrder = []
        self.listOfCubes = []
        self._creatDefaultCube(firsCubePosition[0], firsCubePosition[1], "up", "white")

    def _creatDefaultCube(self, x, y, direction, color):
        Rect(self.size, self.size, x, y, color, self.size, 0, False, self.listOfCubes).appendMoveOrder(1000, direction)

        self._directionOfCubes.append(direction)

    def creatCubes(self):
        temp = Color()
        temp.getRandomColor()
        self._lastCubes = self.listOfCubes[-1]
        self._lastDirection = self._directionOfCubes[-1]
        x = self._lastCubes.x
        y = self._lastCubes.y
        if self._lastDirection == "up":
            self._creatDefaultCube(x, y + self.size, "up", temp.colorRGB)
        if self._lastDirection == "bottom":
            self._creatDefaultCube(x, y - self.size, "bottom", temp.colorRGB)
        if self._lastDirection == "right":
            self._creatDefaultCube(x - self.size, y, "right", temp.colorRGB)
        if self._lastDirection == "left":
            self._creatDefaultCube(x + self.size, y, "left", temp.colorRGB)

    def orderMove(self, direction):
        self._changeDir = True
        self._sneakDir = direction
        self._moveOrder.append([0, direction])

    def start(self):
        print(self._moveOrder)

    def move(self):
        i = 0
        for item in self._moveOrder:

            if item[0] < len(self.listOfCubes):

                self.listOfCubes[item[0]].changeOrder(1000, item[1], 0)
                self._directionOfCubes[item[0]] = item[1]
                item[0] = item[0] + 1
            else:
                i = 1

        if i:
            self._moveOrder.pop(0)

        for item in self.listOfCubes:
            item.move()

    def show(self):
        for item in self.listOfCubes:
            item._show(window)


class Prize(object):
    listPrize = []

    def __init__(self, x=0, y=0, randomPara=True, type="little", destroyer=False,
                 listForAppend=listPrize):
        super().__init__()
        if randomPara:
            list = ["little", "medium", "large"]
            type = random.choice(list)
            x = random.randint(0, 2000)
            y = random.randint(0, 1000)
        if type == "little":
            self.color = "blue"
            self.x = x
            self.value = 5
            self.size = 30
        if type == "medium":
            self.color = "orange"
            self.value = 10
            self.size = 40
        if type == "large":
            self.color = "red"
            self.value = 15
            self.size = 50
        self.x = x
        self.y = y
        self.w = self.size
        self.h = self.size
        Prize.listPrize.append(self)


    def _show(self):
        pygame.draw.rect(window, self.color,
                         ((self.x - self.size // 2, self.y - self.size // 2), (self.size, self.size)), 0)

    def destroy(self):
        Prize.listPrize.remove(self)



sneak = Sneak((1000, 700))
for num in range(5):
    sneak.creatCubes()
sneak.move()
sneak.start()

i = 0
while True:
    window.fill((0, 0, 0))
    sneak.show()

    sneak.listOfCubes[0].check(Prize.listPrize,"prize")
    sneak.listOfCubes[0].check(sneak.listOfCubes[1:], "snake")


    events = pygame.event.get()

    for item in Prize.listPrize:
        item._show()
    if len(Prize.listPrize) < 4 :
        Prize(0,0,True)
    ManagementWindow.showTitleScore()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sneak.orderMove("up")
            if event.key == pygame.K_a:
                sneak.creatCubes()
            if event.key == pygame.K_DOWN:
                sneak.orderMove("bottom")
            if event.key == pygame.K_RIGHT:
                sneak.orderMove("right")
            if event.key == pygame.K_LEFT:
                sneak.orderMove("left")

    if i - 8 == 0:
        sneak.move()

        i = 0
    else:
        i += 1

    pygame.display.update()

    for item in events:
        if item.type == pygame.QUIT:
            pygame.quit()
            exit()
