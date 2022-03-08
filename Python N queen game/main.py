import oop_packet
from oop_packet import *
import thorpy
def main():
    thorpy.Application(size=(600, 400))
    mygame = oop_packet.MyGame()
    mygame.launch_game()
    store=mygame.send_main()
    app2=Chess_game(store)
    app2.setup()

main()