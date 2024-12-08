# Reinforcement Learning Snake Games

This project demonstrates the implementation of various **Reinforcement Learning (RL)** algorithms applied to the classic **Snake Game**. The aim is to train an AI agent to play the game autonomously by learning optimal strategies through interactions with the environment. Each algorithm is implemented in its respective folder with detailed explanations.

## Overview

Reinforcement learning algorithms like **Deep Q-Learning (DQN)**, **SARSA**, and **Q-Learning** are explored in this project. Each approach showcases a unique way to train the agent, balancing exploration and exploitation to maximize rewards. The trained agents demonstrate adaptive gameplay, optimizing their performance over time.

### Key Features

- **Game Environment**: A grid-based Snake game environment built using Python and Pygame.
- **Reinforcement Learning Algorithms**:
  - **DQN**: Uses a neural network for action-value function approximation.
  - **SARSA**: Learns on-policy action-value estimates using the SARSA update rule.
  - **Q-Learning**: Implements off-policy learning through Q-value updates.
- **State-Action Representations**: 
  - Encodes the snake's position, food location, and obstacles to guide decision-making.
- **Visualization**: Graphs and logs tracking training performance.

## How to Use

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-repo/reinforcement-learning-snake-games.git
   cd reinforcement-learning-snake-games
   ```

2. Navigate to the desired algorithm folder (e.g., `DQN_SnakeGame`, `SARSA_SnakeGame`, `QLearning_SnakeGame`) for specific instructions.

3. Follow the `README.md` in each folder to set up dependencies, run the training, and visualize results.

## Dependencies

The project relies on Python and several libraries. Install the required dependencies with:

```bash
pip install -r requirements.txt
```

**Common Libraries**:
- Python 3.7+
- Pygame
- NumPy
- Matplotlib

Specific dependencies for neural network-based approaches like DQN may include TensorFlow or PyTorch.

## Additional Notes

Each folder contains a dedicated `README.md` that explains the respective algorithm, its implementation details, and usage.
