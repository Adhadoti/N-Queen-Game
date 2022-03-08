from test2 import *
import thorpy
def main():
    application = thorpy.Application(size=(600, 400), caption="Guess the number")
    ok=MyGame()
    mygame = ok.MyGame(player_name="Jack", min_val=0, max_val=100, trials=5)
    mygame.launch_game()
    application.quit()

main()