import pygame
from classes.Font import Font
from entities.CollisonTester import CollisionTester

class Dashboard(Font):
    def __init__(self, filePath, size, screen):
        Font.__init__(self, filePath, size)
        self.state = "menu"
        self.screen = screen
        self.levelName = "1-1"
        self.points = 0
        self.coins = 0
        self.ticks = 0
        self.time = 0
        self.CT = CollisionTester()

    def update(self):
        self.drawText("TIME", 450, 20, 15)
        self.drawText(self.timeString(), 455, 37, 15)

        # update Time
        self.ticks += 1
        if self.ticks == 60:
            self.ticks = 0
            self.time += 1

    def drawGrid(self, level, mario):
        input = [[pygame.Color(0,0,0)]*15]*60
        color = pygame.Color(0,0,0)
        arr = []
        for x in range(int(mario.rect.x/32) - 1, int(mario.rect.x/32) + 8):
            arr.append(x)
            for y in range(11):
                input[x][y] = self.CT.test(x,y,level,mario)
                if input[x][y] == 0:
                    color = pygame.Color(0,0,255)
                if input[x][y] == 1:
                    color = pygame.Color(255,255,255)
                if input[x][y] == -1:
                    color = pygame.Color(255,0,0)
                if not input[x][y] == 3:
                    pygame.draw.rect(self.screen, color, ((x * 8), y * 8, 8, 8))

    def drawText(self, text, x, y, size):
        for char in text:
            charSprite = pygame.transform.scale(self.charSprites[char], (size, size))
            self.screen.blit(charSprite, (x, y))
            if char == " ":
                x += size//2
            else:
                x += size

    def coinString(self):
        return "{:02d}".format(self.coins)

    def pointString(self):
        return "{:06d}".format(self.points)

    def timeString(self):
        return "{:03d}".format(self.time)
