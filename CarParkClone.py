import os
import time
from collections import deque
import psutil

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
        if move == 'l':
            return [[pos[0], pos[1] - 1] for pos in car_pos]
        elif move == 'r':
            return [[pos[0], pos[1] + 1] for pos in car_pos]
    else:
        if move == 'u':
            return [[pos[0] - 1, pos[1]] for pos in car_pos]
        elif move == 'd':
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
        if len(car_positions[car]) > 1:
            if car_positions[car][0][0] == car_positions[car][1][0]:
                horizontal_cars[car] = True
            else:
                horizontal_cars[car] = False
        else:
            horizontal_cars[car] = True
    return horizontal_cars

def find_target_pos(board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == '0':
                return [i, j]
    return None

def write_output(file_path, path, cost, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage):
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(f"Lista de movimientos: {[state.get_move() for state in path]}\n")
        file.write(f"Costo de la ruta: {cost}\n")
        file.write(f"Cantidad de nodos expandidos: {nodes_expanded}\n")
        file.write(f"Profundidad: {search_depth}\n")
        file.write(f"Máxima profundidad de la búsqueda: {max_search_depth}\n")
        file.write(f"Tiempo de ejecución: {running_time} segundos\n")
        file.write(f"Máxima memoria RAM consumida: {max_ram_usage} MB\n")

class GameState:
    def __init__(self, board, car_positions, moves=0, parent=None):
        self.board = board
        self.car_positions = car_positions
        self.moves = moves
        self.parent = parent

    def __eq__(self, other):
        return self.board == other.board and self.car_positions == other.car_positions

    def __hash__(self):
        return hash((str(self.board), str(self.car_positions)))

    def __repr__(self):
        return f"GameState(moves={self.moves}, board={self.board})"

    def is_goal(self, target_pos):
        return self.board[target_pos[0]][target_pos[1]] == 'A'

    def get_successors(self, horizontal_cars):
        successors = []
        move_order = ['u', 'd', 'l', 'r']
        visited_states = set()

        for car in sorted(self.car_positions):
            for move in move_order:
                new_positions = get_new_positions(self.car_positions, car, move, horizontal_cars[car])
                if is_valid_move(self.board, self.car_positions, car, new_positions):
                    new_board = [row[:] for row in self.board]
                    new_car_positions = {k: [pos[:] for pos in v] for k, v in self.car_positions.items()}
                    move_car(new_board, new_car_positions, car, new_positions)
                    new_state = GameState(new_board, new_car_positions, self.moves + 1, self)
                    if new_state not in visited_states:
                        successors.append(new_state)
                        visited_states.add(new_state)

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

import os
import time
from collections import deque
import psutil

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
        if move == 'l':
            return [[pos[0], pos[1] - 1] for pos in car_pos]
        elif move == 'r':
            return [[pos[0], pos[1] + 1] for pos in car_pos]
    else:
        if move == 'u':
            return [[pos[0] - 1, pos[1]] for pos in car_pos]
        elif move == 'd':
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
        if len(car_positions[car]) > 1:
            if car_positions[car][0][0] == car_positions[car][1][0]:
                horizontal_cars[car] = True
            else:
                horizontal_cars[car] = False
        else:
            horizontal_cars[car] = True
    return horizontal_cars

def find_target_pos(board):
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == '0':
                return [i, j]
    return None

def write_output(file_path, path, cost, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage):
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(f"Lista de movimientos: {[state.get_move() for state in path]}\n")
        file.write(f"Costo de la ruta: {cost}\n")
        file.write(f"Cantidad de nodos expandidos: {nodes_expanded}\n")
        file.write(f"Profundidad: {search_depth}\n")
        file.write(f"Máxima profundidad de la búsqueda: {max_search_depth}\n")
        file.write(f"Tiempo de ejecución: {running_time} segundos\n")
        file.write(f"Máxima memoria RAM consumida: {max_ram_usage} MB\n")

class GameState:
    def __init__(self, board, car_positions, moves=0, parent=None):
        self.board = board
        self.car_positions = car_positions
        self.moves = moves
        self.parent = parent

    def __eq__(self, other):
        return self.board == other.board and self.car_positions == other.car_positions

    def __hash__(self):
        return hash((str(self.board), str(self.car_positions)))

    def __repr__(self):
        return f"GameState(moves={self.moves}, board={self.board})"

    def is_goal(self, target_pos):
        return self.board[target_pos[0]][target_pos[1]] == 'A'

    def get_successors(self, horizontal_cars):
        successors = []
        move_order = ['u', 'd', 'l', 'r']
        visited_states = set()

        for car in sorted(self.car_positions):
            for move in move_order:
                new_positions = get_new_positions(self.car_positions, car, move, horizontal_cars[car])
                if is_valid_move(self.board, self.car_positions, car, new_positions):
                    new_board = [row[:] for row in self.board]
                    new_car_positions = {k: [pos[:] for pos in v] for k, v in self.car_positions.items()}
                    move_car(new_board, new_car_positions, car, new_positions)
                    new_state = GameState(new_board, new_car_positions, self.moves + 1, self)
                    if new_state not in visited_states:
                        successors.append(new_state)
                        visited_states.add(new_state)

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
def bfs(initial_state, target_pos, horizontal_cars):
    visited = set()
    queue = deque([initial_state])
    visited.add(initial_state)
    nodes_expanded = 0
    max_search_depth = 0

    start_time = time.time()

    while queue:
        state = queue.popleft()
        
        if state.is_goal(target_pos):
            path = []
            temp = state
            while temp.parent:
                path.append(temp)
                temp = temp.parent
            path.reverse()

            running_time = time.time() - start_time
            max_ram_usage = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

            write_output("output.txt", path, state.moves, nodes_expanded, len(path), max_search_depth, running_time, max_ram_usage)

            return state, path, nodes_expanded, len(path), max_search_depth

        successors = state.get_successors(horizontal_cars)
        for successor in successors:
            if successor not in visited:
                visited.add(successor)
                queue.append(successor)
                nodes_expanded += 1
                max_search_depth = max(max_search_depth, successor.moves)

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

    file_path = f"IA-project/Levels/Level{level_number}.txt"
    if not os.path.isfile(file_path):
        input("Nivel no válido o archivo no encontrado, presione Enter para continuar: ")
        clear()
        return start()

    with open(file_path, "rt", encoding="utf-8") as f:
        level = [list(line) for line in f.read().splitlines()]
    return level

def main():
    board = start()

    while True:
        clear()
        car_positions = find_car_positions(board)
        horizontal_cars = find_orientations(car_positions)
        target_pos = find_target_pos(board)

        initial_state = GameState(board, car_positions)
        solution, path, nodes_expanded, search_depth, max_search_depth = bfs(initial_state, target_pos, horizontal_cars)

        if solution:
            print("\nTablero final:")
            print_board(solution.board)
            print("\nSolución encontrada:")
            solution.print_path()
        else:
            print("\nNo se encontró solución.")

        input("\nPresione Enter para continuar...")

        clear()
        board = start()

if __name__ == "__main__":
    main()

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

    file_path = f"IA-project/Levels/Level{level_number}.txt"
    if not os.path.isfile(file_path):
        input("Nivel no válido o archivo no encontrado, presione Enter para continuar: ")
        clear()
        return start()

    with open(file_path, "rt", encoding="utf-8") as f:
        level = [list(line) for line in f.read().splitlines()]
    return level

def main():
    board = start()

    while True:
        clear()
        car_positions = find_car_positions(board)
        horizontal_cars = find_orientations(car_positions)
        target_pos = find_target_pos(board)

        initial_state = GameState(board, car_positions)
        solution, path, nodes_expanded, search_depth, max_search_depth = bfs(initial_state, target_pos, horizontal_cars)

        if solution:
            print("\nTablero final:")
            print_board(solution.board)
            print("\nSolución encontrada:")
            solution.print_path()
        else:
            print("\nNo se encontró solución.")

        input("\nPresione Enter para continuar...")

        clear()
        board = start()

if __name__ == "__main__":
    main()