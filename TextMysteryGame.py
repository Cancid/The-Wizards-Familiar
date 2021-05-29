from input import input_request
import mapper
from random import randint
from threading import Timer
from enum import Enum
from typing import List, Set, Dict, Tuple, Optional, Callable, Iterator, Union, Literal

class Engine(object):
    def __init__(self, player):
        self.player = player
        map = mapper.Map()
        print(map)
        map.generate_map_from_room_guide(player.location)
        self.map = map

    started = False
    def play(self):
        self.player.output('Press ENTER to Play')


    def input_request(self, command):
        try:
            object: Optional[str] = command.split(' ')[1]
            command = command.split(' ')[0]
            # if an Index Error (aka no object returned) set object to none
        except IndexError:
            # if no second in list, set object to None
            object = None
        print(self.player.interaction_state)
        if self.player.interaction_state == None:
            moved = self.process_input(command, object)
            current_room = self.player.location
            self.map.display()
            if moved is False:
               self.player.output("You can't go that way.")
            elif self.player.no_desc == False and self.player.interaction_state == None:
                current_room.describe(self.player)
                self.player.visited.append(self.player.location.name)
        elif self.player.interaction_state == 'room':
            self.player.interact(None, command)
        elif self.player.interaction_state != None:
            self.player.interact(command, self.player.interaction_state)



    def process_input(self, command, object):
        if self.started == False:
            self.started = True
            return

        if command in ('f', 'forward', 'l', 'left', 'r', 'right', 'b', 'back',
                        'u', 'up', 'd', 'down'):
            return self.player.move(command, self.map)

        elif command in ('i', 'interact'):
            print('OBJECT>>>>>', object) 
            if object in self.player.location.interactables.keys() or object in self.player.inventory:
                print("I did this.")
                # TODO: make inputs like 'piano' work
                self.player.interaction_state = 'room'
                self.player.interact(command, object)
                return True
            else:
                print("Proccess Input - Interact - No Object")
                self.player.output('With what?')
                self.player.interaction_state = 'room'
                print(self.player.interaction_state)
                return True
            
        elif command in ('desc', 'description'):
            self.player.output(self.player.location.description)
            self.player.no_desc = True
            return True
        elif command in ('h', 'help'):
            self.player.output('This is a list of commands.')
            self.player.no_desc = True
            return True
        elif command == 'inv':
            self.player.output(str((self.player.inventory)))
            self.player.no_desc = True
            return True
        else:
            self.player.output("Please enter a valid response.")
            self.player.no_desc = True
            return True


class Room(Enum):
    FOYER = 0
    HALLWAY = 1
    KITCHEN = 2
    MASTER_BEDROOM = 3
    LANDING = 4
    SECRET_ROOM = 5
    STUDY = 6
    GARDEN = 7
    CLOSET = 8
    RITUAL_ROOM = 9
    FAILURE = 5

class PlayerLocation(object):
    left = None
    right = None
    forward = None
    back = None
    up = None
    down = None
    teleport = None
    lock = False
    interactables: Optional[dict] = None

    # inits the current room with mandatory and optional variables
    def __init__(self, room, name: str, description: str = 'No description'):
        self.room = room
        self.name = name
        self.description = description

    # "enters" the room
    def describe(self, player) -> Room:
        if self.name in player.visited:
            player.output(f'You are in the {self.name}. This room was visited. What do you do?')
        else:
            player.output(f"This is the {self.name}. {self.description}. What do you do?")

    def locked(self, player):
        player.output('The door is locked, what is the code?')
        code = input('CODE> ')
        if code == LOCK_SOLUTION:
            self.locked = False
            player.output('You unlock the door.')
            return True
        elif code in ('e', 'exit'):
            return False
        else:
            player.output('Incorrect code. The door remains locked.')
            return False


class Player(object):

    last_moved = [None, None, None, None]
    interaction_state = None

    def __init__(self, location, inventory, puzzles, visited, no_desc):
        self.location = location
        self.inventory = inventory
        self.puzzles = puzzles
        self.visited = visited 
        self.no_desc = no_desc

    game_text = ''
    def output(self, text):
        self.game_text = '\n\n' + text

    def move(self, command, map):
        if self.location == foyer and SECRET_ROOM_SOLUTION == True:
            self.location.left = secret_room
        self.no_desc = False
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
        elif command in ('u', 'up'):
            if self.location.up:
                self.last_moved.pop(0)
                self.last_moved.append('u')
                map.update_player('up')
            new_location = self.location.up
        elif command in ('d', 'down'):
            if self.location.down:
                self.last_moved.pop(0)
                self.last_moved.append('d')
                map.update_player('down')
            new_location = self.location.down


        if not new_location:
            return False
        else:
            self.location = new_location
            if self.location.lock == True:
                self.location.locked()
                # TODO: ignore directional pop & append instead of resetting
                self.last_moved = [None, None, None, None]
            if self.last_moved == BOX_SOLUTION:
                self.puzzles.append('puzzle_solve')
            return True

    def interact(self, command, object): 
        
        # TODO: if room has no interactables ERROR
        
        if command in ('e', 'exit'):
            print("Player - Interact- Exit")
            self.interaction_state = None
            self.location.describe(self)
            return
        elif object not in self.location.interactables and object not in self.inventory:
            print("Player - Interact - Invalid Response")
            self.output('Please enter a valid response.')
            return 
        elif object in self.location.interactables:
            print("Player - Interact - Location Interactable")
            interactable = self.location.interactables.get(object)
            print('>>>>>>>>>>>>>', interactable)
        elif object in self.inventory:
            interactable = usable_items.get(object)
        interactable.describe(self)
        if command not in interactable.interaction:
            print("Player - Interact - No Command")
            self.interaction_state = interactable.name
            print(self.interaction_state)
        else:
            print("Payer - Interact - Has Command")
            new_item = interactable.interact(self, command)
            if new_item is not None:
                self.add_item(new_item)

    def add_item(self, new_item):
        self.inventory.append(new_item)




class Interactables(object):
    action_1: Optional[str] = None
    action_2: Optional[str] = None
    item: Optional[str] = None
    interaction: Optional[dict] = None
    description: Optional[str] = None
    timer = False

    # init an interactable with optional actions
    def __init__(self, name: str):
        self.name = name

    #return name as string to caller
    def __str__(self):
        return self.name

    def describe(self, player):
        print(">>>>", self)
        print(player)
        description = f"{self.description}"
        if self.interaction is not None:
            # print(self.interaction)
            for act in self.interaction.values():
                if act.description is not None and act.active == True:
                    description += act.description
        player.output(description)

    # allows player to choose what to do with object
    def interact(self, player, command: Optional[str] = None) -> None:
        if self.item == True:
            player.inventory.append(self.name)
            self.item = False
            player.output(f'You pick up the {self.name}.')
        if command.split(' ')[0] in ('g', 'get', 't', 'take'):
            try:
                command = str(command.split(' ')[1])
                return command
            except IndexError:
                player.output('Get what?')
                return
        elif command in ('e', 'exit'):
            player.interaction_state = None
            player.location.describe(player)
            return
        elif command not in self.interaction or not ('e', 'exit'):
            player.output("Please enter a valid response.")
            player.interaction_state = 'room'
            return
        elif command == self.action_1 or self.action_2:
            new_item = self.interaction.get(command).use(player, self.name)
        self.no_desc = False
        player.interaction_state = None
        return new_item
    #else:
        #new_item = None
        #return new_item

  #if self.timer == True:
  #          timeout = 10
  #          t = Timer(1, print, ['Sorry, times up'])
  #          t.start()
  #          prompt = "You have %d seconds to choose the correct answer...\n" % timeout
  #          print(prompt)
  #          if choice == self.action_1 or self.action_2:
  #              print('TIMER CANCELED')
  #              t.cancel()

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



    def use(self, player, interactable):
        if self.active == False:
            return None
        print("INV:", player.inventory)
        print('PUZZLES', player.puzzles)
        print("KEY:", self.key)
        was_unlocked = False
        if self.key is not None:
            for i in player.inventory:
                if i in self.key:
                    was_unlocked = True
            for i in player.puzzles:
                if i == self.key:
                    was_unlocked = True
            if was_unlocked == True:
                player.output(self.unlock)
                if self.item == True:
                    player.output(f'You take the {self.name}.')
                    self.active = False
                    return self.name
            else:
                player.output(self.purpose)
        else:
            player.output(self.purpose)
            if self.key == None and self.item == True:
                player.output(f'You take the {self.name}.')
                self.active = False
                return self.name


class Landscape(object):
    action_1: Optional[str] = None
    action_2: Optional[str] = None
    landscape: Optional[list] = None
    interaction = None
    description: Optional[str] = None

    def __init__(self, name: str):
        self.name = name

    def describe(self, player):
        player.output(self.description)

    def interact(self, player, choice: Optional[str] = None) -> None:
        spin = randint(0, 2)
        land = self.landscape[spin]
        print(land)
        new_item = None
        if choice == self.action_1:
            player.location = player.location.teleport[spin]
            player.interaction_state = None
            player.last_moved = [None, None, None, None]
            player.location.describe(player)
            return
        elif choice == self.action_2:
            object = str(self.action_2)
            new_item = self.interaction.get(object).use(self.player)
            return new_item
        elif choice in ('e', 'exit'):
            player.interaction_state = None
            return
        else:
            player.output('Please enter a valid response.')
            return


class Code_Interactable(object):
    description: Optional[str] = None
    item = None
    solution = None
    unlock = None
    locked = None
    # Immutable
    interaction = None

    def __init__(self, name: str):
        self.name = name
    
    def describe(self, player):
        player.output(self.description)

    def interact(self, player, code: Optional[str] = None) -> None:
        if code == self.solution:
            player.output(self.unlock)
            if self.item != None:
                new_item = self.item
            return new_item
        else:
            player.output(self.locked)
            player.interaction_state = None
            new_item = None
            return new_item



foyer = PlayerLocation(Room.FOYER, 'foyer', 'A large open room. A grand piano with worn keys is here. A beautiful fireplace is on the left wall.')
secret_room = PlayerLocation(Room.SECRET_ROOM, 'secret_room')
hallway = PlayerLocation(Room.HALLWAY, 'hallway')
kitchen = PlayerLocation(Room.KITCHEN, 'kitchen', """"Small compared to the rest of the house. It looks like it hasn't been used in years. There is an oven on the far wall, with cabinets above it. There is a pantry crammed in the corner.""")
master_bedroom = PlayerLocation(Room.MASTER_BEDROOM, 'Master Bedroom')
landing = PlayerLocation(Room.LANDING, 'landing')
study = PlayerLocation(Room.STUDY, 'study')
garden = PlayerLocation(Room.GARDEN, 'garden')
closet = PlayerLocation(Room.CLOSET, 'closet')
ritual_room = PlayerLocation(Room.RITUAL_ROOM, 'ritual room')



# -----------------------------------------------------------------------
# INTERACTIONS

    # OPEN_ITEM
open_item = Interaction('Tincture of a Thousand Possibilites', 'It is locked.')
open_item.key = 'puzzle_solve'
open_item.unlock = "The box opens. A glowing gold tintcure is inside. It is labeled 'Tincture of a Thousand Possibilites"

    # PLAY
play = Interaction('play', 'You play the piano.')
play.key = 'music sheets'
play.unlock = 'You play a beautiful song.'

    # MUSIC
music = Interaction('music sheets', 'They have a song on them.')
music.description = 'Sheets of music are still placed on it.'

    #NEWT_OIL
newt_oil = Interaction('newt oil', 'On the top shelf is a bottle labaled "Newt Oil". You hear something swimming around inside.')
    
    #SELF_PRAISING FLOWER
self_praising_flower = Interaction('self praising flower', 'On the bottome shelf is a bag labeled "Self Praising Flower". The flower seems to be hyping itself up.')
    
    #TRUE SWEETENER
true_sweetener = Interaction('true sweetener', 'You notice a box labeled "True Sweetener". The box reads: /"ONLY USE ONE./"')
    
    # HIPPOGRYPH EGGS
hippogryph_eggs = Interaction('hippogryph eggs', 'A carton of hippogryph eggs is the only thing left here. They are rainbow in color. Grade A.')
    
    # BAKE
bake = Interaction('tasty treat', "You don't have enough ingrediants to bake with.")
bake.key = ('self praising flower', 'hippogryph eggs', 'newt oil', 'true sweetener')
bake.unlock = 'You bake a tasty treat.'

    # RUN
run = Interaction('run', 'You run away.')

    # LEAF
leaf = Interaction('feyleaf', 'The leaf shimmers out of existence when you go to grab it.')
leaf.key = 'Gloves of Lightest Touch'
leaf.unlock= 'Your grip is soft as a cloud. You take the leaf.'

    # READ_SPELLS
read_spells = Interaction('read', open('spell.txt', 'r').read())

    # GLOVES
gloves = Interaction('Gloves of Lightest Touch', 'They seem almost weightless. Plush interior.')

    # WIZARD_HAT
hat = Interaction('Wizard Hat', 'Purple and pointed, with the stars and everything. Not very original.')

   # RITUAL
ritual = Interaction('ritual', "You don't have the proper materials to perform a ritual.")
ritual.key = ('Tincture of a Thousand Possibilites', 'feyleaf')
ritual.unlock = '''The familiar joins you in the circle. As the Ritual commences, all the runes begin to alight.
                You feel the veil between the planes of existence begin to grow weak. The familiar seems to nod
                in gratitude as his form becomes to slowly dissipate. You did it! You sent the familiar home.'''
    
    # READ LETTER 
read_letter = Interaction('read', open('letter.txt', 'r').read())


# ----------------------------------------------------------------------
# INTERACTABLES

    # FIREPLACE
fireplace = Interactables('fireplace')
fireplace.description = 'You feel warm.'

    # PIANO
piano = Interactables('piano')
piano.description = '''A beautiful piano covered in dust sits on the
                        far right end of the foyer.'''.replace('    ', '')
piano.action_1 = 'play'
piano.action_2 = 'music'
piano.interaction = {'play': play, 'music': music}


    # PORTRAIT
portrait = Code_Interactable('portrait')
portrait.description = '''A portrait of an old wizard. As you approach the wizard becomes animated!
                        "I am Mordecai! What is my favorite spell?"'''.replace('   ', '')
portrait.unlock = "Mordecai's hand extends from the painting and hands you a strange rod. You take the Rod of Infinite Possibilites."
sparkle = portrait.unlock
portrait.solution = 'sparkle'
portrait.interaction = {'sparkle': sparkle}
portrait.locked = "Sorry, that just isn't it."
portrait.item = 'Rod of Infinite Possibilities'


    # LANDSCAPE
painting = Landscape('painting')
painting.description = 'A painting of a beautiful landscape.'
painting.landscape = ['foyer', 'kitchen', 'master_bedroom']
painting.interaction = {'run': run}
painting.action_1 = 'stare'
painting.action_2 = 'run'

    # BOX
box = Interactables('box')
box.description = 'A locked box.'
box.interaction = {'open': open_item}
box.action_1 = 'open'

    # PANTRY
pantry = Interactables('pantry')
pantry.description = "A pantry left mostly bare but a few ingrediants."
pantry.interaction = {'flower': self_praising_flower, 'oil': newt_oil}
pantry.action_1 = 'flower'
pantry.action_2 = 'oil'

    # CABINET
cabinet = Interactables('cabinet')
cabinet.description = "A cabinet with spice bottles left mostly empty."
cabinet.interaction = {'sweetener': true_sweetener}
cabinet.action_1 = 'sweetener'

    #ICEBOX
ice_box = Interactables('icebox')
ice_box.description = 'You open the lid. Strangely, there is no ice in it but its still freezing cold.'
ice_box.interaction = {'eggs': hippogryph_eggs}
ice_box.action_1 = 'eggs'


    #OVEN
oven = Interactables('oven')
oven.description = "It hasn't been used in years. But it still has power. Although you aren't sure from where..."
oven.interaction = {'bake': bake}
oven.action_1 = 'bake'

    #FEYLEAF
feyleaf = Interactables('feyleaf')
feyleaf.description = "A deep green plant. Its leaves seem to shimmer in and out of existernce."
feyleaf.interaction = {'leaf': leaf}
feyleaf.action_1 = 'leaf'

    #SPELLBOOK
spellbook = Interactables('spellbook')
spellbook.description = "The title read's 'Mordecai's Mysterious Magiks"
spellbook.interaction = {'read': read_spells}
spellbook.action_1 = 'read'

    #WARDROBE
wardrobe = Interactables('wardrobe')
wardrobe.description = 'It is old and warn, but made of beautiful mahogany. Some gloves of and a wizard hat are stuffed in here.'
wardrobe.interaction = {'gloves': gloves, 'hat': hat}
wardrobe.action_1 = 'gloves'
wardrobe.action_2 = 'hat'

    # RITUAL CIRCLE
ritual_circle = Interactables('circle')
ritual_circle.description = 'A series of geometric shapes and runes all surrounded by a large circle are engraved into the stone floor. The center circle looks big enough to sit in.'
ritual_circle.interaction = {'ritual': ritual}
ritual_circle.action_1 = 'ritual'

    # LETTER
letter = Interactables('letter')
letter.description = 'A letter from your late grandfather, the great wizard Mordecai.'
letter.interaction = {'read': read_letter}
letter.action_1 = 'read'

# ----------------------------------------------------------------------
# ITEMS

music.item = True
newt_oil.item = True
self_praising_flower.item = True
hippogryph_eggs.item = True;
true_sweetener.item = True
gloves.item = True
hat.item = True
leaf.item = True
box.item = True
spellbook.item = True
open_item.item = True
bake.item = True
letter.item = True

usable_items = {'box': box, 'spellbook': spellbook, 'letter': letter}



#-----------------------------------------------------------------------
# DIRECTIONS/ITEMS
    
    # FOYER
foyer.forward = hallway
foyer.interactables = {'fireplace': fireplace, 'piano': piano}

    # SECRET ROOM
secret_room.right = foyer

    # HALLWAY
hallway.forward = garden
hallway.back = foyer
hallway.left = kitchen
hallway.right = master_bedroom
hallway.up = landing
hallway.teleport = [foyer, kitchen, master_bedroom]
hallway.interactables = {'portrait': portrait, 'painting': painting} #'bust': bust,
                        #'landscape painting': landscape_painting

    # MASTER BEDROOM
master_bedroom.left = hallway
master_bedroom.interactables = {'box': box, 'spellbook': spellbook}
    
    # KITCHEN
kitchen.right = hallway
kitchen.interactables = {'pantry': pantry, 'cabinet': cabinet, 'icebox': ice_box, 'oven': oven}
landing.down = hallway

    # LANDING
landing.forward = closet
landing.left = study

    # STUDY
study.lock = True
study.forward = ritual_room
study.right = hallway

    #GARDEN
garden.back = hallway
garden.interactables = {'feyleaf': feyleaf}

    #CLOSET
closet.back = landing
closet.interactables = {'wardrobe': wardrobe}

    #RITUAL ROOM
ritual_room.back = study
ritual_room.interactables = {'circle': ritual_circle}



#------------------------------------------------------------
# PUZZLES

BOX_SOLUTION = ['l', 'l', 'r', 'r']
SECRET_ROOM_SOLUTION = True
LOCK_SOLUTION = 1
#str(randint(100, 999))
print(LOCK_SOLUTION)



class RoomGuide(object):

    room_guide = {
        Room.FOYER: foyer,
        Room.SECRET_ROOM: secret_room,
        Room.HALLWAY: hallway,
        Room.KITCHEN: kitchen,
        Room.MASTER_BEDROOM: master_bedroom,
        Room.LANDING: landing,
        Room.STUDY: study,
        Room.CLOSET: closet
    }

    def __init__(self, room: Room):
        self.room = room

    def next_room(self, room_name):
        new_room = self.room_guide.get(room_name)
        return new_room



