#! /usr/bin/env python3.9
from TextMysteryGame import RoomGuide, Player, Engine, Room
from tkinter_gui import init_gui


a_map = RoomGuide(Room.FOYER)
a_player = Player(a_map.next_room(a_map.room), ['license', 'letter'], [], [], False)
a_game = Engine(a_player)
a_game.play()


root = init_gui(a_game)
root.mainloop()
