# La primer heuristica seria la cantidad de vehiculos en el camino hacia el 0.
def blocking_cars_heuristic(board, car_pos, target_pos, max_value, weight):
    row, col = car_pos[0], car_pos[1]
    blocking_cars = 0
    for i in range(col, target_pos[1]):
        if board[row][i] not in ('.', 'A', 'B'):
            blocking_cars += 1
    normalized_blocking_cars = blocking_cars / max_value
    return normalized_blocking_cars * weight

# La segunda el espacio libre adelante 
def free_space_heuristic(board, car_pos, max_value,weight):
    row, col = car_pos[0], car_pos[1]
    free_space = 0
    for i in range(col + 1, len(board[0])):
        if board[row][i] == '.':
            free_space += 1
        else:
            break
    normalized_free_space = free_space / max_value
    return normalized_free_space * weight

# La tercera heuristica de la distancia total hasta el  0
def distance_goal_heuristic(board, car_pos, target_pos, max_value, weight):
    row, col = car_pos[0], car_pos[1]
    obstacles = 0
    for i in range(col, target_pos[1]):
        if board[row][i] not in  ('.', 'A', 'B'):
            obstacles += 1
    distance = (target_pos[1] - col) + obstacles
    normalized_distance = distance / max_value
    return normalized_distance * weight
    

