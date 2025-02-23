def calculate_rewards(state, action, previous_score):
    """
    Calcula las recompensas para el equipo izquierdo basándose en el estado, la acción y el marcador anterior.
    Solo calcula recompensas cuando el equipo izquierdo realiza una acción.
    """
    reward = 0
    
    # El marcador (score) está en la primera posición del estado
    score = state[0]['score']  # Acceder al marcador actual en el 'state'

    # Verificar que el equipo que realizó la acción sea el equipo izquierdo
    if state[0]['ball_owned_team'] == 0:  # Si el equipo izquierdo posee la pelota (ball_owned_team = 0)
        
        # 1) Marcar un gol. (Dependiendo si voy ganando / perdiendo / empatando)
        if score[0] > score[1] and previous_score[0] <= previous_score[1]:  # Si el equipo está ganando
            reward += 10  # Premio máximo por marcar un gol cuando se está ganando
        elif score[0] < score[1] and previous_score[0] >= previous_score[1]:  # Si el equipo está perdiendo
            reward += 8  # Premio algo menor por marcar un gol cuando se está perdiendo
        elif score[0] == score[1] and previous_score[0] == previous_score[1]:  # Si el marcador está empatado
            reward += 9  # Premio por marcar un gol en empate

        # 2) Dar una asistencia que resulte en gol
        # Necesitarás lógica para identificar cuando un pase resulta en gol.
        if action == 10:  # Suponiendo que 10 es la acción de pase que resulta en asistencia
            reward += 5  # Asignamos recompensa por asistencia

        # 3) Realizar un pase exitoso
        if action == 9:  # Suponiendo que 9 es la acción de pase exitoso
            reward += 3  # Recompensa por pase exitoso

        # 4) Realizar una intercepción
        if action == 11:  # Suponiendo que 11 es la acción de intercepción
            reward += 4  # Recompensa por intercepción

        # 5) Realizar un tiro a puerta que requiera una parada
        if action == 7:  # Suponiendo que 7 es la acción de un tiro a puerta que requiere parada
            reward += 6  # Recompensa por tiro a puerta

        # 6) Realizar un regate exitoso
        if action == 12:  # Suponiendo que 12 es la acción de un regate exitoso
            reward += 7  # Recompensa por regate exitoso

        # 7) Realizar un sliding y recuperar el balón
        if action == 13:  # Suponiendo que 13 es la acción de sliding y recuperar balón
            reward += 6  # Recompensa por recuperar balón con sliding

        # 8) Recuperar posesión en el tercio ofensivo
        if action == 14:  # Suponiendo que 14 es la acción de recuperar balón en el tercio ofensivo
            reward += 5  # Recompensa por recuperar el balón en el tercio ofensivo
    
    return reward
