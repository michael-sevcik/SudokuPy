import pygame as pg
from pygame_widgets.button import Button
from sudoku import Sudoku

buttonBarRelativeHeight = 0.1
class sudoku_GUI():

    def __init__(self, height , width, FPS, numberOfCellsToLeaveEmpty):
        """sudoku_GUI after initialization creates a Sudoku game window using PyGame 

        :param height: Default height of a game window in px
        :type height: int
        :param width: Default width of a game window in px
        :type width: int
        :param FPS: Number of frames per second
        :type FPS: int
        :param numberOfCellsToLeaveEmpty: Determins how many cells should be left out empty when generating sudoku grid
        :type numberOfCellsToLeaveEmpty: int
        """
        # FPS setting
        pg.init()
        self.FPS = FPS 
        self.fpsClock = pg.time.Clock()

        # FPS setting
        self.width = width
        self.height = height
        self.sudoku = Sudoku(numberOfCellsToLeaveEmpty)
        self.grid = self.sudoku.grid

        # Game information
        self.isElementPicked = False
        self.pickedElement = None
        self.originalGrid = [[self.grid[i][j] for j in range(9)] for i in range(9)]
        
        # Colours
        self.gridElementColor = (52, 31, 151)
        self.backgroundColor = (242, 238, 203)
        
        # For creating control parts
        self.inicializationDone = False

        # Creates window
        self.create_window()


    def create_window(self):
        """ Creates a width x height resizable window/frame """
        win = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)
        pg.display.set_caption("Sudoku")
        self.win = win
        self.display_layout()
        self.inicializationDone = True

    def create_buttons(self):
        """Creates a buttons to control Sudoku game"""
        self.button1 = Button_in_design(self.win, self.button_pressed, (255, 0, 0),
                                       (0, 255, 0), "button1", self.font)
        self.button2 = Button_in_design(self.win, self.button_pressed, (255, 0, 0),
                                        (0, 255, 0), "button2", self.font)

    def set_buttons_size(self):
        """Sets size of and position of Sudoku game buttons based on the size of the game window."""
        buttonsXCoor = int(self.height * (1 - buttonBarRelativeHeight) - (self.dim / 2))
        self.button1.set_size((buttonsXCoor, 1 * self.dim), 3 * self.dim, self.dim)
        self.button2.set_size((buttonsXCoor, 7 * self.dim), 3 * self.dim, self.dim)

    def display_buttons(self):
        """Displays Sudoku game buttons and if necessary it creates them."""
        if not self.inicializationDone:
            self.create_buttons()
        self.set_buttons_size()
        self.button1.draw()
        self.button2.draw()
    
    def display_grid(self):
        """Displays the Sudoku grid on self. win """
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

        # todo: display error columns... if check

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
        self.dim = int(min(self.width, self.height * (1 - buttonBarRelativeHeight)) // 11) 
        self.win.fill(self.backgroundColor)
        self.font = pg.font.SysFont('arial', round(0.7*self.dim))

        self.display_buttons() 

        self.display_grid()

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
        """Processes a mouse click and if necessary, arranges the change of the given letter."""
        # Position of the mouse
        position = pg.mouse.get_pos()
        self.button1.click(position)
        self.button2.click(position)

        i,j = position[1]//(self.dim), position[0]//(self.dim)
        if j <= 0 or i == 0 or j == 10 or j == 10:
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
            self.grid[self.pickedElement[0]-1][self.pickedElement[1]-1] = charCode - 48 # TODO: intergrate Sudoku class element change
            self.isElementPicked = False
            self.display_layout()
            return
        return

    def FPS_hold(self):
        """ Holds the main loop as long as needed based on the set FPS """
        self.fpsClock.tick(self.FPS)

    def button_pressed(self): 
        print("button pressed")
        self.fpsClock.tick(5)
        self.create_window # TODO: repair

    def check(self):
        """ Processes the important events in pg.event.get() """ # todo: specify comment
        events = pg.event.get()
        for event in events:
            if event.type == pg.VIDEORESIZE:
                self.resize(event.size)
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse_click()
            if event.type == pg.QUIT:
                pg.quit()
                return False
            if self.isElementPicked and event.type == pg.KEYDOWN:
                self.key_pressed(event)
        
        self.FPS_hold()
        return True


class Button_in_design():
    def __init__(self, pygameWin, functionToCallOnPress, inactiveColour, pressedCollour, buttonText, font, border_thickness = 4):
        """button class creates clickable button
         
        :param pygameWin: Surface on which to draw
        :type pygameWin: pygame.Surface
        :param functionToCallOnPress: Surface on which to draw
        :type functionToCallOnPress: pygame.Surface
        :param inactiveColour: Tuple (R, G, B) where Red, Green, Blue are between 0 and 256
        :type inactiveColour: (int, int, int)
        :param pressedCollour: Tuple (R, G, B) where Red, Green, Blue are between 0 and 256
        :type pressedCollour: (int, int, int)
        :param buttonText: Text displayed on button
        :type buttonText: string
        :param font: fontsize in px
        :type font: pygame.font
        :param border_thickness: border thickness in px
        :type border_thickness: int
        """
        self.win = pygameWin
        self.functionToCallOnPress = functionToCallOnPress
        self.inactiveColour = inactiveColour
        self.pressedCollour = pressedCollour
        self.text = buttonText
        self.font = font
        self.pressed = False
        self.border_thickness = border_thickness

    def set_size(self, position, height, width):
        """Draws button on the pygame win

        :param position: Tuple (xCoor, yCoor) in px
        :type position: (int, int)
        :param height: Geight of the button in px
        :type height: int
        :param width: Width of the button in px
        :type width: int
        """
        self.position = position
        self.height = height
        self.width = width

    def draw(self):
        """Draws button on the pygame.Surface"""
        # backround
        buttonInnerColour = self.pressedCollour if self.pressed else self.inactiveColour
        self.rect = pg.draw.rect(self.win, buttonInnerColour, 
            (self.position[1], self.position[0], self.height, self.width))
        # button text
        text = self.font.render(self.text, True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (self.position[1] + (self.height / 2), self.position[0] + (self.width / 2))
        self.win.blit(text, textRect)

        # button border
        pg.draw.line(self.win, (0,0,0), (self.position[1], self.position[0]),
                     (self.position[1] + self.height + (self.border_thickness / 2), self.position[0]), self.border_thickness )

        pg.draw.line(self.win, (0,0,0), (self.position[1] + self.height, self.position[0]), 
                     (self.position[1] + self.height, self.position[0] + self.width + (self.border_thickness / 2)), self.border_thickness)

        pg.draw.line(self.win, (0,0,0), (self.position[1], self.position[0] + self.width), 
                     (self.position[1] + self.height, self.position[0] + self.width), self.border_thickness)

        pg.draw.line(self.win, (0,0,0), (self.position[1], self.position[0]), 
                     (self.position[1], self.position[0] + self.width), self.border_thickness)

    def click(self, mouse_pos): # todo: maybe implement auto changing of the pressed state
        """checks if you click on the button and makes the call to the action just one time"""
        if self.rect.collidepoint(mouse_pos):
            if self.pressed == False:
                print("Execunting code for button '" + self.text + "'")
                self.functionToCallOnPress()
                self.pressed = True
                self.draw()
        else: self.pressed = False