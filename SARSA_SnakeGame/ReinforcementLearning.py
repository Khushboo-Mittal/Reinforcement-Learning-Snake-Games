# META DATA - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Developer details: 
        # Name: Khushboo Mittal
        # Role: Architect
    # Version:
        # Version: V 1.0 (24 October 2024)
            # Developers: Khushboo Mittal
            # Unit test: Pass
            # Integration test: Pass
     
     # Description: This code snippet implements a SARSA-based Snake Game using Pygame. The snake is trained through 
     # Reinforcement Learning to learn optimal movement strategies using the SARSA algorithm. The objective is to 
     # avoid collisions while eating randomly placed apples. The game tracks the agent's state and updates the Q-table accordingly.

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python: 3.12.4
            # Pygame: 2.6.1
            # matplotlib==3.9.2
            # numpy==2.1.3
        
            
            
#to run: python app.py  
# Inspiration for this code was taken from GeeksForGeeks article "SARSA Reinforcement Learning". 

import random
import pickle
import numpy as np

class Sarsa:
    def __init__(self, actions, e=0.1, alpha=0.1, gamma=0.9):
        self.Q = {}  # Initialize the Q-table as an empty dictionary to store state-action values
        self.A = actions  # List of possible actions that the agent can take
        self.e = e  # Epsilon for the epsilon-greedy policy (exploration rate)
        self.alpha = alpha  # Learning rate for updating Q-values
        self.gamma = gamma  # Discount factor for future rewards

    def getQ(self, state, action):
        # Retrieve the Q-value for a given state-action pair
        # If the Q-value doesn't exist, return a small random value to initialize it
        return self.Q.get((state, action), random.uniform(-0.1, 0.1))

    def updateQ(self, s1, a1, s2, a2, reward):
        # Update the Q-value using the SARSA update rule
        current_q = self.getQ(s1, a1)  # Get the current Q-value for the state-action pair
        future_q = self.getQ(s2, a2)  # Get the Q-value for the next state-action pair
        # Compute the new Q-value based on the reward and future Q-value
        new_q = current_q + self.alpha * (reward + self.gamma * future_q - current_q)
        # Update the Q-table with the new Q-value
        self.Q[(s1, a1)] = new_q

    def getA(self, state):
        # Determine the action to take in a given state using an epsilon-greedy policy
        if random.random() < self.e:
            return random.choice(self.A)  # Choose a random action with probability epsilon (exploration)
        # Compute Q-values for all actions in the current state
        q_values = [self.getQ(state, a) for a in self.A]
        max_q = max(q_values)  # Find the maximum Q-value
        # Identify all actions that have the maximum Q-value
        best_actions = [a for a, q in zip(self.A, q_values) if q == max_q]
        # Choose randomly among the best actions to break ties
        return random.choice(best_actions)

    def saveQ(self, filename="q_table.pkl"):
        # Save the Q-table to a file using pickle for persistence
        with open(filename, "wb") as f:
            pickle.dump(self.Q, f)

    def loadQ(self, filename="q_table.pkl"):
        # Load a saved Q-table from a file
        try:
            with open(filename, "rb") as f:
                self.Q = pickle.load(f)  # Load the Q-table into memory
        except FileNotFoundError:
            # Handle the case where the file doesn't exist and start fresh
            print("No Q-table found, starting fresh.")
