from tkinter import *
from tkinter import ttk
from input import process_input

def player_action(event, engine):
    action = ent_player_act.get()
    ent_player_act.delete(0, END)

game_script = ""
def output(text):
    game_script = 'This is the first line'
    game_script = '\n' + text
    game_output.set(game_output.get() + game_script)
    # NOTE: Could be slow with large amounts of text

def init_gui():

    root = Tk()
    root.title("The Wizard's Familiar")

    TITLE = open('title.txt', 'r').read()

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E ,S))

    lb_title = ttk.Label(mainframe, text=TITLE, width=110, anchor=CENTER, border=5)
    lb_title.grid(row=1, column=1, pady=10)

    ent_player_act = Entry(mainframe, width=50)
    ent_player_act.grid(row=3, column=1, pady=10, ipady=10)

    
        


    game_output = StringVar()
    lb_game = Label(mainframe, width=100, height=25, pady=10, padx=10, textvariable=game_output, justify=LEFT, anchor=NW, relief='solid', borderwidth=5)
    lb_game.grid(row=2, column=1)


    #text = 'this is a test'



    #root.bind("<Return>", player_action)
    print(root)
    return root