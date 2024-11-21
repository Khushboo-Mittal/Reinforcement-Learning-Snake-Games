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
from ReinforcementLearning import Sarsa
from models import Apple, Snake

pygame.init()

# Colors
white = (0, 0, 0)
black = (255, 255, 255)

# Window size
display_width, display_height = 150, 150
block_size = 10

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
FPS = 20

# Initialize SARSA agent
actions = ["up", "left", "right"]
agent = Sarsa(actions, e=0.01)
agent.loadQ()  # Load Q-table if available

# List to store cumulative rewards of each episode
episode_rewards = []

def training_game(episodes=1000):
    scores = []
    
    for episode in range(episodes):
        print(f"Episode {episode + 1}")
        pygame.event.pump()
        game_over = False

        # Initialize snake and apple
        snake = Snake(gameDisplay, display_width, display_height, block_size)
        apple = Apple(gameDisplay, display_width, display_height, block_size, snake.snake_list)

        # Initial state and action
        old_state = snake.get_state(apple.get_apple_pos())
        old_action = "up"
        
        # Track cumulative reward for the current episode
        total_reward = 0

        while not game_over:
            # Get new state and action
            new_state = snake.get_state(apple.get_apple_pos())
            new_action = agent.getA(tuple(new_state))

            # Set the direction based on the selected action
            if new_action == "up":
                snake.direction = "up"
            elif new_action == "down":
                snake.direction = "down"
            elif new_action == "left":
                snake.direction = "left"
            elif new_action == "right":
                snake.direction = "right"

            # Move the snake
            snake.move()

            # Check if the snake eats the apple
            if snake.snake_list[-1] == list(apple.get_apple_pos()):
                snake.grow()  # Increase the snake's length
                apple.update_apple_pos(snake.snake_list)
                reward = 500  # Reward for eating the apple
            else:
                reward = -10  # Default penalty for each step

            # Check if the snake is alive
            if not snake.is_alive():
                game_over = True
                reward = -100  # Penalty for dying
                scores.append(snake.snake_length - 1)

            # Add reward to the cumulative episode reward
            total_reward += reward

            # Update Q-table using SARSA
            agent.updateQ(tuple(old_state), old_action, tuple(new_state), new_action, reward)

            # Prepare for the next step
            old_state = new_state
            old_action = new_action

            # Update display
            gameDisplay.fill(white)
            apple.display()
            snake.display()
            pygame.display.update()

            # Control game speed
            clock.tick(FPS)

        episode_rewards.append(total_reward)  # Store the total reward for this episode
        agent.saveQ()  # Save Q-table after each episode

    # After training is done, plot the rewards
    plot_rewards()

def plot_rewards():
    # Plot the rewards over the episodes
    plt.plot(episode_rewards)
    plt.title("Cumulative Rewards per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.show()

if __name__ == "__main__":
    training_game()
