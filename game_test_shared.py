class Engine(object):

    player_inventory = []
    # Sets the room location init from class
    def __init__(self, room_location):
        self.room_location = room_location
        print("room_location set to:", self.room_location)

    def room_change(self):
        # passes the room_location to RoomGuide
        current_room = self.room_location.start_guide()
        print(">>> Current room:", current_room)
        finished = False
        # loops engine till game is over
        while finished != True:
            # enters the current_room
            play_room = current_room.enter(self.player_inventory)
            # if map returns no room tells player they can't go that way
            if play_room is None:
                print("You can't go that way.")
                #returns to beginning of while loop
                continue
            # sets the RoomGuide to room returned by the previos rooms enter()
            current_room = self.room_location.next_room(play_room)
            # loop repeats
            print("Current room after while:", current_room)


class Room(object):
    left = None
    right = None
    forward = None
    back = None
    interactables = None
    # inits the current room with mandatory and optional variables
    def __init__(self, name, description = 'No description'):
        self.name = name
        self.description = description

    #ensures the room name is returned as a string to engine
    def __str__(self):
            return self.name

    # "enters" the room
    def enter(self, player_inventory):
        print(f"This is the {self}. {self.description} What do you do?")
        choice = input('> ')
        # seperates user input at any space, returns list
        command = choice.split(' ')[0]
        # if no second in list, set object to None
        try:
            object = choice.split(' ')[1]
        # if an Index Error (aka no object returned) set object to none
        except IndexError:
            object = None

        # player actions
        if command in ('i', 'interact'):
            if object is None:
                print("With what?")
                object = input('WITH> ')
            new_item = self.interactables.get(object).interact(player_inventory)
            if new_item is not None:
                player_inventory.append(new_item)
                print('>>>INV:', player_inventory)
            return str(self)

        elif command == 'f':
            return self.forward

        elif command == 'l':
            return self.left

        elif command == 'r':
            return self.right

        elif command == 'b':
            return self.back

        else:
            return 'dead'

class Interactables(object):
    action_1 = None
    action_2 = None
    interaction = None
    descripion = None
    # init an interactable with optional actions
    def __init__(self, name):
        self.name = name

    # return name as string to caller
    def __str__(self):
        return self.name

    # allows player to choose what to do with object
    def interact(self, player_inventory):
        print(f"{self.description}")
        for a in self.interaction.values():
            if a.description is not None and a.active == True:
                print(a.description)
        choice = input('>OBJECT ')
        if choice == self.action_1:
            object = str(self.action_1)
            print('>>>>> object:', object)
        elif choice == self.action_2:
            object = str(self.action_2)
        else:
            return 'dead'
        new_item = self.interaction.get(object).use(player_inventory)
        return new_item



class Interaction(object):
    active = True
    item = False
    key = None
    unlock = None
    description = None

    def __init__(self, name, purpose):
        self.name = name
        self.purpose = purpose

    def use(self, player_inventory):
        if self.active == False:
            return
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


class Dead(object):

    def __str__(self):
        return 'dead'

    def enter(self):
        print("You died. Play again?")
        choice = input('> ')
        if choice == 'y':
            a_game.room_change()
        if choice == 'n':
            exit(1)
        else:
            print('Please select a valid response.')
            return 'dead'


class RoomGuide(object):

    foyer = Room('foyer', 'This is a fancy foyer. There is a fireplace and a piano.')
    hallway = Room('hallway')
    kitchen = Room('kitchen')
    master_bedroom = Room('Master Bedroom')

    fireplace = Interactables('fireplace')
    piano = Interactables('piano')

    play = Interaction('play', 'You play the piano.')
    music = Interaction('music sheets', 'They have a song on them.')
    music.item = True

    foyer.forward = 'hallway'
    foyer.interactables = {'fireplace': fireplace, 'piano': piano}
    hallway.back = 'foyer'
    hallway.left = 'kitchen'
    hallway.right = 'Master Bedroom'
    master_bedroom.left = 'hallway'
    kitchen.right = 'hallway'

    piano.description = '''A beautiful piano covered in dust sits on the
                            far right end of the foyer.'''.replace('  ', '')
    piano.action_1 = 'play'
    piano.action_2 = 'music'
    piano.interaction = {'play': play, 'music': music}

    play.key = 'music sheets'
    play.unlock = 'You play a beautiful song.'

    music.description = 'Sheets of music are still placed on it.'


    room_guide = {
        'foyer': foyer,
        'dead':Dead(),
        'hallway':hallway,
        'kitchen':kitchen,
        'Master Bedroom':master_bedroom,
        #'you win': YouWin()
    }


    def __init__(self, room):
        self.room = room

    def next_room(self, room_name):
        new_room = self.room_guide.get(room_name)
        return new_room

    def start_guide(self):
        return self.next_room(self.room)


a_map = RoomGuide('foyer')
a_game = Engine(a_map)
a_game.room_change()
