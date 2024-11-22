# META DATA - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Developer details: 
        # Name: Prachi Tavse
        # Role: Architect

    # Version:
        # Version: V 1.0 (24 October 2024)
            # Developers: Prachi Tavse
            # Unit test: Pass
            # Integration test: Pass
     
    # Description: This code snippet implements an Advantage Actor-Critic (A2C) algorithm for solving the Frozen Lake 
    # environment using the OpenAI Gym. The agent is trained using reinforcement learning to navigate the grid world, 
    # where it learns an optimal policy to reach the goal while avoiding holes. The A2C algorithm employs both an actor 
    # (policy network) and a critic (value network) to train the agent.

# CODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # Dependency: 
        # Environment:     
            # Python: 3.11.0
            # tensorflow==2.16.1
            # numpy>=1.23.5,<2.0.0
            # gym==0.26.2
            # matplotlib>=3.6.0,<4.0.0
# Inspiration for this code was taken from GeeksForGeeks article "Actor-Critic Algorithm in Reinforcement Learning".

import gym
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt
from matplotlib import colors
from collections import deque
import pickle
import os

actor_model_path = "actor_model_weights.pkl"
critic_model_path = "critic_model_weights.pkl"

# Initialize the FrozenLake environment
env = gym.make("FrozenLake-v1", is_slippery=False)
state_size = env.observation_space.n
action_size = env.action_space.n

# Function to visualize the environment grid in a single plot
def visualize_environment(env, state, episode, step, fig, ax):
    grid_size = (4, 4)
    grid = np.zeros(grid_size)

    # Mark the goal
    goal_state = 15
    grid[goal_state // 4, goal_state % 4] = 1  # Mark the goal with a 1

    # Mark the holes
    holes = [5, 7, 11, 12]
    for hole in holes:
        grid[hole // 4, hole % 4] = 0.5  # Mark holes with 0.5
    # Mark the agent's position
    agent_position = state
    grid[agent_position // 4, agent_position % 4] = 0.75  # Mark agent with 0.75

    ax.clear()  # Clear the previous plot
    cmap = colors.ListedColormap(['lightblue', 'yellow', 'blue', 'red'])
    bounds = [0, 0.25, 0.5, 0.75, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    ax.imshow(grid, cmap=cmap, norm=norm)
    ax.set_xticks([])  # Remove x ticks
    ax.set_yticks([])  # Remove y ticks
    ax.set_title(f'Episode {episode} / Step {step}')
    plt.draw()
    plt.pause(0.05)  # Short pause to allow for real-time updates

# Build the actor model
actor_model = tf.keras.Sequential([
    layers.Dense(64, input_dim=state_size, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(action_size, activation='softmax')
])

# Build the critic model
critic_model = tf.keras.Sequential([
    layers.Dense(64, input_dim=state_size, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)  # Single output for the state value
])

# Optimizers for the actor and critic
actor_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
critic_optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)

# Training parameters
gamma = 0.99 # Discount factor to weigh future rewards.
num_episodes = 1000
max_steps = 200
success_threshold = 0.9  # Early stopping success rate threshold
epsilon = 0.1 # probability of exploratory action
epsilon_min = 0.01  # Minimum exploration rate
epsilon_decay = 0.995  # Decay rate per episode

# Tracking success rate over recent episodes
recent_rewards = deque(maxlen=100)  # Store rewards for the last 100 episodes
success_rates = []  # Store success rates for plotting

# Set up the plotting window outside the loop
fig, ax = plt.subplots()
goal_state = 15
holes = [5, 7, 11, 12]

# Main training loop
for episode in range(num_episodes):
    state = env.reset()[0]  # Reset environment and get initial state
    episode_reward = 0
    done = False

    with tf.GradientTape(persistent=True) as tape:  # Persistent to allow reuse for both models
        for step in range(max_steps):
            # Visualize environment at each step
            visualize_environment(env, state, episode, step, fig, ax)

            state_one_hot = np.identity(state_size)[state]  # One-hot encode state into a 16-dimensional vector
            state_input = np.array([state_one_hot]) #shapes this vector as an input for the networks

            # Get action probabilities from actor and sample an action
            action_probs = actor_model(state_input, training=True)
            action = np.random.choice(action_size, p=action_probs.numpy().flatten()) # samples an action based on these probabilities

            #epsilon-greedy exploration
            if np.random.rand() < epsilon:
                action = np.random.choice(action_size)
            else:
                action_probs = actor_model(state_input, training=True)
                action = np.argmax(action_probs.numpy().flatten())

            # Take action and observe result
            next_state, reward, done, _, _ = env.step(action)
            next_state_one_hot = np.identity(state_size)[next_state]
            next_state_input = np.array([next_state_one_hot])

            # Modify reward for holes and end of episode
            if next_state in holes:
                reward = -0.5  # Penalize for falling into a hole
            elif done and reward == 0:  # If episode ends without reaching goal
                reward = -0.2  # Smaller penalty for failing to reach the goal

            # Compute state values and advantage
            state_value = critic_model(state_input, training=True)[0, 0]
            next_state_value = critic_model(next_state_input, training=True)[0, 0]
            advantage = reward + gamma * next_state_value - state_value

            # Compute actor and critic losses
            actor_loss = -tf.math.log(action_probs[0, action]) * advantage
            critic_loss = tf.square(advantage)

            episode_reward += reward
            state = next_state  # Update the state

            # Stop if episode is done
            if done:
                break

    # reduces exploration over time, helping the policy converge
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    # Compute gradients and apply updates
    actor_gradients = tape.gradient(actor_loss, actor_model.trainable_variables)
    critic_gradients = tape.gradient(critic_loss, critic_model.trainable_variables)
    actor_optimizer.apply_gradients(zip(actor_gradients, actor_model.trainable_variables))
    critic_optimizer.apply_gradients(zip(critic_gradients, critic_model.trainable_variables))

    # Store success/failure (1 for reaching the goal, 0 otherwise)
    recent_rewards.append(1 if reward == 1 else 0)  # Reward 1 indicates success in FrozenLake

    # Print episode stats every 10 episodes
    if episode % 10 == 0:
        success_rate = np.mean(recent_rewards)
        success_rates.append(success_rate)
        print(f"Episode {episode}, Reward: {episode_reward}, Success Rate: {success_rate * 100:.2f}%")

    # Check early stopping condition
    if len(recent_rewards) == recent_rewards.maxlen and np.mean(recent_rewards) >= success_threshold:
        print(f"Early stopping at episode {episode} with success rate {np.mean(recent_rewards) * 100:.2f}%")
        break

# Save the actor and critic model weights after training
with open(actor_model_path, 'wb') as f:
    pickle.dump(actor_model.get_weights(), f)
    
with open(critic_model_path, 'wb') as f:
    pickle.dump(critic_model.get_weights(), f)

print("Models saved successfully!")

# To load the model weights in the future, you can use this:
with open(actor_model_path, 'rb') as f:
    actor_weights = pickle.load(f)
    actor_model.set_weights(actor_weights)

with open(critic_model_path, 'rb') as f:
    critic_weights = pickle.load(f)
    critic_model.set_weights(critic_weights)

print("Models loaded successfully!")

env.close()

plt.figure()
plt.plot(range(0, len(success_rates) * 10, 10), [sr * 100 for sr in success_rates], marker='o')
plt.xlabel("Episodes")
plt.ylabel("Success Rate (%)")
plt.title("Agent Success Rate Over Time")
plt.grid()
plt.show()
