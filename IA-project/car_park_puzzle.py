import msvcrt
import os
from collections import deque
import heapq

def heuristic(state, target_pos):
    a_pos = state.car_positions['A'][0]  # Asumiendo que 'A' está horizontal y solo necesitamos la primera partee
    return abs(a_pos[0] - target_pos[0]) + abs(a_pos[1] - target_pos[1])

def a_star(initial_state, target_pos, horizontal_cars):
    open_set = []
    heapq.heappush(open_set, (heuristic(initial_state, target_pos), initial_state))
    visited = set()

    while open_set:
        _, state = heapq.heappop(open_set)
        if state.is_goal(target_pos):
            state.print_path()
            return state
        visited.add(state)
        for successor in state.get_successors(horizontal_cars):
            if successor not in visited:
                heapq.heappush(open_set, (successor.moves + heuristic(successor, target_pos), successor))
                visited.add(successor)
    return None

# Algoritmos de búsquedas
def bfs(initial_state, target_pos, horizontal_cars):
    visited = set()
    queue = deque([initial_state])

    while queue:
        state = queue.popleft()
        if state.is_goal(target_pos):
            state.print_path()
            return state
        visited.add(state)
        for successor in state.get_successors(horizontal_cars):
            if successor not in visited:
                queue.append(successor)
                visited.add(successor)
    return None

def dfs(initial_state, target_pos, horizontal_cars):
    visited = set()
    stack = [initial_state]

    while stack:
        state = stack.pop()
        if state.is_goal(target_pos):
            state.print_path()
            return state
        visited.add(state)
        for successor in state.get_successors(horizontal_cars):
            if successor not in visited:
                stack.append(successor)
                visited.add(successor)
    return None



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_color():
    os.system("color 04")
 
class GameState:
    def __init__(self, board, car_positions, moves=0, parent=None):
        self.board = board
        self.car_positions = car_positions
        self.moves = moves
        self.parent = parent

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def is_goal(self, target_pos):
        return self.board[target_pos[0]][target_pos[1]] == 'A'

    def get_successors(self, horizontal_cars):
        successors = []
        for car in self.car_positions:
            for move in ['w', 'a', 's', 'd']:
                new_positions = get_new_positions(self.car_positions, car, move, horizontal_cars[car])
                if is_valid_move(self.board, self.car_positions, car, new_positions):
                    new_board = [row[:] for row in self.board]
                    new_car_positions = {k: [pos[:] for pos in v] for k, v in self.car_positions.items()}
                    move_car(new_board, new_car_positions, car, new_positions)
                    successors.append(GameState(new_board, new_car_positions, self.moves + 1, self))
        return successors

    def print_path(self):
        if self.parent:
            self.parent.print_path()
        print_board(self.board)

def print_board(board):
    for row in board:
        print(" ".join(row))
    print()
 
def is_valid_move(board, car_positions, car, new_positions):
    for new_pos in new_positions:
        if not (0 <= new_pos[0] < len(board) and 0 <= new_pos[1] < len(board[0])):
            return False
        if board[new_pos[0]][new_pos[1]] != '.' and board[new_pos[0]][new_pos[1]] != 'M' and board[new_pos[0]][new_pos[1]] != car:
            return False
    return True
 
def move_car(board, car_positions, car, new_positions):
    # Borrar la posición actual del auto
    for pos in car_positions[car]:
        board[pos[0]][pos[1]] = '.'
    # Mover el auto a la nueva posición
    for pos in new_positions:
        board[pos[0]][pos[1]] = car
    car_positions[car] = new_positions
 
def get_new_positions(car_positions, car_to_move, move, horizontal):
    car_pos = car_positions[car_to_move]
    if horizontal:
        if move == 'a':  # Izquierda
            return [[pos[0], pos[1] - 1] for pos in car_pos]
        elif move == 'd':  # Derecha
            return [[pos[0], pos[1] + 1] for pos in car_pos]
    else:
        if move == 'w':  # Arriba
            return [[pos[0] - 1, pos[1]] for pos in car_pos]
        elif move == 's':  # Abajo
            return [[pos[0] + 1, pos[1]] for pos in car_pos]
    return car_pos  # No cambia la posición si el movimiento no es válido
 
def find_car_positions(board):
    car_positions = {}
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell.isalpha() and cell != 'M':  # Encontrar todas las letras que representan autos
                if cell not in car_positions:
                    car_positions[cell] = []
                car_positions[cell].append([i, j])
    return car_positions

def start(levels):
    print(""""
  ___   __   ____    ____   __   ____  __ _    ____  _  _  ____  ____  __    ____ 
 / __) / _\ (  _ \  (  _ \ / _\ (  _ \(  / )  (  _ \/ )( \(__  )(__  )(  )  (  __)
( (__ /    \ )   /   ) __//    \ )   / )  (    ) __/) \/ ( / _/  / _/ / (_/\ ) _) 
 \___)\_/\_/(__\_)  (__)  \_/\_/(__\_)(__\_)  (__)  \____/(____)(____)\____/(____)
          
          Seleccione el número del nivel que desea jugar:

          1- Nivel 1
          2- Nivel 2
          """)
    try:
        level = int(input("Digite el número del nivel: "))

        if level not in levels.keys():
            input("Nivel no válido, presione Enter para continuar: ")
            clear()
            start(levels)
        
        return level
    except:
        input("Nivel no válido, presione Enter para continuar: ")
        clear()
        start(levels)

def main():
    # Ejemplo de juego simple
    board1 = [['.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.'],
             ['A', 'A', '.', 'C', 'B', '.', 'M'],
             ['.', '.', '.', 'C', 'B', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.']]
    
    board2 = [['.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', 'F', 'F', '.', '.', '.'],
             ['.', '.', 'E', 'D', 'D', '.', '.'],
             ['A', 'A', 'E', 'C', 'B', '.', 'M'],
             ['.', '.', '.', 'C', 'B', '.', '.'],
             ['.', '.', 'G', '.', '.', '.', '.'],
             ['.', '.', 'G', '.', '.', '.', '.']]
 
    levels_boards = { 1: board1, 2: board2 }
    horizontal_cars = {"A": True, "B": False, "C": False, "D": True, "E": False, "F": True, "G": False}
    target_pos = [3, 6]

    level = start(levels_boards)
    board = levels_boards[level]
    car_positions = find_car_positions(board)
    initial_state = GameState(board, car_positions)

    print("Seleccione el algoritmo de búsqueda:")
    print("1- BFS")
    print("2- DFS")
    print("3- A*")
    choice = input("Digite el número del algoritmo: ").strip()

    if choice == '1':
        solution = bfs(initial_state, target_pos, horizontal_cars)
    elif choice == '2':
        solution = dfs(initial_state, target_pos, horizontal_cars)
    elif choice == '3':
        solution = a_star(initial_state, target_pos, horizontal_cars)
    else:
        print("Opción no válida.")
        return

    if solution:
        print("¡Felicidades! El juego ha sido resuelto.")
    else:
        print("No se encontró solución.")
 

if __name__ == "__main__":
    set_color()
    main()