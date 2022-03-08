import thorpy, test2 #note that mygame.py must be in the same folder

application = thorpy.Application(size=(600, 400), caption="Guess the number")
mygame = test2.MyGame()
mygame.launch_game()
application.quit()