import random
from termcolor import colored
import time

class Sudoku():
    def __init__(self):
        self.grid = [[Cell(j,i) for i in range(9)] for j in range(9)]
        self.tl = MiniSquare([self.grid[i][0:3] for i in range(3)])
        self.tc = MiniSquare([self.grid[i][3:6] for i in range(3)])
        self.tr = MiniSquare([self.grid[i][6:9] for i in range(3)])
        self.cl = MiniSquare([self.grid[i+3][0:3] for i in range(3)])
        self.cc = MiniSquare([self.grid[i+3][3:6] for i in range(3)])
        self.cr = MiniSquare([self.grid[i+3][6:9] for i in range(3)])
        self.bl = MiniSquare([self.grid[i+6][0:3] for i in range(3)])
        self.bc = MiniSquare([self.grid[i+6][3:6] for i in range(3)])
        self.br = MiniSquare([self.grid[i+6][6:9] for i in range(3)])
        self.miniSquares = [[self.tl, self.tc, self.tr], [self.cl, self.cc, self.cr], [self.bl, self.bc, self.br]]
        
    def display(self):
        print("\n" * 40)
        for i in range(len(self.grid)):
            rowToPrint = ""
            for cell in self.grid[i]:
                if cell.value is not None:
                    character = str(cell.value)
                else:
                    character = " "
                if not cell.fixed:
                    if cell.working:
                        rowToPrint += colored(character, color="yellow")
                    else:
                        rowToPrint += colored(character, color="green")
                else:
                    rowToPrint += character
                if cell.column % 3 == 2 and cell.column != len(self.grid[i]):
                    rowToPrint += "|"
            print(rowToPrint)
            if i % 3 == 2 and i != len(self.grid):
                print("---+---+---")
                
    def solve(self):
        solved = False
        rowSolving = 0
        columnSolving = 0
        solvingStack = Stack(81)
        while not solved:
            if self.grid[rowSolving][columnSolving].fixed:
                if columnSolving < 8:
                    columnSolving += 1
                elif columnSolving == 8 and rowSolving == 8:
                    solved = True
                else:
                    columnSolving = 0
                    rowSolving += 1
            else:
                if rowSolving == 8 and columnSolving == 8 and self.grid[8][8].value is not None:
                    solved = True
                else:
                    if self.grid[rowSolving][columnSolving].value is None:
                        number = 1
                    else:
                        self.grid[rowSolving][columnSolving].value = None
                    numberFits = False
                    while not numberFits and number <= 9:
                        self.grid[rowSolving][columnSolving].value = number
                        self.grid[rowSolving][columnSolving].working = True
                        self.display()
                        self.grid[rowSolving][columnSolving].value = None
                        self.grid[rowSolving][columnSolving].working = False
                        time.sleep(0.01)
                        fitsInSquare = True
                        fitsInRow = True
                        fitsInColumn = True
                        # checking if fits in square
                        square = self.miniSquares[rowSolving // 3][columnSolving // 3]
                        for cell in square.cellsArray:
                            if cell.value == number:
                                fitsInSquare = False
                        # checking if fits in row
                        row = self.grid[rowSolving]
                        for cell in row:
                            if cell.value == number:
                                fitsInRow = False
                        # checking column
                        for row in self.grid:
                            cell = row[columnSolving]
                            if cell.value == number:
                                fitsInColumn = False
                        # check all conditions
                        if fitsInColumn and fitsInRow and fitsInSquare:
                            numberFits = True
                            solvingStack.push([rowSolving, columnSolving, number])
                            self.grid[rowSolving][columnSolving].value = number
                            if columnSolving < 8:
                                columnSolving += 1
                            elif columnSolving == 8 and rowSolving < 8:
                                columnSolving = 0
                                rowSolving += 1
                        else:
                            number += 1
                    if number > 9: # if no number works
                        previous = solvingStack.pop()
                        number = previous[2] + 1
                        rowSolving = previous[0]
                        columnSolving = previous[1]
                    
    def inputValues(self, preset=None):
        if preset is None:
            print("Enter the sudoku as you would read (each row left to right, top to bottom rows)")
            for i in range(len(self.grid)):
                for j in range(len(self.grid[i])):
                    number = input()
                    if number != "":
                        self.grid[i][j].value = int(number)
                        self.grid[i][j].fixed = True
        else:
            for rowI in range(len(preset)):
                for cellI in range(len(preset[rowI])):
                    if preset[rowI][cellI] == "":
                        self.grid[rowI][cellI].value = None
                    else:
                        self.grid[rowI][cellI].value = preset[rowI][cellI]
                        self.grid[rowI][cellI].fixed = True
                        

class MiniSquare(Sudoku):
    def __init__(self, grid):
        self.grid = grid
        self.cellsArray = []
        for row in self.grid:
            for cell in row:
                self.cellsArray.append(cell)


class Cell():
    def __init__(self, row, column, fixed=False, working=False):
        self.value = None
        self.row = row
        self.column = column
        self.fixed = fixed
        self.working = working
        
        
class Stack():
    def __init__(self, max):
        self.stack = [None for i in range(max)]
        self.maxLength = max
        self.pointer = -1
        
    def push(self, value):
        self.pointer += 1
        if self.pointer < self.maxLength:
            self.stack[self.pointer] = value
        else:
            self.pointer -= 1
            print('Stack Full')
            
    def pop(self):
        if self.pointer >= 0:
            popped = self.stack[self.pointer]
            self.pointer -= 1
            return popped
        else:
            print("Stack Empty")
            return None
        

s = Sudoku()
PRESET = [[3,"","",9,"","","",1,5],
          [7,1,"",3,"",5,"","",2],
          ["","",4,"","","",6,8,""],
          [9,"","","","",2,8,"",7],
          [6,"",5,"",8,"","","",""],
          ["",2,3,6,1,"","",4,""],
          ["","","",7,2,6,1,"",""],
          ["",5,6,"","",3,2,"",4],
          ["",8,"",1,"",4,9,3,""]]
ELEMENTARY = [["","","","",5,"","","",9],
          [7,2,"","",1,"","","",8],
          [5,"",1,4,7,"","",6,""],
          ["",8,"",1,"","",5,"",3],
          ["","","","",4,"",2,"",""],
          [6,"","",9,"",3,"",7,""],
          ["","",5,"","","",8,"",1],
          [8,"","",6,"",1,"",2,""],
          ["","",3,"",9,"","",4,""]]
s.inputValues(preset=ELEMENTARY)
start = time.time()
s.solve()
end = time.time()
s.display()
print(f"Total time: {end-start} seconds")