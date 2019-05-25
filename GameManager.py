import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Mario import Mario
from classes.Trainer import Trainer
from classes.Model import Model
from classes.Grader import Grader
from GeneticTrainer import GeneticTrainer
from pygame.locals import *
import sys
import time
from classes.Sprites import Sprites
import torch
from Plotter import Plotter


class GameManager:

    def __init__(self):
        self.pygame = pygame
        self.stop_timeout = 0
        self.fallen = False
        self.max_frame_rate = 120
        self.isMut = False
        self.gen = 0
        self.timeout = 10
        self.fittest = []
        self.frame = 0
        self.pop = 10
        self.gen_cap = 10000
        self.count = 0
        self.grader = Grader()
        self.plotter = Plotter()
        self.gt = GeneticTrainer()
        self.clock = None
        self.mut_rate = 0.1
        self.num_best = 8
        self.pygame.mixer.pre_init(44100, -16, 2, 4096)
        self.pygame.init()
        self.screen = self.pygame.display.set_mode((640, 480))
        self.dashboard = Dashboard("./img/font.png", 8, self.screen)
        self.sound = Sound()
        self.level = Level(self.screen, self.sound, self.dashboard)
        self.mario = [Mario(0, 0, self.level, self.screen, self.dashboard, self.sound) for _ in range(self.pop)]
        self.fittest_index = self.grader.calc_fittest(self.mario)
        self.death_count =  0

    def userInput(self):
        if self.pygame.key.get_pressed()[K_s] and self.count > self.frame + 10:
            self.frame = self.count
            self.gt.saveModel(self.mario[self.death_count])

        if self.pygame.key.get_pressed()[K_l] and self.count > self.frame + 10:
            self.frame = self.count
            self.gt.loadModel(self.mario)

        if self.pygame.key.get_pressed()[K_LSHIFT] and self.count > self.frame + 10:
            self.frame = self.count
            if self.isMut:
                self.isMut = False
            else:
                self.isMut = True

        if self.pygame.key.get_pressed()[K_RIGHT] and self.count > self.frame + 10:
            self.frame = self.count
            self.dashboard.time = 10

    def draw(self):
        self.pygame.display.set_caption("{:d} FPS".format(int(self.clock.get_fps())))
        self.level.drawLevel(self.mario[self.death_count].camera)
        self.dashboard.update()
        self.dashboard.drawGrid(self.level, self.mario[self.death_count])
        self.dashboard.drawText("GENERATION: " + str(self.gen + 1), 10, 10, 10)
        self.dashboard.drawText("BOT: " + str(self.death_count + 1), 10, 30, 10)
        if self.gen > 0:
            if self.fittest[self.gen - 1] is not None:
                self.dashboard.drawText("FITTEST: " + str(self.fittest[self.gen - 1]), 10, 50, 10)
        self.dashboard.drawText("GENERATION HAS MUTATION: " + str(self.isMut), 10, 70, 10)

    def resetLevel(self):
        self.dashboard.ticks = 0
        self.dashboard.time = 0

        self.level.entityList = []
        self.level.loadLevel("Level1-1.json")

        if not self.fallen:
            self.mario[self.death_count].fitness = self.grader.calc_fitness(self.mario[self.death_count])
        else:
            self.mario[self.death_count].fitness = 0

    def initGen(self):
        self.death_count = 0

        for i in self.mario:
            i.restart = False
            i.rect.x = 0
            i.rect.y = 250

        self.clock = pygame.time.Clock()

    def run(self):
        while self.gen < self.gen_cap:
            self.initGen()

            while self.death_count < self.pop:
                #for i in self.mario: i.camera.x = 0
                self.mario[self.death_count].camera.y = 0
                self.mario[self.death_count].rect.x = 0
                self.mario[self.death_count].rect.y = 288
                self.mario[self.death_count].vel.x = 0
                self.mario[self.death_count].vel.y = 0

                while not self.mario[self.death_count].restart and self.dashboard.time < self.timeout:
                    self.count += 1
                    self.fallen = False

                    if self.mario[self.death_count].rect.x == 0:
                        self.stop_timeout += 1
                        if self.stop_timeout > 30:
                            self.mario[self.death_count].restart = True
                            self.stop_timeout = 0

                    if self.mario[self.death_count].rect.y/32 > 11:
                        self.mario[self.death_count].restart = True
                        self.fallen = True

                    self.userInput()
                    self.draw()
                    self.mario[self.death_count].update()
                    self.pygame.display.update()
                    self.clock.tick(self.max_frame_rate)

                self.resetLevel()
                self.death_count += 1

            print(str(self.gen) + " | " + str(sum(sum(self.mario[self.fittest_index].brain.fc1.weight.data))))

            self.fittest_index = self.grader.calc_fittest(self.mario)
            self.fittest.append(self.mario[self.fittest_index].fitness)
            self.plotter.show(self.fittest)

            if self.grader.Pass:
                self.gt.saveModel(self.mario[self.fittest_index])

            self.gt.clone(self.mario, self.fittest_index)

            if self.isMut:
                self.gt.mutate(self.mario, self.num_best)

            self.gen += 1

