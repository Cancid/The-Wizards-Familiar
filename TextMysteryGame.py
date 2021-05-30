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
        print(self.player.interaction_state)
        if self.player.interaction_state == None:
            moved = self.process_input(command)
            current_room = self.player.location
            self.map.display()
            if moved is False:
               self.player.output("You can't go that way.")
            elif self.player.no_desc == False and self.player.interaction_state == None:
                current_room.describe(self.player)
                self.player.visited.append(self.player.location.name)
        elif self.player.interaction_state == 'room':
            self.player.interact(None, command)
        elif self.player.interaction_state is not None:
            object = self.player.location.interactables.get(self.player.interaction_state)
            object.interact(self.player, command)
            self.player.interaction_state = None



    def process_input(self, command):
        if self.started == False:
            self.started = True
            return

        if command in ('f', 'forward', 'l', 'left', 'r', 'right', 'b', 'back',
                        'u', 'up', 'd', 'down'):
            return self.player.move(command, self.map)

        #elif command in ('i', 'interact'):
        if command in self.player.location.interactables.keys() or command in self.player.inventory:
            print("I did this.")
            # TODO: make inputs like 'piano' work
            self.player.interact(command)
            return True
        #else:
        #    print("Proccess Input - Interact - No Object")
        #    self.player.output('With what?')
        #    self.player.interaction_state = 'room'
        #    print(self.player.interaction_state)
        #    return True
            
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
            print("Process Input - INVALID")
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
            player.output(f"This is the {self.name}. {self.description} What do you do?")

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
                self.location.locked(self)
                # TODO: ignore directional pop & append instead of resetting
                self.last_moved = [None, None, None, None]
            if self.last_moved == ORB_SOLUTION:
                self.puzzles.append('puzzle_solve')
            return True

    def interact(self, command): 
        
        # TODO: if room has no interactables ERROR
        print(command)
        if self.interaction_state is not None:
            interactable = self.location.interactables.get(self.interaction_state)
            if command not in interactable.interaction:
                print("Player - Interact - No Command")
                self.interaction_state = interactable.name
                print(self.interaction_state)
            else:
                print("Payer - Interact - Has Command")
                new_item = interactable.interact(self, command)
                if new_item is not None:
                    self.add_item(new_item)
        else:
            if command in ('e', 'exit'):
                print("Player - Interact- Exit")
                self.interaction_state = None
                self.location.describe(self)
                return
            elif command not in self.location.interactables and command not in self.inventory:
                print("Player - Interact - Invalid Response")
                self.output('Please enter a valid response.')
                return 
            elif command in self.location.interactables:
                print("Player - Interact - Location Interactable")
                interactable = self.location.interactables.get(command)
            elif command in self.inventory:
                interactable = usable_items.get(command)
            self.interaction_state = interactable.name
            interactable.describe(self)
        

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
        player.no_desc = True
        description = f"{self.description}"
            # print(self.interaction)
        for act in self.interaction.values():
            if act.description is not None and act.active == True:
                description += act.description
        if self.item == True:
            player.inventory.append(self.name)
            self.item = False
            description += f' You pick up the {self.name}.'
        player.output(description)

    # allows player to choose what to do with object
    def interact(self, player, command: Optional[str] = None) -> None:
        if command in ('e', 'exit'):
            player.interaction_state = None
            player.location.describe(player)
            return
        elif command not in self.interaction or not ('e', 'exit'):
            print('>>>>>>DOING THIS')
            player.output("Please enter a valid response.")
            player.interaction_state = self.name
            return
        elif command == self.action_1 or self.action_2:
            print("><><><><><><", command)
            new_item = self.interaction.get(command).use(player)
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



    def use(self, player):
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
                    player.output(f'You take the {self.name}. {self.description}')
                    self.active = False
                    return self.name
            else:
                player.output(self.purpose)
        else:
            player.output(self.purpose)
            if self.key == None and self.item == True:
                player.output(f'You take the {self.name}. {self.description}')
                self.active = False
                player.inventory.append(self.name)
                return self.name


class Landscape(object):
    action_1: Optional[str] = None
    action_2: Optional[str] = None
    landscape: Optional[list] = None
    interaction = None
    description: Optional[str] = None

    def __init__(self, name: str):
        self.name = name
        self.spin = randint(0, 2)
    
    def describe(self, player):
        land = self.landscape[self.spin]
        player.output(land)
        print(land)

    def interact(self, player, choice: Optional[str] = None) -> None:
        if choice == 'stare':
            player.location = player.location.teleport[self.spin]
            player.interaction_state = None
            player.last_moved = [None, None, None, None]
            player.location.describe(player)
            return
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



foyer = PlayerLocation(Room.FOYER, 'foyer', 'A large open room. A grand piano with worn keys is here. A beautiful fireplace is still burning on the left wall.')
secret_room = PlayerLocation(Room.SECRET_ROOM, 'secret_room')
hallway = PlayerLocation(Room.HALLWAY, 'hallway', "Candelabras line this long hallway. A portrait of your grandfather is on the left wall, a large mural that's image seems to shift slowly is painted across the right wall. An alcove holds a spiral staircase leading to the upper portions of the mansion.")
kitchen = PlayerLocation(Room.KITCHEN, 'kitchen', """Small compared to the rest of the house. It looks like it hasn't been used in years. There is an oven on the far wall, with cabinets above it. There is a pantry crammed in the corner.""")
master_bedroom = PlayerLocation(Room.MASTER_BEDROOM, 'Master Bedroom', "A large four post bed sits in the center of the room. A nightstand made of gnarled oak is one side of it. A large spellbook sits on the stand. Globules of light flutter through the air, providing dim light to the roonm.")
landing = PlayerLocation(Room.LANDING, 'landing', "Seemingly hundreds of small frames are hung all over the walls of the wooden landing. A cobalt blue door is on your left. A door made of redwood is on your right. A small closet seems to be in front of you.")
study = PlayerLocation(Room.STUDY, 'study', "This room seems to be hald library and hald labratory. Books are scattered across a desk and a strange metal orb sits on a labratory table covered in beakers and a potions.")
garden = PlayerLocation(Room.GARDEN, 'garden' "Only the smallest indication of a stone wall peaks out of the ivy that covers every surface of this small garden. You can see the starry night sky overhead. Among shelves and shelves of plants, one marked 'feyleaf' catches your attention.")
closet = PlayerLocation(Room.CLOSET, 'closet', 'A small walk-in closet full of your standard junk. A large dark wood wardrobe stands on the far end.')
ritual_room = PlayerLocation(Room.RITUAL_ROOM, 'ritual room', "This entire room appears to be made of stone. Strange runes mark the walls. A glowing blue circle seems to be engraved into the floor taking up most of the room.")



# -----------------------------------------------------------------------
# INTERACTIONS

    # OPEN_ITEM
open_item = Interaction('Tincture of a Thousand Possibilites', 'It is locked.')
open_item.key = 'puzzle_solve'
open_item.unlock = "The orb slides open. A glowing gold tintcure is inside. It is labeled 'Tincture of a Thousand Possibilites"

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
fantastic_flour = Interaction('fantastic flour', "It says 'fantastic', but it looks pretty regular to you.")
    
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
gloves = Interaction('Gloves of Lightest Touch', '', 'They seem almost weightless. Plush interior.')

    # WIZARD_ROBES
robes = Interaction('Wizard Robes', '', 'Purple, with the stars and everything. Not very original.')

   # RITUAL
ritual = Interaction('ritual', "You don't have the proper materials to perform a ritual.")
ritual.key = ('Tincture of a Thousand Possibilites', 'feyleaf', 'tasty treat', 'Rod of Planeshift')
ritual.unlock = '''The familiar joins you in the circle. As the Ritual commences, all the runes begin to alight.
                You feel the veil between the planes of existence begin to grow weak. The familiar seems to nod
                in gratitude as his form becomes to slowly dissipate. You did it! You sent the familiar home.'''
    
    # READ LETTER 
read_letter = Interaction('read', open('letter.txt', 'r').read())


# ----------------------------------------------------------------------
# INTERACTABLES

    # FIREPLACE
fireplace = Interactables('fireplace')
fireplace.description = 'The fire burns despite their being no logs. You feel warm.'

    # PIANO
piano = Interactables('piano')
piano.description = '''A beautiful piano covered in dust sits on the far right end of the foyer.'''
piano.action_1 = 'play'
piano.action_2 = 'music'
piano.interaction = {'play': play, 'music': music}


    # PORTRAIT
portrait = Code_Interactable('portrait')
portrait.description = '''A portrait of an old wizard. As you approach the wizard becomes animated!
                        "I am Mordecai! What is my favorite spell?"'''.replace('   ', '')
portrait.unlock = "Mordecai's hand extends from the painting and hands you a strange rod. You take the Rod of Planeshift."
sparkle = portrait.unlock
portrait.solution = 'sparkle'
portrait.interaction = {'sparkle': sparkle}
portrait.locked = "Sorry, that just isn't it."
portrait.item = 'Rod of Planeshift'


    # Mural
mural = Landscape('mural')
mural.landscape = ['This mural looks suspicially like the foyer.',
                    'This mural seems to be of a small, dusty kitchen.',
                    'A painting of a bedroom wit a regal looking bed and a large tome on the nightstand.',
                    'A beautiful, serene garden is painted on the wall.',
                    'This is a painting of a... junk closet? Strange.',
                    'A stone room, covered in strange, glowing runes is depicted.']
mural.interaction = 'stare'
mural.action_2 = 'run'

    # ORB
orb = Interactables('orb')
orb.description = "It appears to be locked. Though you aren't sure how."
orb.interaction = {'open': open_item}
orb.action_1 = 'open'

    # PANTRY
pantry = Interactables('pantry')
pantry.description = "A pantry left mostly bare but a few ingredients. You see a bag labeled Fantastical Flour and a box of something called True Sweetener."
pantry.interaction = {'flour': fantastic_flour, 'sweetener': true_sweetener}
pantry.action_1 = 'flour'
pantry.action_2 = 'oil'

    # CABINET
cabinet = Interactables('cabinet')
cabinet.description = "A cabinet with spice bottles left mostly empty. A can of newt oil catches your eye."
cabinet.interaction = {'oil': newt_oil}
cabinet.action_1 = 'sweetener'

    #ICEBOX
ice_box = Interactables('icebox')
ice_box.description = 'You open the lid. Strangely, there is no ice in it but its still freezing cold. A carton of hippogryph eggs sits upon the ice.'
ice_box.interaction = {'eggs': hippogryph_eggs}
ice_box.action_1 = 'eggs'


    #OVEN
oven = Interactables('oven')
oven.description = "It looks like it hasn't been used in years, you're not sure how it has power, but it looks like it could stead be used to bake."
oven.interaction = {'bake': bake}
oven.action_1 = 'bake'

    #FEYLEAF
feyleaf = Interactables('feyleaf')
feyleaf.description = "A deep green plant. Its leaves seem to shimmer in and out of existernce. You think you might be able to pick a leaf."
feyleaf.interaction = {'leaf': leaf}
feyleaf.action_1 = 'leaf'

    #SPELLBOOK
spellbook = Interactables('spellbook')
spellbook.description = "The title read's 'Mordecai's Mysterious Magiks'."
spellbook.interaction = {'read': read_spells}
spellbook.action_1 = 'read'

    #WARDROBE
wardrobe = Interactables('wardrobe')
wardrobe.description = 'It is old and warn, but made of beautiful mahogany. Some gloves of and wizard robes are stuffed in here.'
wardrobe.interaction = {'gloves': gloves, 'robes': robes}
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
fantastic_flour.item = True
hippogryph_eggs.item = True
true_sweetener.item = True
gloves.item = True
robes.item = True
leaf.item = True
orb.item = True
spellbook.item = True
open_item.item = True
bake.item = True
letter.item = True

usable_items = {'orb': orb, 'spellbook': spellbook, 'letter': letter}



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
hallway.right = ritual_room
hallway.up = landing
hallway.teleport = [foyer, kitchen, master_bedroom, garden, closet, ritual_room]
hallway.interactables = {'portrait': portrait, 'mural': mural}

    # MASTER BEDROOM
master_bedroom.left = landing
master_bedroom.interactables = {'spellbook': spellbook}
    
    # KITCHEN
kitchen.right = hallway
kitchen.interactables = {'pantry': pantry, 'cabinet': cabinet, 'icebox': ice_box, 'oven': oven}
landing.down = hallway

    # LANDING
landing.forward = closet
landing.left = study
landing.right = master_bedroom

    # STUDY
study.right = landing
study.interactables = {'orb': orb}

    #GARDEN
garden.back = hallway
garden.interactables = {'feyleaf': feyleaf}

    #CLOSET
closet.back = landing
closet.interactables = {'wardrobe': wardrobe}

    #RITUAL ROOM
#ritual_room.lock = True
ritual_room.left = hallway
ritual_room.interactables = {'circle': ritual_circle}



#------------------------------------------------------------
# PUZZLES

ORB_SOLUTION = ['l', 'l', 'r', 'r']
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



