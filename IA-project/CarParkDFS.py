import os
import time
from collections import deque
import psutil

#samil quezada 

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_color():
    os.system("color 04")

def print_board(board):
    for row in board:
        print("  ".join(row))
    print()

def is_valid_move(board, car_positions, car, new_positions):
    for new_pos in new_positions:
        if not (0 <= new_pos[0] < len(board) and 0 <= new_pos[1] < len(board[0])):
            return False
        if board[new_pos[0]][new_pos[1]] != '.' and board[new_pos[0]][new_pos[1]] != '0' and board[new_pos[0]][new_pos[1]] != car:
            return False
    return True

def move_car(board, car_positions, car, new_positions):
    for pos in car_positions[car]:
        board[pos[0]][pos[1]] = '.'
    for pos in new_positions:
        board[pos[0]][pos[1]] = car
    car_positions[car] = new_positions

def get_new_positions(car_positions, car_to_move, move, horizontal):
    car_pos = car_positions[car_to_move]
    if horizontal:
        if move == 'a':
            return [[pos[0], pos[1] - 1] for pos in car_pos]
        elif move == 'd':
            return [[pos[0], pos[1] + 1] for pos in car_pos]
    else:
        if move == 'w':
            return [[pos[0] - 1, pos[1]] for pos in car_pos]
        elif move == 's':
            return [[pos[0] + 1, pos[1]] for pos in car_pos]
    return car_pos

def find_car_positions(board):
    car_positions = {}
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell.isalpha() and cell != '0' and cell != 'B':
                if cell not in car_positions:
                    car_positions[cell] = []
                car_positions[cell].append([i, j])
    return car_positions

def find_orientations(car_positions):
    horizontal_cars = {}
    for car in car_positions:
        if car_positions[car][0][0] == car_positions[car][1][0]:
            horizontal_cars[car] = True
        else:
            horizontal_cars[car] = False
    return horizontal_cars

def find_target_pos(board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == '0':
                return [i, j]

# Función para escribir las métricas de rendimiento en un archivo de textoo
def write_output(file_path, solution, cost, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage):
    with open(file_path, 'w', encoding="utf-8") as file:
        moves = [state.get_move() for state in solution[1:]]  # Excluimos el estado inicial
        file.write(f"Lista de movimientos: {moves}\n")
        file.write(f"Costo de la ruta: {cost}\n")
        file.write(f"Cantidad de nodos expandidos: {nodes_expanded}\n")
        file.write(f"Profundidad: {search_depth}\n")
        file.write(f"Máxima profundidad de la búsqueda: {max_search_depth}\n")
        file.write(f"Tiempo de ejecución: {running_time:.2f} segundos\n")
        file.write(f"Máxima memoria RAM consumida: {max_ram_usage:.2f} MB\n")

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

    def get_move(self):
            if not self.parent:
                return "Inicial"
            for car in self.car_positions:
                if self.car_positions[car] != self.parent.car_positions[car]:
                    old_pos = self.parent.car_positions[car][0]
                    new_pos = self.car_positions[car][0]
                    if old_pos[0] < new_pos[0]:
                        return f"{car}: Abajo"
                    elif old_pos[0] > new_pos[0]:
                        return f"{car}: Arriba"
                    elif old_pos[1] < new_pos[1]:
                        return f"{car}: Derecha"
                    elif old_pos[1] > new_pos[1]:
                        return f"{car}: Izquierda"
            return "Desconocido"

    def print_path(self):
        if self.parent:
            self.parent.print_path()
        print_board(self.board)

#DFS con output
def dfs(initial_state, target_pos, horizontal_cars):
    stack = [initial_state]
    visited = set()
    nodes_expanded = 0
    max_search_depth = 0

    while stack:
        state = stack.pop()
        
        if state.is_goal(target_pos):
            path = []
            temp = state
            while temp:
                path.append(temp)
                temp = temp.parent
            path.reverse()

            write_output("output.txt", path, state.moves, nodes_expanded, len(path) - 1, max_search_depth, time.time(), psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024))

            return state, path, nodes_expanded, len(path) - 1, max_search_depth

        if state not in visited:
            visited.add(state)
            nodes_expanded += 1
            max_search_depth = max(max_search_depth, state.moves)

            for successor in state.get_successors(horizontal_cars):
                if successor not in visited:
                    stack.append(successor)

    return None, [], nodes_expanded, 0, max_search_depth

# Implementación del algoritmo BFS
def bfs(initial_state, target_pos, horizontal_cars):
    visited = set()
    queue = deque([initial_state])
    nodes_expanded = 0  
    max_search_depth = 0 

    while queue:
        state = queue.popleft()
        if state.is_goal(target_pos):
            path = []
            temp = state
            while temp.parent:
                path.append(temp)
                temp = temp.parent
            path.reverse()

            write_output("output.txt", path, state.moves, nodes_expanded, len(path), max_search_depth, time.time(), psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024))
            return state, path, nodes_expanded, len(path), max_search_depth

        visited.add(state)
        for successor in state.get_successors(horizontal_cars):
            if successor not in visited:
                queue.append(successor)
                visited.add(successor)
                nodes_expanded += 1  # Incrementar contador de nodos expandidos
                max_search_depth = max(max_search_depth, successor.moves)  # Actualizar la máxima profundidad de búsqueda
    return None, [], nodes_expanded, 0, max_search_depth

def start():
    print(r"""
  ___   __   ____    ____   __   ____  __ _    ____  _  _  ____  ____  __    ____
 / __) / _\ (  _ \  (  _ \ / _\ (  _ \(  / )  (  _ \/ )( \(__  )(__  )(  )  (  __)
( (__ /    \ )   /   ) __//    \ )   / )  (    ) __/) \/ ( / _/  / _/ / (_/\ ) _)
 \___)\_/\_/(__\_)  (__)  \_/\_/(__\_)(__\_)  (__)  \____/(____)(____)\____/(____)
         
          Seleccione el número del nivel que desea jugar:
 
          1- Nivel 1
          2- Nivel 2
          3- Nivel 3
          4- Nivel 4
          5- Nivel 5
          6- Nivel 6
          7- Nivel 7
          8- Nivel 8
          9- Nivel 9
          10- Nivel 10
          11- Nivel 11
          12- Nivel 12
          
          """)

    level_number = int(input("Digite el número del nivel: "))

    file_path = f"D:\IA-project\Levels\Level{level_number}.txt"
    if not os.path.isfile(file_path):
        input("Nivel no válido o archivo no encontrado, presione Enter para continuar: ")
        clear()
        return start()

    with open(file_path, "rt", encoding="utf-8") as f:
        level = [list(line) for line in f.read().splitlines()]
    return level

def select_algorithm():
    while True:
        print("\nSeleccione el algoritmo que desea utilizar:")
        print("1. Breadth First Search (BFS)")
        print("2. Depth First Search (DFS)")
        choice = input("Ingrese el número de eleccion: ")
        if choice in ['1', '2']:
            return 'bfs' if choice == '1' else 'dfs'
        print("Opción no válida. Por favor, intente de nuevo.")

def main():
    board = start()
    algorithm = select_algorithm()

    while True:
        clear()
        car_positions = find_car_positions(board)
        horizontal_cars = find_orientations(car_positions)
        target_pos = find_target_pos(board)

        start_time = time.time()
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        initial_state = GameState(board, car_positions)
        
        if algorithm == 'bfs':
            solution, path, nodes_expanded, search_depth, max_search_depth = bfs(initial_state, target_pos, horizontal_cars)
        else:
            solution, path, nodes_expanded, search_depth, max_search_depth = dfs(initial_state, target_pos, horizontal_cars)

        end_time = time.time()
        final_memory = process.memory_info().rss
        running_time = end_time - start_time
        max_ram_usage = (final_memory - initial_memory) / (1024 * 1024)

        print("\nTablero final:")
        print_board(board)
        print("\nSolución encontrada:")
        solution.print_path()

        print(f"\nAlgoritmo utilizado: {'BFS' if algorithm == 'bfs' else 'DFS'}")
        print(f"Nodos expandidos: {nodes_expanded}")
        print(f"Profundidad de la solución: {search_depth}")
        print(f"Máxima profundidad de búsqueda: {max_search_depth}")
        print(f"Tiempo de ejecución: {running_time:.2f} segundos")
        print(f"Máxima memoria RAM consumida: {max_ram_usage:.2f} MB")

        input("\nPresione Enter para continuar...")

        clear()
        board = start()
        algorithm = select_algorithm()

if __name__ == "__main__":
    main()