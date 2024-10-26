# SNAKE GAME WITH Q-LEARNING
This repository contains a Python implementation of the classic Snake game enhanced with a Q-learning algorithm for AI-driven gameplay. The game utilizes the Pygame library for graphics and user interaction, and it features a visual representation of the snake's movements and the environment.

## Table of Contents
- Reinforcement Learning
- Features
- Installation
- Usage
- Q-table Explanation
- Game Execution

## Reinforcement Learning
Reinforcement Learning (RL) is a type of machine learning where an agent learns to make decisions by taking actions in an environment to maximize cumulative reward. The key components of reinforcement learning include:

- **Agent**: The learner or decision-maker (in this case, the Snake).
- **Environment**: The context within which the agent operates (the game grid).
- **State**: A representation of the current situation of the agent (e.g., the position of the snake and the food).
- **Action**: A set of all possible moves the agent can take (e.g., moving up, down, left, or right).
- **Reward**: A feedback signal that evaluates the outcome of an action (e.g., positive reward for eating food, negative reward for hitting a wall).

## Features
- Interactive Gameplay: Play the classic Snake game with controls for manual gameplay.
- AI Agent: Implemented Q-learning for an AI agent to play the game automatically.
- Visual Representation: A clear visual representation of the snake, food, and score.
- Customizable Parameters: Easily adjustable game settings such as snake speed and scaling.

## Installation
Install necessary python libraries as 
`pip install pygame numpy`

## Usage
To train q_agent run `python snakeql.py`
To start the game with a particular episode, first set the episode number in main function in game.py and run the following command:

`python game.py`

## Q-table Explanation
The Q-table is a multi-dimensional array that stores the expected rewards for each state-action pair. Each dimension represents a feature of the game state, and the last dimension corresponds to the possible actions (up, down, left, right).
`self.table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))`
- The first 12 dimensions represent binary states of the game.
- The last dimension (size 4) corresponds to the available actions.
During training, the Q-values are updated using the Bellman equation, allowing the agent to learn optimal strategies for playing the game.

## Game Execution
The run_game function is the main driver for executing the game for a specific episode:
- Loads a Q-table from a file corresponding to the episode number.
- Controls the game loop and checks for end conditions.
- Ends the game and displays the score if the snake dies.

