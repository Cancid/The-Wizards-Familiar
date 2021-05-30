from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont



def init_gui(engine):

    root = Tk()
    screen_width=root.winfo_screenwidth() 
    screen_height=root.winfo_screenheight()
    root.title("The Wizard's Familiar")

    
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    
    
    TITLE = open('title.txt', 'r').read()

    mainframe = Frame(root, width=screen_width, height=screen_height)
    mainframe.grid(sticky='nsew')
    mainframe.config(background="mediumpurple3")
    mainframe.grid_columnconfigure(1,weight=1)
    mainframe.grid_rowconfigure(1,weight=1)


    lb_title = ttk.Label(mainframe, text=TITLE, anchor=CENTER, border=5, background="mediumpurple3")
    lb_title.grid(row=0, column=1, pady=10, sticky='nsew')

    ent_player_act = Entry(mainframe, width=50)
    ent_player_act.grid(row=2, column=1, pady=10, ipady=10, padx=20, sticky='ns')

    scroll_bar = Scrollbar(mainframe, orient=VERTICAL, width=15)
    scroll_bar.grid(row=1, column=2, padx= (0, 20), sticky='nsew')
    scroll_bar.config(bg="gray25")

    font = tkFont.Font(family='Yu Gothic', size=14)

    t_game = Text(mainframe, pady=10, padx=10, relief='solid', borderwidth=5)
    t_game.grid(row=1, column=1, padx=(20,0), ipadx=10, sticky='nsew')
    t_game.config(bg="gray8", font=font, fg="ghostwhite", wrap=WORD)

    t_game.configure(yscrollcommand=scroll_bar.set)
    scroll_bar.config(command=t_game.yview)

    lexicon = ["piano", "fireplace", "portrait", "cabinet", "pantry", "icebox", "wardrobe", "'feyleaf'", "box", "spellbook", "circle", "mural", "flour", "oil", "bake", "sweetener", "eggs", "robes", "gloves", "circle", "leaf", "Sweetener", "feyleaf"]

    def output():
        game_output = engine.player.game_text
        t_game.configure(state="normal")
        t_game.insert(END,"  " + game_output)
        for w in lexicon:
            idx = "1.0"
            while idx:
                idx = t_game.search(w, idx, stopindex=END)
                if idx:
                    lastidx = '%s+%dc' % (idx, len(w))
                    t_game.tag_add("italic", idx, lastidx)
                    idx = lastidx
        t_game.see(END)
        t_game.configure(state="disabled")
    
    def action_out(action):
        t_game.configure(state="normal")
        t_game.insert(END, "  \n\nYou: " + action)
        idx = "1.0"
        while idx:
            idx = t_game.search('You:', idx, stopindex=END)
            if idx:
                lastidx = '%s+%dc' % (idx, 3.0)
                t_game.tag_add("bold", idx, lastidx)
                idx = lastidx
        t_game.see(END)
        t_game.configure(state="disabled")
        


    def player_action(event, engine):
        action = ent_player_act.get()
        if engine.started ==True:
            action_out(action)
        ent_player_act.delete(0, END)
        engine.input_request(action)
        output()

    
    italics_font = tkFont.Font(t_game, t_game.cget("font"))
    italics_font.config(slant="italic", weight="bold")
    t_game.tag_configure("italic", font=italics_font, foreground='magenta3')

    bold_font= tkFont.Font(t_game, t_game.cget("font"))
    bold_font.config(weight="bold")
    t_game.tag_configure("bold", font=bold_font, foreground="magenta3")


    root.bind("<Return>", lambda event, arg=engine: player_action(event, arg))

    output()
    #root.bind("<Return>", player_action)
    print(root)
    return root