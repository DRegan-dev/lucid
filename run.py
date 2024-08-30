# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
class Room:
    def __init__(self, name, description, items=None, exits=None):
        self.name = name
        self.description = description
        self.items = items or []
        self.exits = exits or {}

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item.name != item_name]

    def add_item(self, item):
        self.items.append(item)

    def get_exit(self, direction):
        return self.exits.get(direction)

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.inventory = []

    def move_to(self, room_name):
        self.current_room = room_name

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def has_item(self, item_name):
        return any(item.name == item_name for item in self.inventory)

    
def command_handling(command, player, rooms):
    words = command.split()
    action = words[0] if words else ""

    current_room = rooms[player.current_room]
    if player.current_room == "Bedroom":
        if action in ["go", "move"]:
            if len(words) < 2:
                print("You need to specify a direction.")
                return 
            direction = words[1]

            if direction == "north":
                print("You approach the large balance scale. There are stacks of cash weighing down one side. It seems symbolic. Weighing decisions you have made and will make...")
            elif direction == "south":
                print("You move toward the desk with a mirror and a picture frame on top of it")
            elif direction == "east":
            next_room = current_room.get_exit(direction)
            if next_room and next_room in rooms:
                player.move_to(next_room)
                print(f"You move {direction}.")
            else:
                print("You can't go that way")
        elif action == "look":
            print(f"You are in {rooms[player.current_room].description}") 
        elif action == "take":
            item_name = " ".join(words[1:])
            current_room = rooms[player.current_room]
            item = next((item for item in current_room.items if item.name.lower() == item_name.lower()), None)
            if item:
                player.add_to_inventory(item)
                current_room.remove_item(item_name)
                print(f"You take the {item_name}.")
            else: 
                print("Your inventory is empty")
        else:
            print("Unknown command.")

    elif player.current_room == "Office":
        if action in ["go", "move"]:
            if len(words) < 2:
                print("You need to specify a direction.")
                return
            direction = words[1]

            if direction == "east":
                print("You move towards the desk, where the computer screen flickers and the phone rings loudly")
            elif direction == "west":
                next_room = current_room.get_exit(direction)
                if next_room and next_room in rooms:
                    player.move_to(next_room)
                    print(f"You move{direction}.")
                else:
                    print("You can;t go that way")
            else:
                print("There's nothing in that direction of interest")

    elif player.current_room == "Garden":
        if action in ["go", "move"]:
            if len(words) < 2:
                print("You need to specify a direction.")
                return
            direction = words[1]

            if direction == "north":
                print("You move towards your child, who sits behind a group of parents and children singing Happy Birthday.")
            elif direction == "east":
                print("You appraoch a vacant picnic table, empty plates and cups tell of a party that has just ended. You see a knife.")
            else:
                print("Theres nothing in that direction of interest")

    elif player.current_room == "Hallway":
        if action in ["go", "move"]:
            if len(words) < 2:
                print("You need to specify a direction.")
                return
            direction = words[1]


            if direction == "down":
                print("You look down at your feet and see a drawing your child has done")
            elif direction == "east":
                next_room = current_room.get_exit(direction)
                if next_room and next_room in rooms:
                    player.move_to(next_room)
                    print(f"You move {direction}.")
                else:
                    print("You can;t go that way")
            else:
                print("Theres nothing of interest in that direction")

    if not words:
        print("You must enter a command.")
        return

    action = words[0].lower()

    if action in ["go", "move"]:
        direction = words[1].lower() if len(words) > 1 else None
        move_player(direction, player, rooms)

    elif action == "look":
        look_around(player, rooms)

    elif action == "take":
        item_name= " ".join(words[1:])
        take_item(item_name, player, rooms)

    elif action == "inventory":
        show_inventory(player)

    else:
        print("Unknown Command.") 

def move_player(direction, player, rooms):
    current_room = rooms[player.current_room]
    next_room = current_room.get_exit(direction)

    if next_room:
        player.move_to(next_room)
        print(f"You move {direction}.")
    else:
        print("You can't go that way")

def look_around(player, rooms):
    current_room = rooms[player.current_room]
    print(f"You are in (current_room.name).")
    if current_room.items:
        print("You see:")
        for item in current_room.items:
            print(f" - {item.name}: {item.description}")

def take_item(item_name, player, rooms):
    current_room = rooms[player.current_room]
    item = next((item for item in current_room.items if item.name.lower() == item_name.lower()), None)

    if item:
        player.add_to_inventory(item)
        current_room.remove_item(item_name)
        print(f"You take the {item_name}")
    else: 
        print(f"There is no such item here")

def show_inventory(player):
    if player.inventory:
        print(f"You are carrying:")
        for item in player.inventory:
            print(f" - {item.name}: {item.description}")
    else:
        print("You are not carrying anything")

def setup_game():
    # Defines Rooms
    bedroom = Room("Bedroom", "A dimly lit room with shadows in every corner", exits={"east": "Office"})
    office = Room("Office", "A desk, a chair, a computer screen and paper suspended in mid air. Windows top to bottom", exits={"west": "Bedroom", "south": "Garden"})
    backgarden = Room("Garden", "Bright sunny garden, childs birthday party", exits={"north": "Office", "west": "Hallway"})
    hallway = Room("Hallway", "Long Hallway with a door at either end, one take you back to the beginning. The other takes you to the end", exits={"west": "Bedroom", "east": "Hospital room"})
    
    # Add items to rooms
    bedroom.add_item(Item("Mirror", "A small rectangular mirror."))
    bedroom.add_item(Item("Picture Frame", "A picture frame containing a picture of your family, a beloved memory they hold dear, and yet, you are absent from it"))

    office.add_item(Item("Phone", "A ringing phone, your kid is trying to call you"))
    office.add_item(Item("Origami Key", "A piece of paper folded in the shape of a key. Written on its surface it says: 'To move forward you must journey within"))

    backgarden.add_item(Item("Knife", "A sharp steel knife, perfect for cutting a cake and other things..."))

    hallway.add_item(Item("Your child's drawing", "A drawing your kid made for you, they are waving goodbye as you leave for work. You were too focused on getting to your job on time, you didn't see them wave"))

    # Defines Player
    player = Player("Hero", "Bedroom") 

    # Dictionary of rooms
    rooms = {
        "Bedroom": bedroom,
        "Office": office,
        "Garden": backgarden,
        "Hallway": hallway
    }

    return rooms, player

def main():
    rooms, player = setup_game()

    print("Welcome to Lucid")
    print("To start the game, type 'begin'")

    start_command = input().strip().lower()
    while start_command != "begin":
        print("To start the game, type 'begin'")
        start_command = input().strip().lower()

    while True:
        current_room = rooms[player.current_room]
        print(f"\n{current_room.description}")

        if player.current_room == "Bedroom":
            print("To the north, you see a large balance scale")
            print("To the south, there is a desk with two picture frames, each holding a cherished memory.")
            print("To the east, the door leads out of the room")
        elif player.current_room == "Office":
            print("The office is chaos in suspended animation. Papers are thrown everywhere trapped in mid flight. Ouside the window a swirling hurricane carries faint voices on its forceful wind.")
            print("To the east, there is a desk with a computer and a ringing phone")
            print("To the west, a door will take you where you need to go")
        elif player.current_room == "Garden":
            print("The heat from the sun finds your skin, in the distance you can hear children singing happy birthday to your kid")
            print("To the north, your kid sits behind a group of parents and their children singing Happy Birthday.")
            print("To the east, a vacant picnic table")
        elif player.current_room == "Hallway":
            print("The hallway seems to stretch infinitely, the doors on either end promising both hope and despair")
            print("You look down at your feet as you enter the hallway. A picture that your child has drawn.")

        if current_room.name != "Bedroom":
            exits = current_room.exits
            items = current_room.items

            if exits:
                print("\nFrom here, you can go:")
                for direction, room_name in exits.items():
                    print(f"- {direction.title()} to the {room_name}")
            else:
                print("\nThere are no obvious exits from this room.")

            if items:
                print(f"\nIn this room, you see:")
                for item in items:
                    print(f"- {item.name}: {item.description}")
            else:
                print("\nThere are no items in this room.")

        command = input("> ").strip().lower()
        if command.lower() in ["quit", "exit"]:
            print("Thanks for playing!")
            break

        command_handling(command, player, rooms)

if __name__ == "__main__":
    main()