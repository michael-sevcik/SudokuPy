import pygame as pg
from pygame_widgets.button import Button
from sudoku import Sudoku

def button_pressed():
    print("button pressed")

class GUI_class():
    
    grid = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]]

    def __init__(self, height , width, FPS):
        """ Inicializes user gui 

        :param height: Default height of a game window in px
        :type height: int
        :param width: Default width of a game window in px
        :type width: int
        :param FPS: Number of frames per second
        :type FPS: int

        """
        # FPS setting
        pg.init()
        self.FPS = FPS 
        self.fpsClock = pg.time.Clock()

        # FPS setting
        self.width = width
        self.height = height
        self.sudoku = Sudoku(5)
        self.grid = self.sudoku.generate()

        # Game information
        self.isElementPicked = False
        self.pickedElement = None
        self.originalGrid = [[self.grid[i][j] for j in range(9)] for i in range(9)]
        self.isButtonPressed = False # todo: determine if this should be deleted
        
        # Colours
        #self.buffer = 5        # todo: determine if this should be deleted
        self.gridElementColor = (52, 31, 151)
        self.backgroundColor = (242, 238, 203)
        
        # Creates window
        self.create_window()

    def create_window(self):
        """ Creates a width x height resizable window/frame """
        win = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        pg.display.set_caption("Sudoku")
        #pg.display.flip() # todo determine if this should be deleted.
        self.win = win
        self.create_button()
        self.display_layout()

    def create_button(self):
        self.button = Button(
        self.win, 100, 100, 300, 150, text='Hello',
        fontSize = 50, margin = 20,
        inactiveColour = (255, 0, 0),
        pressedColour = (0, 255, 0), radius=20,
        onClick = lambda: button_pressed())
    
    def display_grid(self):
        """ Displays the Sudoku grid on self. win """
        # Highlights a position of the picked element
        if (self.isElementPicked and 
            self.originalGrid[self.pickedElement[0] - 1][self.pickedElement[1] - 1] == 0):
            pg.draw.rect(self.win, (255,255,255), 
                        (self.pickedElement[1]*self.dim, self.pickedElement[0]*self.dim, self.dim, self.dim))

        # Displays values
        for i in range(0, len(self.grid[0])):
            for j in range(0, len(self.grid[0])):
                if 0 <= self.grid[i][j] < 10:
                    if self.originalGrid[i][j] != 0:
                        value = self.font.render(str(self.grid[i][j]), True, (0, 0, 0))
                    else: value = self.font.render(str(self.grid[i][j]), True, self.gridElementColor)
                    self.win.blit(value, ((j+1)*self.dim + round(0.4*self.dim), (i+1)*self.dim + self.dim//10))

        # Draws lines of Sudoku grid
        for i in range(0,10):
            if(i%3 == 0):
                pg.draw.line(self.win, (0,0,0), (self.dim + self.dim*i, self.dim), (self.dim + self.dim*i ,10*self.dim ), 4 )
                pg.draw.line(self.win, (0,0,0), (self.dim, self.dim + self.dim*i), (10*self.dim, self.dim + self.dim*i), 4 )
            else:
                pg.draw.line(self.win, (0,0,0), (self.dim + self.dim*i, self.dim), (self.dim + self.dim*i ,10*self.dim ), 2 )
                pg.draw.line(self.win, (0,0,0), (self.dim, self.dim + self.dim*i), (10*self.dim, self.dim + self.dim*i), 2 )
        
    def display_layout(self):
        """ Displays all GUI elements on self.win """
        # Dimension of one sudoku cell
        self.dim = min(self.width, self.height) // 11
        self.win.fill(self.backgroundColor)
        self.font = pg.font.SysFont('arial', round(0.7*self.dim))

        self.display_grid()
        
        self.button.draw()
        pg.display.update()

    def resize(self, size):
        """ A function to change the size of a window

        :param size: Tuple (width, height) in px
        :type size: (int, int)
        """
        self.width, self.height = size

        # redraw win in new size
        self.create_window()
        print(self.win.get_size())  # test

    def mouse_click(self):
        """ Processes a mouse click
       
        If necessary, arranges the change of the given letter.
        """
        # Position of a mouse
        position = pg.mouse.get_pos()

        i,j = position[1]//(self.dim), position[0]//(self.dim)
        if j <= 0 or i == 0 or j == 10 or j == 10: # todo: p
            self.isElementPicked = False
        if 0 < i < 10 and 0 < j < 10:
            self.isElementPicked = True
            self.pickedElement = (i, j)
        self.display_layout()

    def key_pressed(self, event):
        """ Processes the event pygame.KEYDOWN and, if necessary, arranges the change of the given letter.
        
        :param event: Event in which keydown was captured
        :type event: pygame.event
        """
        # Determines if the picked element is user changeble
        if(self.originalGrid[self.pickedElement[0]-1][self.pickedElement[1]-1] != 0):
            return

        # Changes the value of the picked element to the based on the key that was pressed
        try: charCode = ord(event.unicode)
        except: return
        if(0 <= charCode - 48 < 10):  #Checking for valid input
            self.grid[self.pickedElement[0]-1][self.pickedElement[1]-1] = charCode - 48
            self.isElementPicked = False
            self.display_layout()
            return
        return

    def FPS_hold(self):
        """ Holds the main loop as long as needed based on the set FPS """
        self.fpsClock.tick(self.FPS)

    #def button_pressed(self):
    #    print("button pressed")
    #    self.fpsClock.tick(5)
    #    self.create_window

    def check(self):
        """ Processes the important events in pg.event.get() """ # todo specify comment
        events = pg.event.get()
        for event in events:
            if event.type == pg.VIDEORESIZE:
                self.resize(event.size)
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse_click(events)
            if event.type == pg.QUIT:
                pg.quit()
                return False
            if self.isElementPicked and event.type == pg.KEYDOWN:
                self.key_pressed(event)
            if self.button.listen(events):
                print()
        
        print(int(self.fpsClock.get_fps()))
        self.FPS_hold()
        return True

