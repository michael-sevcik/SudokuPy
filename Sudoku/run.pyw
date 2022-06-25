# Is used to create Sudoku app
from GUI import sudoku_GUI

windowStartupWidth = 550
windowStartupHeight = 600
fpsRate = 30
numberOfCellsToLeaveEmpty = 25

def main():
    gui = sudoku_GUI(windowStartupHeight, windowStartupWidth, fpsRate, numberOfCellsToLeaveEmpty)

    run = True
    while run:
        run = gui.check()

if __name__ == '__main__':
    main()