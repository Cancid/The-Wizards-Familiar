import mapper
from enum import Enum
from typing import List, Set, Dict, Tuple, Optional, Callable, Iterator, Union, Literal

class Engine(object):
     #what would this be?


    # Sets the room location init from class
    def __init__(self, room_location: object, player):
        self.player = player
        map = mapper.Map()
        print(map)
        self.room_location = room_location
        map.generate_map_from_room_guide(room_location)
        self.map = map
        print("room_location set to:", self.room_location)

    def room_change(self) -> None:
        # passes the room_location to RoomGuide
        current_room = self.room_location.start_guide()
        #print(">>> Current room:", current_room)
        finished = False
        # loops engine till game is over
        while finished != True:
            # enters the current_room
            self.map.display()
            #print('>>>>>>', current_room)
            current_room.describe(self.player)
            self.player.visited.append(self.player.location.room)
            # if map returns no room tells player they can't go that way
            moved = input_request(self.player, self.map)
            if not moved:
                print("You can't go that way.")
                #returns to beginning of while loop
                continue
            # sets the RoomGuide to room returned by the previos rooms enter()
            print(self.player.location.room)
            current_room = self.player.location#.next_room(self.player.location.room)
            print(str(current_room))
            # loop repeats
            #print("Current room after while:", current_room)

class Room(Enum):
    FOYER = 1
    HALLWAY = 2
    KITCHEN = 3
    MASTER_BEDROOM = 4
    FAILURE = 5

class PlayerLocation(object):
    left = None
    right = None
    forward = None
    back = None
    interactables: Optional[dict] = None

    # inits the current room with mandatory and optional variables
    def __init__(self, room: Room, name: str, description: str = 'No description', no_desc: bool = False):
        self.room = room
        self.name = name
        self.description = description
        self.no_desc = no_desc

    # "enters" the room
    def describe(self, player) -> Room:
        if player.no_desc == True:
            pass
        elif self.room in player.visited:
            print(f'You are in the {self.name}. This room was visited. What do you do?')
        else:
            print(f"This is the {self.name}. {self.description} What do you do?")


class Player(object):

    def __init__(self, location, inventory, visited, no_desc):
        self.location = location
        self.inventory = inventory
        self.visited = visited
        self.no_desc = no_desc

    def move(self, command, map):

    #if command in ('f', 'forward', 'l', 'left', 'r', 'right', 'b', 'back'):
        self.no_desc = False
        print(self.location.no_desc)
        if command in ('f', 'forward'):
            if self.location.forward:
                map.update_player("forward")
            new_location = self.location.forward
        elif command in ('l', 'left'):
            if self.location.left:
                map.update_player("left")
            new_location = self.location.left
        elif command in ('r', 'right'):
            if self.location.right:
                map.update_player("right")
            new_location = self.location.right
        elif command in ('b', 'back'):
            if self.location.back:
                map.update_player("back")
            new_location = self.location.back

        if not new_location:
            return False
        else:
            self.location = new_location
            return True

    def interact(self, command, object):
        if object is None:
            print("With what?")
            object = input('WITH> ')
        new_item: Optional[str] = player.location.interactables.get(object).interact(player.inventory) #TODO: typo error
        if new_item is not None:
            player.add_item(new_item)
            print('>>>INV:', player.inventory)
        player.no_desc = True
        return True

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
    if command in ('i', 'interact'):
        return player.interact(command, object)

    elif command in ('f', 'forward', 'l', 'left', 'r', 'right', 'b', 'back'):
        return player.move(command, map)

    else:
        print("Please enter a valid resposne.")
        return True



    #elif command in ('d', 'desc', 'description'):
    #    print(self.description)
    #    return PlayerLocation.room
    #elif command in ('h', 'help'):
    #    print('This is the list of commands.')
    #    return PlayerLocation.room
#
    #elif len(choice.split(' ')) == 2:
    #    command = choice.split(' ')[0]
    #    object = choice.split(' ')[1]
    #    print(object)
    #    try:
    #        new_item = self.interactables.get(object).interact(player_inventory, command)
    #        if new_item is not None:
    #            player_inventory.append(new_item)
    #            print('>>>INV:', player_inventory)
    #            return PlayerLocation.room
    #        else:
    #            return PlayerLocation.room
    #    except AttributeError:
    #        print('Please enter a valid response.')
    #        return PlayerLocation.room
#
    #else:
    #    print('Please enter a valid response.')
    #    return PlayerLocation.room
#
    #return PlayerLocation.room        #    print(self.visited_description)

class Interactables(object):
    action_1: Optional[str] = None
    action_2: Optional[str]= None
    interaction: Optional[dict] = None
    description: Optional[str] = None
    # init an interactable with optional actions
    def __init__(self, name: str):
        self.name = name

    #return name as string to caller
    def __str__(self):
        return self.name

    # allows player to choose what to do with object
    def interact(self, player_inventory: list[str], choice: Optional[str] = None) -> None:
        print(self.description)
        if self.interaction is not None:
            # print(self.interaction)
            for act in self.interaction.values():
                if act.description is not None and act.active == True:
                    print(act.description)
        if choice is None:
            choice = input('>OBJECT ')
        if choice == self.action_1:
            object = str(self.action_1)
        elif choice == self.action_2:
            object = str(self.action_2)
        else:
            print('Please enter a valid response.')
            self.no_desc = True
            self.interact(player_inventory)
        try:
            new_item = self.interaction.get(object).use(player_inventory)
            print('NEW_ITEM AFTER INT:', new_item)
            self.no_desc = False
            return new_item
        except:
            pass


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

    def use(self, player_inventory: list[str]) -> Optional[str]:
        if self.active == False:
            return None
        print("INV:", player_inventory)
        print("KEY:", self.key)
        if self.key is not None and len(player_inventory) > 0:
            for i in player_inventory:
                if i == self.key:
                    print(self.unlock)
                else:
                    print(self.purpose)

        else:
            print(self.purpose)
            if self.item == True:
                print(f'You take the {self.name}.')
                self.active = False
                return self.name





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
    #bust = Interactables('bust')
    #landscape_painting = Interactables('landscape_painting')
    #cabinet = Interactables('cabinet')
    #bed = Interactables('bed')

    play = Interaction('play', 'You play the piano.')
    music = Interaction('music sheets', 'They have a song on them.')
    music.item = True

    foyer.forward = hallway
    foyer.interactables = {'fireplace': fireplace, 'piano': piano}
    hallway.back = foyer
    hallway.left = kitchen
    hallway.right = master_bedroom
    hallway.interactables = {'portrait': portrait} #'bust': bust,
                            #'landscape painting': landscape_painting
    master_bedroom.left = hallway
    kitchen.right = hallway

    piano.description = '''A beautiful piano covered in dust sits on the
                            far right end of the foyer.'''.replace('    ', '')

    fireplace.description = 'You feel warm.'
    piano.action_1 = 'play'
    piano.action_2 = 'music'
    piano.interaction = {'play': play, 'music': music}
    portrait.description = '''An old women with black hair in a fine purple gown
                                stares back at you. You swear a sinsiter smile slowly curls
                                across her face the longer you look at it.'''.replace('   ', '')

    play.key = 'music sheets'
    play.unlock = 'You play a beautiful song.'

    music.description = 'Sheets of music are still placed on it.'


    room_guide = {
        Room.FOYER: foyer,
        Room.FAILURE: failure,
        Room.HALLWAY: hallway,
        Room.KITCHEN: kitchen,
        Room.MASTER_BEDROOM: master_bedroom,
        #'you win': YouWin()
    }

    def __init__(self, room: Room):
        self.room = room

    def next_room(self, room_name: Room) -> PlayerLocation:
        new_room = self.room_guide.get(room_name)
        return new_room

    def start_guide(self) -> PlayerLocation:
        return self.next_room(self.room)


a_map = RoomGuide(Room.FOYER)
a_player = Player(a_map.start_guide(), [], [], False)
a_game = Engine(a_map, a_player)
a_game.room_change()
