import mapper
from random import randint
from threading import Timer
from enum import Enum
from typing import List, Set, Dict, Tuple, Optional, Callable, Iterator, Union, Literal
from collections import Counter
import os


DIRECTION_INDEX = ['f','b','l','r','u','d','forward','backward','left','right','up','down']

dir_path = os.path.dirname(os.path.realpath(__file__))


class Engine(object):

    def __init__(self):
        self.player = None
        self.map = None

    started = False

    def play(self):
        a_map = RoomGuide(Room.FOYER)
        a_player = Player(a_map.next_room(a_map.room), ['license', 'letter'], [])
        self.player = a_player
        self.player.last_interact("letter")
        map = mapper.Map()
        print(map)
        map.generate_map_from_room_guide(self.player.location)
        self.map = map
        press_play = "Press ENTER to Play \n\n"
        self.player.output(open(dir_path + "/data/opening_scene.txt", "r").read())
        self.player.output(f"{press_play:^150}")
  

    def process_input(self, command):


        if self.started == False:
            self.player.output("Welcome to the Wizard's Familiar!\n")
            self.player.output(open(dir_path + '/data/help.txt', "r").read() + "\nTry reading the letter in your *inventory!")
            self.started = True
            return


        if self.player.win == True:
            congrats = "Congratulations!\nPlay Again?\nY/N"
            self.player.output(f"{congrats}")
            if command in ("yes", "y"):
                self.play()
            elif command in ("no", "n"):
                exit(0)
            return
        
        if self.player.location == foyer and self.player.location.left is None and play.was_unlocked == True:
            self.player.location.left = secret_room
            self.map.generate_map_from_room_guide(self.player.location)

        if command in DIRECTION_INDEX:
            self.player.interaction_state = None
            self.player.move(command, self.map)

        elif command in ('desc', 'description'):
            print(self.player.location.name)
            self.player.location.describe(self.player)
            return True
        elif command in ('h', 'help'):
            self.player.output(open(dir_path + '/data/help.txt', "r").read())
            return True
        elif command in ("i", "inv", "inventory"):
            self.player.output(str(self.player.inventory))
            return True

        elif (
            (self.player.last_interacted in self.player.location.interactables.values()
            or self.player.last_interacted in self.player.inventory)
            and command in self.player.last_interacted.interaction.keys()
        ):
            self.player.last_interacted.interact(self.player, command, self.map)

        elif command in self.player.location.interactables.keys() or command in self.player.inventory:
            self.player.interact(command)
            

        elif self.player.interaction_state is not None:
            if self.player.interaction_state in self.player.inventory:
                object = usable_items.get(self.player.interaction_state)
            else:
                object = self.player.location.interactables.get(self.player.interaction_state)
            object.interact(self.player, command, self.map)
        
        else:
            print("Process Input - INVALID")
            self.player.output("Please enter a valid response.")
            return True
            


class Player(object):

    last_moved = [None]
    interaction_state = None
    win = False

    def __init__(self, location, inventory, puzzles):
        self.location = location
        self.inventory = inventory
        self.puzzles = puzzles
    
    last_interacted = None
    def last_interact(self, item_name):
        if item_name in self.inventory:
            self.last_interacted = usable_items.get(item_name)
        else:
            self.last_interacted = self.location.interactables.get(item_name)


    game_text = ''
    def output(self, text):
        self.game_text = self.game_text + '\n\n' + text


    def move(self, command, map):
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
        elif command in ('u', 'up'):
            if self.location.up:
                map.generate_map_from_room_guide(self.location.up)
                map.update_player('up')
            new_location = self.location.up
        elif command in ('d', 'down'):
            if self.location.down:
                map.generate_map_from_room_guide(self.location.down)
                map.update_player('down')
            new_location = self.location.down
        if not new_location:
             self.output("You can't go that way.")
             return
        else:
            self.location = new_location
            self.location.describe(self)
        if "orb" in self.inventory and "puzzle_solve" not in self.puzzles:
            if len(self.last_moved) == 4:
                self.last_moved.pop(0)
            self.last_moved.append(self.location.name)
            self.orb_movement()
            return True

    def interact(self, command): 
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

    #slicer = 1
    #list_size = 3
    
    stage = 0
    def orb_movement(self):
        move_text = ["The orb seems to deconstruct itself like a slide puzzle to reveal a second layer.",
                        "The orb's second layer slides away.", 
                        "The orb twists, lowering another layer of its exterior.",
                        "The orb reconfigures itself, revealing a final layer.",
                        "The final layer of the orb shrinks to reveal a seam with a latch in the center."]
            
        visit_counter = Counter(self.last_moved)
        print(visit_counter)
        for count in visit_counter.values():
            if count >= 2:
                self.last_moved = []
                self.stage = 0
                self.output("The orb whirrs. Growing back to its original size.")
                return
        self.output(move_text[self.stage])
        if self.stage == 4:
            self.puzzles.append('puzzle_solve')
        self.stage += 1



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
    interactables = None

    def __init__(self, room, name: str, description: str = 'No description'):
        self.room = room
        self.name = name
        self.description = description


    def describe(self, player) -> Room:
        description = f"You are in the {self.name}. "
        description += self.description
        for i in self.interactables.values():
            if i.item is not None and i.item == True or i.event is not None and i.event == True:
               description += i.purpose
        if "callidopie" in player.puzzles:
            cal_text = self.callidopie()
            description += cal_text
        player.output(description + " What do you do?")

    def callidopie(self):
            cal_event = randint(0,9)
            events = [" Callidopie swirls around you excitedly.", " Callidope peers at you quizzically.",
             " Callidopie casts a spell to make rainbows appear in the air." ]
            if self.name == kitchen:
                events.append(" Callidopie goes rummaging through the pantry.")
            elif self.name == ritual_room:
                events.append(" Callidopie brims with excitment.")
            elif self.name == master_bedroom:
                events.append(" Callidopie curls around your shoulders, seemingly in a state of sorrow.")
            elif self.name == closet:
                events.append(" Callidopie dives into a pile of clothes, emerging wearing an oversized wizard's hat. She swirls around the room, cooing.")
            if cal_event >= len(events):
                event_select = ""
            else:
                event_select = events[cal_event]
                print(event_select)
            events.pop()
            return event_select

      
                
class Interactables(object):
    action_1: Optional[str] = None
    action_2: Optional[str] = None
    item: Optional[str] = None
    event = None
    interaction: Optional[dict] = None
    description: Optional[str] = None
    purpose = None


    def __init__(self, name: str):
        self.name = name

    #return name as string to caller
    def __str__(self):
        return self.name

    def describe(self, player):
        player.last_interact(self.name)
        description = f"{self.description}"
        if self.interaction is not None:
            for act in self.interaction.values():
                if act.description is not None and act.active == True:
                    description += act.description
        if self.item == True:
            player.inventory.append(f'{self.name}')
            player.last_interact(self.name)
            self.item = False
            description += f' You pick up the {self.name}.'
            player.interaction_state = None
        player.output(description)

       
  
    def interact(self, player, command, map) -> None:
        if command in ('e', 'exit'):
            player.interaction_state = None
            player.location.describe(player)
            return
        elif command in DIRECTION_INDEX:
            player.interaction_state = None
            player.move(command, map)
        elif command not in self.interaction or not ('e', 'exit'):
            player.output("Please enter a valid response.")
            return
        elif command == self.action_1 or self.action_2:
            new_item = self.interaction.get(command)
            if new_item.active == False:
                player.output("I can't do that anymore.")
            else:
                new_item.use(player, map)
                for act in self.interaction.keys():
                    if act in player.puzzles:
                        self.event = False
                return new_item



class Interaction(object):
    active: bool = True
    item: bool = False
    key: Optional[str] = None
    unlock: Optional[str] = None
    was_unlocked = False
    # description = None

    def __init__(self, name: str, purpose: str, description: Optional[str] = None) -> None:
        self.name = name
        self.purpose = purpose
        self.description = description


    def use(self, player, map):
        if self.active == False:
            return None
        self.was_unlocked = False
        if self.key is not None:
            key_list = []
            for i in player.inventory:
                if i in self.key:
                    key_list.append(i)
                if Counter(key_list) == Counter(self.key):
                    self.was_unlocked = True
                    for i in key_list:
                        print(i)
                        print(key_list)
                        player.inventory.remove(i)
            for i in player.puzzles:
                if i == self.key:
                    self.was_unlocked = True
            if self.was_unlocked == True:
                if self.name == "ritual":
                    player.output(self.unlock)
                    player.win = True
                else:
                    player.output(self.unlock)
                    if self.item == True:
                        player.output(f"You take the {self.name}.")
                        player.inventory.append(self.name)
                        self.active = False
                    if self.name == "callidopie":
                        player.puzzles.append(self.name)
                        self.active = False
                    if self.name == "play":
                        player.location.left = secret_room
                        map.generate_map_from_room_guide(player.location)
                        player.move("l", map)
            else:
                player.output(self.purpose)
        else:
            player.output(self.purpose)
            if self.key == None and self.item == True:
                player.output(f'You take the {self.name}.')
                player.inventory.append(self.name)
                self.active = False
        player.interaction_state = None
        return



class Landscape(object):
    action_1: Optional[str] = None
    action_2: Optional[str] = None
    landscape: Optional[list] = None
    interaction = None
    description: Optional[str] = None
    item = None
    event = None

    def __init__(self, name: str):
        self.name = name
    
    spin = None
    def describe(self, player):
        self.spin = randint(0, 4)
        land = self.landscape[self.spin]
        player.output(land + self.description)
        print(land)

    def interact(self, player, choice, map):
        if choice in DIRECTION_INDEX:
            player.interaction_state = None
            player.move(choice, map)
        if choice == 'stare':
            player.location = player.location.teleport[self.spin]
            map.generate_map_from_room_guide(player.location)
            player.interaction_state = None
            player.last_moved = [None, None, None, None]
            player.location.describe(player)
            return
        elif choice in ('e', 'exit'):
            player.interaction_state = None
            player.location.describe(player)
            return
        else:
            player.output('Please enter a valid response.')
            return



class Code_Interactable(object):
    description: Optional[str] = None
    has_item = None
    item = None
    solution = None
    unlock = None
    locked = None
    purpose = None
    active = True
    event = None
    # Immutable
    interaction = None

    def __init__(self, name: str):
        self.name = name
    
    def describe(self, player):
        if self.active == False:
            player.output("I can't do that anymore.")
            player.interaction_state = None
        else:
            player.output(self.description)

    def interact(self, player, code, map) -> None:
        if code in DIRECTION_INDEX:
            player.interaction_state = None
            player.move(code, map)
            return
        if code in ("e", "exit"):
            player.interaction_state = None
            player.location.describe(player)
            return
        elif code == self.solution:
            player.output(self.unlock)
            self.active = False
            if self.has_item != None:
                player.inventory.append(self.has_item)
            if self.name == "lock":
                player.location.right = ritual_room
                map.generate_map_from_room_guide(player.location)
                player.move("r", map)

        else:
            player.output(self.locked)
        player.interaction_state = None





foyer = PlayerLocation(Room.FOYER, 'foyer', 'A large open room. A grand *piano with worn keys is here. A beautiful *fireplace is still burning on the left wall.')
secret_room = PlayerLocation(Room.SECRET_ROOM, 'secret room', "Behind the fireplace is a small alcove lined with shelves. All manner of gems, artifacts, trophies, and more fill the shelves.")
hallway = PlayerLocation(Room.HALLWAY, 'hallway', "Candelabras line this long hallway. A *portrait of your grandfather is on the left wall, a large *mural that's image seems to shift slowly is painted across the right wall. An alcove holds a spiral staircase leading to the upper portions of the mansion.")
kitchen = PlayerLocation(Room.KITCHEN, 'kitchen', "Small compared to the rest of the house. It looks like it hasn't been used in years. There is an *oven on the far wall, with a *cabinet above it. There is a *pantry crammed in the corner next an *icebox.")
master_bedroom = PlayerLocation(Room.MASTER_BEDROOM, 'Master Bedroom', "A large four post bed sits in the center of the room. A nightstand made of gnarled oak is one side of it. Globules of light flutter through the air, providing dim light to the room.")
landing = PlayerLocation(Room.LANDING, 'landing', "Seemingly hundreds of small frames are hung all over the walls of the wooden landing. A cobalt blue door is on your left. A door made of redwood is on your right. A small closet seems to be in front of you.")
study = PlayerLocation(Room.STUDY, 'study', "This room seems to be hald library and hald labratory. Books are scattered across a desk and there is a labratory table covered in beakers and a potions.")
garden = PlayerLocation(Room.GARDEN, 'garden', "Only the smallest indication of a stone wall peaks out of the ivy that covers every surface of this small garden. You can see the starry night sky overhead. Among shelves and shelves of plants, one marked '*faeleaf' catches your attention.")
closet = PlayerLocation(Room.CLOSET, 'closet', 'A small walk-in closet full of your standard junk. A large dark wood *wardrobe stands on the far end.')
ritual_room = PlayerLocation(Room.RITUAL_ROOM, 'ritual room', "This entire room appears to be made of stone. Strange runes mark the walls. A glowing blue *circle seems to be engraved into the floor taking up most of the room.")



# -----------------------------------------------------------------------
# INTERACTIONS

    # OPEN_ITEM
open_item = Interaction('Tincture of a Thousand Possibilites', "It won't open.")
open_item.key = ('puzzle_solve')
open_item.unlock = "The orb slides open. A glowing gold tintcure is inside. It is labeled 'Tincture of a Thousand Possibilites."

    # PLAY
play = Interaction('play', 'You play the piano.')
play.key = ['music sheets']
play.unlock = "You perform 'Mordedcai's Myserious Melody'. As you press the final key, you hear a rumbling from across the room! The fireplace has shifted to reveal a small passage behind."

    # MUSIC
music = Interaction('music sheets', "Of all the sheets of music one labeled 'Mordecai's Mysterious Melody' catches your eye. It looks very complex to play.", ' *Sheets of music are still placed on it.')

    # NEWT_OIL
newt_oil = Interaction('newt oil', 'You hear something swimming around inside.', ' On the top shelf is a bottle labaled "Newt *Oil".',)
    
    # SELF_PRAISING FLOWER
fantastic_flour = Interaction('fantastic flour', " It says 'fantastic', but it looks pretty regular to you.", " A bag is on the bottom shelf. It says \"Fantastic *Flour\".")
    
    #TRUE SWEETENER
true_sweetener = Interaction('true sweetener', 'The box instructs: "ONLY USE ONE"".', ' You notice a box labeled "True *Sweetener".', )
    
    # HIPPOGRYPH EGGS
hippogryph_eggs = Interaction('hippogryph eggs', 'They are rainbow in color. Grade A.', ' A carton of hippogryph *eggs is the only thing left here.')
    
    # BAKE
bake = Interaction('tasty treat', "You don't have enough ingrediants to *bake with.")
bake.key = ('fantastic flour', 'hippogryph eggs', 'newt oil', 'true sweetener')
bake.unlock = 'You bake a tasty treat.'

    # LEAF
leaf = Interaction('faeleaf', 'The leaf shimmers out of existence when you go to grab it.')
leaf.key = ['Gloves of Lightest Touch']
leaf.unlock= 'With the Gloves of Lightest Touch your grip is soft as a cloud. You take the leaf.'

    # READ_SPELLS
read_spells = Interaction('read', open(dir_path + '/data/spell.txt', 'r').read())

    # GLOVES
gloves = Interaction('Gloves of Lightest Touch',  'They seem almost weightless. Plush interior.', ' A pair of sky blue *gloves with patterns of clouds that seem to swirl on their own are hung on a hook.',)

    # WIZARD_ROBES
robes = Interaction('wizard robes', 'Purple, with the stars and everything. Not very original.', ' A set of *robes hangs within.')

   # RITUAL
ritual = Interaction('ritual', "You don't have the proper materials to perform a ritual.")
ritual.key = ('Tincture of a Thousand Possibilites', 'faeleaf', 'Rod of Planeshift', 'wizard robes', 'faedust')
ritual.unlock = '''Callidopie joins you in the circle. As the Ritual commences, all the runes begin to alight. You feel the veil between the planes of existence begin to grow weak. Callidopie seems to nod in gratitude as her form becomes to slowly dissipate. You did it! You sent the familiar home.'''

   # READ LETTER 
read_letter = Interaction("read", open(dir_path + "/data/letter.txt", "r").read())

    # READ NOTE
read_note = Interaction("read", "A single phrase is scrawled on the paper: grandaughter's initials")

    #READ LICENSE
read_license = Interaction("read", open(dir_path + "/data/license.txt", "r").read())

    # REST
rest = Interaction("rest", "Resting by the fire, you recall your fondest memory of your grandfather. You would always ask him to make you glitter, and he would cast his favorite spell Sparkle on you.")

    # READ_RECIPE
read_recipe = Interaction("read", open(dir_path + "/data/recipe.txt", "r").read())

    # CALLIDOPIE
callidopie = Interaction("callidopie", "You call out to Callidopie. Her head tilts to the side curiously, but she doesn't budge.")
callidopie.key = ["tasty treat"]
callidopie.unlock = "You extend the tasty treay out to Callidopie. Her radiant butterfly wings unfurl and she swoops down to perch on your arm cooing as she enjoys the treat. Callidopie is now following you!"




# -----------------------------------]-----------------------------------
# INTERACTABLES

    # FIREPLACE
fireplace = Interactables('fireplace')
fireplace.description = 'The fire burns despite their being no logs. You feel warm. There is a lounge chair you could *rest in beside it.'
fireplace.interaction = {'rest': rest}
fireplace.action_1 = 'rest'

    # PIANO
piano = Interactables('piano')
piano.description = 'A beautiful piano covered in dust sits on the far right end of the foyer. I know how to *play it.'
piano.action_1 = 'play'
piano.action_2 = 'sheets'
piano.interaction = {'play': play, 'sheets': music}


    # PORTRAIT
portrait = Code_Interactable('portrait')
portrait.description = '''A portrait of your grandfather in his purple robes and pointed wizard hat. As you approach the painting becomes animated!
                        "I am Mordecai! What is my favorite spell?"'''.replace('   ', '')
portrait.unlock = "Mordecai's hand extends from the painting and hands you a strange rod. You take the Rod of Planeshift."
sparkle = portrait.unlock
portrait.solution = 'sparkle'
portrait.interaction = {'sparkle': sparkle}
portrait.locked = "Sorry, that just isn't it."
portrait.has_item = 'Rod of Planeshift'


    # MURAL
mural = Landscape('mural')
mural.description = " If I *stare at it for too long I can feel my essence begin to shift."
mural.landscape = ['This mural looks suspicially like the foyer.',
                    'This mural seems to be of a small, dusty kitchen.',
                    'A painting of a bedroom with a regal looking bed and a large tome on the nightstand.',
                    'A beautiful, serene garden is painted on the wall.',
                    'This is a painting of a... junk closet? Strange.']
mural.interaction = 'stare'

    # ORB
orb = Interactables('orb')
orb.purpose = ' A strange metal *orb sits on the table.'
orb.description = "There is an inscription around the center ring: 'Five places I must go, but never the same or I will grow.' It looks like it might *open. Though you aren't sure how."
orb.interaction = {'open': open_item}
orb.action_1 = 'open'

    # PANTRY
pantry = Interactables('pantry')
pantry.description = "A pantry left mostly bare but a few ingredients."
pantry.interaction = {'flour': fantastic_flour, 'oil': newt_oil}
pantry.action_1 = 'flour'
pantry.action_2 = 'oil'

    # RECIPE BOOK
recipe_book = Interactables("recipe")
recipe_book.purpose = " A *recipe book sits next to the oven. It looks old and relatively unused."
recipe_book.description = "The title reads 'Mama Mordecai's Mystical Morsels'. I can *read it."
recipe_book.interaction = {"read": read_recipe}
recipe_book.action_1 = "read"

    # CABINET
cabinet = Interactables('cabinet')
cabinet.description = "A cabinet with spice bottles left mostly empty."
cabinet.interaction = {'sweetener': true_sweetener}
cabinet.action_1 = 'sweetener'

    # ICEBOX
ice_box = Interactables('icebox')
ice_box.description = 'You open the lid. Strangely, there is no ice in it but its still freezing cold.'
ice_box.interaction = {'eggs': hippogryph_eggs}
ice_box.action_1 = 'eggs'

    # OVEN
oven = Interactables('oven')
oven.description = "It looks like it hasn't been used in years, you're not sure how it has power, but it looks like it could still be used to *bake."
oven.interaction = {'bake': bake}
oven.action_1 = 'bake'

    # FAELEAF
faeleaf = Interactables('faeleaf')
faeleaf.description = "A deep green plant. Its leaves seem to shimmer in and out of existernce. You think you might be able to pick a *leaf."
faeleaf.interaction = {'leaf': leaf}
faeleaf.action_1 = 'leaf'

    # SPELLBOOK
spellbook = Interactables('spellbook')
spellbook.purpose = " A *spellbook sits on the nightstand."
spellbook.description = "Scrawled across the cover in elaborate filigerie: 'Mordecai's Mysterious Magiks'. I can *read it."
spellbook.interaction = {'read': read_spells}
spellbook.action_1 = 'read'

    #WARDROBE
wardrobe = Interactables('wardrobe')
wardrobe.description = 'It is old and warn, but made of beautiful mahogany.'
wardrobe.interaction = {'robes': robes, 'gloves': gloves}
wardrobe.action_1 = 'gloves'
wardrobe.action_2 = 'hat'

    # RITUAL CIRCLE
ritual_circle = Interactables('circle')
ritual_circle.description = 'A series of geometric shapes and runes all surrounded by a large circle are engraved into the stone floor. The center circle looks big enough to sit and perform a *ritual in.'
ritual_circle.interaction = {'ritual': ritual}
ritual_circle.action_1 = 'ritual'

    # LETTER
letter = Interactables('letter')
letter.description = 'A letter from your late grandfather, the great wizard Mordecai. I can *read it.'
letter.interaction = {'read': read_letter}
letter.action_1 = 'read'

    # RITUAL_ROOM_LOCK
ritual_room_lock = Code_Interactable('lock')
ritual_room_lock.description = "The doors are engraved with depictions of mythical creatues. As you approach you hear your grandfather's voice say: What is the passcode?"
ritual_room_lock.purpose = " A set of oversized doubledoors leads somewhere to the right. There is a *lock on the handles."
ritual_room_lock.locked = "Incorrect!"
ritual_room_lock.unlock = "The lock falls free from the door."
ritual_room_lock.solution = 'wmw'
ritual_room_lock.interaction = None

    # NOTE
note = Interactables('note')
note.description = "A hastily scrawled note. It's your grandfather's handwriting. I can *read it."
note.purpose = " You barely notice a *note hanging out of one of the draws of the desk."
note.interaction = {'read': read_note}
note.action_1 = 'read'

    # LICENSE
license = Interactables("license")
license.description = "My driver's license. I can *read it but I don't see why I need to."
license.interaction = {"read": read_license}
license.action_1 = "read"

    # FAEDUST
faedust = Interactables("faedust")
faedust.description = "So fine it is barely visible, it sparkles like a thousand minisculue diamonds."
faedust.purpose = " Among the items your eyes finally fall upon a small bowl labeled '*Faedust'."
faedust.interaction = {}

    # SHELF
shelf = Interactables("shelf")
shelf.description = "Barely visible as her scales shimmer to match the texture of the items around her, a small dragon-like creature peers down at you with a glowing yellow eyes, antennas like a moth, wings like a butterfly, and a tail like a chameleon. This must be *Callidopie. She looks at you nervously, but expectently. "
shelf.purpose = " As you enter the room you barely catch the sound of talons scraping and bottles shifting. On the top *shelf, a bottle finishes rocking on its base."
shelf.interaction = {"callidopie": callidopie}
shelf.action_1 = "callidopie"


# ----------------------------------------------------------------------
# ITEMS & EVENTS

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
ritual_room_lock.item = True
note.item = True
faedust.item = True
recipe_book.item = True
shelf.event = True

usable_items = {'orb': orb, 'spellbook': spellbook, 'letter': letter, 'note': note, 'license': license, 'recipe': recipe_book}



#-----------------------------------------------------------------------
# DIRECTIONS/ITEMS
    
    # FOYER
foyer.forward = hallway
foyer.interactables = {'fireplace': fireplace, 'piano': piano}

    # SECRET ROOM
secret_room.right = foyer
secret_room.interactables = {'faedust': faedust, "shelf": shelf}


    # HALLWAY   
hallway.forward = garden
hallway.back = foyer
hallway.left = kitchen
hallway.up = landing
hallway.teleport = [foyer, kitchen, master_bedroom, garden, closet, ritual_room]
hallway.interactables = {'portrait': portrait, 'mural': mural, 'lock': ritual_room_lock}

    # MASTER BEDROOM
master_bedroom.left = landing
master_bedroom.interactables = {'spellbook': spellbook}
    
    # KITCHEN
kitchen.right = hallway
kitchen.interactables = {'pantry': pantry, 'cabinet': cabinet, 'icebox': ice_box, 'oven': oven, 'recipe': recipe_book}
landing.down = hallway

    # LANDING
landing.forward = closet
landing.left = study
landing.right = master_bedroom
landing.interactables = {}

    # STUDY
study.right = landing
study.interactables = {'orb': orb, 'note': note}

    # GARDEN
garden.back = hallway
garden.interactables = {'faeleaf': faeleaf}

    # CLOSET
closet.back = landing
closet.interactables = {'wardrobe': wardrobe}

    # RITUAL ROOM
ritual_room.lock = True
ritual_room.left = hallway
ritual_room.interactables = {'circle': ritual_circle}



#------------------------------------------------------------



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


