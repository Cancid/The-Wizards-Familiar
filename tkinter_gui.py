from tkinter import *
from tkinter import ttk
from input import process_input



def init_gui(engine):

    root = Tk()
    root.title("The Wizard's Familiar")

    TITLE = open('title.txt', 'r').read()

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E ,S))

    lb_title = ttk.Label(mainframe, text=TITLE, width=110, anchor=CENTER, border=5)
    lb_title.grid(row=1, column=1, pady=10)

    ent_player_act = Entry(mainframe, width=50)
    ent_player_act.grid(row=3, column=1, pady=10, ipady=10)


    scroll_bar = Scrollbar(mainframe, orient=VERTICAL, width=10)
    scroll_bar.grid( row=1, column=3)

    t_game = Text(mainframe, width=100, height=25, pady=10, padx=10, relief='solid', borderwidth=5)
    t_game.grid(row=2, column=1)

    t_game.configure(yscrollcommand=scroll_bar.set)
    scroll_bar.config(command=t_game.yview)

    def output():
        game_output = engine.player.game_text
        t_game.configure(state="normal")
        t_game.insert(END, game_output)
        t_game.see(END)
        t_game.configure(state="disabled")

    def player_action(event, engine):
        action = ent_player_act.get()
        ent_player_act.delete(0, END)
        engine.input_request(action)
        output()

    root.bind("<Return>", lambda event, arg=engine: player_action(event, arg))

    output()
    #root.bind("<Return>", player_action)
    print(root)
    return root