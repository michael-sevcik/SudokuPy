from random import randint, shuffle     # Randint and shuffle are used for generating Sudoku grid

class Sudoku:
    def __init__(self, numberOfCellsToLeaveEmpty):
        """ Initializes a Sudoku object
        
        :param numberOfCellsToLeaveEmpty: Determins how many cells should be left out empty when generating sudoku grid
        :type numberOfCellsToLeaveEmpty: int
        """
        self.emptySpaces = []
        # List of lists of bools for each column/row/box determiting if a number can be used in them
        # e.g. if columns[1][3] == true then number 3 is not used yet in the 2nd column
        self.columns = [[True for _ in range(9)] for _ in range(9)]
        self.rows = [[True for _ in range(9)] for _ in range(9)]
        self.boxes = [[True for _ in range(9)] for _ in range(9)]
        self.generate()

    def generate(self) -> list:
        """ Function to generate elements into the Sudoku grid. """
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
        self.solve()

        # Leaves 20 cells empty
        leftOutCells = {}
        while len(leftOutCells) < 20:
            self.cell = (randint(0, 8), randint(0, 8))
            if self.cell not in leftOutCells :
                grid[self.cell[0]][self.cell[1]] = 0
                leftOutCells[self.cell] = True

        list

        return self.grid # todo: determine if this should return something

    def which_box(self, i, j):
        """ Returns number of box that the given cell belongs
        param i: Cell's row
        type i: int
        param j: Cell's column
        type j: int
        """
        return (3*(i // 3) + (j // 3))

    def setElement(self, columns, rows, boxes, coordinations, mode):
        """ Sets auxiliary data structures according to the mode param
        
        :param columns: 2D list which says if a number is possible to use in a given column
        :type i: list of lists with booleans values
        :param rows: 2D list which says if a number is possible to use in a given row
        :type i: list of lists with booleans values
        :param boxes: 2D list which says if a number is possible to use in a given box
        :type i: list of lists with booleans values
        :param coordinations: (cell's row, cell's column)
        :type coordinations: (int, int)
        :param mode: True for is free to use, False for is used
        :type mode: bool
        """
        i, j = coordinations
        indexN = self.grid[i][j] - 1
        columns[j][indexN] = mode
        rows[i][indexN] = mode
        boxes[self.which_box(i, j)][indexN] = mode

    def find_possible_n(self, columns, rows, boxes, i, j, startIndex = 0):
        """ Finds first possible number to put in the given cell
        
        :param columns: 2D list which says if a number is possible to use in a given column
        :type i: list of lists with booleans values
        :param rows: 2D list which says if a number is possible to use in a given row
        :type i: list of lists with booleans values
        :param boxes: 2D list which says if a number is possible to use in a given box
        :type i: list of lists with booleans values
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
            if (columns[j][x] and
                rows[i][x] and
                boxes[indexOfBox][x]):
                    number = x + 1
                    wasFound = True
                    break
        return (wasFound, number)

    def solve(self):
        """ Fills in all empty spaces in Sudoku grid.
        
        Empty space is represented with 0
        """

        

        # Finds all empty cells that needs to be filled
        cellsToSolve = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.columns[j][self.grid[i][j] - 1] = False
                    self.rows[i][self.grid[i][j] - 1] = False
                    self.boxes[self.which_box(i, j)][self.grid[i][j] - 1] = False
                else: cellsToSolve.append([i, j, 0])    #[row n, column n, starting index]
        
        # Fills what needs to be filled
        if cellsToSolve:
            solvedCells = [] # List of already filled cells

            # Repeate untill all the cells are filled
            while len(solvedCells) < len(cellsToSolve):
                i, j, startingIndex  = cellsToSolve[len(solvedCells)]
                possibleN = self.find_possible_n(self.columns, self.rows, self.boxes, i, j, startingIndex)

                # If possible number was found
                if possibleN[0]: 
                    self.grid[i][j] = possibleN[1]
                    cellsToSolve[len(solvedCells)][2] = possibleN[1] # Set startingindex to prevent infinete loop
                    self.setElement(self.columns, self.rows, self.boxes, (i, j), False)
                    solvedCells.append((i, j))

                # If there are solved cells that we can restore to be unsolved
                elif len(solvedCells) > 0: 
                    cellsToSolve[len(solvedCells)][2] = 0
                    toRestore = solvedCells.pop()
                    self.setElement(self.columns, self.rows, self.boxes, toRestore, True)
                    self.grid[i][j] = 0
                else: return False # No possible solutions
                
        else: return True

def main():
    """ Prints generated Sudoku grid """
    sudoku = Sudoku()
    for row in sudoku.grid:
        print(*row)
    print()
    
    
if __name__ == '__main__':
    main()