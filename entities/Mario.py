import pygame
import math
import numpy as np

from classes.Animation import Animation
from classes.Camera import Camera
from classes.Collider import Collider
from entities.CollisonTester import CollisionTester
from classes.EntityCollider import EntityCollider
from classes.Input import Input
from classes.Sprites import Sprites
from entities.EntityBase import EntityBase
from traits.bounce import bounceTrait
from traits.go import goTrait
from traits.jump import jumpTrait
from classes.Pause import Pause
from classes.Model import Model
from entities.Goomba import Goomba
from entities.Koopa import Koopa
import torch


class Mario(EntityBase):
    def __init__(self, x, y, level, screen, dashboard, sound, gravity=0.75):
        super(Mario, self).__init__(x, y, gravity)
        self.x = x
        self.spriteCollection = Sprites().spriteCollection
        self.CT = CollisionTester()
        self.camera = Camera(self.rect, self)
        self.sound = sound
        self.level = level
        self.OI = Input(self)
        self.closest_mob = None
        self.closest_object = None
        self.output =0
        self.inAir = False
        self.brain = Model().share_memory()
        self.fitness = 0

        self.animation = Animation(
            [
                self.spriteCollection["mario_run1"].image,
                self.spriteCollection["mario_run2"].image,
                self.spriteCollection["mario_run3"].image,
            ],
            self.spriteCollection["mario_idle"].image,
            self.spriteCollection["mario_jump"].image,
        )

        self.traits = {
            "jumpTrait": jumpTrait(self),
            "goTrait": goTrait(self.animation, screen, self.camera, self),
            "bounceTrait": bounceTrait(self),
        }

        self.levelObj = level
        self.collision = Collider(self, level)
        self.screen = screen
        self.EntityCollider = EntityCollider(self)
        self.dashboard = dashboard
        self.restart = False
        self.pause = False
        self.pauseObj = Pause(screen, self, dashboard)

    def getInputs(self):
        map = []
        input = []
        for x in range(60):
            map.append(self.CT.test(x, 11, self.level, self))
            if map[x] == 3:
                map[x] = 0

        for x in range(int(self.rect.x/32), int(self.rect.x/32) + 8):
            input.append(map[x])
        return torch.FloatTensor(input)

    def update(self):
        self.updateTraits()
        self.moveMario()
        self.camera.move()
        self.applyGravity()
        self.checkEntityCollision()
        self.output = self.brain.forward(self.getInputs())
        #print(self.output)
        self.OI.checkForInput(self.output)

    def moveMario(self):
        self.rect.y += self.vel.y
        self.collision.checkY()
        self.rect.x += self.vel.x
        self.collision.checkX()

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Item":
                    self._onCollisionWithItem(ent)
                elif ent.type == "Block":
                    self._onCollisionWithBlock(ent)
                elif ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)

    def _onCollisionWithItem(self, item):
        self.levelObj.entityList.remove(item)
        self.dashboard.points += 100
        self.dashboard.coins += 1
        self.sound.play_sfx(self.sound.coin)

    def _onCollisionWithBlock(self, block):
        if not block.triggered:
            self.dashboard.coins += 1
            self.sound.play_sfx(self.sound.bump)
        block.triggered = True

    def _onCollisionWithMob(self, mob, collisionState):
        if collisionState.isTop and (mob.alive or mob.alive == "shellBouncing"):
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            self.bounce()
            self.killEntity(mob)
        elif collisionState.isTop and mob.alive == "sleeping":
            self.sound.play_sfx(self.sound.stomp)
            self.rect.bottom = mob.rect.top
            mob.timer = 0
            self.bounce()
            mob.alive = False
        elif collisionState.isColliding and mob.alive == "sleeping":
            if mob.rect.x < self.rect.x:
                mob.leftrightTrait.direction = -1
                mob.rect.x += -5
            else:
                mob.rect.x += 5
                mob.leftrightTrait.direction = 1
            mob.alive = "shellBouncing"
        elif collisionState.isColliding and mob.alive:
            self.gameOver()

    def bounce(self):
        self.traits["bounceTrait"].jump = True

    def killEntity(self, ent):
        if ent.__class__.__name__ != "Koopa":
            ent.alive = False
        else:
            ent.timer = 0
            ent.alive = "sleeping"
        self.dashboard.points += 100

    def gameOver(self):
        self.restart = True

    def getPos(self):
        return self.camera.x + self.rect.x, self.rect.y

    def setPos(self,x,y):
        self.rect.x = x
        self.rect.y = y
