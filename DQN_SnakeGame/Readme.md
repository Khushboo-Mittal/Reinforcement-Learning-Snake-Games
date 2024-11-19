# DQN Snake Game
---

## Overview

This project demonstrates a **Snake Game** implemented using **Deep Q-Learning (DQN)**. The game involves training an AI agent to play the Snake game autonomously. The agent learns through reinforcement learning by interacting with the game environment, improving its score over multiple episodes.

## Features

- **Deep Q-Learning Agent**: 
  - Utilizes a neural network to predict Q-values for state-action pairs.
  - Implements experience replay for efficient training.
  - Employs an epsilon-greedy policy for exploration and exploitation.

- **Game Environment**: 
  - Built using the `pygame` library.
  - Features grid-based movement, food spawning, and collision handling.

- **Training and Performance Visualization**:
  - Tracks performance metrics like scores and maximum scores per episode.
  - Includes a plotting function to visualize the training results.

## Prerequisites

Ensure you have the following dependencies installed:

- Python 3.7 or later
- `pygame`
- `numpy`
- `matplotlib`
- `tensorflow`
- `keras`

Install the dependencies using:

```bash
pip install pygame numpy matplotlib tensorflow keras
```

## File Structure

- **`dqn.py`**: The main script containing the game logic, DQN agent implementation, and training loop.

## How It Works

### Game Logic

1. **Game Environment**:
   - A `SnakeGame` class defines the environment, including snake movement, food spawning, collision detection, and UI updates.
   - The state representation includes:
     - Snake's head position.
     - Food position.
     - Direction of the snake.

2. **Rewards**:
   - **+10** for eating food.
   - **-1** for moving without eating.
   - **-10** for collisions.

3. **Actions**:
   - `0`: Move forward.
   - `1`: Turn right.
   - `2`: Turn left.

### DQN Agent

- **Neural Network Architecture**:
  - Input layer with six features (state size).
  - Two hidden layers with 64 neurons each and ReLU activation.
  - Output layer with three neurons (one for each action).

- **Learning Parameters**:
  - Discount factor (`gamma`): 0.95.
  - Exploration-exploitation trade-off controlled by `epsilon`.
  - Replay memory size: 5000 experiences.
  - Learning rate: 0.001.

### Training Process

- The agent interacts with the environment for a specified number of episodes.
- Experiences are stored in replay memory.
- After each episode, the agent trains on a batch of experiences.

### Performance Tracking

- Scores and maximum scores are tracked for each episode.
- A graph is plotted at the end of training to show the agent's performance over time.

## Usage

1. Clone or download this repository.

2. Run the script:

   ```bash
   python dqn.py
   ```

3. Adjust the number of training episodes by modifying the `main()` function:

   ```python
   main(episode_number=1000)
   ```

4. The trained model's weights are periodically saved as `.h5` files in the current directory.

## Visualizing Results

After training, the script plots the following metrics:
- **Score per Episode**: The agent's score for each episode.
- **Maximum Score**: The highest score achieved up to each episode.

