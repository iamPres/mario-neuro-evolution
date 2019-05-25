import pygame
from pygame.locals import *
import torch
from entities.EntityBase import EntityBase
import sys

class Input:
    def __init__(self, entity):
        self.mouseX = 0
        self.mouseY = 0
        self.entity = entity


    def checkForInput(self, input):
        self.checkForKeyboardInput(input)
        self.checkForMouseInput()
        self.checkForQuitAndRestartInputEvents()

    def checkForKeyboardInput(self, input):
        pressedKeys = input

        if pressedKeys[0] > 0 and not pressedKeys[1] > 0: # Left / Right
            self.entity.traits["goTrait"].direction = -1
        elif pressedKeys[1] > 0 and not pressedKeys[0] > 0:
            self.entity.traits["goTrait"].direction = 1
        else:
            self.entity.traits['goTrait'].direction = 0

        jump = pressedKeys[2] > 0 # Space / Up
        self.entity.traits['jumpTrait'].jump(jump)

        self.entity.traits['goTrait'].boost = pressedKeys[3] > 0 # Boost

    def checkForMouseInput(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.isRightMouseButtonPressed():
            self.entity.levelObj.addKoopa(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
            self.entity.levelObj.addGoomba(
                mouseY / 32, mouseX / 32 - self.entity.camera.pos.x
            )
        if self.isLeftMouseButtonPressed():
            self.entity.levelObj.addCoin(
                mouseX / 32 - self.entity.camera.pos.x, mouseY / 32
            )

    def checkForQuitAndRestartInputEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and \
                (event.key == pygame.K_ESCAPE or event.key == pygame.K_F5):
                self.entity.pause = True
                self.entity.pauseObj.createBackgroundBlur()

    def isLeftMouseButtonPressed(self):
        return pygame.mouse.get_pressed()[0]

    def isRightMouseButtonPressed(self):
        return pygame.mouse.get_pressed()[2]
