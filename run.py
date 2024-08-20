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

    if not words:
        print("You must enter a command.")
        return

    action = words[0].lower()

    if action in ["go", "move"]:
        direction = words[1].lower() if len(words > 1 else None)
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

def setup_game():
    # Defines Rooms
    bedroom = Room("Bedroom", "A dimly lit room with shadows in every corner", exits={"east": "office"})
    office = Room("Office", "A desk, a chair, a computer screen and paper suspended in mid air. Windows top to bottom", exits={"west": "Bedroom", "south": "Backgarden"})
    backgarden = Room("Garden", "Bright sunny garden, childs birthday party", exits={"north": "Office", "west": "hallway"})
    hallway = Room("Long Hallway, with a door at either end, one take you back to the beginning. The other takes you to the end", exits={"west": "Bedroom", "east": "Hospital room"})
    
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
        "Garden": garden,
        "Hallway": hallway
    }

    return rooms, player

def main():
    rooms, player = setup_game()

    print("Welcome to Lucid")

    while True:
        current_room = rooms[player.current_room]
        print(f"\n{current_room.description}")

        command = input("> ")
        if command.lower() in ["quit", "exit"]:
            print("Thanks for playing!")
            break

        command_handling(command, player, rooms)

if __name__ == "__main__":
    main()