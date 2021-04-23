import math

# TODO Features:
# Player position on map
# Discover areas as the player progresses
# Doors that appear on map
# CoLoRs
# Better error handling
# Better clarity around what 0,0 represents

# TODO Bugs:
# A map that is not connected properly can cause a forever hang

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

    # creates a "Position" from a string like "2, 3"
    @staticmethod
    def from_string(input_string):
        x, y = input_string.split(",")
        int_x = int(x.strip())
        int_y = int(y.strip())
        return Position(int_x, int_y)

    
    def forward(self):
        return Position(self.x, self.y + 1)

    def back(self):
        return Position(self.x, self.y - 1)

    def left(self):
        return Position(self.x - 1, self.y)

    def right(self):
        return Position(self.x + 1, self.y)

class Map:
    # Mutable
    map_array = None
    player_location = None

    # Non-mutable
    justification = 3 # must be odd
    player_icon = "X"
    room_icon = "0"
    v_conn_icon = "|"
    h_conn_icon = "-"
    empty_icon = " "

    # Print the map to stdout
    def display(self):
        if self.map_array is None:
            print("Map has not been initialized")
            return

        for y, row in enumerate(self.map_array):
            row_string = ""
            for x, item in enumerate(row):
                if (
                    self.player_location is not None 
                    and self.player_location.x == x
                    and self.player_location.y == y
                ):
                    row_string += self.player_icon.center(self.justification)
                elif item == "room":
                    row_string += self.room_icon.center(self.justification)
                elif item == "h_conn":
                    row_string += self.h_conn_icon * self.justification
                elif item == "v_conn":
                    row_string += self.v_conn_icon.center(self.justification)
                else:
                    row_string += self.empty_icon.center(self.justification)
            print(row_string)
    
    def update_player(self, direction):
        if direction == "forward":
            self.player_location.y -= 2 # Because map is oriented "backwards"
        elif direction == "back":
            self.player_location.y += 2 # Because map is oriented "backwards"
        elif direction == "right":
            self.player_location.x += 2
        elif direction == "left":
            self.player_location.x -= 2
        else:
            print("Unrecognized direction")

    # Room Interface
    # left
    # right
    # forward
    # back 
    def generate_map_from_room_guide(self, room_guide):
        print("Generating map:")
        # =====================================================================
        # Generate a dictionary mapping string describing a position to strings
        # describing a room
        # 
        # E.g. {"0, 4": "connector"}
        # =====================================================================
        map_dict = {}
        first_room = room_guide.next_room(room_guide.room)
        queue = [(Position(0,0), first_room)]

        while len(queue) > 0:
            # Add room to dictionary of positions
            cur_pos, cur_room = queue.pop()
            map_dict[str(cur_pos)] = "room"

            # Add connectors to dictionary of positions
            # also add connected rooms to "to-do" list
            # TODO: Ugly
            forward_room = room_guide.next_room(cur_room.forward)
            back_room = room_guide.next_room(cur_room.back)
            right_room = room_guide.next_room(cur_room.right)
            left_room = room_guide.next_room(cur_room.left)
            if str(cur_pos.forward()) not in map_dict and forward_room is not None:
                map_dict[str(cur_pos.forward())] = "v_conn"
                queue.append((cur_pos.forward().forward(), forward_room))
            if str(cur_pos.back()) not in map_dict and back_room is not None:
                map_dict[str(cur_pos.back())] = "v_conn"
                queue.append((cur_pos.back().back(), back_room))
            if str(cur_pos.right()) not in map_dict and right_room is not None:
                map_dict[str(cur_pos.right())] = "h_conn"
                queue.append((cur_pos.right().right(), right_room))
            if str(cur_pos.left()) not in map_dict and left_room is not None:
                map_dict[str(cur_pos.left())] = "h_conn"
                queue.append((cur_pos.left().left(), left_room))

        # =====================================================================
        # Turn map dictionary into a 2d array that represents the map
        # TODO: I hate using strings here, look into python "enums"
        # 
        # E.g. 
        # [
        #   ["empty", "empty", "room", "empty", "empty"],
        #   ["room", "connector", "room", "connector", "room"],
        #   ["empty", "empty", "room", "empty", "connector"],
        #   ["empty", "empty", "room", "empty", "room"],
        #   ["empty", "empty", "room", "empty", "empty"],`
        #   ["empty", "empty", "room", "connector", "room"]
        # ]
        # =====================================================================
        map_array = []

        # Get the height and width of the map by finding the mininum and
        # maximum x and y value
        # Why do we do this? We're going to index into an array. Array indices
        # can't be negative.
        # TODO: This generally feels gross but I don't know why?
        min_x = math.inf
        max_x = -math.inf
        min_y = math.inf
        max_y = -math.inf
        for key in map_dict.keys():
            position = Position.from_string(key)
            if position.x > max_x:
                max_x = position.x
            if position.x < min_x:
                min_x = position.x
            if position.y > max_y:
                max_y = position.y
            if position.y < min_y:
                min_y = position.y
        height = (max_y - min_y) + 1 # Off by one, I am dumb
        width = (max_x - min_x) + 1

        print(f"Height: {height}, Width: {width}")

        for y in range(0, height):
            map_array.append([])
            for x in range(0, width):
                map_array[y].append("empty")

        # Assign dict values to the array
        for key, value in map_dict.items():
            position = Position.from_string(key)
            non_negative_x = position.x - min_x
            # Subtract from "max_y" otherwise the array will appear "upside down"
            non_negative_y = max_y - (position.y - min_y)
            map_array[non_negative_y][non_negative_x] = value
            if position.x == 0 and position.y == 0:
                self.player_location = Position(non_negative_x, non_negative_y)
        
        self.map_array = map_array
