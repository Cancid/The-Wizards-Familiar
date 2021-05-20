from tkinter import *
from tkinter import ttk


root = Tk()
root.title("The Wizard's Familiar")

TITLE = open('title.txt', 'r').read()
 
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E ,S))

lb_title = ttk.Label(mainframe, text=TITLE, width=110, anchor=CENTER, border=5)
lb_title.grid(row=1, column=1, pady=10)


game_output = StringVar()
def output(text):
    game_script = 'This is the first line'
    game_script = game_script + '\n' + text
    game_output.set(game_script)

output('This is a test')

ent_player_act = Entry(mainframe, width=50)
ent_player_act.grid(row=3, column=1, pady=10, ipady=10)


lb_game = Label(mainframe, width=100, height=25, pady=10, padx=10, textvariable=game_output, justify=LEFT, anchor=NW, relief='solid', borderwidth=5)
lb_game.grid(row=2, column=1)


#text_box = Text(mainframe, width=200)
#text_box.grid(row=1, column=0)
#text_box.configure(state="normal")

def player_action(player_act):
    action = ent_player_act.get()
    ent_player_act.delete(0, END)
    print(action)

root.bind("<Return>", player_action)


root.mainloop()