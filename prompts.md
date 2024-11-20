# Prompts for Reinforcement Learning Project

## Business Problem Statement
Develop reinforcement learning algorithms to enable an intelligent agent to learn optimal strategies in various environments. The project focuses on training agents through trial-and-error methods to improve decision-making capabilities, applicable to real-world scenarios such as robotics and game AI.

---

## Prompts for Each Algorithm

### SARSA Snake Game
- **Objective**: Create a SARSA-based agent to play the Snake Game.
- **Prompt**: Implement the SARSA algorithm to update a Q-table based on state-action transitions, rewarding the agent for eating apples and penalizing for collisions.
- **Success Criteria**: Agent learns a strategy to maximize score by avoiding obstacles and consuming apples efficiently.

### Q-Learning Snake Game
- **Objective**: Build a Q-learning agent for the Snake Game.
- **Prompt**: Use Q-learning to enable the agent to update a Q-table, balancing exploration and exploitation to learn optimal movement strategies.
- **Success Criteria**: Agent achieves high scores by learning to avoid walls and its own body while seeking apples.

### DQN Snake Game
- **Objective**: Develop a Deep Q-Network (DQN) agent for the Snake Game.
- **Prompt**: Implement a neural network-based Q-learning approach, using experience replay and target networks to approximate Q-values for state-action pairs.
- **Success Criteria**: Agent demonstrates consistent strategy by maximizing score through learned actions without manual adjustments.

### Frozen Lake Actor-Critic (A2C)
- **Objective**: Implement an Actor-Critic agent using the A2C algorithm for Frozen Lake.
- **Prompt**: Create an actor-critic setup where the agent learns a policy and estimates value functions, aiming to navigate the frozen lake environment to reach the goal safely.
- **Success Criteria**: Agent shows a high success rate in reaching the goal by avoiding hazards, using a balance of actor and critic feedback.

---

## End Note
These prompts provide a structured guide for implementing and training each reinforcement learning algorithm, focusing on practical applications and measurable performance.
