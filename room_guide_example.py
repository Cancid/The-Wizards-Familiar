
    room_guide = [
        foyer,
        failure,
        hallway,
        kitchen,
        master_bedroom,
    ]

    def __init__(self, room: Room):
        self.room = room

    def next_room(self, room_name):
        new_room = self.room_guide[room_name]
        return new_room

a_map = RoomGuide(0)
a_player = Player(a_map.next_room(a_map.room), [], [], False)
a_game = Engine(a_map, a_player)
a_game.start()
