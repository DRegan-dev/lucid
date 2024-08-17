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
        self.items = [items for item in self.items if item.name != item_name]

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
        self.inventory.appenf(item)

    

    

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

    garden.add_item(Item("Knife", "A sharp steel knife, perfect for cutting a cake and other things..."))

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

