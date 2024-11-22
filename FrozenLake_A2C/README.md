# FrozenLake Game with Actor Critic (A2C) Reinforcement Learning

This project contains the implementation of a FrozenLake Game trained with the **Actor-Critic (A2C)** algorithm. The objective of the game is to train the model to find path from starting point to the finishing point while avoiding the 'holes'.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Acknowlwdgement](#acknowledgement)
- [Features](#features)  
- [Installation](#installation)  
- [How to Run](#how-to-run)  
- [Project Structure](#project-structure)  
- [How It Works](#how-it-works)  
- [Dependencies](#dependencies)  
- [Developer Info](#developer-info)  

---

## Project Overview
This project uses the Actor-Critic (A2C) reinforcement learning algorithm to train an agent in a FrozenLake environment. The agent learns to maximize rewards by:

Reaching the goal while avoiding holes on the board.
Learning an optimal policy through an actor-critic approach, where the actor selects actions, and the critic estimates the value of each state.
Leveraging both policy gradients and value updates to improve over time.
The project is implemented using **Python 3.11.0** and **TensorFlow 2.16.1** for model building and training.

---

## Acknowledgement
Inspiration was taken by GeeksForGeeks Article "Actor-Critic Algorithm in Reinforcement Learning".

---

## Features
- **A2C Algorithm**: Combines actor and critic models to update policies and state values simultaneously.
- **Model Persistence**: Actor and critic model weights are saved using a pickle file to - retain progress between sessions.
- **Epsilon-Greedy Exploration**: The agent balances exploration and exploitation during training.
- **Visual Environment Updates**: The environment grid is rendered dynamically to display the agent's progress.
- **Adjustable Rewards**: Rewards are modified based on the agent's actions and outcomes to improve learning.

---

## Installation
1. Clone the repository from GitHub.
2. Make sure Python 3.11.5 and TensorFlow 2.16.1 are installed.

---

## How to Run
1. Open a terminal or command prompt in the project directory.
2. Run the following command to start training the agent:
   ```bash
   python FrozenLake_ActorCritic.py
   ```
   
---

## Project Structure
```
A2C_FrozenLake/
│
├── FrozenLake_A2C.py          # Main script to run the training and environment visualization
├── actor_model_weights.pkl    # Saved actor model weights
├── critic_model_weights.pkl   # Saved critic model weights
├── agent_success_rate.png     # Visualization of the agent's success rate over episodes
├── prompts.md     # Business problem statement and conceptual questions for the A2C algorithm
├── requirements.txt     # required libraries for the implementation
└── README.md                  # Project documentation

```

---

## How It Works

### 1. **Reinforcement Learning (SARSA)**
- **Actor-Critic Algorithm**:  
- The actor model predicts the action probabilities for the current state.
- The critic model estimates the value of the current state.
- The agent selects actions based on an epsilon-greedy policy to balance exploration and exploitation.
- After each move, both the actor and critic are updated using gradients derived from the advantage, calculated as:
advantage = 𝑟 + 𝛾 ⋅ value of next state − value of current state
- The actor loss is the negative log probability of the chosen action, scaled by the advantage. The critic loss is the squared error of the advantage.
- It makes into a continuous update mechanism where policies (actions) and values (states) evolve in sync.

### 2. **Game Logic**
- **FrozenLake Environment:**:  
  - The agent moves within a grid representing a frozen lake with a goal, holes, and safe tiles.
  - Moving into a hole results in a negative reward, while reaching the goal provides a positive reward.
  - Episodes terminate upon reaching the goal or falling into a hole, resetting the environment for the next episode.

- **State Representation**:  
  - The environment states are represented by the grid position of the agent.
  - The A2C algorithm uses this information to determine optimal actions at each position.

---

## Dependencies
- **Python**: 3.11.0  
- **TensorFlow**: 2.16.1 
   Install dependencies with:
   ```bash
   pip install tensorflow==2.16.1
   ```

---
