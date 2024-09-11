# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Class representing a room in the game
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


# Class representing an item in the game
class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

# Class representing a player in the game
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
    
    def show_inventory(self):
        if self.inventory:
            print(f"You are carrying: ")
            for i, item in enumerate(self.inventory, 1):
                print(f"{i}. {item.name}: {item.description}")
        else:
            print("You are not carrying anything")

def show_available_directions(player, rooms):
    current_room = rooms[player.current_room]
    exits = current_room.exits

    if exits:
        print("\nYou can go: ")
        for direction, room_name in exits.items():
            print(f"- {direction.capitalize()}: {room_name}")
    else:
        print("\nThere are no obvious exits from this room.")

def handle_item_interaction(player, room):
    for item in room.items:
        while True:
            item_action = input(f"Type 'take' to pick up the {item.name}, or 'leave' to leave it: ").strip().lower()
            if item_action == "take":
                player.add_to_inventory(item)
                room.remove_item(item.name)
                print(f"You take the {item.name}.")
                if item.name.lower() == "origami key" and room.name == "Office":
                    room.exits["west"] = "Garden"
                    print("Type 'go west' to use the key to unlock the exit and move on.")
                elif item.name.lower() == "picture frame" and room.name == "Bedroom":
                    room.exits["east"] = "Office"
                    print("The picture brings the scale into balance and you hear a claick as the door to the east unlocks.")

                break
            elif item_action == "leave":
                print(f"You leave the {item.name}.")

def handle_bedroom(player, rooms, direction):
    current_room = rooms[player.current_room]

    if direction == "north":
        print("You approach the large balance scale. There are stacks of cash weighing down one side. It seems symbolic. Weighing decisions you have made and will make...")
        
        while True:
            if not player.inventory:
                print("You have nothing in your inventory to balance it out")
                break
        
            player.show_inventory()
            item_choice = input("Enter the number of the item you want to use: ").strip()

            if item_choice.isdigit():
                item_index = int(item_choice) - 1
                if 0 <= item_index < len(player.inventory):
                    item_used = use_item_from_inventory(player.inventory[item_index], player, rooms)
                    if item_used:
                        if player.inventory[item_index].name.lower() == "picture frame":
                            current_room.exits["east"] = "Office"
                            print("The picture brings the scale into balance and you hear a click as the door to the east unlocks.")
                        break
                else:
                    print("Invalid Choice")
            else:
                print("Invalid input.")

    elif direction == 'south':
        print("You move toward the desk with a mirror and a picture frame on top of it")
        handle_item_interaction(player, rooms[player.current_room])
    elif direction == 'east':
        if "east" in current_room.exits:
            next_room = rooms[player.current_room].get_exit(direction)
            if next_room:
                player.move_to(next_room)
                print("You move east")
            
        else:
            print("The door to the east is locked You need to find a way to unlock it.")
            

    show_available_directions(player, rooms)

def handle_office(player, rooms, direction):

    if direction == "east":
        print("You move towards the desk, where the computer flickers and the phone rings loudly")
        handle_item_interaction(player, rooms[player.current_room])

    elif direction == "west":
        next_room = rooms[player.current_room].get_exit(direction)
        if next_room:
            player.move_to(next_room)
            print("You move west.")
        else:
            print("The door to the west is locked. You must find the key to unlock it")

    show_available_directions(player, rooms)

def handle_garden(player, rooms, direction):
    current_room = rooms[player.current_room]

    if direction == "north":
        if player.has_item("knife"):
            next_room = current_room.get_exit(direction)
            if next_room:
                print("You use the knife to cut through the 2d picture and exit the party")
                player.move_to(next_room)
        else:
            print("You move towards your child, who sits behind a group of parents and children singing Happy Birthday. You cannot reach them. Maybe its too late...")

    elif direction == "east":
        print("You approach a vacant picnic table, empty plates and cups tell of a party that has just ended. You see a knife")
        handle_item_interaction(player, current_room)
        
        if player.has_item("knife") and "north" not in current_room.exits:
            current_room.exits["north"] = "Hallway"
            print("Its a jungle out there")
            print("As you pick up the knife, the singing stops. You turn to find out why and see the party scene you had just been immersed in has turned into a 2d picture on paper.")
            print("Type 'go north' to use the knife to cut through the picture and exit the party.")
            
    else:
        print("Invalid direction. Try again.")
    

    show_available_directions(player, rooms)

def handle_hallway(player, rooms, direction):
    

    if direction == "down":
        print("You look down at your feet and see a drawing you child has done.")
        for item in rooms[player.current_room].items:
            item_action = input(f"Type 'take' to pick up the {item.name}").strip().lower()
            if item_action == "take":
                player.add_to_inventory(item)
                rooms[player.current_room].remove_item(item.name)
                print(f"You take the {item.name}.")
                print(f"{item.description}")
                print("You must now make the ultimate decision")
    elif direction in ["east", "west"]:
        next_room = rooms[player.current_room].get_exit(direction)
        if next_room:
            player.move_to(next_room)
            print(f"You move {direction}")
            if direction == "west":
                print(end_of_game_sequence())
            elif direction == "east":
                restart_game()
                return
    else:
        print("Invalid direction. Try again.")


    show_available_directions(player, rooms)

def command_handling(command, player, rooms):

    words = command.split()
    if not words:
        print("You must enter a command.")
        return

    action = words[0].lower()
    direction = words[1].lower() if len(words) > 1 else None

    if action in ["go", "move"]:
        if not direction:
            print("You need to specify a direction")
            return

    current_room = rooms[player.current_room]

    if player.current_room == "Bedroom":
        handle_bedroom(player, rooms, direction)
    elif player.current_room == "Office":
        handle_office(player, rooms, direction)
    elif player.current_room == "Garden":
        handle_garden(player, rooms, direction)
    elif player.current_room == "Hallway":
        handle_hallway(player, rooms, direction)
    else:
        print("Unknown room.")
    
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

def show_inventory(player, rooms):
    if player.inventory:
        print(f"You are carrying:")
        for i, item in enumerate(player.inventory, 1):
            print(f"{i}. {item.name}: {item.description}")

            use_item = input("Would you like to you an item? (yes/no) ").strip().lower()
            if use_item == "yes":
                item_choice = input("Enter the number of the item you want to use: ").strip()
                if item_choice.isdigit():
                    item_index = int(item_choice) - 1
                    if 0 <= item_index < len(player.inventory):
                        use_item_from_inventory(player.inventory[item_index], player, rooms)
                    else:
                        print("Invalid choice.")
                else:
                    print("Invalid input")
            else:
                print("You choose not to use any item.")
    else:
        print("You are not carrying anything")

def use_item_from_inventory(item, player, rooms):
    current_room = rooms[player.current_room]

    if item.name.lower() == "mirror":
        print("You use the mirror. It reflects the only thing that you've ever truly been interested in... Yourself. It does not bring the scales into balance.")
        return False
    elif item.name.lower() == "picture frame":
        print("You use the picture frame. Portrait of a happy family that you never prioritized")
        if player.current_room == "Bedroom":
            current_room.exits["east"] = "Office"
            print("The picture brings the scale into balance and you hear a click as the door to the east unlocks")
            print ("Type 'go east' to exit the room")
        return True
    elif item.name.lower() == "phone":
        print("You answer the phone. Its your child asking when you'll be home")
        return False
    elif item.name.lower() == "origami key":
        print("You use the origami key.")
        if player.current_room == "Office":
            current_room.exits["west"] = "Garden"
            print("Type 'go west' tp exit the room.")
        return True
    elif item.name.lower() == "knife":
        print("You carefully handle the knife and cut a door shaped hole in the picture")
        if player.current_room == "Garden":
            current_room.exits["north"] = "Hallway"
            print("You use the knife to cut through the 2d picture, revealing an exit.")
            print("Type 'go north' to exit the garden.")
        return True
    else:
        print(f"The {item.name} doesn't seem to have any immediate use")
        return False

def setup_game():
    # Defines Rooms
    bedroom = Room("Bedroom", "A dimly lit room with shadows in every corner", exits={})
    office = Room("Office", "A desk, a chair, a computer screen and paper suspended in mid air. Windows top to bottom", exits={})
    backgarden = Room("Garden", "Bright sunny garden, childs birthday party", exits={})
    hallway = Room("Hallway", "Long Hallway with a door at either end, one take you back to the beginning. The other takes you to the end", exits={"west": "Bedroom", "east": "Hospital room"})
    
    # Add items to rooms
    bedroom.add_item(Item("Mirror", "A small rectangular mirror."))
    bedroom.add_item(Item("Picture Frame", "A picture frame containing a picture of your family, a beloved memory they hold dear, and yet, you are absent from it"))

    office.add_item(Item("Phone", "A ringing phone, your kid is trying to call you"))
    office.add_item(Item("Origami Key", "A piece of paper folded in the shape of a key. Written on its surface it says: 'To move forward you must journey within"))

    backgarden.add_item(Item("Knife", "A sharp steel knife, perfect for cutting a cake and other things..."))

    hallway.add_item(Item("Drawing", "A drawing your kid made for you, they are waving goodbye as you leave for work. You were too focused on getting to your job on time, you didn't see them wave"))

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
    print("To start the game, type 'Begin'")

    start_command = input().strip().lower()
    while start_command != "begin":
        print("To start the game, type 'begin'")
        start_command = input().strip().lower()

    print_current_room_description(player, rooms)

    while True:
        command = input("> ").strip().lower()
        if command in ["quit", "exit"]:
            print("Thanks for playing")
            break

        current_room_before = player.current_room

        command_handling(command, player, rooms)
        print_current_room_description(player, rooms)

def print_current_room_description(player, rooms):
    current_room = rooms[player.current_room]
    print(f"\n{current_room.description}")

    if player.current_room == "Bedroom":
        print("To the north, you see a large balance scale")
        print("To the south, there is a desk with a mirror and a picture frame")
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


if __name__ == "__main__":
    main()