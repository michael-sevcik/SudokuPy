from random import randint, shuffle # Randint and shuffle are used for generating Sudoku grid

class Sudoku:
    """Sudoku class provides backend functionalities for generating and operating with sudoku grid"""
    def __init__(self, numberOfCellsToLeaveEmpty):
        """Initializes a Sudoku object
        
        :param numberOfCellsToLeaveEmpty: Determins how many cells should be left out empty when generating sudoku grid
        :type numberOfCellsToLeaveEmpty: int
        """
        self.numberOfCellsToLeaveEmpty = numberOfCellsToLeaveEmpty
        
        self.cellsToSolve = [] # list of empty cells
        self.solvedCells = [] # List of already filled cells
        
        # Dict of error cells tuples { coordinations : reason), coordinations = (i, j)
        # reason is tuple of bools (row, column, box) true for more then one duplicit number in the same part
        self.errorCells = {}
        
        # Dict of cells changed by user { coordinations : True }, coordinations = (i, j)
        self.cellsChangedByUser = {}

        # List of lists of bools for each column/row/box determiting if a number can be used in them
        # e.g. if columns[1][3] == true then number 3 is not used yet in the 2nd column
        self.columns = [[True for _ in range(9)] for _ in range(9)]
        self.rows = [[True for _ in range(9)] for _ in range(9)]
        self.boxes = [[True for _ in range(9)] for _ in range(9)]
        self.generate()

    def generate(self) -> list:
        """Function to generate elements into the Sudoku grid. """
        # Creates a shuffled row
        shuffledRow = [i for i in range(1,10)]
        shuffle(shuffledRow)

        # Creates an empty Sudoku grid
        grid = [[0 for _ in range(9)] for _ in range(9)]

        # Places shuffled row into the lower 2 thirds of the grid
        randIndex = randint(3, 8)
        grid[randIndex] = shuffledRow

        # Places shifted shuffledRow as row 0
        shiftNPlaces = randint(1, 8)
        for i in range(9):
            grid[0][i] = shuffledRow[(i + shiftNPlaces) % 9]

        # Fills the grid
        self.grid = grid
        self.map_grid()
        while self.solve() == 1: pass

        # Leaves numberOfCellsToLeaveEmpty cells empty
        leftOutCells = {}
        while len(leftOutCells) < self.numberOfCellsToLeaveEmpty:
            cell = (randint(0, 8), randint(0, 8))
            if cell not in leftOutCells: 
                self.set_cell_as_empty(cell)
                leftOutCells[cell] = True
        self.map_grid()

    def which_box(self, i, j):
        """Returns number of box that the given cell belongs
        param i: Cell's row
        type i: int
        param j: Cell's column
        type j: int
        """
        return (3*(i // 3) + (j // 3))

    def set_cell_as_empty(self, coordinations):
        """Sets value of a cell to 0 and changes auxiliary data structures accordingly
        
        :param coordinations: (cell's row, cell's column)
        :type coordinations: (int, int)
        """
        i, j = coordinations
        indexN = self.grid[i][j] - 1
        self.grid[i][j] = 0
        
        # Removes pottential record in self.cellsChangedByUser
        if (i, j) in self.cellsChangedByUser:
            del self.cellsChangedByUser[(i, j)]
            
        # Removes pottantial errorCells records of duplicit values
        if (i, j) in self.errorCells:
            del self.errorCells[(i, j)]
        else:
            self.columns[j][indexN] = True
            self.rows[i][indexN] = True
            self.boxes[self.which_box(i, j)][indexN] = True
       
    def set_cells_value(self, coordinations, value):
        """Sets value of a cell and changes auxiliary data structures accordingly

        :param coordinations: (cell's row, cell's column)
        :type coordinations: (int, int)
        :param mode: True for is free to use, False for is used
        :type mode: bool
        :param value: New value of element
        :type value: int
        """
        i, j = coordinations
        # if original value of the element is not 0 as empty
        if self.grid[i][j] != 0:
            self.set_cell_as_empty(coordinations)

        self.grid[i][j] = value
        indexN = value - 1

        if value > 0:
            box_index = self.which_box(i, j)
            # Checks for duplicit values
            isColumnProblem = not self.columns[j][indexN]
            isRowProblem = not self.rows[i][indexN]
            isBoxProblem = not self.boxes[box_index][indexN]
            if isColumnProblem or isRowProblem or isBoxProblem:
                self.errorCells[coordinations] = (isColumnProblem, isRowProblem, isBoxProblem)
            else:
                self.columns[j][indexN] = False
                self.rows[i][indexN] = False
                self.boxes[box_index][indexN] = False
                
    def set_cells_value_user(self, coordinations, value):
        """Sets value of a cell, changes auxiliary data structures accordingly and register cell as changed by user

        :param coordinations: (cell's row, cell's column)
        :type coordinations: (int, int)
        :param mode: True for is free to use, False for is used
        :type mode: bool
        :param value: New value of element
        :type value: int
        """
        self.set_cells_value(coordinations, value)
        self.cellsChangedByUser[coordinations] = True
        
        # Check each error cell if it is still still an error cell after some value is changed because it can make other cell valid
        i, j = coordinations
        originalValue = self.grid[i][j]
        errorCells = list(self.errorCells.keys())

        for errorCell in errorCells:
            errrorI, errorJ = errorCell
            if self.grid[errrorI][errorJ] == originalValue and errorCell != coordinations:
                if i == errrorI:
                    problemsWithCell = self.errorCells[errorCell]
                    self.errorCells[errorCell] = (False, problemsWithCell[1], problemsWithCell[2])
                if j == errorJ:
                    problemsWithCell = self.errorCells[errorCell]
                    self.errorCells[errorCell] = (problemsWithCell[0], False, problemsWithCell[2])
                if self.which_box(i, j) == self.which_box(errrorI, errorJ):
                    problemsWithCell = self.errorCells[errorCell]
                    self.errorCells[errorCell] = (problemsWithCell[0], problemsWithCell[1], False)
            if self.errorCells[errorCell] == (False, False, False):
                del self.errorCells[errorCell]
                        
 
    def find_possible_n(self, i, j, startIndex = 0):
        """Finds first possible number to put in the given cell
        
        :param i: Cell's row
        :type i: int
        :param j: Cell's column
        :type j: int
        :param j: First number from which this method starts looking a possible number
        :type j: int
        :return: Returns tuple (bool if possible number exists, int possible number)
        """
        indexOfBox = self.which_box(i, j)
        wasFound = False
        number = 0
        for x in range(startIndex, 9): #maybe n of step is needed
            if (self.columns[j][x] and
                self.rows[i][x] and
                self.boxes[indexOfBox][x]):
                    number = x + 1
                    wasFound = True
                    break
        return (wasFound, number)
    
    def map_grid(self):
        """Finds all empty cells that needs to be filled and puts information to auxiliary data structures - rows, columns, boxes"""
        self.cellsToSolve = []
        self.solvedCells = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.columns[j][self.grid[i][j] - 1] = False
                    self.rows[i][self.grid[i][j] - 1] = False
                    self.boxes[self.which_box(i, j)][self.grid[i][j] - 1] = False
                else: self.cellsToSolve.append([i, j, 0])    #[row n, column n, starting index]
    
    def is_win(self):
        """Checks if the sudoku is solved"""
        if (self.numberOfCellsToLeaveEmpty <= len(self.cellsChangedByUser) and len(self.errorCells) == 0):
            return True
        return False

    def solve(self):
        """Fills in all empty spaces in Sudoku grid
        
        The method works only if cells in grid are all valid
        :return: 0 if solved, 1 when there are empty cells left in sudoku grid, 2 when solution does not exist.
        """
        # Fills what needs to be filled
        if self.cellsToSolve:
            # If there are leftout cells, try to fill them
            if len(self.solvedCells) < len(self.cellsToSolve):
                # if it is filled and not wrong, use it  
                i, j, startingIndex  = self.cellsToSolve[len(self.solvedCells)]
                possibleN = self.find_possible_n(i, j, startingIndex)
                
                # If there is already a valid number, try to leave it
                if self.grid[i][j] != 0:
                    self.solvedCells.append((i, j))
                    
                # If possible number was found
                elif possibleN[0]: 
                    self.grid[i][j] = possibleN[1]
                    self.cellsToSolve[len(self.solvedCells)][2] = possibleN[1] # Set startingindex to go though only not visited states
                    self.set_cells_value((i, j), possibleN[1])
                    self.solvedCells.append((i, j))

                # If there are solved cells that we can restore to be empty
                elif len(self.solvedCells) > 0: 
                    self.cellsToSolve[len(self.solvedCells)][2] = 0
                    toRestore = self.solvedCells.pop()
                    self.set_cell_as_empty(toRestore)
                    
                else:
                    # If there are no computer solved cells to revert, empty cells added by user
                    if len(self.cellsChangedByUser) > 0:
                        for i in range(len(self.cellsToSolve)):
                            self.set_cell_as_empty(self.cellsToSolve[i][:2])
                        self.cellsToSolve[0][2] = 0
                    else: 
                        self.cellsToSolve[0][2] = 0
                        # return 2 # no possible solution
                        
                return 1 # some cells might be still empty     
            
        return 0 # all cells filled
    
def main():
    """Prints generated Sudoku grid """
    sudoku = Sudoku(20)
    for row in sudoku.grid:
        print(*row)
    print()
   
if __name__ == '__main__':
    main()