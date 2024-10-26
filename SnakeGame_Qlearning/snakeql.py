#-----------------------------------------------------------------------------------------------------------------------------------


# This code is based on the tutorial "AI Learns to Play Snake - Q Learning Explanation" by "Tech Tribe"


#-----------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import random
from snake import LearnSnake
import pickle

class SnakeQAgent():
    def __init__(self):
        # define initial parameters
        self.discount_rate = 0.95 #how much future rewards are considered compared to immediate rewards. A value of 0.95 means that future rewards are valued highly.
        self.learning_rate = 0.1 # how much new information overrides old information in the Q-table.
        self.eps = 1.0 #initial exploration rate, where 1.0 means the agent will explore (choose random actions) all the time at the beginning.
        self.eps_discount = 0.9992 #to reduce the exploration rate over time
        self.min_eps = 0.001 #This sets a floor for the exploration rate, ensuring the agent never stops exploring entirely.
        self.num_episodes = 1000
        self.table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))  # initializes the Q-table as a NumPy array filled with zeros
        self.env = LearnSnake()
        self.score = [] #keep track of the scores obtained by the agent in each episode.
        self.survived = [] # how long the agent survived in each episode.
        
    # epsilon-greedy action choice
    def get_action(self, state):
        # select random action (exploration)
        if random.random() < self.eps: #This line generates a random number between 0 and 1. If this number is less than self.eps (the exploration rate), the agent will choose a random action
            return random.choice([0, 1, 2, 3])
        
        # select best action (exploitation)
        return np.argmax(self.table[state])
    
    def train(self):
        for i in range(1, self.num_episodes + 1):
            self.env  = LearnSnake()
            steps_without_food = 0
            length = self.env.snake_length
            
            # print updates
            if i % 25 == 0:
                print(f"Episodes: {i}, score: {np.mean(self.score)}, survived: {np.mean(self.survived)}, eps: {self.eps}, lr: {self.learning_rate}")
                self.score = []
                self.survived = []
               
            # occasionally save latest model
            if (i < 500 and i % 10 == 0) or (i >= 500 and i < 1000 and i % 200 == 0) or (i >= 1000 and i % 500 == 0):
                with open(f'SnakeGame_Qlearning/pickle/{i}.pickle', 'wb') as file:
                    pickle.dump(self.table, file)
                
            current_state = self.env.get_state()
            self.eps = max(self.eps * self.eps_discount, self.min_eps)
            #self.eps_discount is factor used to gradually reduce self.eps
            #self.min_eps is the minimum value that self.eps can reach. It ensures that the agent retains some level of exploration even after many episodes.
            done = False
            while not done:
                # choose action and take it
                action = self.get_action(current_state)
                new_state, reward, done = self.env.step(action)
                
                # Bellman Equation Update
                self.table[current_state][action] = (1 - self.learning_rate)\
                    * self.table[current_state][action] + self.learning_rate\
                    * (reward + self.discount_rate * max(self.table[new_state])) 
                current_state = new_state
                
                steps_without_food += 1
                if length != self.env.snake_length:
                    length = self.env.snake_length
                    steps_without_food = 0
                if steps_without_food == 1000:
                    # break out of loops
                    break
            
            # keep track of important metrics
            self.score.append(self.env.snake_length - 1)
            self.survived.append(self.env.survived)
        
if __name__ == '__main__':
    # Create an instance of the SnakeQAgent class
    agent = SnakeQAgent()
    # Start the training process for the Q-learning agent
    agent.train()        