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
            # Python: 3.11.5
            # Pygame: 2.1.0
        
            
            
#to run: python app.py  

import random
import pickle
import numpy as np

class Sarsa:
    def __init__(self, actions, e=0.1, alpha=0.1, gamma=0.9):
        self.Q = {}  # Initialize the Q-table
        self.A = actions  # List of possible actions
        self.e = e  # Exploration rate
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor

    def getQ(self, state, action):
        return self.Q.get((state, action), random.uniform(-0.1, 0.1))  # Random small initial Q-values

    def updateQ(self, s1, a1, s2, a2, reward):
        # Update the Q-value using the SARSA formula
        current_q = self.getQ(s1, a1)
        future_q = self.getQ(s2, a2)
        new_q = current_q + self.alpha * (reward + self.gamma * future_q - current_q)
        self.Q[(s1, a1)] = new_q

    def getA(self, state):
        # Epsilon-greedy policy with decaying epsilon
        if random.random() < self.e:
            return random.choice(self.A)  # Random action (explore)
        q_values = [self.getQ(state, a) for a in self.A]
        max_q = max(q_values)
        # Get all actions with the highest Q value and choose randomly among them
        best_actions = [a for a, q in zip(self.A, q_values) if q == max_q]
        return random.choice(best_actions)

    def saveQ(self, filename="q_table.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.Q, f)

    def loadQ(self, filename="q_table.pkl"):
        try:
            with open(filename, "rb") as f:
                self.Q = pickle.load(f)
        except FileNotFoundError:
            print("No Q-table found, starting fresh.")
