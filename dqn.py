import pygame
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import os
import matplotlib.pyplot as plt

# Constants
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake game class
class SnakeGame:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake AI')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (BLOCK_SIZE, 0)
        self.spawn_food()
        self.score = 0

    def spawn_food(self):
        self.food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                     random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Action 0: straight, 1: right, 2: left
        self.move_snake(action)

        self.snake.insert(0, self.new_head)
        if self.snake[0] == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

        done = self.is_collision()
        reward = -10 if done else (10 if self.snake[0] == self.food else 0)

        self.update_ui()
        self.clock.tick(10)

        return reward, done, self.score

    def move_snake(self, action):
        # Actions: 0 = forward, 1 = right, 2 = left
        if action == 1:  # Right turn
            self.direction = (-self.direction[1], self.direction[0])
        elif action == 2:  # Left turn
            self.direction = (self.direction[1], -self.direction[0])

        x, y = self.snake[0]
        self.new_head = (x + self.direction[0], y + self.direction[1])

    def is_collision(self):
        x, y = self.snake[0]
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in self.snake[1:]:
            return True
        return False

    def update_ui(self):
        self.display.fill(WHITE)
        for x, y in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()

    def get_state(self):
        """Get the current state of the game as a flat array."""
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        
        # State representation: [snake head x, snake head y, food x, food y, direction]
        direction = np.array(self.direction) // BLOCK_SIZE  # Convert to grid coordinates
        state = np.array([
            head_x // BLOCK_SIZE,
            head_y // BLOCK_SIZE,
            food_x // BLOCK_SIZE,
            food_y // BLOCK_SIZE,
            direction[0],
            direction[1]
        ])
        return state

# DQN Agent
class DQNAgent:
    def __init__(self):
        self.state_size = 6  # Updated to match the state size
        self.action_size = 3
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

# Main loop
def main():
    game = SnakeGame()
    agent = DQNAgent()
    episodes = 10 # Total number of episodes
    scores = []  # List to store scores for each episode
    max_scores = []  # List to store maximum scores
    losses = []  # List to store losses during training

    try:
        for e in range(episodes):
            state = game.get_state().reshape(1, agent.state_size)  # Get the initial state
            game.reset()
            score = 0

            while True:
                action = agent.act(state)
                reward, done, current_score = game.step(action)

                next_state = game.get_state().reshape(1, agent.state_size)  # Get the next state
                agent.remember(state, action, reward, next_state, done)

                state = next_state
                score += current_score  # Accumulate score

                if done:
                    scores.append(score)  # Store the score of this episode
                    max_scores.append(max(scores) if scores else score)  # Store the maximum score
                    print(f"Episode: {e}/{episodes}, Score: {score}, Epsilon: {agent.epsilon}")
                    break

            if len(agent.memory) > 32:
                loss = agent.replay(32)
                losses.append(loss)  # Store the loss

            # Save model every 100 episodes
            if e % 100 == 0:
                agent.save(f"snake_dqn_{e}.weights.h5")

        # Plotting the performance metrics
        plot_performance(scores, max_scores)

    except KeyboardInterrupt:
        print("Training interrupted")

def plot_performance(scores, max_scores):
    """Function to plot the performance metrics."""
    plt.figure(figsize=(12, 6))
    plt.plot(scores, label='Score per Episode', color='blue')
    plt.plot(max_scores, label='Max Score', color='green')
    plt.xlabel('Episodes')
    plt.ylabel('Scores')
    plt.title('DQN Agent Performance in Snake Game')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
