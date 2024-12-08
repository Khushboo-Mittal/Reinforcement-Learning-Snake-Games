# META DATA - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Developer details: 
        # Name: Khushboo Mittal
        # Role: Architect
    # Version:
        # Version: V 1.2 (20 November 2024)
            # Developers: Khushboo Mittal
            # Unit test: Pass
            # Integration test: Pass
     
    # Description: This script implements a Q-learning agent to play the Snake game. 
    # The agent learns through trial and error, using a Q-table to store 
    # state-action values and update them based on rewards received in 
    # the game. The agent follows an epsilon-greedy policy to balance 
    # exploration and exploitation.

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python: 3.10.8
            # pygame==2.5.2
            # numpy==1.23.5

import numpy as np
import random
import pickle
from snake_game import SnakeGame  # Import the SnakeGame class from the snake_game module

class QLearningAgent:
    def __init__(self):
        # Initialize hyperparameters for Q-learning
        self.learning_rate = 0.1  # Rate at which Q-values are updated
        self.discount_rate = 0.9  # Discount factor for future rewards
        self.epsilon = 1.0  # Exploration rate (probability of exploring random actions)
        self.epsilon_decay = 0.995  # Decay rate for exploration (epsilon decreases over time)
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.q_table = {}  # Dictionary to store Q-values for (state, action) pairs
        self.actions = [0, 1, 2, 3]  # Possible actions: 0: Up, 1: Down, 2: Left, 3: Right
        self.score = 0  # Initialize score
        self.game = SnakeGame()  # Create an instance of the SnakeGame

    def get_q_value(self, state, action):
        # Retrieve the Q-value for a given state-action pair from the Q-table
        # If no Q-value exists for this pair, return 0.0 (starting value)
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        # Choose an action based on the epsilon-greedy policy
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: Choose a random action
            return random.choice(self.actions)
        else:
            # Exploitation: Choose the action with the highest Q-value
            q_values = [self.get_q_value(state, action) for action in self.actions]
            return np.argmax(q_values)  # Return the action with the maximum Q-value

    def update_q_value(self, state, action, reward, next_state):
        # Update the Q-value using the Bellman equation
        # Bellman equation: Q(s, a) = Q(s, a) + α * (reward + γ * max_a' Q(s', a') - Q(s, a))
        
        best_next_action = np.argmax([self.get_q_value(next_state, a) for a in self.actions])
        current_q = self.get_q_value(state, action)  # Get the current Q-value for the state-action pair
        target = reward + self.discount_rate * self.get_q_value(next_state, best_next_action)  # Calculate the target
        new_q = current_q + self.learning_rate * (target - current_q)  # Update Q-value based on the learning rate
        self.q_table[(state, action)] = new_q  # Save the new Q-value in the Q-table

    def train(self, episodes=1000):
        # Train the Q-learning agent over a specified number of episodes
        for episode in range(episodes):
            self.game.reset_game()  # Reset the game at the start of each episode
            state = self.game.get_state()  # Get the initial state of the game
            total_reward = 0  # Initialize total reward for this episode
            
            while not self.game.game_over:  # Continue until the game is over
                action = self.choose_action(state)  # Choose an action based on the current state
                reward = self.game.step(action)  # Perform the action in the game, receiving a reward
                next_state = self.game.get_state()  # Get the next state after the action
                
                # Update the Q-table with the new information
                self.update_q_value(state, action, reward, next_state)
                state = next_state  # Update the current state for the next iteration
                total_reward += reward  # Add the reward from this step to the total reward
                
                # Render the game every 100 episodes to visualize training
                if episode % 100 == 0:
                    self.game.render(score=total_reward, episode=episode)
                score = total_reward  # Store the score for the episode

            # Decay the exploration rate over time (epsilon-greedy)
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
            
            # Print the episode statistics every 50 episodes
            if episode % 50 == 0:
                print(f"Episode {episode}, Total Reward (score): {total_reward}, Epsilon: {self.epsilon}")

        # Save the learned Q-table to a file for later use
        with open('q_table.pkl', 'wb') as f:
            pickle.dump(self.q_table, f)  # Use pickle to save the Q-table

        self.game.close()  # Close the game window when training is finished

if __name__ == "__main__":
    # Main script to run the Q-learning agent
    agent = QLearningAgent()  # Create an instance of the QLearningAgent
    agent.train(episodes=1000)  # Train the agent for 1000 episodes
