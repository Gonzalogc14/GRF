import gfootball.env as football_env

# Crear el entorno sin representación gráfica
env = football_env.create_environment(
    env_name='11_vs_11_easy_stochastic',  # Modo de juego 11 vs 11
    representation='raw',  # Usar representación raw para obtener observaciones brutas
    render=False           # Desactivar el renderizado gráfico
)

# Resetear el entorno para comenzar un nuevo partido
obs = env.reset()

# Inicializar los contadores de pases y pases fallidos para el equipo izquierdo
left_team_passes = 0
right_team_passes = 0
left_team_failed_passes = 0

# Jugar el partido completo
done = False
while not done:
    # Acciones aleatorias para ambos equipos
    actions = env.action_space.sample()
    
    # Step en el entorno
    obs, reward, done, info = env.step(actions)
    
    # Verificar las acciones para contar los pases
    if actions in [9, 10, 11]:  # Las acciones 9, 10 y 11 son los pases
        if obs[0]['ball_owned_team'] == 0:  # Si el equipo que tiene la pelota es el equipo izquierdo
            left_team_passes += 1
        else:  # Si el equipo que tiene la pelota es el equipo derecho
            right_team_passes += 1
        
        # Contar pases fallidos para el equipo izquierdo
        if obs[0]['ball_owned_team'] != 0:  # Si la pelota ya no está con el equipo izquierdo
            left_team_failed_passes += 1

# Mostrar los resultados de los pases al final del partido
print(f"Left Team Passes: {left_team_passes}")
print(f"Right Team Passes: {right_team_passes}")
print(f"Left Team Failed Passes: {left_team_failed_passes}")

# Cerrar el entorno
env.close()
