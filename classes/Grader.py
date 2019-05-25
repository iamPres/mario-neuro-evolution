import math

class Grader:
    def __init__(self):
        self.Pass = False
        self.threshold = 1500

    def calc_fitness(self, mario):
        fitness = mario.rect.x
        return fitness

    def calc_fittest(self, mario):
        fitness = [i.fitness for i in mario]
        fittest = fitness.index(max(fitness))
        if fittest > self.threshold:
            self.Pass = true
        return fittest
