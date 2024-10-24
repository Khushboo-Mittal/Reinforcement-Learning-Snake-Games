import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 400, 400  # Reduced grid size
BLOCK_SIZE = 80
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
ACTIONS = [LEFT, RIGHT, UP, DOWN]

# Q-learning parameters
alpha = 0.1      # Learning rate
gamma = 0.9      # Discount factor
epsilon = 0.1    # Exploration rate

# Initialize Q-table: (grid_x, grid_y, action) -> Q-value
q_table = np.zeros((GRID_WIDTH, GRID_HEIGHT, len(ACTIONS)))

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Q-learning Snake")

clock = pygame.time.Clock()

def random_food(snake):
    """Generate random food position that is not on the snake."""
    while True:
        food = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
        if food not in snake:
            return food

def draw_grid():
    """Draw the grid lines for better visualization."""
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_snake(snake):
    """Draw the snake on the screen."""
    for block in snake:
        rect = pygame.Rect(block[0] * BLOCK_SIZE, block[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

def draw_food(food):
    """Draw the food on the screen."""
    rect = pygame.Rect(food[0] * BLOCK_SIZE, food[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, RED, rect)

def get_state(snake, food):
    """Get the current state: snake's head and food position."""
    head = snake[0]
    return head[0], head[1], food[0], food[1]

def get_next_action(state):
    """Choose an action using epsilon-greedy."""
    if random.uniform(0, 1) < epsilon:
        return random.choice(ACTIONS)  # Explore
    else:
        x, y = state[0], state[1]
        return np.argmax(q_table[x, y])  # Exploit

def take_action(snake, action):
    """Move the snake in the given direction."""
    head = snake[0]
    if action == LEFT:
        new_head = [head[0] - 1, head[1]]
    elif action == RIGHT:
        new_head = [head[0] + 1, head[1]]
    elif action == UP:
        new_head = [head[0], head[1] - 1]
    elif action == DOWN:
        new_head = [head[0], head[1] + 1]
    
    snake.insert(0, new_head)  # Add new head to the snake
    return snake

def is_collision(snake):
    """Check if the snake hits the wall or itself."""
    head = snake[0]
    return (
        head[0] < 0 or head[0] >= GRID_WIDTH or 
        head[1] < 0 or head[1] >= GRID_HEIGHT or 
        head in snake[1:]
    )

def reward(snake, food):
    """Calculate reward based on whether snake eats food or collides."""
    if snake[0] == food:
        return 10  # Food eaten
    elif is_collision(snake):
        return -10  # Snake hit wall or itself
    else:
        return -1  # Otherwise, small penalty to encourage movement

def update_q_table(state, action, r, new_state):
    """Update the Q-table based on the state, action, reward, and new state."""
    x, y = state[0], state[1]
    nx, ny = new_state[0], new_state[1]
    old_value = q_table[x, y, action]
    future_value = np.max(q_table[nx, ny])
    q_table[x, y, action] = old_value + alpha * (r + gamma * future_value - old_value)

def game_loop():
    snake = [[GRID_WIDTH // 2, GRID_HEIGHT // 2]]  # Initial snake position
    food = random_food(snake)  # Random food position
    score = 0
    action = RIGHT

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        state = get_state(snake, food)
        action = get_next_action(state)
        snake = take_action(snake, action)

        r = reward(snake, food)
        if r == 10:  # Food eaten
            food = random_food(snake)
            score += 1
        else:
            snake.pop()  # Remove tail segment if no food eaten

        if r == -10:  # Collision
            break  # End game

        new_state = get_state(snake, food)
        update_q_table(state, action, r, new_state)

        # Rendering
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        
        pygame.display.update()

        clock.tick(15)  # Control the speed of the game

    return score

# Function to plot the Q-table
def plot_q_table(episode):
    """Save the Q-table plots as images instead of displaying them."""
    plt.figure(figsize=(9, 6))

    # Plot Q-values for each action
    for i, action in enumerate(["LEFT", "RIGHT", "UP", "DOWN"]):
        plt.subplot(2, 2, i + 1)
        sns.heatmap(q_table[:, :, i], annot=True, cmap="coolwarm", cbar=True)
        plt.title(f"Q-values for {action} action")

    plt.tight_layout()
    plt.savefig(f"q_table_episode_{episode}.png")  # Save the figure
    plt.close()  # Close the plot to free up resources

    
def show_game_over(score):
    """Display a Game Over message with the score."""
    font = pygame.font.SysFont(None, 55)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)  # Pause for 2 seconds

# Main function to run the game
if __name__ == "__main__":
    episodes = 30  # Reduced number of episodes
    for episode in range(episodes + 1):
        score = game_loop()
        print(f"Episode {episode}, Score: {score}")
        
        if episode % 10 == 0:  # Plot the Q-table every 10 episodes
            print(f"Saving Q-table after episode {episode}")
            plot_q_table(episode) 
             
    show_game_over(score)

    pygame.quit()

