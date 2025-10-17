# John M Brimhall 2025 Game Project for IT-140
# Version 2, including dictionaries.

#Imports
import os
from random import randint
from time import sleep

# Core Variables
game_state = 1 # Keeps central loops running. 0 = quit, 2 = win.
timeout = 0
player_inventory = [] # Storage for items.
sleep_timer = 1 # Dictates the duration to pause before printing the next message. (Alterable in the settings)
current_room = 'Entrance' # Current player location
previous_room = 'Entrance' # Cache for the players previous room. Used for fleeing battles.
room_map = [
        ['     ','*****','*****'], # 0 Y
        ['     ','*   -','-   *'], # 1
        ['     ','**|**','*****'], # 2
        ['     ','  |  ','*****'], # 3
        ['     ','  |  ','*   *'], # 4
        ['     ','  |  ','**|**'], # 5
        ['*****','**|**','**|**'], # 6
        ['*   -','-   -','-   *'], # 7
        ['*****','**|**','*****'], # 8
        ['     ','**|**','*****'], # 9
        ['     ','*   -','-   *'], # 10
        ['     ','*****','*****'] # 11
    ] #     0       1       2    X    (For the map command)
room_checks = {
    'Index': {
        'Entrance': {'X': 0, 'Y': 7},
        'Foyer': {'X': 1, 'Y': 7},
        'Ominous Room': {'X': 1, 'Y': 1},
        'Boss Room': {'X': 2, 'Y': 1},
        'Ravaged Room': {'X': 2, 'Y': 7},
        'Sunlit Room': {'X': 2, 'Y': 4},
        'A Putrid Smell': {'X': 1, 'Y': 10},
        'Horrid Stench': {'X': 2, 'Y': 10},
        'Secret Room': {'X': 0, 'Y': 10},
        'Garden': {'X': 0, 'Y': 4}
    },
    'Been Searched': {
        'Entrance': False,
        'Foyer': False,
        'Ominous Room': False,
        'Boss Room': False,
        'Ravaged Room': False,
        'Sunlit Room': False,
        'A Putrid Smell': False,
        'Horrid Stench': False,
        'Secret Room': False,
        'Garden': False
        }
    } # Data to be read for the search command. Houses room coordinates related to room_map
player_stats = {
    'Name': 'Ghatte',
    'Health': 50,
    'Damage': 3,
    'Description': 'Mercenary on a job to slay the beast residing in this building.'
} # Player data.
room_nav = {
    'Entrance': {  # room 1
        'Directions': {
            'East': 'Foyer'
        },
        'Movement': {
            'East': 'You entered the ravaged building.',
            'North': 'You stepped into the trampled garden.'
        },
        "Description": {
            "Basic": "You're at the Entrance to the building. The door is torn off.\n"
                     "There are scratch marks all over the structure. There must be creatures within.",
            "Search": "The woods around you feel more welcoming than the building.\n"
                      "A torn up doorway lies to your east.\n"
					  "But there appears the be an opening in the brush.\n"
        },
        "ID": 1,
        "Interact": False,
        "Enemy": False,
        "Item": "none",
		"Searched": False
    },
    'Foyer': {  # room 2
        'Directions': {
            'North': 'Ominous Room',
            'East': 'Ravaged Room',
            'South': 'A Putrid Smell',
            'West': 'Entrance'
        },
        'Movement': {
            'North': 'You entered an ominous room. A large door to your East.',
            'East': 'You entered another torn up room.',
            'South': 'You followed a stench into the next room.',
            'West': 'You stepped outside for some air.'
        },
        "Description": {
            "Basic": "You're in the central room of the building.\n"
                     "Scratch marks and debris litter the floors and walls.",
            "InteractTrue": "You notice a glint out of the corner of your eye.",
            "InteractFalse": "There's nothing in here but a mess.",
            "Search": "Before you lies three open passages. Scratch marks and debris litter the area.\n"
                      "There appears to be a bottle in the debris.\n",
            "Searched": "Before you lies three open passages. Scratch marks and debris litter the area.\n"
                        "The only thing left here is a mess.\n"
        },
        "ID": 2,
        "Interact": True,
        "Enemy": True,
        "EnemyStats": {
            "Name": "Wild Beast",
            "Description": "A small beast, feral and angry.",
            "MoreDesc": "This creature took up residence in this building after the Grand Beast scared off the owners.",
            "Health": 6,
            "Damage": 3,
            "Picture": """                        ,     ,\n                        |\---/|\n                       /  , , |\n                  __.-'|  / \ /\n         __ ___.-'        ._O|\n      .-'  '        :      _/\n     / ,    .        .     |\n    :  ;    :        :   _/\n    |  |   .'     __:   /\n    |  :   /'----'| \  |\n    \  |\  |      | /| |\n     '.'| /       || \ |\n     | /|.'       '.l \\_\n     || ||             '-'\n     '-''-'"""
        },
        "Item": "Potion"
    },
    'Ominous Room': {  # room 3
        'Directions': {
            'East': 'Boss Room',
            'South': 'Foyer'
        },
        'Movement': {
            'East': 'You re-entered the Beasts den.',
            'South': 'You re-entered the central room.'
        },
        "Description": {
            "Basic": "The claw marks are very large in this room.\n"
                     "This must be the way towards the beast you're here for.",
            "InteractTrue": "There is a locked door to your East.",
            "InteractFalse": "The doorway into the beasts den is to your East.",
            "HasKey": "You have the key for the door.",
            "NoKey": "You should go and look for the key. It must be nearby.",
            "Search": "You hear scratching and growling in the next room...\n"
                      "A large locked door blocks your path.\n",
            "Searched": "You hear scratching and growling in the next room...\n"
                        "The wide open door beckons you.\n"
        },
        "ID": 3,
        "Interact": True,
        "Enemy": False,
        "Item": "none"
    },
    'Boss Room': {  # room 4
        'Directions': {
            'East': 'Ominous Room'
        },
        'Movement': {
            'East': 'You left the Beasts lair.'
        },
        "Description": {
            "BossDead": "It appears the Beast has been killed.\n"
                        "It was crushed by a ceiling chandelier..."
        },
        "ID": 4,
        "Interact": False,
        "Enemy": True,
        "EnemyStats": {
            "Name": "Grand Beast",
            "Description": "A large, ferocious beast. The one you're here for.",
            "MoreDesc": "The beast that scared off the owners. It's been terrorizing the nearby townspeople.",
            "Health": 30,
            "Damage": 9,
            "Picture": """      /^\      /^\ \n      |  \    /  |\n      ||\ \../ /||\n      )'        `(\n     ,;`w,    ,w';,\n     ;,  ) __ (  ,;\n      ;  \(\/)/  ;;\n     ;|  |vwwv|    ``-...\n      ;  `lwwl'   ;      ```''-.\n     ;| ; `""' ; ;              `.\n      ;         ,   ,          , |\n      '  ;      ;   l    .     | |\n      ;    ,  ,    |,-,._|      \;\n       ;  ; `' ;   '    \ `\     \;\n       |  |    |  |     |   |    |;\n       |  ;    ;  |      \   \   (;\n       | |      | l       | | \  |\n       | |      | |       | |  ) |\n       | |      | ;       | |  | |\n       ; ,      : ,      ,_.'  | |\n      :__'      | |           ,_.'\n               `--'"""
        },
        "Item": "none"
    },
    'Ravaged Room': {  # room 5
        'Directions': {
            'North': 'Sunlit Room',
            'West': 'Foyer'
        },
        'Movement': {
            'North': "You're blinding by the beams of light shining through the roof.",
            'West': 'You re-entered the central room.'
        },
        "Description": {
            "Basic": "There are debris and scratch marks all over the room.\n"
                     "You see light shining through the next room.",
            "Search": "There's a lever under some debris. Maybe you should pull it.\n",
            "Searched": "Just rubble and scratch marks...\n"
        },
        "ID": 5,
        "Interact": True,
        "Enemy": True,
        "EnemyStats": {
            "Name": "Wild Beast",
            "Description": "A small beast, feral and angry.",
            "MoreDesc": "This creature took up residence in this building after the Grand Beast scared off the owners.",
            "Health": 6,
            "Damage": 3,
            "Picture": """                        ,     ,\n                        |\---/|\n                       /  , , |\n                  __.-'|  / \ /\n         __ ___.-'        ._O|\n      .-'  '        :      _/\n     / ,    .        .     |\n    :  ;    :        :   _/\n    |  |   .'     __:   /\n    |  :   /'----'| \  |\n    \  |\  |      | /| |\n     '.'| /       || \ |\n     | /|.'       '.l \\_\n     || ||             '-'\n     '-''-'"""
        },
        "Item": "none"
    },
    'Sunlit Room': {  # room 6
        'Directions': {
            'South': 'Ravaged Room'
        },
        'Movement': {
            'South': 'You left the glimmering sunlight, into the torn up room.'
        },
        "Description": {
            "Basic": "There is sunlight gleaming down through the ceiling.\n"
                     "The room is in shambles, and the ceiling has caved in.",
            "Search": "The warm sunlight feels nice.\n"
                      "Theres something glimmering in the rubble.\n",
            "Searched": "The warm sunlight feels nice.\n"
        },
        "ID": 6,
        "Interact": True,
        "Enemy": False,
        "Item": "Key"
    },
    'A Putrid Smell': {  # room 7
        'Directions': {
            'North': 'Foyer',
            'East': 'Horrid Stench'
        },
        'Movement': {
            'North': 'You re-entered the central room.',
            'East': 'Scrunching your nose, you walk into a wave of odor.',
            'West': 'You entered a damp, untouched room.'
        },
        "Description": {
            "Basic": "A foul stench emanates from this direction.\n"
                     "A couple of dead adventurers lay near the doorway. They must have been attacked.\n"
                     "Amongst the fetid stench, you catch a musty smell.",
            "Search": "There's a bottle of oil on this adventurers corpse. Could be useful...\n",
            "Searched": "Nothing left but that smell...\n",
            "Secret": "The wall to the West looks unusual...\n",
            "Open": "A secret passage is open on the West wall.\n"
        },
        "ID": 7,
        "Interact": True,
        "Enemy": False,
        "Item": "Oil"
    },
    'Horrid Stench': {  # room 8
        'Directions': {
            'West': 'A Putrid Smell'
        },
        'Movement': {
            'West': 'You stepped away from the stench of decay.'
        },
        "Description": {
            "Basic": "This is where the stench is coming from.\n"
                     "The room is littered in various animal carcases. This must be where they eat.",
            "InteractTrue": "Could be worth looking around...",
            "InteractFalse": "Nothing here but death and decay.",
            "Search": "There's a potion under the carcases. Could be useful.\n",
            "Searched": "Just a mess of carcases...\n"
        },
        "ID": 8,
        "Interact": True,
        "Enemy": True,
        "EnemyStats": {
            "Name": "Large Beast",
            "Description": "Larger than the others. Angrier...",
            "MoreDesc": "This one must be very well fed. It's large and ferocious.",
            "Health": 12,
            "Damage": 6,
            "Picture": """                        ,     ,\n                        |\---/|\n                       /  , , |\n                  __.-'|  / \ /\n         __ ___.-'        ._O|\n      .-'  '        :      _/\n     / ,    .        .     |\n    :  ;    :        :   _/\n    |  |   .'     __:   /\n    |  :   /'----'| \  |\n    \  |\  |      | /| |\n     '.'| /       || \ |\n     | /|.'       '.l \\_\n     || ||             '-'\n     '-''-'"""
        },
        "Item": "Potion"
    },
    'Secret Room': {  # room 9, Room 7's list will be updated when this room gets unlocked.
        'Directions': {
            'East': 'A Putrid Smell'
        },
        'Movement': {
            'East': 'You left the damp hidden room.'
        },
        "Description": {
            "Basic": "This room appears untouched by the beasts dwelling within the building.\n"
                     "Water is dripping in from a crack in the ceiling.\n"
                     "A musty smell emanates from here.",
            "Search": "Cobwebs, dust, mold. And a lever.\n",
            "Searched": "Cobwebs, dust, mold. And the lever.\n"
        },
        "ID": 9,
        "Interact": True,
        "Enemy": False,
        "Item": "none"
    },
    'Garden': {  # room 10
        'Directions': {
            'South': 'Entrance'
        },
        'Movement': {
            'South': 'You return to the main entrance.'
        },
        "Description": {
            "Basic": "A trampled garden lays here.\n"
                     "The beasts left nothing untouched.",
            "InteractTrue": "Perhaps I should look around.",
            "InteractFalse": "Nothing in here but trampled plants",
            "Search": "Even in its current state, the garden still feels serene.\n"
                      "There's a vial of oil partially buried in the dirt.\n"
        },
        "ID": 10,
        "Interact": True,
        "Enemy": True,
        "EnemyStats": {
            "Name": "Injured Beast",
            "Description": "A frail creature.",
            "Health": 4,
            "Damage": 1
        },
        "Item": "Oil"
    },
} # The map itself. And all relevant data for each room.
valid_inputs = {
    'North': {
        'north', 'n', 'up'
    },
    'East': {
        'east', 'e', 'Right'
    },
    'South': {
        'south', 's', 'down'
    },
    'West': {
        'west', 'w', 'left'
    },
    'Search': {
        'search', 'look', 'examine'
    },
    'Inventory': {
        'inventory', 'backpack', 'item', 'items'
    },
    'Pickup': {
        'pickup', 'grab', 'yoink', 'pull', 'pull the lever kronk'
    },
    'Attack': {
        'attack', 'fight', 'kill', 'hit'
    },
    'Run': {
        'flee', 'run', 'escape'
    },
    'Heal': {
        'heal', 'healing', 'recover', 'potion'
    },
    'Close': {
        'close', 'exit', 'back'
    },
    'Settings': {
        'settings', 'options', 'option'
    },
    'Check': {
        'check', 'self', 'inquire'
    },
    'Map': {
        'map', 'maps'
    },
    'Help': {
        'help'
    }
} # Glossary of valid inputs.
# Definitions and core mechanics.

# Basic input information to be displayed.
# VALID MODULES "movement", "battle", "inventory", "help"
def show_info(screen):
    if game_state == 1:
        if sleep_timer > 0:
            sleeper = sleep_timer / 4
        else:
            sleeper = 0
        print('')
        if screen == 'movement':
            try:
                print('Directions: |', end='')
                if 'North' in room_nav[current_room]['Directions']:
                    print(" 'North' : " + room_nav[current_room]['Directions']['North'], end=' |')
                if 'East' in room_nav[current_room]['Directions']:
                    print(" 'East' : " + room_nav[current_room]['Directions']['East'], end=' |')
                if 'South' in room_nav[current_room]['Directions']:
                    print(" 'South' : " + room_nav[current_room]['Directions']['South'], end=' |')
                if 'West' in room_nav[current_room]['Directions']:
                    print(" 'West' : " + room_nav[current_room]['Directions']['West'], end=' |')
                print('')
                sleep(sleeper)
            except:
                pass
            print("Type 'go (direction) to move in that direction.")
            sleep(sleeper)
            print("Other options: Inventory, Search, Pickup, Check, Map, Settings")
            sleep(sleeper)
            print('')
            print("What do will you do?")
        elif screen == 'battle':
            print("Valid options: Attack, Heal, Flee")
            sleep(sleeper)
            print("Other Options: Inventory, Check, Settings")
            sleep(sleeper)
            print('')
        elif screen == 'inventory':
            print("Type the item number or name that you'd like to select.")
            print("Or type 'exit' to exit back to navigation.")
            print('')
        elif screen == 'help':
            print("When you see '?' in the bottom line, its expecting an input.")
            print("Directional inputs are North, East, South, West.")
            print("However alternatives are acceptable. ('N' or 'up' for North, etc.)")
            print("It can be difficult to visualize the space you're navigating. The map can help.")
            print("If the delays on text displays is annoying. Theres an option to change it in the settings.")
            print('')
        else:
            print("Invalid request. Check the caller.")

# Check for y/n yes or no.
def yes_no(user):
    if user == 'yes' or user == 'y':
        return True
    elif user == 'no' or user == 'n':
        return False
    else:
        return False

# This clears the screen to allow more text to show. (Thanks google.)
# This does not work in pycharm. But it works in windows command prompt runner.
def clear_console():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

# Runs to check if user input matches a list of possible inputs. Outputs via return if successful.
# Returns: 1 = north, 2 = east, 3 = south, 4 = west, 5 = examine, 6 = inventory, 7 = pickup, 8 = attack
# Returns: 9 = flee, 10 = heal, 11 = close, 12 = Settings, 13 = Check Self
def verify_input(user_input):
    global game_state
    global timeout
    user_input = user_input.lower()
    if 'go' in user_input or 'move' in user_input:
        user_input = user_input.replace('go ', '')
        user_input = user_input.replace('move ', '')
        if user_input in valid_inputs['North']:
            return 1
        elif user_input in valid_inputs['East']:
            return 2
        elif user_input in valid_inputs['South']:
            return 3
        elif user_input in valid_inputs['West']:
            return 4
        else: return 0
    elif user_input in valid_inputs['North']:
        return 1
    elif user_input in valid_inputs['East']:
        return 2
    elif user_input in valid_inputs['South']:
        return 3
    elif user_input in valid_inputs['West']:
        return 4
    elif user_input in valid_inputs['Search']:
        return 5
    elif user_input in valid_inputs['Inventory']:
        return 6
    elif user_input in valid_inputs['Pickup']:
        return 7
    elif user_input in valid_inputs['Attack']:
        return 8
    elif user_input in valid_inputs['Run']:
        return 9
    elif user_input in valid_inputs['Heal']:
        return 10
    elif user_input in valid_inputs['Close']:
        return 11
    elif user_input in valid_inputs['Settings']:
        return 12
    elif user_input in valid_inputs['Check']:
        return 13
    elif user_input in valid_inputs['Map']:
        return 14
    elif user_input in valid_inputs['Help']:
        return 15
    elif user_input == "woogi rules okay":
        return 99
    elif user_input == "quit":
        game_state = 0
        return 50
    else:
        return 0 # Tells the caller that the user input is invalid.
    # Most of these are self-explanatory.

# Tells the main loop what to say when you arrive in a new room.
def check_room():
    global current_room
    global room_map
    x = room_checks['Index'][current_room]['X']
    y = room_checks['Index'][current_room]['Y']
    x2 = room_checks['Index'][previous_room]['X']
    y2 = room_checks['Index'][previous_room]['Y']
    room_map[y][x] = room_map[y][x].replace('   ', ' @ ')
    room_map[y][x] = room_map[y][x].replace(' X ', ' @ ')
    if room_checks['Been Searched'][previous_room] and not current_room == previous_room:
        room_map[y2][x2] = room_map[y][x].replace(' @ ', ' X ')
    elif not room_checks['Been Searched'][previous_room] and not current_room == previous_room:
        room_map[y2][x2] = room_map[y][x].replace(' @ ', '   ')
    if game_state == 1:
        if current_room == "Secret Room" and not room_checks['Been Searched']['Secret Room']:
            room_map[9][0] = '+++++'
            room_map[10][0] = '+   -'
            room_map[11][0] = '+++++'
        elif current_room == "Garden" and not room_checks['Been Searched']['Garden']:
            room_map[3][0] = '+++++'
            room_map[4][0] = '+   +'
            room_map[5][0] = '++|++'
            room_map[6][0] = '**|**'

        if room_nav[current_room]['Enemy']:
            check_enemy()
        try:
            print(room_nav[current_room]['Description']['Basic'])
            sleep(sleep_timer)
        except:
            pass

# Function for pickup. Simplistic, maybe will make more interesting later.
def pickup_item():
    global player_inventory
    global room_nav
    if room_nav[current_room]['Interact'] and room_nav[current_room]['Item'] == "Potion":
        print("\nYou found a healing potion. Item added to inventory.\n")
        player_inventory.append("potion")
        room_nav[current_room]['Interact'] = False
        if current_room == 'Foyer':
            room_nav[current_room]['Description']['Search'] = "\nThe branching paths are laid out before you.\n"
        elif current_room == 'Horrid Stench':
            room_nav[current_room]['Description']['Search'] = "\nNothing remains but rotting flesh.\n"
        input("Press enter to continue...")
    elif current_room == "Ravaged Room" and room_nav["Ravaged Room"]['Interact']:
        print("\nYou found a hidden lever. You pulled it.")
        print("You heard a rumble from the other room...\n")
        room_nav['A Putrid Smell']['Secret'] = True
        room_nav['A Putrid Smell']['Directions']['West'] = "Secret Room"
        room_nav[current_room]['Interact'] = False
        room_nav['Ravaged Room']['Description']['Search'] = "\nNothing left here but rubble.\n"
        input("Press enter to continue...")
    elif room_nav[current_room]['Interact'] and room_nav[current_room]['Item'] == "Key":
        print("\nYou found the key to the bosses door.\n")
        player_inventory.append("key")
        room_nav[current_room]['Interact'] = False
        room_nav[current_room]['Description']['Search'] = "\nThe warm sunlight glistens into the wreckage below.\n"
        input("Press enter to continue...")
    elif room_nav[current_room]['Interact'] and room_nav[current_room]['Item'] == "Oil":
        print("\nYou found the beast oil. Item added to inventory.\n")
        player_inventory.append("oil")
        room_nav[current_room]['Interact'] = False
        if current_room == 'A Putrid Smell':
            room_nav[current_room]['Description']['Search'] = "\nThere's nothing of value left on the adventurers.\n"
        elif current_room == 'Garden':
            room_nav[current_room]['Description']['Search'] = "\nEven in its current state, the garden still feels serene.\n"
        input("Press enter to continue...")
    elif room_nav[current_room]['Interact'] and current_room == 'Secret Room':
        print("\nThere's another lever here. Pull it?")
        user_choice = input("y/n? ")
        if yes_no(user_choice):
            print("You pull the lever. You heard a loud crash in the other room...\n")
            room_nav[current_room]['Interact'] = False
            room_nav['Boss Room']['EnemyStats']['Health'] -= 10
            if int(room_nav['Boss Room']['EnemyStats']['Health']) <= 0:
                room_nav['Boss Room']['Enemy'] = False
            sleep(sleep_timer)
            room_nav[current_room]['Description']['Search'] = "\nOnly cobwebs and dust left to see here.\n"
            input("Press enter to continue...")
        if not user_choice:
            print("\nYou left the lever alone.\n")
            sleep(sleep_timer)
            input("Press enter to continue...")
    else:
        print("\nThere is nothing of interest here.\n")
        sleep(sleep_timer)
        input("Press enter to continue...")

# Calculates health related systems. From enemy health, player health, and healing.
# The primary runner of the backend for battles.
# VALID MOVEMENT MODULES "attack", "gethit", "heal"
def calc_damage(movement):
    randominteger = randint(1, 9)
    global player_stats
    global game_state
    global room_nav
    global player_inventory
    hitdamage = player_stats['Damage']
    enemyname = room_nav[current_room]['EnemyStats']['Name']
    if movement == 'attack':
        print('')
        if 7 < randominteger <= 9:
            hitdamage = player_stats['Damage'] * 2
            print("Critical hit!")

        room_nav[current_room]['EnemyStats']['Health'] -= hitdamage
        enemyhealth = int(room_nav[current_room]['EnemyStats']['Health'])
        if enemyhealth > 0:
            print("You attacked the", enemyname + ", Dealing", hitdamage, "damage.")
            sleep(sleep_timer)
            print("(The", enemyname ,"has", enemyhealth, "health remaining.)\n")
            sleep(sleep_timer)
        elif enemyhealth <= 0 and not current_room == "Boss Room":
            print("You attacked the", enemyname + ", Dealing", hitdamage, "damage.")
            sleep(sleep_timer)
            print("You've killed the", enemyname + ".\n")
            sleep(sleep_timer)
            room_nav[current_room]['Enemy'] = False
        elif enemyhealth <= 0 and current_room == "Boss Room":
            print("You attacked the", enemyname + ", Dealing", hitdamage, "damage.")
            sleep(sleep_timer)
            print("You've Slain the", enemyname + "!\n")
            game_state = 2
            sleep(sleep_timer)
    elif movement == 'gethit':
        enemydamage = int(room_nav[current_room]['EnemyStats']['Damage'])
        if 1 <= randominteger < 3: # Player only took partial damage.
            player_stats['Health'] -= enemydamage / 3
            print("You nearly avoided the attack! You took", int(enemydamage / 3), "damage.")
            sleep(sleep_timer)
        elif 3 <= randominteger < 9: # #player took full damage.
            player_stats['Health'] -= enemydamage
            print("The enemy slashed at you, dealing", enemydamage, "damage.")
            sleep(sleep_timer)
        elif randominteger == 9: # Player avoided all damage.
            print("Miss! The enemy missed their attack!")
            sleep(sleep_timer)

        if player_stats['Health'] <= 0: # Conclude the game as failed. Exit main loop.
            print("You've lost.")
            print("GAME OVER")
            game_state = 0
    elif movement == 'heal':
        if 'potion' in player_inventory:
            player_inventory.remove('potion')
            player_stats['Health'] += randominteger
            if player_stats['Health'] > 50:
                player_stats['Health'] = 50
                print("You were healed to full health.")
            else:
                print("You were healed", randominteger, "health.")
        else:
            print("You don't have any health potions!")
    else:
        print("Invalid request. Check the caller.")

# Tells the game where to move the player, displays flavor text.
def movement_controller(direction):
    global current_room
    global previous_room
    if direction == 1:  # North
        if 'North' in room_nav[current_room]['Directions']:
            print(room_nav[current_room]['Movement']['North'])
            sleep(sleep_timer)
            previous_room = current_room
            current_room = room_nav[current_room]['Directions']['North']
            clear_console()
        else:
            print("You can't go that way")
    elif direction == 2:  # East
        if 'East' in room_nav[current_room]['Directions']:
            if current_room == "Ominous Room":
                if room_nav['Ominous Room']['Interact']:
                    if 'key' in player_inventory:
                        print("The door is locked. But you have the key.")
                        print("Unlock the door..?")
                        user_choice = input("y/n? ")
                        if yes_no(user_choice):
                            print("You unlock the door.")
                            player_inventory.remove('key')
                            room_nav['Ominous Room']['Interact'] = False
                            input("Press enter to continue...")
                            clear_console()
                        else:
                            print("Maybe later...")
                    else:
                        print("The door is locked. You can't go that way.")
                        input("Press enter to continue...")
                        clear_console()
                else:
                    print(room_nav[current_room]['Movement']['East'])
                    sleep(sleep_timer)
                    previous_room = current_room
                    current_room = room_nav[current_room]['Directions']['East']
                    clear_console()
            else:
                print(room_nav[current_room]['Movement']['East'])
                sleep(sleep_timer)
                previous_room = current_room
                current_room = room_nav[current_room]['Directions']['East']
                clear_console()
        else:
            print("You can't go that way")
    elif direction == 3:  # South
        if 'South' in room_nav[current_room]['Directions']:
            print(room_nav[current_room]['Movement']['South'])
            sleep(sleep_timer)
            previous_room = current_room
            current_room = room_nav[current_room]['Directions']['South']
            clear_console()
        else:
            print("You can't go that way")
    elif direction == 4:  # West
        if 'West' in room_nav[current_room]['Directions']:
            print(room_nav[current_room]['Movement']['West'])
            sleep(sleep_timer)
            previous_room = current_room
            current_room = room_nav[current_room]['Directions']['West']
            clear_console()
        else:
            print("You can't go that way")
            sleep(sleep_timer)

# Inventory controller, handles inventory and its functions.
def inventory_controller():
    clear_console()
    global player_stats
    global player_inventory
    global room_nav
    player_inventory = list(filter(None, player_inventory))
    if not player_inventory:
        print("Your inventory is empty.")
        input("Press enter to continue...")
    else:
        print("Here's your inventory:")
        for index, item in enumerate(player_inventory):
            print(f"{index + 1}. {item}")
        show_info('inventory')
        while game_state == 1:
            user_choice = input('? ')
            if user_choice.isdigit() and 0 < int(user_choice) < 5 or user_choice in ['potion', 'key', 'oil']:
                # Converts user word input into index numbers for future handling.
                if user_choice == 'potion':
                    user_choice = player_inventory.index('potion')
                elif user_choice == 'key':
                    user_choice = player_inventory.index('key')
                elif user_choice == 'oil':
                    user_choice = player_inventory.index('oil')
                else:
                    user_choice = int(user_choice) - 1

                if player_inventory[int(user_choice)] == 'potion':
                    print("Will heal you a random amount between 1 and 9.")
                    if player_stats['Health'] == 50:
                        print("You are at full health already.")
                        input('Press ENTER to continue...')
                    else:
                        print("Consume the potion?")
                        user_choice = input('y/n? ')
                        if yes_no(user_choice):
                            calc_damage('heal')
                            sleep(sleep_timer)
                        else:
                            print("You chose not to use it.")
                            sleep(sleep_timer / 2)
                        if not player_inventory:
                            print("Your inventory is empty.")
                        sleep(sleep_timer)
                        input('\nPress ENTER to continue...')
                        if room_nav[current_room]['Enemy']:
                            break
                        elif not player_inventory:
                            break
                elif player_inventory[int(user_choice)] == 'oil':
                    print("Increases your damage against beasts.")
                    print("Use the oil? (No reason not to...)")
                    user_choice = input('y/n? ')
                    if yes_no(user_choice):
                        print("You used the oil on your blade.")
                        print("Your damage has increased.")
                        player_stats['Damage'] += 2
                        player_inventory.remove('oil')
                        sleep(sleep_timer)
                        if not player_inventory:
                            print("Your inventory is empty.")
                        sleep(sleep_timer)
                        input('\nPress ENTER to continue...')
                        if room_nav[current_room]['Enemy']:
                            break
                        elif not player_inventory:
                            break
                    else:
                        print("You chose not to use the oil.")
                        input('Press ENTER to continue...')
                elif player_inventory[int(user_choice)] == 'key':
                    print("The key to the large door.")
                    if current_room == 'Ominous Room':
                        print("Unlock the door?")
                        user_choice = input('? ')
                        if yes_no(user_choice):
                            print("You unlocked the door.")
                            player_inventory.remove('key')
                            room_nav['Ominous Room']['Interact'] = False
                            sleep(sleep_timer)
                            if not player_inventory:
                                print("Your inventory is empty.")
                            sleep(sleep_timer)
                            input('\nPress ENTER to continue...')
                        elif not player_inventory:
                            break
                        else:
                            print("you put the key away.")
                            input('Press ENTER to continue...')
                    else:
                        print("It can't be used here.")
                        input('Press ENTER to continue...')
                else:
                    print("There's nothing there.")
                    input('Press ENTER to continue...')
            elif user_choice in valid_inputs['Close']:
                break
            else:
                print("That's not a valid choice.")
            clear_console()
            print("Here's your inventory:")
            for index, item in enumerate(player_inventory):
                print(f"{index + 1}. {item}")
            show_info('inventory')
        clear_console()

# Controls the primary battle screen and it's inputs.
def battle_controller():
    global current_room
    global room_nav
    print("You've entered a fight!\n")
    while int(room_nav[current_room]['EnemyStats']['Health']) > 0:
        randominteger = randint(1, 10)
        print(room_nav[current_room]['EnemyStats']['Name'], ",", room_nav[current_room]['EnemyStats']['Health'], "Health points.")
        print(room_nav[current_room]['EnemyStats']['Description'])
        show_info('battle')
        user_choice = input('? ')
        if verify_input(user_choice) == 8: # User selects 'Attack'
            calc_damage('attack')
            if int(room_nav[current_room]['EnemyStats']['Health']) > 0:
                calc_damage('gethit')
            input('Press ENTER to continue...')
            clear_console()
        elif verify_input(user_choice) == 9: # User selects 'Flee'
            if randominteger < 8:
                print("You escape successfully..!")
                sleep(sleep_timer)
                current_room = previous_room
                input('Press ENTER to continue...')
                clear_console()
                break
            else:
                print("you failed to flee.")
                sleep(sleep_timer)
                calc_damage('gethit')
                input('Press ENTER to continue...')
                clear_console()
        elif verify_input(user_choice) == 10: # User selects 'Heal'
            calc_damage('heal')
            input('Press ENTER to continue...')
            clear_console()
        elif verify_input(user_choice) == 6:
            inventory_controller()
            clear_console()
        elif verify_input(user_choice) == 12:
            set_settings()
            clear_console()
        elif verify_input(user_choice) == 13:
            check_self()
            clear_console()

# Checks if there is an enemy is present in the room.
def check_enemy():
    if room_nav[current_room]['Enemy']:
        battle_controller()

# Shows player statistics, health and damage primarily. Will show your custom name as well.
def check_self():
    clear_console()
    if room_nav[current_room]["Enemy"]:
        enemypic = r"{}".format(room_nav[current_room]["EnemyStats"]["Picture"])
        print(enemypic)
        print(room_nav[current_room]["EnemyStats"]["Name"])
        print(room_nav[current_room]["EnemyStats"]["Health"], "health points.")
        print(room_nav[current_room]["EnemyStats"]["Damage"], "attack points.")
        print(room_nav[current_room]["EnemyStats"]["Description"])
        print('')
        input('Press ENTER to continue...')
        clear_console()
    else:
        print(player_stats['Name'])
        print('Current health:', player_stats['Health'], '/ 50 Health points.')
        print('Damage:', player_stats['Damage'], 'Points')
        print(player_stats['Description'])
        input('Press ENTER to continue...')
        clear_console()

# Small settings changes, namely disabling the sleep timer for immediate feedback.
def set_settings():
    clear_console()
    global sleep_timer
    while game_state == 1:
        clear_console()
        print('Available settings:')
        print('1: Sleep Timer (Delay for text display)' + ' (Current: ' + str(sleep_timer) , 'second)' if sleep_timer == 1 else 'seconds)')
        print('2: Other Valid Inputs (For all possible inputs)')
        print('3: Change player details')
        print('0: Back\n')
        user_choice = input('? ')
        user_choice = user_choice.lower()
        if user_choice == '1' or user_choice == 'sleep': #Modify sleep timer settings for delayed text display.
            clear_console()
            while game_state == 1:
                print('Options:')
                print('1: Default (1 second)')
                print('2: OFF (no delay)')
                print('3: Custom')
                print('0: Back')
                user_choice = input('? ')
                user_choice = user_choice.lower()
                if user_choice == '1' or user_choice == 'default' or user_choice == 'normal':
                    sleep_timer = 1
                    print("Sleep timer set to ", sleep_timer)
                    input('Press ENTER to continue...')
                    clear_console()
                    sleep(1)
                    break
                elif user_choice == '2' or user_choice == 'off' or user_choice == 'disable':
                    sleep_timer = 0
                    print("Sleep timer set to ", sleep_timer)
                    sleep(1)
                    clear_console()
                    break
                elif user_choice == '3' or user_choice == 'custom':
                    user_choice = input('How long? : ')
                    if user_choice.isdigit():
                        if int(user_choice) > 10:
                            print("\nSetting the timer greater than 10 is not recommended.")
                            print("Setting sleep timer to 10.")
                            sleep_timer = 10
                            input('\nPress ENTER to continue...')
                            clear_console()
                        else:
                            sleep_timer = int(user_choice)
                            print("\nSleep timer set to ", sleep_timer)
                            input('\nPress ENTER to continue...')
                            clear_console()
                        break
                    else:
                        input("That's not a number.")
                        clear_console()
                elif user_choice == '0' or user_choice in valid_inputs['Close']:
                    clear_console()
                    break
        elif user_choice == '2' or user_choice == 'other' or user_choice == 'inputs': # Shows all alternate inputs that're accepted.
            clear_console()
            allinputs = str(valid_inputs)
            allinputs = allinputs.replace('{', '')
            allinputs = allinputs.replace('}}', '')
            allinputs = allinputs.replace('}, ', '\n')
            print("List of valid inputs based on suggested input:")
            print(allinputs)
            print("Quit : Shuts the game down.")
            input('Press ENTER to continue...')
            clear_console()
        elif user_choice == '3' or user_choice == 'change': # Allows the player to change their Name or Description. (Added this for fun)
            clear_console()
            while game_state == 1:
                print("What would you like to change?")
                print("1 - Name")
                print("2 - Description")
                print("0 - Exit\n")
                user_choice = input('? ')
                if user_choice == '1' or user_choice == 'name':
                    print("What would you like your name to be?")
                    player_stats['Name'] = input("? ")
                    if player_stats['Name'] == "":
                        player_stats['Name'] = input("Ghatte")
                        print("Name reset to default.")
                        sleep(sleep_timer)
                        input("Press ENTER to continue...")
                        clear_console()
                    else:
                        print("Your name has been changed to \"" + player_stats['Name'] + "\"")
                        sleep(sleep_timer)
                        input("Press ENTER to continue...")
                        clear_console()
                elif user_choice == '2' or user_choice == 'description':
                    print("What would you like your description to be?")
                    player_stats['Description'] = input("? ")
                    if player_stats['Description'] == "":
                        player_stats['Description'] = "Mercenary on a job to slay the beast residing in this building."
                        print("Description reset to default.")
                        sleep(sleep_timer)
                        input("Press ENTER to continue...")
                        clear_console()
                    else:
                        print("Your description has been changed to \"" + player_stats['Description'] + "\"")
                        sleep(sleep_timer)
                        input("Press ENTER to continue...")
                        clear_console()
                elif user_choice == '0' or user_choice in valid_inputs['Close']:
                    break
                else:
                    print("That's not a valid choice.")
                    sleep(sleep_timer)
                    clear_console()
        elif user_choice == '0' or user_choice == 'back':
            clear_console()
            break
        else:
            print("That's not a valid choice.")
            sleep(sleep_timer)

# New search function, removes redundant room description and better hides the presence of items/levers.
def search_area():
    global room_map
    global room_checks
    print("")
    x = room_checks['Index'][current_room]['X']
    y = room_checks['Index'][current_room]['Y']
    if room_nav[current_room]["Interact"]:
        print(room_nav[current_room]['Description']['Search'])
    else:
        print(room_nav[current_room]['Description']['Searched'])
    if not room_checks["Been Searched"][current_room] and not current_room == "A Putrid Smell" and not current_room == "Entrance" and not current_room == "Ominous Room":
        room_map[y][x] = room_map[y][x].replace('   ', ' X ')
    elif not room_checks["Been Searched"][current_room] and current_room == "A Putrid Smell":
        if room_nav['Ravaged Room']['Interact']:
            room_map[y][x] = room_map[y][x].replace('*   -', '? X -')
        elif not room_nav['Ravaged Room']['Interact']:
            room_map[y][x] = room_map[y][x].replace('? X -', '- X -')
            room_map[y][x] = room_map[y][x].replace('*   -', '- X -')
    elif not room_checks["Been Searched"][current_room] and current_room == "Entrance":
        room_nav['Entrance']['Directions']['North'] = "Garden"
        room_map[y - 1][x] = room_map[y - 1][x].replace('*****', '**?**')
        room_map[y][x] = room_map[y][x].replace('   ', ' X ')
    elif not room_checks["Been Searched"]["Ominous Room"] and current_room == "Ominous Room":
        room_map[y][x] = room_map[y][x].replace('   ', ' X ')
        room_map[1][2] = room_map[1][2].replace('   ', ' ! ')
    room_checks["Been Searched"][current_room] = True
    sleep(sleep_timer)

# Prints the map
def print_map():
    clear_console()
    for row in range(len(room_map)):
        for column in range(len(room_map[row])):
            if column % 2 == 0 and not column == 0:
                print(room_map[row][column])
            else:
                print(room_map[row][column], end=' ')
    print('\nLEGEND:\n* or + = Wall\n| or - = Passage\nX = Room has been Searched\n! = Your target\n@ = Your current location.')
    print('\nYou were given a rough layout of the building. It looks like this.')
    input('Press ENTER to continue...')

# Displays helpful information
def show_help():
    clear_console()
    show_info('help')
    input('Press ENTER to continue...')

#####################################################################################################

# Core loop, repeated until the game is quit or completed.
# Amount of loops is counted to be displayed on completion.
def central_loop():
    global current_room
    global room_nav
    global game_state

    if not current_room in room_nav or current_room == '': # Just in case the player is not in a valid room.
        print("Error? Weird but okay. Moving you to entrance.")
        current_room = 'Entrance'

    check_room()
    show_info('movement')
    while game_state == 1:
        user_choice = input('? ')
        # Check user input to a list of potential options, sends back return code if it matches.
        if 0 < verify_input(user_choice) < 5: # If user inputs a directional movement.
            movement_controller(verify_input(user_choice))
            break
        elif verify_input(user_choice) == 5: # If user inputs the check room command
            search_area()
        elif verify_input(user_choice) == 6: # If user opens their inventory
            inventory_controller()
            break
        elif verify_input(user_choice) == 7: # If user picks up whatever is in the room.
            pickup_item()
            break
        elif verify_input(user_choice) == 12: # If user opens the settings menu.
            set_settings()
            break
        elif verify_input(user_choice) == 13: # If user checks their stats
            check_self()
            break
        elif verify_input(user_choice) == 14:
            print_map()
            break
        elif verify_input(user_choice) == 15:
            show_help()
            break
        elif verify_input(user_choice) == 50: # If user quits the game.
            break
        elif verify_input(user_choice) == 99:
            print("\nThanks for playing my little game :)\n")
            player_stats['Damage'] = 50
            player_stats['Description'] = "Thinks Woogi is cool and made a neat little game :)"
            sleep(sleep_timer)
            clear_console()
            break
        else:
            print("\nThat's not an option!\n")

#####################################################################################################

# The base runner. Houses every other loop and the final info.
def main(): # Core of the project
    clear_console()
    global player_stats
    global current_room
    global player_stats
    print('Welcome to my little game :)')
    print('')
    print('#######################################') # Flavor text :)
    print('# @@@@@ @   @  @@@  @@@@@ @@@@@ @@@@@ #')
    print('# @     @   @ @   @   @     @   @     #')
    print('# @  @@ @@@@@ @@@@@   @     @   @@@@  #')
    print('# @   @ @   @ @   @   @     @   @     #')
    print('# @@@@@ @   @ @   @   @     @   @@@@@ #')
    print('#######################################')
    print("{:^{}}".format('~ Beast Hunter ~', 39))
    print('')
    sleep(sleep_timer / 2)
    loopcount = 1
    print('Input a name! Or leave blank for default.')
    user_choice = input('? ')
    user_choice_split = user_choice.split(',')
    if 'BossRush' in user_choice_split:
        current_room = 'Boss Room'
        user_choice = user_choice.replace("BossRush", '')
        user_choice = user_choice.replace(',', '')
    if 'God' in user_choice_split:
        player_stats['Health'] = 500
        player_stats['Damage'] = 500
        player_stats['Name'] = 'Kami'
        player_stats['Description'] = 'Purging the beasts'
        user_choice = user_choice.replace("God", '')
        user_choice = user_choice.replace(',', '')
    if 'Woogi' in user_choice_split:
        player_stats['Name'] = 'Woogi'
        player_stats['Description'] = 'Made this lil game'
        user_choice = user_choice.replace("Woogi", '')
        user_choice = user_choice.replace(',', '')
    if user_choice:
        player_stats['Name'] = user_choice
    clear_console()
    while game_state == 1:
        central_loop()
        loopcount += 1
        clear_console()
    if game_state == 2:
        print('Congratulations, you won!')
        if room_nav['Foyer']['Interact'] == False and room_nav['Ominous Room']['Interact'] == False and room_nav['Ravaged Room']['Interact'] == False and room_nav['Sunlit Room']['Interact'] == False and room_nav['A Putrid Smell']['Interact'] == False and room_nav['Horrid Stench']['Interact'] == False and room_nav['Secret Room']['Interact'] == False and room_nav['Garden']['Interact'] == False:
            print('And you found everything on the map! Take a cookie :)')
    if not player_stats['Name'] == "Ghatte":
        print('Thanks for playing,', player_stats['Name'], '! :)')
    else:
        print('Thanks for playing :)')
    print('You played through', loopcount, 'loops.')
    input('Press ENTER to close the game.')

# Ive had occasions where the game crashed in a command terminal when running from my desktop. I couldn't see what the last message was.
# This exists to prevent the console from closing before I have a chance to see it.
# (I wasn't able to re-create the crash. So I'm still not sure what happened...)
try:
    main()
except SyntaxError:
    print("Game Crashed! Reason : SyntaxError")
    sleep(3)
except KeyError:
    print("Game Crashed! Reason : KeyError")
    sleep(3)
except NameError:
    print("Game Crashed! Reason : NameError")
    sleep(3)
except ValueError:
    print("Game Crashed! Reason : ValueError")
    sleep(3)
except ZeroDivisionError:
    print("Game Crashed! Reason : ZeroDivisionError")
    sleep(3)
except KeyboardInterrupt:
    print("Game Crashed! Reason : KeyboardInterrupt")
    sleep(3)
except:
    print("Game Crashed! Reason : Unhandled Exception")
    sleep(3)