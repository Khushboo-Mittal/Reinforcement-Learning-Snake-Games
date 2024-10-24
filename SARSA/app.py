# import pygame
# from ReinforcementLearning import Sarsa
# from models import Apple, Snake

# pygame.init()

# # Colors
# white = (0, 0, 0)
# black = (255, 255, 255)

# # Window size
# display_width, display_height = 150, 150
# block_size = 10

# gameDisplay = pygame.display.set_mode((display_width, display_height))
# pygame.display.set_caption("Snake Game")

# clock = pygame.time.Clock()
# FPS = 20

# # Initialize SARSA agent
# actions = ["up", "left", "right"]
# agent = Sarsa(actions, e=0.01)
# agent.loadQ()  # Load Q-table if available

# def training_game(episodes=10):
#     scores = []

#     for episode in range(episodes):
#         print(f"Episode {episode + 1}")
#         pygame.event.pump()
#         game_over = False

#         # Initialize snake and apple
#         snake = Snake(gameDisplay, display_width, display_height, block_size)
#         apple = Apple(gameDisplay, display_width, display_height, block_size, snake.snake_list)

#         # Initial state and action
#         old_state = snake.get_state(apple.get_apple_pos())
#         old_action = "up"

#         while not game_over:
#             # Get new state and action
#             new_state = snake.get_state(apple.get_apple_pos())
#             new_action = agent.getA(tuple(new_state))
#             print(f"Selected action: {new_action}")

#             # Set the direction based on the selected action
#             if new_action == "up":
#                 snake.direction = "up"
#             elif new_action == "down":
#                 snake.direction = "down"
#             elif new_action == "left":
#                 snake.direction = "left"
#             elif new_action == "right":
#                 snake.direction = "right"

#             # Move the snake
#             snake.move()

#             # Check if the snake eats the apple
#             if snake.snake_list[-1] == list(apple.get_apple_pos()):
#                 snake.grow()  # Increase the snake's length
#                 apple.update_apple_pos(snake.snake_list)
#                 reward = 500  # Reward for eating the apple
#             else:
#                 reward = -10  # Default penalty for each step

#             # Check if the snake is alive
#             if not snake.is_alive():
#                 game_over = True
#                 reward = -100  # Penalty for dying
#                 scores.append(snake.snake_length - 1)

#             # Update Q-table using SARSA
#             agent.updateQ(tuple(old_state), old_action, tuple(new_state), new_action, reward)

#             # Prepare for the next step
#             old_state = new_state
#             old_action = new_action

#             # Update display
#             gameDisplay.fill(white)
#             apple.display()
#             snake.display()
#             pygame.display.update()

#             # Control game speed
#             clock.tick(FPS)

#         agent.saveQ()  # Save Q-table after each episode

#     print(f"Average Score: {sum(scores) / len(scores)}")

# if __name__ == "__main__":
#     training_game(episodes=10)  # Run the game loop for 10 episodes

# import pygame
# from ReinforcementLearning import Sarsa
# from models import Apple, Snake

# pygame.init()

# # Colors
# white = (0, 0, 0)
# black = (255, 255, 255)

# # Window size
# display_width, display_height = 150, 150
# block_size = 10

# gameDisplay = pygame.display.set_mode((display_width, display_height))
# pygame.display.set_caption("Snake Game")

# clock = pygame.time.Clock()
# FPS = 20

# # Initialize SARSA agent with epsilon decay
# actions = ["up", "left", "right", "down"]
# initial_epsilon = 0.1  # Start with more exploration
# min_epsilon = 0.01  # Minimum exploration rate
# decay_rate = 0.995  # Decay epsilon after each episode
# agent = Sarsa(actions, e=initial_epsilon)
# agent.loadQ()  # Load Q-table if available

# def training_game(episodes=1000):
#     scores = []

#     for episode in range(episodes):
#         print(f"Episode {episode + 1}")
#         pygame.event.pump()
#         game_over = False

#         # Initialize snake and apple
#         snake = Snake(gameDisplay, display_width, display_height, block_size)
#         apple = Apple(gameDisplay, display_width, display_height, block_size, snake.snake_list)

#         # Initial state and action
#         old_state = snake.get_state(apple.get_apple_pos())
#         old_action = agent.getA(tuple(old_state))

#         score = 0

#         while not game_over:
#             # Get new state and action
#             new_state = snake.get_state(apple.get_apple_pos())
#             new_action = agent.getA(tuple(new_state))

#             # Set the direction based on the selected action
#             snake.direction = new_action

#             # Move the snake
#             snake.move()

#             # Check if the snake eats the apple
#             if snake.snake_list[-1] == list(apple.get_apple_pos()):
#                 snake.grow()  # Increase the snake's length
#                 apple.update_apple_pos(snake.snake_list)
#                 reward = 500  # Reward for eating the apple
#                 score += 1
#             else:
#                 # Small penalty per step to encourage efficient movement
#                 reward = -1

#             # Check if the snake is alive
#             if not snake.is_alive():
#                 game_over = True
#                 reward = -100  # Penalty for dying
#                 scores.append(score)

#             # Update Q-table using SARSA
#             agent.updateQ(tuple(old_state), old_action, tuple(new_state), new_action, reward)

#             # Prepare for the next step
#             old_state = new_state
#             old_action = new_action

#             # Update display
#             gameDisplay.fill(white)
#             apple.display()
#             snake.display()
#             pygame.display.update()

#             # Control game speed
#             clock.tick(FPS)

#         agent.saveQ()  # Save Q-table after each episode

#         # Decay epsilon
#         agent.e = max(min_epsilon, agent.e * decay_rate)

#     print(f"Average Score: {sum(scores) / len(scores)}")

# if __name__ == "__main__":
#     training_game()

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
