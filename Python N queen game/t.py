import pygame
from pygame.locals import *
from pygame import *
from sys import exit
from random import randint
import thorpy


class Chess_game:
    def __init__(self, w=365, h=400, cell_w=40, cell_h=40, rows=6, cols=8):

        self._screen = None
        self.num = 8
        self._lady_bug = None
        self._clock = pygame.time.Clock()
        self._background_color = (0, 0, 0)  # black rgb
        self._cell_background_color = (255, 255, 255)  # white rgb
        self._gap = 5
        self._input_field = None
        self._window_width = w
        self._window_height = h
        self._cell_width = cell_w
        self._cell_height = cell_h
        self._grid_rows = rows
        self._grid_columns = cols
        self.value = None
        self.ball = None
        self.the_board = []
        self.box_size = None
        self.surf = None
        rand_x = randint(1, self._grid_columns)
        rand_y = randint(1, self._grid_rows)
        self._bug_x = ((rand_x * self._cell_width) + (rand_x * self._gap)) - (self._cell_width / 2)
        self._bug_y = ((rand_y * self._cell_height) + (rand_y * self._gap)) - (self._cell_height / 2)

    def setup(self):
        pygame.init()
        self._screen = pygame.display.set_mode((self._window_width, self._window_height))  # Set the window title
        pygame.display.set_caption("Lady Bug")
        # Load the bug image
        self._lady_bug = pygame.image.load('queen.png')
        self.display_menu()
        self.num = int(self._input_field.get_value().title())
        self.draw_board()

    def make_sound(self):
        beep_sound = pygame.mixer.Sound("air_horn.mp3")  # wav may be recommended for better performance in pygame
        pygame.mixer.Sound.play(beep_sound)
        pygame.mixer.music.stop()


    def draw_board(self):
        """ Draw a chess board with queens, as determined by the the_board. """
        #self._input_field.enter()
        count = 0
        n = self.num
        self.the_board = [[0 for i in range(n)] for j in range(n)]
        pygame.init()
        colors = [(0, 0, 0), (255, 255, 255)]  # Set up colors [red, black]

        n = len(self.the_board)  # This is an NxN chess board.
        surface_sz = 600  # Proposed physical surface size.
        self.box_size = surface_sz / 4
        sq_sz = surface_sz // n  # sq_sz is length of a square.
        surface_sz = n * sq_sz  # Adjust to exactly fit n squares.

        # Create the surface of (width, height), and its window.
        surface = pygame.display.set_mode((surface_sz, surface_sz))
        self.surf = surface
        self.ball = pygame.image.load(r'queen.png')

        # Draw a fresh background (a blank chess board)

        for row in range(n):  # Draw each row of the board.
            c_indx = row % 2  # Alternate starting color
            for col in range(n):  # Run through cols drawing squares
                the_square = (col * sq_sz, row * sq_sz, sq_sz, sq_sz)
                surface.fill(colors[c_indx], the_square)
                # Now flip the color index for the next square
                c_indx = (c_indx + 1) % 2
        pygame.display.flip()
        while True:
            ev = pygame.event.poll()
            if ev.type == pygame.QUIT:
                break;

            if self.place_queen() == True:
                count += 1

            if count == n:
                break
        print(self.the_board)

    def place_queen(self):

        clicked = pygame.mouse.get_pressed()

        if clicked[0] == 1:
            movement_of_mouse = pygame.mouse.get_pos()
            values = list(movement_of_mouse)
            x = values[0]
            x_values = int(int(x) / self.box_size)
            y = values[1]
            y_values = int(int(y) / self.box_size)
            print(x_values, y_values)
            if self.isSafe(x_values, y_values):
                temp_x = x_values
                temp_y = y_values
                self.the_board[x_values][y_values] = '1'
                surface_sz = 600
                self.box_size = surface_sz / self.num
                sq_sz = surface_sz // self.num  # sq_sz is length of a square.
                ball_offset = (sq_sz - self.ball.get_width()) // 2
                x_ball = (sq_sz * (temp_x)) + ball_offset
                y_ball = (sq_sz * (temp_y)) + ball_offset
                self.surf.blit(self.ball, (x_ball, y_ball))
                pygame.display.update()
                return True
        return False

    def isSafe(self, r, c):
        mat = self.the_board
        # return false if two queens share the same column
        if (mat[r][c] == '1'):
            # self.make_sound()
            return False

        for i in range(len(mat)):
            if mat[i][c] == '1' and (i, c) != (r, c):
                print("1")
                self.make_sound()
                return False

        # return false if two queens share the same `` diagonal
        (i, j) = (r, c)
        while i >= 0 and j >= 0:
            if mat[i][j] == '1' and (i, j) != (r, c):
                print("2")
                self.make_sound()
                return False
            i = i - 1
            j = j - 1

        (i, j) = (r, c)
        while i < len(mat) and j >= 0:
            if mat[i][j] == '1' and (i, j) != (r, c):
                print("2")
                self.make_sound()
                return False
            i = i + 1
            j = j - 1

        (i, j) = (r, c)
        while i < len(mat) and j < len(mat):
            if mat[i][j] == '1' and (i, j) != (r, c):
                print("3")
                self.make_sound()
                return False
            i = i + 1
            j = j + 1

        # return false if two queens share the same `/` diagonal
        (i, j) = (r, c)
        while i >= 0 and j < len(mat):
            if mat[i][j] == '1' and (i, j) != (r, c):
                print("4")
                self.make_sound()
                return False
            i = i - 1
            j = j + 1

        for m in range(len(mat)):
            if mat[r][m] == '1' and (r, m) != (r, c):
                print("5")
                self.make_sound()
                return False

        return True

    def update_ui(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            self.draw_board()
            self._clock.tick(60)  # set to 60 FPS self.place_bug()
            # flip allows only a portion of the screen to be updated instead of the entire area
            pygame.display.flip()

    def quit(self):
        pygame.quit()

class TextBox:
    def __init__(self, surface, font_color, x, y, stroke_color=(0, 0, 0)):
        self._text = ""
        self._base_color = stroke_color
        self._font_color = font_color
        self._active_color = (0, 64, 154)
        self._active = False
        self._box = None # the rect containing the text
        self._text_surface = None # the text
        self._screen = surface # where to draw the textbox
        self._x = x
        self._y = y
        self._width = 200 # the width of the textbox
        self._height = 40 # the height of the textbox
        self._font_size = 28
        self._inner_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        self._base_font = pygame.font.Font(None, self._font_size)

    def draw(self):
        if self._active:
            color = self._active_color
        else:
            color = self._base_color

        self._box = pygame.draw.rect(self._screen, color, self._inner_rect, 2)
        self._text_surface = self._base_font.render(self._text, True, self._font_color)
        self._screen.blit(self._text_surface, (self._box.x + 5, self._box.y + 5))
        self._inner_rect.w = max(self._width, self._text_surface.get_width() + 10)

class TextBoxDisplay:
    def __init__(self, w=800, h=600):
        self._window_width=w
        self._window_height=h
        self._background_color=(255, 255, 255)
        self._box_width=40
        self._box_height=40
        self._font_color=(0, 0, 0)
    # add code here to initialize variables
    def setup(self):
        pygame.init()
        # Set window size using a tuple
        self._screen = pygame.display.set_mode((self._window_width, self._window_height))
        self._screen.fill(self._background_color)
        pygame.display.set_caption("Custom TextBox by Dr. Fitz")
        textbox_x = (self._window_width // 2) - (self._box_width // 2)
        textbox_y = (self._window_height // 2) - (self._box_height // 2)
        self._textbox = TextBox(self._screen, self._font_color, textbox_x, textbox_y)
        button_color = (0, 64, 154)
        button_x = textbox_x + 210
        self._button = Button(self._screen, button_color, "Start Game", button_x, textbox_y)


    def update_ui(self):
        playing_game = True
        while playing_game:
            self._clock.tick(45)
            textbox_rect = self._textbox.get_rect() # create a method to return the rect in the TextBox class
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing_game = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if textbox_rect.collidepoint(event.pos):
                    self._textbox.toggle_active(True)
                else:
                    self._textbox.toggle_active(False)
                if self._button.get_rect().collidepoint(event.pos):
                    self._button.toggle_active(True)
                else:
                    self._button.toggle_active(False)
            if event.type == pygame.KEYDOWN and self._textbox.is_active():
                if event.key == pygame.K_BACKSPACE:
                    # Check for backspace
                    # get text input from 0 to -1 to remove 1 character
                    self._user_text = self._user_text[:-1]
                else:
                    self._user_text += event.unicod
                    self._textbox.update_text(self._user_text)

        self._screen.fill(self._background_color)
        self._textbox.draw()
        self._button.draw()
        pygame.display.update()





class application_window():

    def __init__(self):
        self.value=None
        self.insert_=None

    def appli(self):
        application=thorpy.Application((600,600),"N queens by ADD")
        pointer = Chess_game()
        click=thorpy.make_button("Start Game",func=pointer.draw_board)
        thorpy.makeup.add_basic_help(click,"Press to start game")

        self.insert_=thorpy.Inserter(name="Enter value for N:")
        title_element=thorpy.make_text("N queens by ADD",22,(255,255,255))
        elements=[self.insert_,click]
        central_box=thorpy.Box(elements=elements)
        central_box.fit_children(margins=(30,30))
        central_box.center()
        central_box.set_main_color((220,220,220,180))
        background=thorpy.Background(color=(0,0,0),elements=[title_element,central_box])
        thorpy.store(background)
        menu=thorpy.Menu(background)
        print(self.insert_)
        self.get_()
        menu.play()
        print(self.insert_.get_value())
        self.get_()
    def get_(self):

        print("The vale is", self.insert_.get_value())


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 250)
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.n_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.n_lineEdit.setGeometry(QtCore.QRect(225, 70, 100, 20))
        self.n_lineEdit.setObjectName("n_lineEdit")
        self.text_label = QtWidgets.QLabel(self.centralwidget)
        self.text_label.setGeometry(QtCore.QRect(175, 70, 60, 20))
        self.text_label.setObjectName("text_label")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(200, 110, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("background-color: #bbb;\n""border-radius: 8px;")
        self.start_button.setObjectName("start_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Welcome to N Queens by Nicholas Velasquez"))
        self.text_label.setText(_translate("MainWindow", "Enter n:"))
        self.start_button.setText(_translate("MainWindow", "Start Game"))

