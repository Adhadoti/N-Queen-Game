import thorpy
from oop_packet import*

class MyGame(object):

    def __init__(self):
        self.guess = None
        self.e_quit = thorpy.make_button("Quit",
                                         func=thorpy.functions.quit_menu_func)
        pointer=Chess_game()
        self.e_restart = thorpy.make_button("Restart", func=pointer.draw_board())

        self.e_counter = thorpy.make_text(text=self.get_trials_text(),
                                          font_color=(0,0,255))
        self.e_group_menu = thorpy.make_group([self.e_quit, self.e_restart])
        #the inserter element in which player can insert his guess
        self.e_insert = thorpy.Inserter(name="Enter N:")
        self.e_background = thorpy.Background( color=(255, 255, 255),
                                                    elements=[self.e_counter,self.e_insert,self.e_group_menu])
        thorpy.store(self.e_background, gap=20)
        #reaction called each time the player has inserted something
        reaction_insert = thorpy.ConstantReaction(
                            reacts_to=thorpy.constants.THORPY_EVENT,
                            reac_func=self.reac_insert_func,
                            event_args={"id":thorpy.constants.EVENT_INSERT,
                                        "el":self.e_insert})
        self.e_background.add_reaction(reaction_insert)

    def get_trials_text(self):
        return "You have " + "5" + " more chances."

    def reac_insert_func(self): #here is all the dynamics of the game
        value = self.e_insert.get_value()
        self.e_insert.set_value("")
        self.e_insert.unblit_and_reblit()
        try:
            self.guess = int(value)
            print(self.guess)
        except ValueError:
            return

    def launch_game(self):
        self.e_insert.enter() #giv the focus to inserter
        menu = thorpy.Menu(self.e_background) #create and launch the menu
        menu.play()