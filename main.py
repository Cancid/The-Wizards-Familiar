from TextMysteryGame import RoomGuide, Player, Engine, Room
from tkinter_gui import init_gui

def wait_for_input():
    pass


a_map = RoomGuide(Room.FOYER)
a_player = Player(a_map.next_room(a_map.room), ['letter'], [], [], False)
a_game = Engine(a_player)
a_game.play()


root = init_gui(a_game)
#root.bind("<Return>", func)
#root.bind("<Return>", lambda event, arg=a_game: player_action(event, arg))
root.mainloop()
git 
