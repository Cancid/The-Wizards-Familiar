def input_request(player, map):
    choice = input('> ')
    # seperates user input at any space, returns list
    command = choice.split(' ')[0]
    return process_input(player, map, command)

def process_input(player, map, command):

    try:
        object: Optional[str] = choice.split(' ')[1]
    # if an Index Error (aka no object returned) set object to none
    except IndexError:
        # if no second in list, set object to None
        object = None
    if command in ('f', 'forward', 'l', 'left', 'r', 'right', 'b', 'back',
                    'u', 'up', 'd', 'down'):
        return player.move(command, map)

    elif command in ('i', 'interact') or object in player.location.interactables.keys() or object in player.inventory:
        # TODO: make inputs like 'piano' work
        player.interact(command, object)
        return True


    elif command in ('desc', 'description'):
        print(player.location.description)
        player.no_desc = True
        return True
    elif command in ('h', 'help'):
        print('This is a list of commands.')
        return True
    elif command in ('inv'):
        print(player.inventory)
        return True

    else:
        print("Please enter a valid resposne.")
        return True

