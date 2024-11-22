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

import pygame
import matplotlib.pyplot as plt  # Importing for plotting
from ReinforcementLearning import Sarsa  # Importing SARSA class for reinforcement learning
from models import Apple, Snake  # Importing game models for Apple and Snake

pygame.init()  # Initialize all imported pygame modules

# Colors for display
white = (0, 0, 0)  # Background color
black = (255, 255, 255)  # Snake and apple color

# Window size
display_width, display_height = 150, 150  # Dimensions of the game window
block_size = 10  # Size of each block representing a snake segment or apple

# Initialize game display and set window caption
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake Game")

# Set up clock and frames per second
clock = pygame.time.Clock()  # Controls game speed
FPS = 20  # Frames per second for game speed

# Initialize SARSA agent
actions = ["up", "left", "right"]  # Possible actions the agent can take
agent = Sarsa(actions, e=0.01)  # Initialize SARSA agent with exploration rate epsilon
agent.loadQ()  # Load pre-trained Q-table if available

# List to store cumulative rewards of each episode
episode_rewards = []  # Tracks performance over episodes

def training_game(episodes=1000):
    """
    Function to train the SARSA agent in the Snake Game.
    :param episodes: Number of training episodes
    """
    scores = []  # List to store the scores for each episode

    for episode in range(episodes):
        print(f"Episode {episode + 1}")  # Log current episode
        pygame.event.pump()  # Allow pygame to process internal actions
        game_over = False  # Flag to track game-over state

        # Initialize snake and apple objects
        snake = Snake(gameDisplay, display_width, display_height, block_size)
        apple = Apple(gameDisplay, display_width, display_height, block_size, snake.snake_list)

        # Initial state and action
        old_state = snake.get_state(apple.get_apple_pos())  # Get initial state of the environment
        old_action = "up"  # Default initial action
        
        total_reward = 0  # Cumulative reward for the current episode

        while not game_over:
            # Determine new state and action
            new_state = snake.get_state(apple.get_apple_pos())  # Get current state
            new_action = agent.getA(tuple(new_state))  # Choose action based on policy (e-greedy)

            # Set snake's direction based on the chosen action
            if new_action == "up":
                snake.direction = "up"
            elif new_action == "down":
                snake.direction = "down"
            elif new_action == "left":
                snake.direction = "left"
            elif new_action == "right":
                snake.direction = "right"

            # Move the snake in the selected direction
            snake.move()

            # Check if the snake eats the apple
            if snake.snake_list[-1] == list(apple.get_apple_pos()):
                snake.grow()  # Grow the snake upon eating the apple
                apple.update_apple_pos(snake.snake_list)  # Move the apple to a new position
                reward = 500  # Positive reward for eating the apple
            else:
                reward = -10  # Penalty for each step without reward

            # Check if the snake has collided with itself or the wall
            if not snake.is_alive():
                game_over = True  # End the game if the snake dies
                reward = -100  # Penalty for losing the game
                scores.append(snake.snake_length - 1)  # Track score (snake length - 1)

            total_reward += reward  # Update cumulative reward

            # Update the Q-table using SARSA
            agent.updateQ(tuple(old_state), old_action, tuple(new_state), new_action, reward)

            # Transition to the next state-action pair
            old_state = new_state
            old_action = new_action

            # Refresh the game display
            gameDisplay.fill(white)  # Clear the screen
            apple.display()  # Draw the apple
            snake.display()  # Draw the snake
            pygame.display.update()  # Update the display

            # Control the game's speed
            clock.tick(FPS)

        episode_rewards.append(total_reward)  # Store total reward for the episode
        agent.saveQ()  # Save Q-table after each episode

    # Plot rewards after training
    plot_rewards()

def plot_rewards():
    """
    Function to plot cumulative rewards for each training episode.
    """
    plt.plot(episode_rewards)  # Plot the rewards over episodes
    plt.title("Cumulative Rewards per Episode")  # Chart title
    plt.xlabel("Episode")  # X-axis label
    plt.ylabel("Total Reward")  # Y-axis label
    plt.show()  # Display the plot

if __name__ == "__main__":
    training_game()  # Start training the agent
