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
import pygame

# Apple class defines the apple object in the game
class Apple:
    def __init__(self, gameDisplay, display_width, display_height, block_size, snake_list):
        # Initialize the apple with a random position that does not overlap the snake
        self.gameDisplay = gameDisplay
        self.block_size = block_size
        self.update_apple_pos(snake_list)  # Generate initial position

    def update_apple_pos(self, snake_list):
        # Randomly position the apple within the grid, avoiding the snake's body
        self.x = random.randint(0, 14) * 10
        self.y = random.randint(0, 14) * 10
        # Ensure apple does not spawn on the snake's body
        while [self.x, self.y] in snake_list:
            self.x = random.randint(0, 14) * 10
            self.y = random.randint(0, 14) * 10

    def get_apple_pos(self):
        # Return the current position of the apple
        return self.x, self.y

    def display(self):
        # Render the apple as a red rectangle on the game display
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), [self.x, self.y, 10, 10])

# Snake class defines the snake object and its behavior
class Snake:
    def __init__(self, gameDisplay, display_width, display_height, block_size):
        # Initialize the snake with a single block
        self.gameDisplay = gameDisplay
        self.snake_list = [[70, 70]]  # Initial position of the snake
        self.snake_length = 1  # Initial length
        self.block_size = block_size  # Size of each block
        self.direction = "right"  # Initial direction

    def is_alive(self):
        # Check if the snake collides with walls or itself
        head = self.snake_list[-1]
        # Check for collisions with walls
        if not (0 <= head[0] < 150 and 0 <= head[1] < 150):
            return False
        # Check for collisions with itself
        if head in self.snake_list[:-1]:
            return False
        return True

    def get_state(self, apple_pos):
        # Calculate the state of the snake for reinforcement learning
        head = self.snake_list[-1]
        # State includes relative position to apple, danger flags, and direction
        return [
            head[0] - apple_pos[0],  # X distance to apple
            head[1] - apple_pos[1],  # Y distance to apple
            int(self.is_danger_ahead()),  # Danger ahead
            int(self.is_danger_left()),  # Danger to the left
            int(self.is_danger_right()),  # Danger to the right
            self.direction  # Current direction
        ]

    def is_danger_ahead(self):
        # Check for danger directly in front of the snake
        head = self.snake_list[-1]
        if self.direction == "up" and (head[1] - self.block_size < 0 or [head[0], head[1] - self.block_size] in self.snake_list):
            return True
        if self.direction == "down" and (head[1] + self.block_size >= 150 or [head[0], head[1] + self.block_size] in self.snake_list):
            return True
        if self.direction == "left" and (head[0] - self.block_size < 0 or [head[0] - self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "right" and (head[0] + self.block_size >= 150 or [head[0] + self.block_size, head[1]] in self.snake_list):
            return True
        return False

    def is_danger_left(self):
        # Check for danger to the left of the snake
        head = self.snake_list[-1]
        if self.direction == "up" and (head[0] - self.block_size < 0 or [head[0] - self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "down" and (head[0] + self.block_size >= 150 or [head[0] + self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "left" and (head[1] + self.block_size >= 150 or [head[0], head[1] + self.block_size] in self.snake_list):
            return True
        if self.direction == "right" and (head[1] - self.block_size < 0 or [head[0], head[1] - self.block_size] in self.snake_list):
            return True
        return False

    def is_danger_right(self):
        # Check for danger to the right of the snake
        head = self.snake_list[-1]
        if self.direction == "up" and (head[0] + self.block_size >= 150 or [head[0] + self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "down" and (head[0] - self.block_size < 0 or [head[0] - self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "left" and (head[1] - self.block_size < 0 or [head[0], head[1] - self.block_size] in self.snake_list):
            return True
        if self.direction == "right" and (head[1] + self.block_size >= 150 or [head[0], head[1] + self.block_size] in self.snake_list):
            return True
        return False

    def move(self):
        # Update the snake's position based on its current direction
        head = self.snake_list[-1]
        if self.direction == "up":
            new_head = [head[0], head[1] - self.block_size]
        elif self.direction == "down":
            new_head = [head[0], head[1] + self.block_size]
        elif self.direction == "left":
            new_head = [head[0] - self.block_size, head[1]]
        elif self.direction == "right":
            new_head = [head[0] + self.block_size, head[1]]

        # Add the new head to the snake's body
        self.snake_list.append(new_head)
        # Remove the tail if the snake's length exceeds its allowed size
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]

    def grow(self):
        # Increase the snake's length when it eats an apple
        self.snake_length += 1

    def display(self):
        # Render the snake as a series of green rectangles on the game display
        for segment in self.snake_list:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), [segment[0], segment[1], self.block_size, self.block_size])
