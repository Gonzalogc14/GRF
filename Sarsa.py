import gfootball.env as football_env
import numpy as np
from Rewards import calculate_rewards

# SARSA Parameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration probability

# Epsilon-Greedy Action Selection
def epsilon_greedy_action(q_table, state, action_space, epsilon):
    """
    Select an action based on epsilon-greedy strategy.
    - With probability epsilon, select a random action (exploration).
    - Otherwise, select the action with the highest Q-value (exploitation).
    """
    if np.random.rand() < epsilon:
        return action_space.sample()  # Random action (exploration)
    return np.argmax(q_table.get(state, np.zeros(action_space.n)))  # Best action (exploitation)

# Create the environment
env = football_env.create_environment(env_name='11_vs_11_easy_stochastic', representation='raw')

# Define the ranges for discretizing observations
ball_position_range = [(-1.2, 1.2), (-1.0, 1.0), (0.0, 1.0)]  # Ranges for X, Y, Z of the ball
player_position_range = [(-1.2, 1.2), (-1.0, 1.0)]  # Ranges for X, Y of each player

# Initialize Q-Table
q_table = {}

# Discretization of observations
def discretize_observation(obs):
    """
    Discretize the positions of the ball and players into bins.
    - Ball position is discretized into 10 bins for X, Y, and 5 bins for Z.
    - Player positions are discretized into 10 bins for X, Y.
    Returns a tuple representing the discretized state.
    """
    # Discretize ball position (X, Y, Z)
    ball_position = obs['ball']
    ball_x = np.digitize(ball_position[0], np.linspace(ball_position_range[0][0], ball_position_range[0][1], 10))
    ball_y = np.digitize(ball_position[1], np.linspace(ball_position_range[1][0], ball_position_range[1][1], 10))
    ball_z = np.digitize(ball_position[2], np.linspace(ball_position_range[2][0], ball_position_range[2][1], 5))
    
    # Discretize player positions (X, Y) for each player on the left team
    left_team = obs['left_team']
    left_team_discretized = []
    for player in left_team:
        player_x = np.digitize(player[0], np.linspace(player_position_range[0][0], player_position_range[0][1], 10))
        player_y = np.digitize(player[1], np.linspace(player_position_range[1][0], player_position_range[1][1], 10))
        left_team_discretized.append((player_x, player_y))
    
    # Return the discretized observation as a tuple
    return tuple([ball_x, ball_y, ball_z] + [player for player in left_team_discretized])

# Training loop for SARSA
num_episodes = 1000

for episode in range(num_episodes):
    obs = env.reset()
    state = discretize_observation(obs[0])  # Initial state
    action = epsilon_greedy_action(q_table, state, env.action_space, epsilon)  # Initial action
    total_reward = 0
    done = False
    
    while not done:
        next_obs, reward, done, _ = env.step(action)  # Take action and observe the next state
        next_state = discretize_observation(next_obs[0])  # Discretize next state
        next_action = epsilon_greedy_action(q_table, next_state, env.action_space, epsilon)  # Choose next action
        
        # Calculate reward using the custom reward function
        calculated_reward = calculate_rewards(next_obs[0], action, obs[0])
        total_reward += calculated_reward
        
        # Update Q-Table based on SARSA formula
        if state not in q_table:
            q_table[state] = np.zeros(env.action_space.n)  # Initialize Q-values if state not seen before
        if next_state not in q_table:
            q_table[next_state] = np.zeros(env.action_space.n)  # Initialize Q-values for next state if not seen
        
        # Update Q-value for the current state-action pair
        q_table[state][action] += alpha * (calculated_reward + gamma * q_table[next_state][next_action] - q_table[state][action])
        
        # Update state and action for the next iteration
        state = next_state
        action = next_action
    
    # Print total reward for the current episode
    print(f"Episode {episode + 1}: Total Reward = {total_reward}")


