class Engine(object):

    def __init__(self, room_location):
        self.room_location = room_location
        print("room_location set to:", self.room_location)

    def room_change(self):
        current_room = self.room_location.start_guide()
        # passes the room_location to RoomGuide
        print(">>> Current room:", current_room)
        last_room = self.room_location.next_room('you_win')
        #sets the last_roon = victory screen

        finished = False
        while finished != True:
            # enters the current_room
            play_room = current_room.enter()
            if play_room is None:
                print("You can't go that way.")
                continue
            # sets the RoomGuide to room returned by the previos rooms enter()
            current_room = self.room_location.next_room(play_room)
            # loop repeats
            print("Current room after while:", current_room)

class Room(object):

    def __init__(self, name, description = 'No description', forward = None, back = None,
                left = None, right = None, interactables = None
                ):
        self.name = name
        self.forward = forward
        self.back = back
        self.left = left
        self.right = right
        self.interactables = interactables
        self.description = description

    def __str__(self):
            return self.name

    def enter(self):
        print(f"This is the {self}. {self.description} What do you do?")
        # if statement for text? variable for text?
        choice = input('> ')
        command = choice.split(' ')[0]
        try:
            object = choice.split(' ')[1]
        except IndexError:
            object = None

        if command in ('i', 'interact'):
            if object is None:
                print("With what?")
            else:
                self.interactables.get(object).interact()
            # self.interactables[1].interact()
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

    def __init__(self, name, action_1 = None, action_2 = None, #**kwargs):
        self.name = name
        self.action_1 = action_1
        self.action_2 = action_2

    def __str__(self):
        return self.name

    def interact(self):
        print(f"This is a {self}. ")
        choice = input('>OBJECT ')
        if choice == self.action_1:
            print("Something happens")
        elif choice == self.action_2:
            print("Something else happens")
        else:
            return 'dead'


class Interaction(object):

    trigger_word = None
    effect = None



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

    foyer.forward = 'hallway'
    foyer.interactables = {'fireplace': fireplace, 'piano': piano}
    hallway.back = 'foyer'
    hallway.left = 'kitchen'
    hallway.right = 'Master Bedroom'
    master_bedroom.left = 'hallway'
    kitchen.right = 'hallway'

    piano.action_1 = 'play'


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
