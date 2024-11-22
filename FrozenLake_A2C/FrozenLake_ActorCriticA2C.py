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

# Import necessary libraries
import gym  # OpenAI Gym for creating and managing the FrozenLake environment
import numpy as np  # For numerical operations
import tensorflow as tf  # For building neural networks
from tensorflow.keras import layers  # For defining neural network layers
import matplotlib.pyplot as plt  # For visualization
from matplotlib import colors  # For custom colormap for the environment visualization
from collections import deque  # For maintaining a fixed-length queue for recent rewards
import pickle  # For saving and loading model weights
import os  # For file management

# Paths to save actor and critic model weights
actor_model_path = "actor_model_weights.pkl"
critic_model_path = "critic_model_weights.pkl"

# Initialize the FrozenLake environment
env = gym.make("FrozenLake-v1", is_slippery=False)  # Create a deterministic FrozenLake environment
state_size = env.observation_space.n  # Number of discrete states in the environment (16 for 4x4 grid)
action_size = env.action_space.n  # Number of possible actions (4: left, down, right, up)

# Function to visualize the FrozenLake environment in a grid format
def visualize_environment(env, state, episode, step, fig, ax):
    grid_size = (4, 4)  # FrozenLake is a 4x4 grid
    grid = np.zeros(grid_size)  # Initialize a grid with zeros to represent states

    # Mark the goal state in the grid
    goal_state = 15  # The bottom-right corner is the goal
    grid[goal_state // 4, goal_state % 4] = 1  # Mark goal with a value of 1

    # Mark the holes in the grid
    holes = [5, 7, 11, 12]  # Locations of holes in the grid
    for hole in holes:
        grid[hole // 4, hole % 4] = 0.5  # Mark holes with a value of 0.5

    # Mark the agent's current position
    agent_position = state
    grid[agent_position // 4, agent_position % 4] = 0.75  # Mark agent with a value of 0.75

    # Plot the grid
    ax.clear()  # Clear the previous plot
    cmap = colors.ListedColormap(['lightblue', 'yellow', 'blue', 'red'])  # Define colors for the grid
    bounds = [0, 0.25, 0.5, 0.75, 1]  # Define boundaries for color mapping
    norm = colors.BoundaryNorm(bounds, cmap.N)  # Normalize the grid values to the colormap

    ax.imshow(grid, cmap=cmap, norm=norm)  # Display the grid
    ax.set_xticks([])  # Remove x-axis ticks
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_title(f'Episode {episode} / Step {step}')  # Set plot title with current episode and step
    plt.draw()  # Update the plot
    plt.pause(0.05)  # Pause for a short time to allow for real-time updates

# Build the actor model
# This model outputs probabilities for each action given a state
actor_model = tf.keras.Sequential([
    layers.Dense(64, input_dim=state_size, activation='relu'),  # First hidden layer
    layers.Dense(64, activation='relu'),  # Second hidden layer
    layers.Dense(action_size, activation='softmax')  # Output layer with softmax for action probabilities
])

# Build the critic model
# This model estimates the value of a given state
critic_model = tf.keras.Sequential([
    layers.Dense(64, input_dim=state_size, activation='relu'),  # First hidden layer
    layers.Dense(64, activation='relu'),  # Second hidden layer
    layers.Dense(1)  # Single output node for state value
])

# Define optimizers for training the actor and critic models
actor_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)  # Learning rate for actor
critic_optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)  # Learning rate for critic

# Hyperparameters for training
gamma = 0.99  # Discount factor to weigh future rewards
num_episodes = 1000  # Total number of training episodes
max_steps = 200  # Maximum steps per episode
success_threshold = 0.9  # Early stopping threshold for success rate
epsilon = 0.1  # Initial probability of choosing a random action (exploration)
epsilon_min = 0.01  # Minimum exploration probability
epsilon_decay = 0.995  # Decay rate for exploration probability per episode

# Initialize trackers for success rates and recent rewards
recent_rewards = deque(maxlen=100)  # Maintain a rolling window of the last 100 rewards
success_rates = []  # Store success rates for plotting

# Set up a visualization window for the environment
fig, ax = plt.subplots()  # Create a figure and axis for the plot
goal_state = 15  # Define the goal state
holes = [5, 7, 11, 12]  # Define the hole states

# Main training loop
for episode in range(num_episodes):
    state = env.reset()[0]  # Reset the environment and get the initial state
    episode_reward = 0  # Initialize total reward for the episode
    done = False  # Track if the episode has finished

    with tf.GradientTape(persistent=True) as tape:  # Persistent tape for calculating both actor and critic gradients
        for step in range(max_steps):
            # Visualize the environment at the current step
            visualize_environment(env, state, episode, step, fig, ax)

            # One-hot encode the current state
            state_one_hot = np.identity(state_size)[state]
            state_input = np.array([state_one_hot])  # Prepare state as input for the models

            # Get action probabilities from the actor model
            action_probs = actor_model(state_input, training=True)
            action = np.random.choice(action_size, p=action_probs.numpy().flatten())  # Sample action based on probabilities

            # Epsilon-greedy exploration: choose a random action with probability epsilon
            if np.random.rand() < epsilon:
                action = np.random.choice(action_size)
            else:
                action_probs = actor_model(state_input, training=True)
                action = np.argmax(action_probs.numpy().flatten())  # Choose the action with the highest probability

            # Take the chosen action and observe the next state, reward, and termination status
            next_state, reward, done, _, _ = env.step(action)

            # One-hot encode the next state
            next_state_one_hot = np.identity(state_size)[next_state]
            next_state_input = np.array([next_state_one_hot])

            # Adjust reward for specific conditions
            if next_state in holes:
                reward = -0.5  # Penalize for falling into a hole
            elif done and reward == 0:  # Penalize for failing to reach the goal
                reward = -0.2

            # Calculate state value and advantage
            state_value = critic_model(state_input, training=True)[0, 0]  # Current state value
            next_state_value = critic_model(next_state_input, training=True)[0, 0]  # Next state value
            advantage = reward + gamma * next_state_value - state_value  # Temporal difference (TD) advantage

            # Calculate losses for the actor and critic models
            actor_loss = -tf.math.log(action_probs[0, action]) * advantage  # Policy gradient loss
            critic_loss = tf.square(advantage)  # Mean squared error for value estimation

            # Accumulate reward for the episode
            episode_reward += reward
            state = next_state  # Update the current state

            # End the episode if the environment signals done
            if done:
                break

    # Decay epsilon to reduce exploration over time
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    # Calculate gradients and update model weights
    actor_gradients = tape.gradient(actor_loss, actor_model.trainable_variables)
    critic_gradients = tape.gradient(critic_loss, critic_model.trainable_variables)
    actor_optimizer.apply_gradients(zip(actor_gradients, actor_model.trainable_variables))
    critic_optimizer.apply_gradients(zip(critic_gradients, critic_model.trainable_variables))

    # Track success or failure for the current episode
    recent_rewards.append(1 if reward == 1 else 0)  # Reward of 1 indicates success

    # Print progress every 10 episodes
    if episode % 10 == 0:
        success_rate = np.mean(recent_rewards)  # Calculate success rate
        success_rates.append(success_rate)  # Store success rate for plotting
        print(f"Episode {episode}, Reward: {episode_reward}, Success Rate: {success_rate * 100:.2f}%")

    # Check early stopping condition
    if len(recent_rewards) == recent_rewards.maxlen and np.mean(recent_rewards) >= success_threshold:
        print(f"Early stopping at episode {episode} with success rate {np.mean(recent_rewards) * 100:.2f}%")
        break

# Save the trained actor and critic model weights
with open(actor_model_path, 'wb') as f:
    pickle.dump(actor_model.get_weights(), f)

with open(critic_model_path, 'wb') as f:
    pickle.dump(critic_model.get_weights(), f)

# Plot success rates over episodes
plt.figure()
plt.plot(success_rates)
plt.xlabel('Episodes (x10)')
plt.ylabel('Success Rate')
plt.title('Training Progress')
plt.show()
