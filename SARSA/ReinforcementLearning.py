
# import random
# import numpy as np
# import pickle

# class RL:
#     def __init__(self, actions, e=0.05, a=0.1, g=0.95):
#         self.Q = {}
#         self.A = actions
#         self.e = e  # epsilon (exploration rate)
#         self.a = a  # alpha (learning rate)
#         self.g = g  # gamma (discount factor)

#     def getQ(self, state, action):
#         return self.Q.get((state, action), 0.0)

#     def setQ(self, Q):
#         self.Q = Q

#     def loadQ(self):
#         try:
#             self.Q = pickle.load(open("Q.txt", "rb"))
#         except (FileNotFoundError, EOFError):
#             print("Q.txt not found. Initializing empty Q-table.")
#             self.Q = {}

#     def saveQ(self):
#         try:
#             with open("Q.txt", "wb") as f:
#                 pickle.dump(self.Q, f)
#             print("Q-table saved successfully.")
#         except Exception as e:
#             print(f"Error saving Q-table: {e}")

#     def getA(self, state):
#     # Explore: choose a random action with probability epsilon
#         if random.random() < self.e:
#             return random.choice(self.A)  # Random action (explore)

#         # Exploit: choose the action with the maximum Q value
#         q_values = [self.getQ(state, a) for a in self.A]
#         max_q = max(q_values)

#         # Get all actions with the highest Q value and choose randomly among them
#         best_actions = [a for a, q in zip(self.A, q_values) if q == max_q]
#         return random.choice(best_actions)


# class Sarsa(RL):
#     def updateQ(self, state, action, new_state, new_action, reward):
#         q = self.getQ(state, action)
#         new_q = self.getQ(new_state, new_action)
#         self.Q[(state, action)] = q + self.a * (reward + self.g * new_q - q)

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
