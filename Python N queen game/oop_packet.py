import pygame
from random import randint
import thorpy


# This sets the tab where the user enters the number for n
class MyGame(object):

    def __init__(self):
        self.guess = None
        self.link = None
        self.e_quit = thorpy.make_button("Quit", func=thorpy.functions.quit_menu_func)
        self.start_game = thorpy.make_button("START GAME", func=thorpy.functions.quit_menu_func)

        self.e_counter = thorpy.make_text(text=self.get_trials_text(), font_color=(255, 255, 255))
        self.e_group_menu = thorpy.make_group([self.e_quit, self.start_game])
        self.e_insert = thorpy.Inserter(name="Enter N:")
        self.e_background = thorpy.Background(color=(0, 0, 0),
                                              elements=[self.e_counter, self.e_insert, self.e_group_menu])
        thorpy.store(self.e_background, gap=20)
        # reaction called each time the player has inserted something
        reaction_insert = thorpy.ConstantReaction(
            reacts_to=thorpy.constants.THORPY_EVENT,
            reac_func=self.reac_insert_func,
            event_args={"id": thorpy.constants.EVENT_INSERT,
                        "el": self.e_insert})
        self.e_background.add_reaction(reaction_insert)

    def get_trials_text(self):
        return "Welcome to N queens game by Ankur Dhadoti"

    def reac_insert_func(self):  # here is all the dynamics of storing the value from the user
        value = self.e_insert.get_value()
        self.e_insert.set_value("")
        # self.send_main()
        self.e_insert.unblit_and_reblit()
        try:
            self.guess = int(value)

        except ValueError:
            return

    def send_main(self):
        return self.guess

    def launch_game(self):
        menu = thorpy.Menu(self.e_background)
        menu.play()


# This function sets the chess board and the logic everything is there in this class
class Chess_game:
    def __init__(self, user_value, w=365, h=400, cell_w=40, cell_h=40, rows=6, cols=8):

        self._screen = None
        self.num = user_value
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

    # Sets up the layout and board
    def setup(self):
        pygame.init()
        self._screen = pygame.display.set_mode((self._window_width, self._window_height))  # Set the window title
        pygame.display.set_caption("N QUEEN BY ADD")
        # Load the bug image
        self._lady_bug = pygame.image.load('queen.png')
        # self.num = int(self._input_field.get_value().title())
        self.draw_board()

    def make_sound(self):
        beep_sound = pygame.mixer.Sound("air_horn.mp3")  # wav may be recommended for better performance in pygame
        pygame.mixer.Sound.play(beep_sound)
        pygame.mixer.music.stop()

    def make_sound_2(self):
        beep_sound = pygame.mixer.Sound("chess_keep.mp3")  # wav may be recommended for better performance in pygame
        pygame.mixer.Sound.play(beep_sound)
        pygame.mixer.music.stop()

    def draw_board(self):
        """ Draw a chess board with queens, as determined by the the_board. """
        # self._input_field.enter()
        count = 0
        n = self.num
        self.the_board = [[0 for i in range(n)] for j in range(n)]
        pygame.init()
        colors = [(0, 0, 0), (255, 255, 255)]  # Set up colors [red, black]

        n = len(self.the_board)  # This is an NxN chess board.
        surface_sz = 600  # Proposed physical surface size.
        self.box_size = surface_sz / n
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
                break

            if self.place_queen():
                count += 1

            if count == n:
                ok = caution_message()
                ok.launch_game()
                break
        print("the board", self.the_board)

    def place_queen(self):

        clicked = pygame.mouse.get_pressed()

        if clicked[0] == 1:
            movement_of_mouse = pygame.mouse.get_pos()
            values = list(movement_of_mouse)
            x = values[0]
            x_values = int(int(x) / self.box_size)
            y = values[1]
            y_values = int(int(y) / self.box_size)
            # print(x_values, y_values)
            if self.isSafe(x_values, y_values):
                temp_x = x_values
                temp_y = y_values
                self.the_board[x_values][y_values] = '1'
                surface_sz = 600
                self.box_size = surface_sz / self.num
                sq_sz = surface_sz // self.num
                # To keep the queen in the center
                ball_offset = (sq_sz - self.ball.get_width()) // 2
                x_ball = (sq_sz * temp_x) + ball_offset
                y_ball = (sq_sz * temp_y) + ball_offset
                self.surf.blit(self.ball, (x_ball, y_ball))
                pygame.display.update()
                self.make_sound_2()
                return True
        return False

    def isSafe(self, r, c):
        mat = self.the_board
        # return false if two queens share the same column
        if mat[r][c] == '1':
            # self.make_sound()
            return False

        for i in range(len(mat)):
            if mat[i][c] == '1' and (i, c) != (r, c):
                # print("1")
                self.make_sound()
                return False

        # return false if two queens share the same `` diagonal
        (i, j) = (r, c)
        while i >= 0 and j >= 0:
            if mat[i][j] == '1' and (i, j) != (r, c):
                # print("2")
                self.make_sound()
                return False
            i = i - 1
            j = j - 1

        (i, j) = (r, c)
        while i < len(mat) and j >= 0:
            if mat[i][j] == '1' and (i, j) != (r, c):
                # print("2")
                self.make_sound()
                return False
            i = i + 1
            j = j - 1

        (i, j) = (r, c)
        while i < len(mat) and j < len(mat):
            if mat[i][j] == '1' and (i, j) != (r, c):
                # print("3")
                self.make_sound()
                return False
            i = i + 1
            j = j + 1

        # return false if two queens share the same `/` diagonal
        (i, j) = (r, c)
        while i >= 0 and j < len(mat):
            if mat[i][j] == '1' and (i, j) != (r, c):
                # print("4")
                self.make_sound()
                return False
            i = i - 1
            j = j + 1

        for m in range(len(mat)):
            if mat[r][m] == '1' and (r, m) != (r, c):
                # print("5")
                self.make_sound()
                return False

        return True


class caution_message:
    def __init__(self):
        self.e_counter = thorpy.make_text(text=self.get_trials_text(), font_color=(255, 255, 255))

        self.e_background = thorpy.Background(color=(0, 0, 0), elements=[self.e_counter])
        thorpy.store(self.e_background, gap=20)
        reaction_insert = thorpy.ConstantReaction(
            reacts_to=thorpy.constants.THORPY_EVENT,
            reac_func=self.reac_insert_func)
        self.e_background.add_reaction(reaction_insert)

    def get_trials_text(self):
        return "Congratulations you have won!!!!"

    def reac_insert_func(self):
        """ continue """

    def launch_game(self):
        menu = thorpy.Menu(self.e_background)
        menu.play()
