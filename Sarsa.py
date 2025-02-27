import gfootball.env as football_env
import numpy as np

env = football_env.create_environment(env_name='11_vs_11_easy_stochastic', representation='raw')

# Define discretization ranges for observations
ball_position_range = [(-1.2, 1.2), (-1.0, 1.0), (0.0, 1.0)]  # Ranges for X, Y, Z
player_position_range = [(-1.2, 1.2), (-1.0, 1.0)]  # Ranges for X, Y of each player

def discretize_observation(obs):
    """
    Discretize ball and player positions.
    - Ball position is discretized into 10 bins for X, Y, 5 bins for Z.
    - Player positions are discretized into 10 bins for X, Y.
    """
    # Discretize ball position.
    ball_position = obs['ball']
    ball_x = np.digitize(ball_position[0], np.linspace(ball_position_range[0][0], ball_position_range[0][1], 10))
    ball_y = np.digitize(ball_position[1], np.linspace(ball_position_range[1][0], ball_position_range[1][1], 10))
    ball_z = np.digitize(ball_position[2], np.linspace(ball_position_range[2][0], ball_position_range[2][1], 5))
    
    # Discretize player positions.
    left_team = obs['left_team']
    left_team_discretized = []
    for player in left_team:
        player_x = np.digitize(player[0], np.linspace(player_position_range[0][0], player_position_range[0][1], 10))
        player_y = np.digitize(player[1], np.linspace(player_position_range[1][0], player_position_range[1][1], 10))
        left_team_discretized.append((player_x, player_y))
    
    # Return tuple of discretized observations
    return tuple([ball_x, ball_y, ball_z] + [player for player in left_team_discretized])


obs = env.reset()


