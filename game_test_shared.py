import mapper

class Engine(object):
    player_inventory = []
    visited = []
    no_desc = []

    # Sets the room location init from class
    def __init__(self, room_location):
        map = mapper.Map()
        self.room_location = room_location
        map.generate_map_from_room_guide(room_location)
        self.map = map
        print("room_location set to:", self.room_location)

    def room_change(self):
        # passes the room_location to RoomGuide
        current_room = self.room_location.start_guide()
        print(">>> Current room:", current_room)
        finished = False
        # loops engine till game is over
        while finished != True:
            # enters the current_room
            self.map.display()
            play_room = current_room.enter(self.player_inventory, self.visited, self.no_desc, self.map)
            # if map returns no room tells player they can't go that way
            if play_room is None:
                print("You can't go that way.")
                #returns to beginning of while loop
                continue
            # sets the RoomGuide to room returned by the previos rooms enter()
            current_room = self.room_location.next_room(play_room)
            # loop repeats
            print("Current room after while:", current_room)


class Room(object):#Enum):
    #foyer = 1
    #hallway = 2
    #master_bedroom = 3
    #kitchen = 4

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
    def enter(self, player_inventory, visited, no_desc, map):
        if self.name in visited and self.name in no_desc:
            pass
        elif self.name in visited:
            print(f'You are in the {self}. This room was visited. What do you do?')
            no_desc.append(self.name)
        else:
            print(f"This is the {self}. {self.description} What do you do?")
            visited.append(self.name)
            no_desc.append(self.name)
        #else:
        #    print(self.visited_description)
        choice = input('> ')
        # seperates user input at any space, returns list
        command = choice.split(' ')[0]
        try:
            object = choice.split(' ')[1]
        # if an Index Error (aka no object returned) set object to none
        except IndexError:
            # if no second in list, set object to None
            object = None
        if command in ('i', 'interact'):
            if object is None:
                print("With what?")
                object = input('WITH> ')
            new_item = self.interactables.get(object).interact(player_inventory)
            if new_item is not None:
                player_inventory.append(new_item)
                print('>>>INV:', player_inventory)
                return str(self)
            else:
                return str(self)

        elif command in ('f', 'forward', 'l', 'left', 'r', 'right', 'b', 'back'):
            no_desc.pop()
            if command in ('f', 'forward'):
                if self.forward:
                    map.update_player("forward")
                return self.forward
            elif command in ('l', 'left'):
                if self.left:
                    map.update_player("left")
                return self.left
            elif command in ('r', 'right'):
                if self.right:
                    map.update_player("right")
                return self.right
            elif command in ('b', 'back'):
                if self.back:
                    map.update_player("back")
                return self.back

        elif command in ('d', 'desc', 'description'):
            print(self.description)
            return str(self)
        elif command in ('h', 'help'):
            print('This is the list of commands.')
            return str(self)

        elif len(choice.split(' ')) == 2:
            command = choice.split(' ')[0]
            object = choice.split(' ')[1]
            print(object)
            try:
                new_item = self.interactables.get(object).interact(player_inventory, command)
                if new_item is not None:
                    player_inventory.append(new_item)
                    print('>>>INV:', player_inventory)
                    return str(self)
                else:
                    return str(self)
            except AttributeError:
                print('Please enter a valid response.')
                return str(self)

        else:
            print('Please enter a valid response.')
            return str(self)

class Interactables(object):
    action_1 = None
    action_2 = None
    interaction = None
    description = None
    no_desc = False
    # init an interactable with optional actions
    def __init__(self, name):
        self.name = name

    # return name as string to caller
    def __str__(self):
        return self.name

    # allows player to choose what to do with object
    def interact(self, player_inventory, choice = None):
        if self.no_desc == False:
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
    active = True
    item = False
    key = None
    unlock = None
    # description = None

    def __init__(self, name, purpose, description = None):
        self.name = name
        self.purpose = purpose
        self.description = description

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


class Failure(object):

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return 'failure'

    def enter(self, player_inventory):
        print(self.description)
        choice = input('> ')
        if choice == 'y':
            a_game.room_change()
        if choice == 'n':
            exit(1)
        else:
            print('Please select a valid response.')
            return 'failure'


class RoomGuide(object):

    foyer = Room('foyer', 'This is a fancy foyer. There is a fireplace and a piano.')
    hallway = Room('hallway')
    kitchen = Room('kitchen')
    master_bedroom = Room('Master Bedroom')
    failure = Failure('failure', 'You failed! Play again?')

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

    foyer.forward = 'hallway'
    foyer.interactables = {'fireplace': fireplace, 'piano': piano}
    hallway.back = 'foyer'
    hallway.left = 'kitchen'
    hallway.right = 'Master Bedroom'
    hallway.interactables = {'portrait': portrait} #'bust': bust,
                            #'landscape painting': landscape_painting
    master_bedroom.left = 'hallway'
    kitchen.right = 'hallway'

    piano.description = '''A beautiful piano covered in dust sits on the
                            far right end of the foyer.'''.replace('    ', '')

    fireplace.description = 'You feel warm.'
    piano.action_1 = 'play'
    piano.action_2 = 'music'
    piano.interaction = {'play': play, 'music': music}
    portrait.description = '''An old women with black hair in a fine purple gown
                                stares back at you. You swear a sinsiter smile slowly curls
                                across it the longer you look at it.'''.replace('   ', '')

    play.key = 'music sheets'
    play.unlock = 'You play a beautiful song.'

    music.description = 'Sheets of music are still placed on it.'


    room_guide = {
        'foyer': foyer,
        'failure': failure,
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
