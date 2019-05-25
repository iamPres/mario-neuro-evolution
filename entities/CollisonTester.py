from classes.EntityCollider import EntityCollider
import pygame
from classes.Maths import vec2D

class CollisionTester:
    def __init__(self):
        self.rect = None
        self.EC = EntityCollider(self)
        self.vel = vec2D()

    def test(self, x,y, lev, mario):
        self.rect = pygame.Rect(x*32, y*32, 32 ,32)
        levelObj = lev
        level = lev.level
        if level[y][x].rect is not None:
            #print(str(x)+" | "+str(y))
            return 1

        if self.EC.check(mario).isColliding:
            return 0

        count = 0
        for ent in levelObj.entityList:
            collisionState = self.EC.check(ent)
            if collisionState.isColliding:
                count += 1
                if ent.type == "Mob":
                    return -1

        if count == 0:
            return 3



