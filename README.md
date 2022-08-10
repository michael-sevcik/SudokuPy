# Author
Michael Ševčík

MFF UK student 

# Goal
The goal of this project was to develop a Sudoku game app in Python using PyGame as a final class project.

# Solution
This application consists of thee main files:
- run.pyw 
- GUI.py
- Sudoku.py

## run.pyw 
run.pyw is a startup file that creates [sudoku_GUI](#guipy---sudokugui-class) object and runs game loop.

In the game loop `sudoku_GUI.check()` is ran until it returns `False`, which signals terminating of the app. 

## GUI.py - `sudoku_GUI` class
GUI.py contains a definition of `sudoku_GUI` object, a heart of the operation.
- It initiates `PyGame` which is used to create an app window, display content on the window and register user input events. 
- It creates [Sudoku](#sudokupy---sudoku-class), that provides a way to generate, change, check and solve a sudoku.
- It processes user inputs such as are mouse clicks and key presses.
- It displays game information on the app window.

## Sudoku.py - `Sudoku` class
GUI.py contains a definition of `Sudoku` class and `UsageCounter`, which is used to remember a number of uses of a given number in box, column or row.

`Sudoku` class object generates a random sudoku puzzle on initialization with given number boxes to fill in, then provides changing values in grid boxes and a way to solve the grid in steps.

### Generating
- Firstly, one full valid row with shuffled values is generated and added as the first row.
- Then shuffled values are shifted n-places and copied to random row under the first one.
- [`solve()`](#solving) is called after sudoku grid is prepared this way
- Finally, a given number of boxes is left out free.

### Changing values
Values must be changed using `set_cells_value_user()` method in order to let necessary checks and auxiliary data structures updates be performed.

### Checking for invalid cell
When values of cells are changed using `set_cells_value_user()`, information about incorrectly filled in cells (i.e. with number that repeats in the same box, column or row) are stored in `errorCells` dictionary.

### Solving
Solve method performs on each call one step of a process of finding the solution. It is based on backtracking, so it either adds values to the sudoku grid and `solvedCells` list until all cells of sudoku grid are validly filled in or there are no possible numbers to add, in that case algorithm backtracks one step back and tries different combinations.

Firstly, all `errorCells` are emptied. Then, if there are any `cellsToSolve`, solver goes through each of them and fills first possible numbers using the information in [auxiliary data structures](#storing-usage-count-of-given-number-in-a-certain-rowcolumnbox). It tries to incorporate valid cells filled by user, so the algorithm prefers such cell values and changes them only if different combination needs to be tried in a backtracking phase.

`solve` method returns int signaling if it needs to be called again to finish solving the sudoku grid, this makes possible displaying the algorithm step by step to user.

During development, I thought about a simpler solution without [auxiliary data structures](#storing-usage-count-of-given-number-in-a-certain-rowcolumnbox), but I figured it is more effective this way, and in addition, I can use the information about the count of number uses in the validity checking.

```Python 
def solve(self):
    """Fills in all empty spaces in Sudoku grid
    
    The method works only if cells in grid are all valid
    :return: 0 if solved, 1 when there are empty cells left in sudoku grid, 2 when solution does not exist.
    """ 
    # First set any invalid cell to empty
    if len(self.errorCells) > 0:
        cell = self.errorCells.popitem()[0]
        self.set_cell_as_empty(cell)
        return 1
        
    # Fills what needs to be filled
    elif self.cellsToSolve:
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
                    
            return 1 # some cells might be still empty     
        
    return 0 # all cells are filled in
```
### Storing usage count of given number in a certain row/column/box
In `rows`, `columns` and `boxes` variables, which are lists of lists of UsageCounter class objects, that store count of uses of numbers in a given part of sudoku grid, e.g. rows[2][3].count says how many times 4 is used in 3rd row (0-based indexing is used). This information is used to determine whether a number is possible to be used in a certain position, e.g. 
```python
if (rows[0][3].count == 0 and columns[0][3].count == 0 and boxes[0][3].count == 0):
    # 4 is possible to be used on position [0][0] 
```

# Discussion
Overall, I think I developed a playable game, that serves its purpose. It thought me a lot of things about programming and also my style of work. 

Should the development ever continue, the app's GUI in particular could be improved.

***
For more details see the code and code comments

# Sudoku Game - Tutorial
## Starting the game

To start the game run run.pyw in Sudoku directory.

## Game control

When the game window pops up, the Sudoku grid is automatically generated. 

### Picking cell

To pick a cell, you want to fill in, navigate your cursor to the desired location and press the left mouse button. The cell will be highlighted to signal, that it's picked.

### Writing in a cell

Firstly, pick a desired cell, then press a number between 1-9. You cannot change cells that were prefilled.

### Deleting a cell's content

Firstly, pick a desired cell, then press 0, backspace or delete button.

### Checking if filled cells are valid

To check if you have filled cells correctly, press check button. Then, if there are some incorrectly filled cells, the column, row or box, in which the cell is, based on the reason, why it is incorrect.

If you have filled all cells correctly, you will see a win message.

### Solution

If you want to see a correct solution, press the solve button.

### Generating new Sudoku puzzle

To generate a new content, press the restart button.
