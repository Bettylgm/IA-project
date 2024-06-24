import random


class Bobo:
   def __init__(self, board=None, exit_row=2):
       self.exit_row = exit_row  # Ensure exit_row is initialized firstt
       if board is None:
           self.board = self.create_board()
       else:
           self.board = board
   def create_board(self):
       board = [["." for _ in range(6)] for _ in range(6)]
       vehicles = {
           "G": 2,
           "B": 3,
           "O": 3,
           "T": 2,
           "P": 2,
       }
       # Place the "A" car horizontally on the winning roww
       winning_car_a = random.randint(0, 4)
       for i in range(2):
           board[self.exit_row][winning_car_a + i] = "A"
       for vehicle, size in vehicles.items():
           placed = False
           while not placed:
               orientation = random.choice(["H", "V"])
               if orientation == "H":
                   row = random.randint(0, 5)
                   col = random.randint(0, 6 - size)
                   if all(board[row][col + i] == "." for i in range(size)):
                       for i in range(size):
                           board[row][col + i] = vehicle
                       placed = True
               else:
                   row = random.randint(0, 6 - size)
                   col = random.randint(0, 5)
                   if all(board[row + i][col] == "." for i in range(size)):
                       for i in range(size):
                           board[row + i][col] = vehicle
                       placed = True
       return board
   def display_the_game_board(self):
       print("####------------------###")
       for row in self.board:
           print(" ".join(row), "|")
       print("####------------------###")
   def is_possible_to_move(self, coords, direction, steps=1):
       for r, c in coords:
           if direction == "up" and (r - steps < 0 or self.board[r - steps][c] not in (".", self.board[r][c])):
               return False
           if direction == "down" and (r + steps >= len(self.board) or self.board[r + steps][c] not in (".", self.board[r][c])):
               return False
           if direction == "left" and (c - steps < 0 or self.board[r][c - steps] not in (".", self.board[r][c])):
               return False
           if direction == "right" and (c + steps >= len(self.board[r]) or self.board[r][c + steps] not in (".", self.board[r][c])):
               return False
       return True
   def make_move(self, coords, vehicle, direction, steps=1):
       for r, c in coords:
           self.board[r][c] = "."
       new_coords = []
       for r, c in coords:
           if direction == "up":
               new_coords.append((r - steps, c))
           elif direction == "down":
               new_coords.append((r + steps, c))
           elif direction == "left":
               new_coords.append((r, c - steps))
           elif direction == "right":
               new_coords.append((r, c + steps))
       for r, c in new_coords:
           self.board[r][c] = vehicle
   def move(self, direction, vehicle, steps=1):
       if direction not in ("up", "down", "left", "right"):
           print("Invalid direction!")
           return False
       vehicle_coords = self.find_vehicle(vehicle)
       if not vehicle_coords:
           print("Vehicle not found!")
           return False
       if not self.is_possible_to_move(vehicle_coords, direction, steps):
           print("Move is not possible!")
           return False
       self.make_move(vehicle_coords, vehicle, direction, steps)
       return True
   def find_vehicle(self, vehicle):
       vehicle_coords = []
       for r in range(len(self.board)):
           for c in range(len(self.board[r])):
               if self.board[r][c] == vehicle:
                   vehicle_coords.append((r, c))
       return vehicle_coords
   def is_won(self):
       winning_car_position = self.find_vehicle("A")
       if winning_car_position:
           row, col = winning_car_position[0]
           # Check if the winning car is at the far-right edge of the exit row
           if row == self.exit_row and col == len(self.board[row]) - 2:
               return True
       return False

def main():
   bobo = Bobo()
   bobo.display_the_game_board()
   while True:
       vehicle = input("Enter Vehicle Letter: ").upper()
       direction = input("Enter Direction (up, down, left, right): ").lower()
       if bobo.move(direction, vehicle, 1):
           bobo.display_the_game_board()
           if bobo.is_won():
               print("We won 🥳")
               break
       else:
           print("Move failed. Try again.")

if __name__ == "__main__":
   main()