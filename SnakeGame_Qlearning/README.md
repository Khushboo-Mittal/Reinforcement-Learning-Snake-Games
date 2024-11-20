# Snake Game with Q-Learning

This project implements a classic Snake game using Q-learning for reinforcement learning. The agent learns how to play the game by interacting with the environment and adjusting its behavior based on rewards.

---

## Table of Contents

- [Reinforcement Learning](#reinforcement-learning)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Q-table Explanation](#q-table-explanation)
- [Game Execution](#game-execution)

---

## Reinforcement Learning

In this project, we use Q-learning, a popular reinforcement learning algorithm, to train an agent to play the Snake game. The agent takes actions to move the snake, receives rewards for eating food, and negative penalties for colliding with walls or itself. The agent learns the optimal policy by interacting with the environment over multiple episodes.

---

## Features

- **Snake Game**: Classic Snake game with dynamic gameplay.
- **Q-Learning Agent**: An AI agent that learns how to play the game through exploration and exploitation of actions.
- **Rewards and Penalties**: Positive rewards for eating food and negative rewards for dying.
- **Customizable Game**: Adjustable grid size, block size, and other parameters.
- **Training Progress**: The agent's learning progress can be observed with the evolving epsilon (exploration rate) and the score.

---

## Installation

To run this project, you need to install the necessary dependencies. You can install them via `pip`:

1. Clone the repository:
   `git clone https://github.com/CodeCrafters-preprod/DIY_ReinforcementLearning.git`
2. Intsall dependencies:
   `pip install -r requirements.txt`

---

## Usage

To train the Q-learning agent, simply run the following command:
`python q_learning.py`
This will begin training the agent, and the game will be rendered every 100 episodes. The agent will improve its performance over time as it learns through trial and error.

---

## Q-table Explanation

The Q-table stores the state-action values that represent the agent’s knowledge about the environment. Each entry in the Q-table corresponds to a state-action pair, with the associated Q-value indicating the expected reward of taking that action in that state.

- **State:** A combination of the snake's position, the relative location of food, and any imminent dangers (like walls or the snake’s body).
- **Action:** The action taken by the agent (moving up, down, left, or right).
- **Q-value:** A measure of the expected long-term reward for taking an action in a given state.
The Q-values are updated using the Bellman equation after each action.

---

## Game Execution

The Snake game is rendered using the pygame library, and the agent's performance can be observed during the training process. The score is displayed on the screen, and the number of episodes is updated as the agent progresses.

After training, the agent's learned Q-table can be saved to a file and reused for further testing or deployment.





