import mapper
import inspect
from random import randint
from threading import Timer
from enum import Enum
from typing import List, Set, Dict, Tuple, Optional, Callable, Iterator, Union, Literal

class Engine(object):
     #what would this be?


    # Sets the room location init from class
    def __init__(self, player):
        self.player = player
        map = mapper.Map()
        print(map)
        map.generate_map_from_room_guide(player.location)
        self.map = map

    def start(self) -> None:
        # passes the room_location to RoomGuide
        current_room = self.player.location
        #print(">>> Current room:", current_room)
        finished = False
        # loops engine till game is over
        while finished != True:
            # enters the current_room
            self.map.display()
            #print('>>>>>>', current_room)
            current_room.describe(self.player)
            self.player.visited.append(self.player.location.name)
            # if map returns no room tells player they can't go that way
            moved = input_request(self.player, self.map)
            if not moved:
                print("You can't go that way.")
                #returns to beginning of while loop
                continue
            # sets the RoomGuide to room returned by the previos rooms enter()
            print(self.player.location.name)
            current_room = self.player.location#.next_room(self.player.location.room)
            print(str(current_room))
            # loop repeats
            #print("Current room after while:", current_room)

class Room(Enum):
    FOYER = 0
    HALLWAY = 1
    KITCHEN = 2
    MASTER_BEDROOM = 3
    FAILURE = 4

class PlayerLocation(object):
    left = None
    right = None
    forward = None
    back = None
    teleport = None
    interactables: Optional[dict] = None

    # inits the current room with mandatory and optional variables
    def __init__(self, room, name: str, description: str = 'No description', no_desc: bool = False):
        self.room = room
        self.name = name
        self.description = description
        self.no_desc = no_desc

    # "enters" the room
    def describe(self, player) -> Room:
        if player.no_desc == True:
            pass
        elif self.name in player.visited:
            print(f'You are in the {self.name}. This room was visited. What do you do?')
        else:
            print(f"This is the {self.name}. {self.description} What do you do?")


class Player(object):

    last_moved = [None, None, None, None]

    def __init__(self, location, inventory, puzzles, visited, no_desc):
        self.location = location
        self.inventory = inventory
        self.puzzles = puzzles
        self.visited = visited
        self.no_desc = no_desc


    def move(self, command, map):

        self.no_desc = False
        print(self.location.no_desc)
        if command in ('f', 'forward'):
            if self.location.forward:
                self.last_moved.pop(0)
                self.last_moved.append('f')
                map.update_player("forward")
            new_location = self.location.forward
        elif command in ('l', 'left'):
            if self.location.left:
                self.last_moved.pop(0)
                self.last_moved.append('l')
                map.update_player("left")
            new_location = self.location.left
        elif command in ('r', 'right'):
            if self.location.right:
                self.last_moved.pop(0)
                self.last_moved.append('r')
                map.update_player("right")
            new_location = self.location.right
        elif command in ('b', 'back'):
            if self.location.back:
                self.last_moved.pop(0)
                self.last_moved.append('b')
                map.update_player("back")
            new_location = self.location.back

        if not new_location:
            return False
        else:
            self.location = new_location
            if self.last_moved == PUZZLE_SOLUTION:
                self.puzzles.append('puzzle_solve')
            return True

    def interact(self, command, object): # TODO: if room has no interactables ERROR
        while object is None:
            print("With what?")
            object = input('WITH> ')
            if object in ('e', 'exit'):
                return
            elif object not in self.location.interactables:
                print('Please enter a valid respone.')
                object = None
        interactable = self.location.interactables.get(object)
        if interactable is None:
            print('No object with that name in this room.')
            return 
        if command not in interactable.interaction:
            command = None
        new_item = interactable.interact(self, command)
        if new_item is not None:
            self.add_item(new_item)
            print('>>>INV:', self.inventory)
        self.no_desc = True

    def change_room(self, room):
        player.location = player.location[room]

    def add_item(self, new_item):
        self.inventory.append(new_item)


def input_request(player, map):
    choice = input('> ')
    # seperates user input at any space, returns list
    command = choice.split(' ')[0]
    try:
        object: Optional[str] = choice.split(' ')[1]
    # if an Index Error (aka no object returned) set object to none
    except IndexError:
        # if no second in list, set object to None
        object = None
    print(object)
    print(player.location.interactables)

    if command in ('f', 'forward', 'l', 'left', 'r', 'right', 'b', 'back'):
        return player.move(command, map)

    elif command in ('i', 'interact') or object in player.location.interactables.keys():
        # TODO: typing command and object outputs nothing, make inputs like 'piano' work
        player.interact(command, object)
        return True


    elif command in ('d', 'desc', 'description'):
        print(player.location.description)
        player.no_desc = True
        return True
    elif command in ('h', 'help'):
        print('This is a list of commands.')
        return True

    else:
        print("Please enter a valid resposne.")
        return True


class Interactables(object):
    action_1: Optional[str] = None
    action_2: Optional[str] = None
    item_1: Optional[str] = None
    interaction: Optional[dict] = None
    description: Optional[str] = None
    timer = False
    # init an interactable with optional actions
    def __init__(self, name: str):
        self.name = name

    #return name as string to caller
    def __str__(self):
        return self.name

    # allows player to choose what to do with object
    def interact(self, player, choice: Optional[str] = None) -> None:
        print(self.description)
        if self.interaction is not None:
            # print(self.interaction)
            for act in self.interaction.values():
                if act.description is not None and act.active == True:
                    print(act.description)
        object = choice
        while choice is None:
            choice = input('>OBJECT ')
            if choice == self.action_1:
                object = str(self.action_1)
            elif choice == self.action_2:
                object = str(self.action_2)
            elif choice.split(' ')[0] in ('g', 'get', 't', 'take'):
                try:
                    object = str(choice.split(' ')[1])
                except IndexError:
                    object = None
                while object not in (self.interaction, 'e', 'exit'):
                    print("With what?")
                    object = input('WITH> ')
                if object in ('e', 'exit'):
                    return None
            elif choice in ('e', 'exit'):
                return None
            else:
                print('Please enter a valid response.')
                choice = None
        #if self.timer is True:
        #    timeout = 10
        #    t = Timer(timeout, print, ['Sorry, times up'])
        #    t.start()
        #    prompt = "You have %d seconds to choose the correct answer...\n" % timeout
        #    if choice is self.action_1 or self.action_2:
        #        print('TIMER CANCELED')
        #        t.cancel()
        new_item = self.interaction.get(object).use(player)
        print('NEW_ITEM AFTER INT:', new_item)
        self.no_desc = False


        return new_item

    #def timer():
    #    timeout = 10
    #    t = Timer(timeout, print, ['Sorry, times up'])
    #    t.start()
    #    prompt = "You have %d seconds to choose the correct answer...\n" % timeout
    #    if interact():
    #        t.cancel()



class Interaction(object):
    active: bool = True
    item: bool = False
    key: Optional[str] = None
    unlock: Optional[str] = None
    # description = None

    def __init__(self, name: str, purpose: str, description: Optional[str] = None) -> None:
        self.name = name
        self.purpose = purpose
        self.description = description

    def use(self, player):
        if self.active == False:
            return None
        print("INV:", player.inventory)
        print('PUZZLES', player.puzzles)
        print("KEY:", self.key)
        was_unlocked = False
        if self.key is not None:
            for i in player.inventory:
                if i == self.key:
                    was_unlocked = True
            for i in player.puzzles:
                if i == self.key:
                    was_unlocked = True
            if was_unlocked == True:
                print(self.unlock)
            else:
                print(self.purpose)

        else:
            print(self.purpose)
            if self.item == True:
                print(f'You take the {self.name}.')
                self.active = False
                return self.name


class Landscape(object):
    action_1: Optional[str] = None
    action_2: Optional[str] = None
    landscape: Optional[list] = None
    interaction = None
    description: Optional[str] = None
    # init an interactable with optional actions
    def __init__(self, name: str):
        self.name = name


    def interact(self, player, choice: Optional[str] = None) -> None:
        print(self.description)
        spin = randint(0, 2)
        land = self.landscape[spin]
        print(land)
        object = choice
        new_item = None
        while choice is None:
            choice = input('>OBJECT ')
            if choice == self.action_1:
                player.location = player.location.teleport[spin]
                return new_item
            elif choice == self.action_2:
                object = str(self.action_2)
                new_item = self.interaction.get(object).use(player_inventory)
                return new_item
            elif choice in ('e', 'exit'):
                return None
            else:
                print('Please enter a valid response.')
                choice = None
        self.no_desc = False


class Failure(object):

    def __init__(self, room: Room, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return 'failure'

    def enter(self, player_inventory: list[str]) -> str:
        print(self.description)
        choice = input('> ')
        if choice == 'y':
            a_game.room_change()
        if choice == 'n':
            exit(1)
        else:
            print('Please select a valid response.')
            return 'failure'
        return 'failure'



class RoomGuide(object):

    foyer = PlayerLocation(Room.FOYER, 'foyer', 'This is a fancy foyer. There is a fireplace and a piano.')
    hallway = PlayerLocation(Room.HALLWAY, 'hallway')
    kitchen = PlayerLocation(Room.KITCHEN, 'kitchen')
    master_bedroom = PlayerLocation(Room.MASTER_BEDROOM, 'Master Bedroom')
    failure = Failure(Room.FAILURE, 'failure', 'You failed! Play again?')

    fireplace = Interactables('fireplace')
    piano = Interactables('piano')
    portrait = Interactables('portrait')
    landscape = Landscape('landscape painting')
    box = Interactables('box')
    #bust = Interactables('bust')
    #landscape_painting = Interactables('landscape_painting')
    #cabinet = Interactables('cabinet')
    #bed = Interactables('bed')
    open = Interaction('open', 'It is locked.')
    play = Interaction('play', 'You play the piano.')
    music = Interaction('music sheets', 'They have a song on them.')
    music.item = True

    run = Interaction('run', 'You run away.')

    foyer.forward = hallway
    foyer.interactables = {'fireplace': fireplace, 'piano': piano}
    hallway.back = foyer
    hallway.left = kitchen
    hallway.right = master_bedroom
    hallway.teleport = [foyer, kitchen, master_bedroom]
    hallway.interactables = {'portrait': portrait, 'landscape': landscape} #'bust': bust,
                            #'landscape painting': landscape_painting
    master_bedroom.left = hallway
    master_bedroom.interactables = {'box': box}
    kitchen.right = hallway

    piano.description = '''A beautiful piano covered in dust sits on the
                            far right end of the foyer.'''.replace('    ', '')

    fireplace.description = 'You feel warm.'

    piano.action_1 = 'play'
    piano.action_2 = 'music'
    piano.interaction = {'play': play, 'music': music}

    portrait.description = '''An old woman with black hair in a fine purple gown
                                stares back at you. You swear a sinsiter smile slowly curls
                                across her face the longer you look at it.'''.replace('   ', '')
    portrait.interaction = {'run': run}
    portrait.action_1 = 'run'
    portrait.timer = True

    landscape.landscape = ['foyer', 'kitchen', 'master_bedroom']
    landscape.interaction = {'run': run}
    landscape.action_1 = 'stare'
    landscape.action_2 = 'run'

    box.description = 'A locked box.'
    box.interaction = {'open': open}
    box.action_1 = 'open'
    open.key = 'puzzle_solve'
    open.unlock = 'The box opens.'



    play.key = 'music sheets'
    play.unlock = 'You play a beautiful song.'

    music.description = 'Sheets of music are still placed on it.'


    room_guide = {
        Room.FOYER: foyer,
        Room.HALLWAY: hallway,
        Room.KITCHEN: kitchen,
        Room.MASTER_BEDROOM: master_bedroom,
        Room.FAILURE: failure
    }

    def __init__(self, room: Room):
        self.room = room

    def next_room(self, room_name):
        new_room = self.room_guide.get(room_name)
        return new_room

PUZZLE_SOLUTION = ['l', 'l', 'r', 'r']

a_map = RoomGuide(Room.FOYER)
a_player = Player(a_map.next_room(a_map.room), [], [], [], False)
a_game = Engine(a_player)
a_game.start()
