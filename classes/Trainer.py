from classes.Model import Model
#from classes.Input import Input
import torch

class Trainer:
    def __init__(self):
        self.pop = 10
        self.bots = [Model().share_memory() for _ in range(self.pop)]
        print(self.bots[0])
        self.random = torch.randn(5, 5)
        self.params = list(self.bots[0].parameters())
        print(len(self.params))
        print(self.params[0].size())  # conv1's .weight

    def output(self, input):
        #print(input)
        out = self.bots[0](input)
        print(out[0])
        return out

#trainer = Trainer()

#trainer.output()