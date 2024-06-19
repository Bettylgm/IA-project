import heapq
import msvcrt
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
            if cell.isalpha() and cell != '0' and cell != 'B':  # Encontrar todas las letras que representan autos
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

def write_output(file_path, path, cost, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage):
      with open(file_path, 'w', encoding="utf-8") as file:
         file.write(f"Lista de movimientos: {path}\n")
         file.write(f"costo de la ruta: {cost}\n")
         file.write(f"Cantidad de nodos expandidos: {nodes_expanded}\n")
         file.write(f"Profundidad: {search_depth}\n")
         file.write(f"Máxima profundidad de la búsqueda: {max_search_depth}\n")
         file.write(f"Tiempo de ejecución: {running_time}\n")
         file.write(f"Máxima memoria RAM consumida: {max_ram_usage}\n")
 



def start():
    print(""""
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
 
    if level_number != 0:
       with open(f"CarParkingGame\Levels\Level{level_number}.txt", "rt", encoding="utf-8") as f:
        level = [list(line) for line in f.read().splitlines()]
    else:
       input("Nivel no válido, presione Enter para continuar: ")
       clear()
       start()
       
    return level
    
 
 
def main():
  
    board = start()
    
    while True:
        clear()
        
 
        # Encontrar posiciones de todos los autos
        car_positions = find_car_positions(board)
        horizontal_cars = find_orientations(car_positions)
        target_pos = find_target_pos(board)
        
        # algorithms = {'BFS': SearchAlgorithms.bfs, 'DFS': SearchAlgorithms.dfs, 'A*': SearchAlgorithms.astar}
        start_pos = next((i, j) for i, row in enumerate(board) for j, cell in enumerate(row) if cell == 'A')
        
        start_time = time.time()
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Aquí van las llamadas de los algoritmos
        
        end_time = time.time()
        final_memory = process.memory_info().rss
        running_time = end_time - start_time
        max_ram_usage = (final_memory - initial_memory) / (1024 * 1024)  # Convert to MB
        # write_output(f'output.txt' , path, search_depth, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage)
        
        print_board(board)
        
      #  heuristics = {'Heuristic 1': heuristic1, 'Heuristic 2': heuristic2, 'Heuristic 3': heuristic3}
 
       
 
        # write_output()
        if board[target_pos[0]][target_pos[1]] == 'A':
            clear()
            print("¡Felicidades! Has ganado el juego.")
            break
 
        print()
 
    
 
if __name__ == "__main__":
    set_color()
    main()