#! /usr/bin/env python3.9
from wizards_familiar import Engine
from tkinter_gui import init_gui



def play():
    a_game = Engine()
    a_game.play()
    root = init_gui(a_game)
    root.mainloop()

play()


        