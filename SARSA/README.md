# Snake Game with SARSA Reinforcement Learning

This project implements a **Snake Game** powered by the **SARSA (State-Action-Reward-State-Action)** algorithm. The objective of the game is to train the snake to move optimally, eat apples, and avoid collisions by updating a Q-table through reinforcement learning. The snake makes decisions based on its environment and learns from its experiences during gameplay.

---

## Table of Contents
- [Project Overview](#project-overview)  
- [Features](#features)  
- [Installation](#installation)  
- [How to Run](#how-to-run)  
- [Project Structure](#project-structure)  
- [How It Works](#how-it-works)  
- [Dependencies](#dependencies)  
- [Developer Info](#developer-info)  

---

## Project Overview
This game uses **SARSA reinforcement learning** to train a snake agent. The agent tries to maximize its rewards by:
- Eating apples to gain points.
- Avoiding collisions with walls or itself.
- Learning a Q-table that represents optimal actions for given states.

The project is implemented using **Python 3.11.5** and **Pygame 2.1.0** for visual rendering of the game environment.

---

## Features
- **SARSA Algorithm**: A reinforcement learning algorithm that updates Q-values based on state-action pairs.
- **Q-table Persistence**: The Q-table is saved and loaded using a pickle file to maintain progress between sessions.
- **Epsilon-Greedy Exploration**: The agent balances exploration and exploitation during gameplay.
- **Dynamic Snake Behavior**: The snake changes direction based on trained strategies.
- **Apple Generation**: Apples appear randomly without overlapping with the snake body.

---

## Installation
1. Clone the repository from GitHub.
2. Make sure Python 3.11.5 and Pygame 2.1.0 are installed.

   Use the following commands to install Pygame:
   ```bash
   pip install pygame
   ```

---

## How to Run
1. Open a terminal or command prompt in the project directory.
2. Run the following command to start the game:
   ```bash
   python app.py
   ```

---

## Project Structure
```
SARSA/
│
├── app.py                    # Main entry point to run the game
├── models.py                 # Contains the Apple and Snake classes for the game logic
├── ReinforcementLearning.py  # SARSA algorithm implementation
├── q_table.pkl               # Pickled Q-table for saving and loading learned data
├── agent_reward_figure.png   # Visualization of rewards earned by the agent
├── apple.png                 # Apple image for the game
├── snakehead.png             # Snake head image
└── Q.txt                     # Text representation of the Q-table
```

---

## How It Works

### 1. **Reinforcement Learning (SARSA)**
- **SARSA Algorithm**:  
   - The Q-table stores the expected rewards for state-action pairs.
   - The snake selects actions based on an **epsilon-greedy policy** (random or optimal).
   - After each move, the Q-value is updated using the formula:  
     \[
     Q(s, a) = Q(s, a) + \alpha \left[ r + \gamma Q(s', a') - Q(s, a) \right]
     \]  
   - Where:
     - \(Q(s, a)\) is the Q-value of the current state-action pair.
     - \(r\) is the reward.
     - \(Q(s', a')\) is the future Q-value.
     - \(\alpha\) is the learning rate, and \(\gamma\) is the discount factor.

### 2. **Game Logic**
- **Snake Movement and Collision**:  
   - The snake moves one block at a time, and its body grows when it eats an apple.
   - If the snake collides with the wall or itself, the game resets.

- **State Representation**:  
   - The snake’s state includes:
     - Distance to the apple.
     - Danger indicators (ahead, left, and right).
     - Current direction of the snake.

### 3. **Apple Placement**
- **Randomized Apple Position**:  
   - Apples appear at random positions on the grid.
   - If the apple overlaps with the snake body, a new position is generated.

---

## Dependencies
- **Python**: 3.11.5  
- **Pygame**: 2.1.0  
   Install dependencies with:
   ```bash
   pip install pygame
   ```

---

## Developer Info
- **Architect**: Khushboo Mittal  
- **Version**: V 1.0 (24 October 2024)  
- **Unit Test**: Pass  
- **Integration Test**: Pass  



