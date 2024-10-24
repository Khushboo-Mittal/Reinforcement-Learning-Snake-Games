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
import pygame

class Apple:
    def __init__(self, gameDisplay, display_width, display_height, block_size, snake_list):
        self.gameDisplay = gameDisplay
        self.block_size = block_size
        self.update_apple_pos(snake_list)

    def update_apple_pos(self, snake_list):
        self.x = random.randint(0, 14) * 10
        self.y = random.randint(0, 14) * 10
        while [self.x, self.y] in snake_list:
            self.x = random.randint(0, 14) * 10
            self.y = random.randint(0, 14) * 10

    def get_apple_pos(self):
        return self.x, self.y

    def display(self):
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), [self.x, self.y, 10, 10])

class Snake:
    def __init__(self, gameDisplay, display_width, display_height, block_size):
        self.gameDisplay = gameDisplay
        self.snake_list = [[70, 70]]
        self.snake_length = 1
        self.block_size = block_size
        self.direction = "right"

    def is_alive(self):
        head = self.snake_list[-1]
        # Check for collisions with walls
        if not (0 <= head[0] < 150 and 0 <= head[1] < 150):
            return False
        # Check for collisions with self
        if head in self.snake_list[:-1]:
            return False
        return True

    def get_state(self, apple_pos):
        head = self.snake_list[-1]
        # State now includes: relative position to apple, danger in directions, and current direction
        return [
            head[0] - apple_pos[0],  # X distance to apple
            head[1] - apple_pos[1],  # Y distance to apple
            int(self.is_danger_ahead()),
            int(self.is_danger_left()),
            int(self.is_danger_right()),
            self.direction
        ]

    def is_danger_ahead(self):
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
        head = self.snake_list[-1]
        if self.direction == "up":
            new_head = [head[0], head[1] - self.block_size]
        elif self.direction == "down":
            new_head = [head[0], head[1] + self.block_size]
        elif self.direction == "left":
            new_head = [head[0] - self.block_size, head[1]]
        elif self.direction == "right":
            new_head = [head[0] + self.block_size, head[1]]

        # Update the snake's body
        self.snake_list.append(new_head)
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]  # Remove the tail

    def grow(self):
        self.snake_length += 1  # Increase the length of the snake

    def display(self):
        for segment in self.snake_list:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), [segment[0], segment[1], self.block_size, self.block_size])
