from classes.Model import Model
import torch

class GeneticTrainer:
    def __init__(self):
        self.mut_rate = 0.2

    def clone(self, list, fittest):
        state_dict = list[fittest].brain.state_dict()
        for bot in list:
            bot.brain.load_state_dict(state_dict)

    def mutate(self, list, num_best):
        for i, bot in enumerate(list[:num_best]):
            new_genes = Model()
            for param, param_new in zip(bot.brain.parameters(), new_genes.parameters()):
                mask = torch.rand(param.data.size()) < self.mut_rate / (i + 1)
                param.data[mask] = param_new.data[mask]

    def saveModel(self, bot):
        torch.save(bot.brain.state_dict(),
                   f'bot.mdl')  # Save torch model

    def loadModel(self, list):
        for i in list:
            i.brain.load_state_dict(torch.load('bot.mdl'))