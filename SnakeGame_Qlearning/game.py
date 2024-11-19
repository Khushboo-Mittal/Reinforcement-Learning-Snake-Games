# META DATA - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Developer details: 
        # Name: Harshita Jangde
        # Role: Architect

    # Version:
        # Version: V 1.0 (24 October 2024)
            # Developers: Harshita Jangde
            # Unit test: Pass
            # Integration test: Pass
     
    # Description: This code snippet implements a Q-Learning-based Snake Game using Python and Pygame. The snake is 
    # trained through Reinforcement Learning to learn optimal movement strategies by exploring the environment and 
    # updating the Q-table. The objective of the game is to avoid collisions while eating apples placed randomly in the 
    # game field. The Q-Learning algorithm is used to find an optimal policy for the agent by balancing exploration and 
    # exploitation.

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python: 3.11.5
            # Pygame: 2.1.0
            # NumPy: 1.23.1

#-----------------------------------------------------------------------------------------------------------------------------------


# This code is based on the tutorial "AI Learns to Play Snake - Q Learning Explanation" by "Tech Tribe"


#-----------------------------------------------------------------------------------------------------------------------------------

import random
import numpy as np
import pygame
import pickle
import time


# color class
class Color:
    # Define colors as RGB tuples
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.blue = (30, 60, 90)  
        self.green = (0, 100, 0)
        

class VisualSnake:
    def __init__(self):
        # whether to show episode number at the top
        self.show_episode = False
        self.episode = None
        
        # scale adjusts size of whole board (use 1.0 or 2.0)
        self.scale = 1
        self.game_width = int(600 * self.scale)
        self.game_height = int(400 * self.scale)
        
        # padding for score & episode
        self.padding = int(30 * self.scale)
        self.screen_width = self.game_width # Total screen width
        self.screen_height = self.game_height + self.padding # Total screen height
        
        # Size of the snake and food blocks 
        self.snake_size = int(10 * self.scale)
        self.food_size = int(10 * self.scale)
        self.snake_speed = 40 # Speed of the snake in the game
                 
        self.snake_coords = []
        self.snake_length = 1
        self.dir = "right"
        self.board = np.zeros((self.game_height // self.snake_size, self.game_width // self.snake_size))
        
        self.game_close = False
     
        
        # starting location for the snake
        self.x1 = self.game_width / 2
        self.y1 = self.game_height / 2 + self.padding
        
        # Convert the snake's position from pixel coordinates to grid coordinates
        self.r1, self.c1 = self.coords_to_index(self.x1, self.y1)
        self.board[self.r1][self.c1] = 1
        
        # Initialize changes in coordinates (for movement)     
        self.c_change = 1
        self.r_change = 0
          
        self.food_r, self.food_c = self.generate_food()
        self.board[self.food_r][self.food_c] = 2
        
        # Counter to track how long the snake has survived without eating food
        self.survived = 0
        
        # Initialize Pygame, setting up the environment for the game
        pygame.init()
        # Create an instance of the Color class to manage colors in the game
        self.color = Color()
                  
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) 
        
        # Create a clock object to control the frame rate of the game
        self.clock = pygame.time.Clock()
        # Load a font for displaying text in the game (e.g., score, instructions) 
        self.font = pygame.font.SysFont("bahnschrift", int(18 * self.scale))
        # Variable to track the last direction the snake moved (useful for avoiding opposite direction input)
        self.last_dir = None
        self.step()
        
    def print_score(self, score):
        # Render the score text with green color
        value = self.font.render(f"Score: {score}", True, self.color.green)
        self.screen.blit(value, [500 * self.scale, 10])
        
    def print_episode(self):
        # Check if the episode number should be displayed
        if self.show_episode:
            # Render the episode text with green color
            value = self.font.render(f"Episode: {self.episode}", True, self.color.green)
            # Display the episode number on the screen at specified coordinates
            self.screen.blit(value, [10, 10])
        
    def draw_snake(self):
        # Loop through the snake's coordinates in reverse order (to draw the tail first)
        for i in range(len(self.snake_coords) - 1, -1, -1):
            r, c = self.snake_coords[i]
            x, y = self.index_to_coords(r, c)
            
            # Draw the head of the snake in blue
            if i == len(self.snake_coords) - 1:
                # head square color
                pygame.draw.rect(self.screen, self.color.blue, [x, y, self.snake_size, self.snake_size])
            # Draw the head of the snake in blue
            else:
                pygame.draw.rect(self.screen, self.color.green, [x, y, self.snake_size, self.snake_size])
            
    def game_end_message(self):
        # Render the game over message in red
        mesg = self.font.render("Game over!", True, self.color.red)
        self.screen.blit(mesg, [2 * self.game_width / 5, 2 * self.game_height / 5 + self.padding])
        
    # is there danger in this square (body or wall)
    def is_unsafe(self, r, c):
        if self.valid_index(r, c):
          if self.board[r][c] == 1:
              return 1
          return 0
        else:
          return 1


    def get_state(self):
        head_r, head_c = self.snake_coords[-1]
        state = []
        state.append(int(self.dir == "left"))
        state.append(int(self.dir == "right"))
        state.append(int(self.dir == "up"))
        state.append(int(self.dir == "down"))
        state.append(int(self.food_r < head_r))
        state.append(int(self.food_r > head_r))
        state.append(int(self.food_c < head_c))
        state.append(int(self.food_c > head_c))
        state.append(self.is_unsafe(head_r + 1, head_c))
        state.append(self.is_unsafe(head_r - 1, head_c))
        state.append(self.is_unsafe(head_r, head_c + 1))
        state.append(self.is_unsafe(head_r, head_c - 1))
        return tuple(state) # returns tuple of 12 features
    
                
    def valid_index(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])
      
    # board coordinates <==> row, column conversions
    def index_to_coords(self, r, c):
        x = c * self.snake_size
        y = r * self.snake_size + self.padding
        return (x, y)
    def coords_to_index(self, x, y):
        r = int((y - self.padding) // self.snake_size)
        c = int(x // self.snake_size)
        return (r, c)
    
    # randomly place food
    def generate_food(self):
        # Generate random food coordinates within the game area
        food_c = int(round(random.randrange(0, self.game_width - self.food_size) / self.food_size))
        food_r = int(round(random.randrange(0, self.game_height - self.food_size) / self.food_size))
        
        # Check if the generated food coordinates overlap with the snake
        if self.board[food_r][food_c] != 0:
            # If there is overlap, recursively generate new food coordinates
            food_r, food_c = self.generate_food()
        # Return the valid food coordinates
        return food_r, food_c
    
    def game_over(self):
        # Return the current state of the game (whether the game is over)
        return self.game_close
        
        
    def step(self, action="None"):
        # If no action is provided, randomly choose one
        if action == "None":
            action = random.choice(["left", "right", "up", "down"])
        else:
            # Map the action index to its corresponding direction
            action = ["left", "right", "up", "down"][action]
        
        # Process events in the Pygame event queue
        for event in pygame.event.get():
            pass
 
        # take action
        self.last_dir = self.dir # Store the last direction the snake was moving
        
        # Update the direction and changes in coordinates based on the action taken
        if action == "left" and (self.dir != "right" or self.snake_length == 1):
            self.c_change = -1
            self.r_change = 0
            self.dir = "left"
        elif action == "right" and (self.dir != "left" or self.snake_length == 1):
            self.c_change = 1
            self.r_change = 0
            self.dir = "right"
        elif action == "up" and (self.dir != "down" or self.snake_length == 1):
            self.r_change = -1
            self.c_change = 0
            self.dir = "up"
        elif action == "down" and (self.dir != "up" or self.snake_length == 1):
            self.r_change = 1
            self.c_change = 0
            self.dir = "down"

        # Check if the snake has collided with the boundaries of the game area
        if self.c1 >= self.game_width // self.snake_size or self.c1 < 0 or self.r1 >= self.game_height // self.snake_size or self.r1 < 0:
            self.game_close = True
        # Update the snake's head position based on the direction
        self.c1 += self.c_change
        self.r1 += self.r_change
        
        # Clear the screen with a white color
        self.screen.fill(self.color.white)
        # Draw the game border
        pygame.draw.rect(self.screen, (255, 255, 255), (0, self.padding, self.game_width, self.game_height), 1)

        # Get the coordinates of the food and draw it
        food_x, food_y = self.index_to_coords(self.food_r, self.food_c)
        pygame.draw.rect(self.screen, self.color.red, [food_x, food_y, self.food_size, self.food_size])
        
        self.snake_coords.append((self.r1, self.c1))
        
        
        # Check if the new head position is valid
        if self.valid_index(self.r1, self.c1):
            self.board[self.r1][self.c1] = 1
        
        # Manage the length of the snake
        if len(self.snake_coords) > self.snake_length:
            rd, cd = self.snake_coords[0]
            del self.snake_coords[0]
            if self.valid_index(rd, cd):
                self.board[rd][cd] = 0

        # Check for collision with itself
        for r, c in self.snake_coords[:-1]:
            if r == self.r1 and c == self.c1:
                self.game_close = True
                
        self.draw_snake()
        self.print_score(self.snake_length - 1)
        self.print_episode()
        pygame.display.update()
 
        # snake ate the food
        if self.c1 == self.food_c and self.r1 == self.food_r:
            self.food_r, self.food_c = self.generate_food()
            self.board[self.food_r][self.food_c] = 2
            self.snake_length += 1
        self.survived += 1
    
    def run_game(self, episode):
        self.show_episode = True
        self.episode = episode
        self.print_episode()
        pygame.display.update()

        # pass in pickle file with q table (stored in directory pickle with file name being episode #.pickle)
        filename = f"SnakeGame_Qlearning/pickle/{episode}.pickle"
        with open(filename, 'rb') as file:
            table = pickle.load(file)
        time.sleep(5)
        current_length = 2
        steps_unchanged = 0
        while not self.game_over():
            if self.snake_length != current_length:
                steps_unchanged = 0
                current_length = self.snake_length
            else:
                steps_unchanged += 1
                

            state = self.get_state()
            action = np.argmax(table[state])
            if steps_unchanged == 1000:
                # stop if snake hasn't eaten anything in 1000 episodes (stuck in a loop)
                break
            self.step(action)
            self.clock.tick(self.snake_speed)
        if self.game_over() == True:
            # snake dies
            self.screen.fill(self.color.black)
            pygame.draw.rect(self.screen, (255, 255, 255), (0, self.padding, self.game_width, self.game_height), 1)
            self.game_end_message()
            self.print_episode()
            self.print_score(self.snake_length - 1)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
        return self.snake_length
            

if __name__ == "__main__":
    episode = 1000 # Set the number of episodes to run; you can adjust this value as needed
    snake = VisualSnake() # Create an instance of the VisualSnake class
    snake.run_game(episode) # Call the run_game method with the specified episode count