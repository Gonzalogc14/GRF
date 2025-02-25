import gfootball.env as football_env
from Rewards import calculate_rewards

# Número de partidos que quieres jugar
num_partidos = 15

# Variables para almacenar los totales por partido
recompensas_totales_partidos = []
pases_totales_partidos = []
recompensas_positivas_partidos = []
recompensas_negativas_partidos = []

for partido in range(num_partidos):
    # Crear un nuevo entorno para cada partido
    env = football_env.create_environment(env_name='11_vs_11_easy_stochastic', representation='raw')
    obs = env.reset()
    
    total_reward = 0
    total_pases = 0  # Inicializar el contador de pases
    total_recompensas_positivas = 0
    total_recompensas_negativas = 0

    previous_state = obs[0]
    done = False

    while not done:
        actions = env.action_space.sample()
        obs, reward, done, info = env.step(actions)

        current_state = obs[0]
        reward_value = calculate_rewards(obs, actions, previous_state)
        total_reward += reward_value

        # Separar recompensas positivas y negativas
        if reward_value > 0:
            total_recompensas_positivas += reward_value
        elif reward_value < 0:
            total_recompensas_negativas += abs(reward_value)  # Convertimos en positivo para sumar correctamente

        # Contar los pases exitosos (acciones 9, 10 y 11)
        if actions in [9, 10, 11]:  # Si la acción es un pase
            if obs[0]['ball_owned_team'] == 0:  # Si el equipo izquierdo tiene la pelota
                # Verificar que el pase se complete correctamente (el balón sigue siendo del equipo izquierdo)
                total_pases += 1

        previous_state = current_state

    # Almacenar los resultados de este partido
    recompensas_totales_partidos.append(total_reward)
    pases_totales_partidos.append(total_pases)
    recompensas_positivas_partidos.append(total_recompensas_positivas)
    recompensas_negativas_partidos.append(total_recompensas_negativas)

    print(f"Match {partido + 1} - Positive Rewards: {total_recompensas_positivas}, "
          f"Negative Rewards: {total_recompensas_negativas}")

    # Cerrar el entorno después de cada partido
    env.close()
