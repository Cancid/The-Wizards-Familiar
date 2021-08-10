#! /usr/bin/env python3.9
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import os



def init_gui(engine):

    root = Tk()
    screen_width=root.winfo_screenwidth() 
    screen_height=root.winfo_screenheight()
    root.title("The Wizard's Familiar")

    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    root.resizable(height=None, width=None)
    
    dir_path = os.path.dirname(os.path.realpath(__file__))

    TITLE = open(dir_path + '/data/title.txt', 'r').read()

    font = tkFont.Font(family='Yu Gothic', size=14)
    font_bold = tkFont.Font(family="Yu Gothic", size=11, weight="bold")

    mainframe = Frame(root, width=screen_width, height=screen_height)
    mainframe.grid(sticky='nsew')
    mainframe.config(background="mediumpurple3")
    mainframe.grid_columnconfigure(0,weight=1)
    mainframe.grid_rowconfigure(1,weight=1)


    lb_title = Label(mainframe, text=TITLE, border=5, background="mediumpurple3", height=7)
    lb_title.grid(row=0, column=0, pady=(10,0), sticky='sw')


    map_display = StringVar()
    lb_map = Label(mainframe, textvariable=map_display, font=font_bold, background="gray8", fg="ghostwhite", bd=4, relief=RIDGE)
    lb_map.grid(row=0, column=1, sticky='se', pady=(10), padx=(40,10))
    lb_map.config(height=7, width=14)
    

    ent_player_act = Entry(mainframe, width=50)
    ent_player_act.grid(row=2, columnspan=2, pady=10, ipady=10, sticky='n')
    ent_player_act.config(background="gray25", foreground="ghostwhite", relief='solid', borderwidth=3, font=font, justify=CENTER, width=25)


    scroll_bar = Scrollbar(mainframe, orient=VERTICAL, width=15)
    scroll_bar.grid(row=1, column=2, padx= (0, 20), sticky='nsew')
    scroll_bar.config(bg="gray25", activebackground="gray40")


    t_game = Text(mainframe, pady=10, padx=10, relief='solid', borderwidth=5)
    t_game.grid(row=1, columnspan=2, padx=(20,0), ipadx=10, sticky='nsew')
    t_game.config(bg="gray8", font=font, fg="ghostwhite", wrap=WORD)


    t_game.configure(yscrollcommand=scroll_bar.set)
    scroll_bar.config(command=t_game.yview)


    lexicon = ["*piano", "*fireplace", "*portrait", "*recipe", "*cabinet", "*pantry", "*icebox", "*wardrobe", "*Feyleaf",
                "*spellbook", "*mural", "*flour", "*oil", "*bake", "*faeleaf", "*sweetener", "*eggs", "*robes", "*license",
                "*gloves", "*circle", "*leaf", "*Sweetener", "*feyleaf", "*Sweetener", "*Oil", "*Flour", 
                "*orb", "*note", "*lock", "*letter", "*rest", "*read", "*sheets", "*ritual room", "*dust", "*Sheets",
                "*Dust", "*ritual", "*highlighted", "*play", "*stare", "*inventory", "*i", "*help", "*h", "*description",
                "*desc", "*right", "*left", "*forward", "*back", "*f", "*b", "*l", "*r", "*up", "*down", "*u", "*d",
                "*open", "*oven", "*Faedust", "*shelf", "*Callidopie"] #, "*sparkle"]
    

    def map_out():
       map = engine.map.display()
       map_display.set(map)


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
                    idx_delete = '%s+%dc' % (idx, 1)
                    t_game.delete(idx, idx_delete)
                    idx = lastidx
        engine.player.game_text = ''
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
        if engine.started == True:
            action_out(action)
        ent_player_act.delete(0, END)
        engine.process_input(action.lower())
        map_out()
        output()

    
    italics_font = tkFont.Font(t_game, t_game.cget("font"))
    italics_font.config(slant="italic", weight="bold")
    t_game.tag_configure("italic", font=italics_font, foreground='magenta3')

    bold_font= tkFont.Font(t_game, t_game.cget("font"))
    bold_font.config(weight="bold")
    t_game.tag_configure("bold", font=bold_font, foreground="magenta3")

    t_game.tag_configure("right", justify="right")
    t_game.tag_configure("center", justify="center")

    ent_player_act.focus_set()

    root.bind("<Return>", lambda event, arg=engine: player_action(event, arg))

    output()

    print(root)
    return root