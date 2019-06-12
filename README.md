# Super Mario Neuro-Evolution Implementation in Python

This is inspired by [mx0c](https://github.com/mx0c/super-mario-python)

## Setup

### 1. Install [Torch](https://pytorch.org/)

I reccomend installing it with [conda](https://www.anaconda.com/distribution/)

### 2. Install Dependencies

* $ pip install -r requirements.txt

## Standalone windows build

* $ pip install py2exe
* $ python compile.py py2exe

## Usage

This trainer comes with many useful debugging fuctions:  
Press <b>LEFT SHIFT</b> to enable / disable mutation for the following iteration  
Press <b>RIGHT</b> to fast foward through a bot if it is standing still (DO NOT USE IF BOT IS MOVING)  
Press <b>S</b> to save the current bot's neural architecture into the Models/ folder  
Press <b>L</b> to load the any neual architecture located in the root project directory (The program will only load a model named bot.mdl)

## Net Architecture

This net takes in 8 bits of input data to look at tiles that it could potenitally stand on up to 8 tiles away. It passes that data through an MLP with two linear layers. The bot has four outputs: Left, Right, Jump, and boost.

## Program Layout

<b>Model.py</b> - Defines neural architecture  
<b>GameManager.py</b> - Configures and resets training exersizes, holds all training parameters  
<b>GeneticTrainer.py</b> - Organizes methods relating to the genetic training process  
<b>Grader.py</b> - Calculates fitness of each bot, finds fittest bot in iteration  
<b>Mario.py</b> - Encapsulates Model() instance, organized as an object array. Defines inputs to net  
<b>Inputs.py</b> - Passes output of the net into the game instance  
<b>Models/</b> - Holds all saved neural architectures  

## Performance (Fitness vs. Time):
![Alt text](img/WORKING.png "current state")
