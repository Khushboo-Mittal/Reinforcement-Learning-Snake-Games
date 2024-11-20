# ================================================================
# Snake Game Implementation for Q-Learning
# ================================================================
# This script implements the Snake game, which will be used for 
# training a Q-learning agent. The game includes all necessary 
# functions to run the game, reset the game state, update the snake's 
# position, and provide feedback (reward) based on the snake's actions.
#
# Metadata:
# Author: Harshita Jangde
# Date Created: 20-11-2024
# Purpose: Implement Snake game to interact with Q-learning agent
# ================================================================

import pygame
import random
import numpy as np

class SnakeGame:
    def __init__(self, width=400, height=400, block_size=20):
        # Initialize game parameters: screen width, height, and block size
        self.width = width
        self.height = height
        self.block_size = block_size
        self.reset_game()  # Reset the game state
        
        # Initialize Pygame
        pygame.init()
        self.font = pygame.font.Font(None, 34)  # Font for rendering score and episode number
        self.screen = pygame.display.set_mode((self.width, self.height))  # Set up the screen
        pygame.display.set_caption('Q-Learning Snake')  # Set window title
        self.clock = pygame.time.Clock()  # Initialize clock for frame rate control

    def reset_game(self):
        # Reset the snake and food for a new game
        self.snake = [(self.width // 2, self.height // 2)]  # Start snake at the center
        self.direction = (0, -self.block_size)  # Initial snake direction (up)
        self.food = self._place_food()  # Place food randomly
        self.game_over = False  # Game is not over at the start
        self.score = 0  # Score is zero at the start

    def _place_food(self):
        # Randomly place food on the grid, avoiding the snake's body
        while True:
            x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
            y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size
            if (x, y) not in self.snake:  # Ensure food doesn't spawn where the snake is
                return (x, y)

    def step(self, action):
        # Action mapping: [0: Up, 1: Down, 2: Left, 3: Right]
        directions = [(0, -self.block_size), (0, self.block_size), (-self.block_size, 0), (self.block_size, 0)]
        
        # Prevent 180-degree turns (e.g., can't go left if you're moving right)
        if not ((action == 0 and self.direction == (0, self.block_size)) or   # Up while moving down
                (action == 1 and self.direction == (0, -self.block_size)) or  # Down while moving up
                (action == 2 and self.direction == (self.block_size, 0)) or   # Left while moving right
                (action == 3 and self.direction == (-self.block_size, 0))):   # Right while moving left
            self.direction = directions[action]  # Change direction based on action

        # Move snake by adding a new head in the current direction
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        self.snake.insert(0, new_head)  # Add new head to the snake body

        # Check if the snake hits the wall or itself
        if (new_head[0] < 0 or new_head[0] >= self.width or 
            new_head[1] < 0 or new_head[1] >= self.height or 
            new_head in self.snake[1:]):  # Check if new head collides with the body
            self.game_over = True  # End the game if there's a collision
            return -10  # Negative reward for dying

        # Check if the snake eats food
        if new_head == self.food:
            self.score += 1  # Increase score when food is eaten
            self.food = self._place_food()  # Place new food after eating
            reward = 10  # Positive reward for eating food
        else:
            self.snake.pop()  # Remove the tail of the snake if no food was eaten
            reward = 0  # No reward for a normal move

        return reward  # Return the reward for the current action

    def get_state(self):
        # Return a simplified state representation:
        # [food position relative to snake, dangers (walls, body)]
        head_x, head_y = self.snake[0]  # Get the position of the snake's head
        food_left = int(self.food[0] < head_x)  # 1 if food is left of the snake
        food_right = int(self.food[0] > head_x)  # 1 if food is right of the snake
        food_up = int(self.food[1] < head_y)  # 1 if food is above the snake
        food_down = int(self.food[1] > head_y)  # 1 if food is below the snake

        # Check for dangers (walls or the snake's body) in all 4 directions
        danger_left = int((head_x - self.block_size, head_y) in self.snake or head_x - self.block_size < 0)
        danger_right = int((head_x + self.block_size, head_y) in self.snake or head_x + self.block_size >= self.width)
        danger_up = int((head_x, head_y - self.block_size) in self.snake or head_y - self.block_size < 0)
        danger_down = int((head_x, head_y + self.block_size) in self.snake or head_y + self.block_size >= self.height)

        # Return a tuple representing the state: food directions and danger directions
        return (food_left, food_right, food_up, food_down, danger_left, danger_right, danger_up, danger_down)

    def render(self, score, episode):
        # Handle events like closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit Pygame
                quit()         # Exit the program

        # Draw the game using Pygame
        self.screen.fill((255, 255, 255))  # Clear the screen (white background)
        for block in self.snake:  # Draw each part of the snake
            pygame.draw.rect(self.screen, (0, 100, 0), (*block, self.block_size, self.block_size))  # Green snake blocks
        pygame.draw.rect(self.screen, (100, 0, 0), (*self.food, self.block_size, self.block_size))  # Red food

        # Display the score and episode number on the screen
        score_text = self.font.render(f"Score: {score}", True, (0,0,0))  # Create score text
        episode_text = self.font.render(f"Episode: {episode}", True, (0,0,0))  # Create episode text
        self.screen.blit(score_text, (10, 10))  # Position score at top-left corner
        self.screen.blit(episode_text, (10, 40))  # Position episode number below score
        pygame.display.flip()  # Update the screen
        self.clock.tick(10)  # Control the frame rate (10 frames per second)

    def close(self):
        # Close the Pygame window when done
        pygame.quit()
