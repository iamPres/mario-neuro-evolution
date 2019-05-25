# Super Mario Neuro-Evolution Implementation in Python

This is inspired by mx0c: https://github.com/mx0c/super-mario-python

## Setup

### 1. Install Torch

Here's how to install torch: https://pytorch.org/
I reccomend installing it with conda.

### 2. Install Dependencies

* $ pip install -r requirements.txt

## Standalone windows build

* $ pip install py2exe
* $ python compile.py py2exe

## Usage

This trainer comes with many useful debugging fuctions:  
Press LEFT SHIFT to enable / disable mutation for the following iteration  
Press RIGHT to fast foward through a bot if it is standing still (DO NOT USE IF BOT IS MOVING)  
Press S to save the current bot's neural architecture into the Models/ folder  
Press L to load the any neual architecture located in the root project directory

## Net Architecture

This net takes in 8 bits of input data to look at tiles that it could potenitally stand on up to 8 tiles away. It passes that data through an MLP with two linear layers. The bot has four outputs: Left, Right, Jump, and boost.

## Program Layout

Model.py - Defines neural architecture  
GameManager.py - Configures and resets training exersizes, holds all training parameters  
GeneticTrainer.py - Organizes methods relating to the genetic training process  
Grader.py - Calculates fitness of each bot, finds fittest bot in iteration  
Mario.py - Encapsulates Model() instance, organized as an object array. Defines inputs to net  
Inputs.py - Passes output of the net into the game instance  
Models/ - Holds all saved neural architectures  

## Current state (Fitness vs. Time):
![Alt text](img/WORKING.png "current state")
