# John B 2025 Game Project for IT-140

#Imports
import os
from random import randint
from time import sleep

# Core Variables
game_state = 1
room_id = 1
# Start with 99 to avoid having to initiate math from within a check.
room_state = [99, 0, 1, 1, 0, 1, 1, 1, 1, 1] # Room states of all rooms.
# Placeholder for 0, (1)Entry, (2)Hub, (3)Locked Door, (4)Boss Room, (5)East Room, (6)Key Room, (7)Upgrade Room, (8)South-east Room, (9)Hidden Room
player_inventory = [''] # Storage for items.
enemy_hp = [99, 0, 6, 0, 30, 6, 0, 0, 12, 0] # Hp for various enemies. Boss included. Will be filtered based on room_id.
enemy_damage = [99, 0, 3, 0, 9, 3, 0, 0, 6, 0] # Damage values for various enemies. Boss included. Filtered based on room_id
player_hp = 50
player_damage = 3
player_name = 'Ghatte'
sleep_timer = 1

# Definitions and core mechanics.

# Basic input information to be displayed.
# VALID MODULES "movement", "battle", "inventory"
def show_info(screen):
    print('')
    print("What do will you do?")
    if screen == 'movement':
        print("Valid Directions : North, South, East, West")
        print("Other options: Inventory, Search, Pickup, Check, Settings")
        print('')
    elif screen == 'battle':
        print("Valid options: Attack, Heal, Flee")
        print("Other Options: Inventory, Check, Settings")
        print('')
    elif screen == 'inventory':
        print("Type the item number or name that you'd like to select.")
        print("Or type 'exit' to exit back to navigation.")
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
        return True

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
    user_input = user_input.lower()
    if user_input in ['north', 'n', 'up']:
        return 1
    elif user_input in ['east', 'e', 'right']:
        return 2
    elif user_input in ['south', 's', 'down']:
        return 3
    elif user_input in ['west', 'w', 'left']:
        return 4
    elif user_input in ['examine', 'search', 'look']:
        return 5
    elif user_input in ['inventory', 'items', 'backpack']:
        return 6
    elif user_input in ['pickup', 'grab', 'yoink']:
        return 7
    elif user_input in ['attack', 'fight', 'kill']:
        return 8
    elif user_input in ['flee', 'run', 'escape']:
        return 9
    elif user_input in ['heal', 'healing', 'recover', 'potion']:
        return 10
    elif user_input in ['exit', 'back', 'close']:
        return 11
    elif user_input in ['settings', 'options', 'option']:
        return 12
    elif user_input in ['check', 'self', 'inquire']:
        return 13
    elif user_input == "quit":
        game_state = 0
        return 50
    else:
        return 0 # Tells the caller that the user input is invalid.
    # Most of these are self-explanatory.Inv

# Tells the main loop what to say when you arrive in a new room.
def check_room():
    global room_id
    global game_state
    check_enemy()
    if room_id == 1: # Entrance Room
        print("You're at the Entrance to the building. The door is torn off.")
        print("There are scratch marks all over the structure. There must be creatures within.")
        print("The doorway is to the East.")
    elif room_id == 2: # Hub room, connected to all paths. Potion in this room
        print("You're in the central room of the building.")
        print("Scratch marks and debris litter the floors and walls.")
        if room_state[room_id] == 1:
            print("You notice a glint out of the corner of your eye.")
        elif room_state[room_id] == 0:
            print("There's nothing in here but a mess.")
        print("You see doorways to your North, East, and South.")
    elif room_id == 3: # Locked door room, entrance to boss.
        print("The claw marks are very large in this room.")
        print("This must be the way towards the beast you're here for.")
        if room_state[room_id] == 1:
            print("There is a locked door to your East.")
            if 'key' in player_inventory:
                print("You have the key for the door.")
            else:
                print("You should go and look for the key. It must be nearby.")
        elif room_state[room_id] == 0:
            print("The doorway into the beasts den is to your East.")
    elif room_id == 4: # Boss room.
        if room_state[room_id] == 2:
            print("It appears the Beast has been killed.")
            sleep(sleep_timer)
            print("It were crushed by a ceiling chandelier...")
            sleep(sleep_timer)
            game_state = 2
        else:
            print("You can't actually read this. If you can then something is wrong. Also the beast is right behind you.")
    elif room_id == 5: # East room. Secret lever to hidden room.
        print("There are debris and scratch marks all over the room.")
        if room_state[room_id] == 0:
            print("There is an activated lever in this room.")
        print("There's a doorway to your North. You see light shining through it.")
    elif room_id == 6: # Room with the boss key in it.
        print("There is sunlight gleaming down through the ceiling.")
        print("The room is in shambles, and the ceiling has caved in.")
        if room_state[room_id] == 1:
            print("There's something glimmering in the sunlight.")
        elif room_state[room_id] == 0:
            print("Nothing in here but debris.")
    elif room_id == 7: # Room with the upgrade in it. Connected to hidden room.
        print("A foul stench emanates from this direction.")
        print("A couple of dead adventurers lay near the doorway. They must have been attacked.")
        print("Amongst the fetid stench, you catch a musty smell.")
        if room_state[5] == 1:
            if room_state[room_id] == 1:
                print("You wonder if the adventurers had anything useful.")
            elif room_state[room_id] == 0:
                print("Nothing here but that smell.")
        elif room_state[5] == 0:
            if room_state[room_id] == 1:
                print("You wonder if the adventurers had anything useful.")
            elif room_state[room_id] == 0:
                print("A doorway has opened to your West.")
        print("There is another door to your East.")
    elif room_id == 8: # Room with second potion in it.
        print("This is where the stench is coming from.")
        print("The room is littered in various animal carcases. This must be where they eat.")
        if room_state[room_id] == 0:
            print("Nothing here but death and decay.")
    elif room_id == 9: # Hidden room. Has lever to remove boss health.
        print("This room appears untouched by the beasts dwelling within the building.")
        print("Water is dripping in from a crack in the ceiling.")
        print("A musty smell emanates from here.")
        if room_state[room_id] == 1:
            print("Under the dust, there's a lever on the wall.")
        elif room_state[room_id] == 0:
            print("The lever is pulled.")
    else: # If somehow room_id becomes an unexpected number. Resets player to the entrance.
        print("Something went wrong. This room doesn't exist.")
        room_id = 1

# Function for pickup. Simplistic, maybe will make more interesting later.
def pickup_item():
    global player_inventory
    global room_state
    global enemy_hp
    if (room_id == 2 and room_state[room_id] == 1) or (room_id == 8 and room_state[room_id] == 1):
        print("\nYou found a healing potion. Item added to inventory.\n")
        player_inventory.append("potion")
        room_state[room_id] = 0
        input("Press enter to continue...")
    elif room_id == 5 and room_state[room_id] == 1:
        print("\nYou found a hidden lever. You pulled it.\n")
        room_state[room_id] = 0
        input("Press enter to continue...")
    elif room_id == 6 and room_state[room_id] == 1:
        print("\nYou found the key to the bosses door.\n")
        player_inventory.append("key")
        room_state[room_id] = 0
        input("Press enter to continue...")
    elif room_id == 7 and room_state[room_id] == 1:
        print("\nYou found the beast oil. Item added to inventory.\n")
        player_inventory.append("oil")
        room_state[room_id] = 0
        input("Press enter to continue...")
    elif room_id == 9 and room_state[room_id] == 1:
        print("\nThere's another lever here. Pull it?")
        user_choice = input("y/n? ")
        user_choice = yes_no(user_choice)
        if user_choice:
            print("You pull the lever. You heard a loud crash in the other room...\n")
            room_state[room_id] = 0
            enemy_hp[4] -= 10
            if enemy_hp[4] <= 0:
                room_state[4] = 2
            sleep(sleep_timer)
            input("Press enter to continue...")
        if not user_choice:
            print("\nYou left the lever alone.\n")
            sleep(sleep_timer)
            input("Press enter to continue...")
    else:
        print("\nThere is nothing of interest here.\n")
        sleep(sleep_timer)

# Calculates health related systems. From enemy health, player health, and healing.
# The primary runner of the backend for battles.
# VALID MOVEMENT MODULES "attack", "gethit", "heal"
def calc_damage(movement):
    randominteger = randint(1, 9)
    global game_state
    global player_hp
    global enemy_hp
    global player_inventory
    hitdamage = player_damage
    if movement == 'attack':
        print('')
        if 7 < randominteger <= 9:
            hitdamage = player_damage * 2
            print("Critical hit!")

        enemy_hp[room_id] -= hitdamage
        if enemy_hp[room_id] > 0 and room_id != 4:
            print("You hit the Creature for", hitdamage, "damage.")
            sleep(sleep_timer)
            print("(The Creature has", enemy_hp[room_id], "health remaining.)")
            sleep(sleep_timer)
        elif enemy_hp[room_id] <= 0 and room_id != 4:
            print("You hit the Creature for", hitdamage, "damage.")
            sleep(sleep_timer)
            print("You've killed the Creature.")
            sleep(sleep_timer)
        elif enemy_hp[room_id] > 0 and room_id == 4:
            print("You attacked the Beast, Dealing", hitdamage, "damage.")
            sleep(sleep_timer)
            print("(The Beast has", enemy_hp[room_id], "health left.)")
            sleep(sleep_timer)
        elif enemy_hp[room_id] <= 0 and room_id == 4:
            print("You attacked the Beast, Dealing", hitdamage, "damage.")
            sleep(sleep_timer)
            print("You've Slain the Beast!")
            game_state = 2
            sleep(sleep_timer)
    elif movement == 'gethit':
        if 1 <= randominteger < 3: # Player only took partial damage.
            player_hp -= enemy_damage[room_id] / 3
            print("You nearly avoided the attack! You took", enemy_damage[room_id], "damage.")
            sleep(sleep_timer)
        elif 3 <= randominteger < 9: # #player took full damage.
            player_hp -= enemy_damage[room_id]
            print("The enemy slashed at you, dealing", enemy_damage[room_id], "damage.")
            sleep(sleep_timer)
        elif randominteger == 9: # Player avoided all damage.
            print("Miss! The enemy missed their attack!")
            sleep(sleep_timer)

        if player_hp <= 0: # Conclude the game as failed. Exit main loop.
            print("You've lost.")
            print("GAME OVER")
            game_state = 0
    elif movement == 'heal':
        if 'potion' in player_inventory:
            player_inventory.remove('potion')
            player_hp += randominteger
            if player_hp > 50:
                player_hp = 50
                print("You were healed to full health.")
            else:
                print("You were healed", randominteger, "health.")
        else:
            print("You don't have any health potions!")
    else:
        print("Invalid request. Check the caller.")
    print('')

# Tells the game where to move the player, displays flavor text.
def movement_controller(direction):
    global room_id
    clear_console()
    # North
    if direction == 1: # North
        if room_id == 2:
            room_id = 3
            print("You entered a small room.")
            sleep(sleep_timer)
            return True
        elif room_id == 5:
            room_id = 6
            print("You're blinding by the beams of light shining through the roof.")
            sleep(sleep_timer)
            return True
        elif room_id == 7:
            room_id = 2
            print("You re-entered the central room.")
            sleep(sleep_timer)
            return True
        else:
            print("There's a wall there.")
            sleep(sleep_timer)
            return False
    # East
    elif direction == 2: # East
        if room_id == 1:
            room_id = 2
            print("You entered the ravaged building.")
            sleep(sleep_timer)
            return True
        elif room_id == 2:
            room_id = 5
            print("You entered another torn up room.")
            sleep(sleep_timer)
            return True
        elif room_id == 3: # Entering boss room
            if room_state[room_id] == 1:
                if "key" in player_inventory:
                    print("The door here is locked. But you have the key.")
                    print("Unlock the door?")
                    user_choice = input('y/n? ')
                    if yes_no(user_choice):
                        print("You unlocked the door and stepped inside...")
                        room_state[room_id] = 0
                        player_inventory.remove('key')
                        room_id = 4
                        sleep(sleep_timer)
                        return True
                    elif not yes_no(user_choice):
                        print("You refused to open the door. For now.")
                        sleep(sleep_timer)
                        return False
                    return None
                else:
                    print("The door is locked. You can't go this way.")
                    sleep(sleep_timer)
                    return False
            else:
                print("You re-entered the Beasts den.")
                room_id = 4
                sleep(sleep_timer)
                return True
        elif room_id == 7:
            room_id = 8
            print("Scrunching your nose, you walk into a wave of odor.")
            sleep(sleep_timer)
            return True
        elif room_id == 9:
            room_id = 7
            print("You left the damp hidden room.")
            sleep(sleep_timer)
            return True
        else:
            print("There's a wall there.")
            sleep(sleep_timer)
            return False
    # South
    elif direction == 3: # South
        if room_id == 3:
            room_id = 2
            print("You re-entered the central room.")
            sleep(sleep_timer)
            return True
        elif room_id == 2:
            room_id = 7
            print("You followed a stench into the next room.")
            sleep(sleep_timer)
            return True
        elif room_id == 6:
            room_id = 5
            print("You left the glimmering sunlight, into the torn up room.")
            sleep(sleep_timer)
            return True
        else:
            print("There's a wall there.")
            sleep(sleep_timer)
            return False
    # West
    elif direction == 4:
        if room_id == 2:
            room_id = 1
            print("You stepped outside for some air.")
            sleep(sleep_timer)
            return True
        elif room_id == 4:
            room_id = 3
            print("You left the Beasts lair.")
            sleep(sleep_timer)
            return True
        elif room_id == 5:
            room_id = 2
            print("You re-entered the central room.")
            sleep(sleep_timer)
            return True
        elif room_id == 7:
            if room_state[5] == 0:
                room_id = 9
                print("You entered a damp, untouched room.")
                sleep(sleep_timer)
                return True
            else:
                print("There's a wall there. Something's off about it, though.")
                sleep(sleep_timer)
                return False
        elif room_id == 8:
            room_id = 7
            print("You stepped away from the stench of decay.")
            sleep(sleep_timer)
            return True
        else:
            print("There's a wall there.")
            sleep(sleep_timer)
            return False
    else:
        print("Invalid request. Check the caller.")
        return False

# Inventory controller, handles inventory and its functions.
def inventory_controller():
    clear_console()
    global player_inventory
    global player_hp
    global player_damage
    global player_inventory
    global room_state
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
                    if player_hp == 50:
                        print("You are at full health already.")
                        input('Press ENTER to continue...')
                    else:
                        print("Consume the potion?")
                        user_choice = input('? ')
                        if yes_no(user_choice):
                            calc_damage('heal')
                        input('Press ENTER to continue...')
                        if enemy_hp[room_id] > 0:
                            break
                elif player_inventory[int(user_choice)] == 'oil':
                    print("Increases your damage against beasts.")
                    print("Use the oil? (No reason not to...)")
                    user_choice = input('y/n? ')
                    if yes_no(user_choice):
                        print("You used the oil on your blade.")
                        print("Your damage has increased.")
                        player_damage = 5
                        player_inventory.remove('oil')
                        input('Press ENTER to continue...')
                        if enemy_hp[room_id] > 0:
                            break
                    else:
                        print("You chose not to use the oil.")
                        input('Press ENTER to continue...')
                elif player_inventory[int(user_choice)] == 'key':
                    print("The key to the large door.")
                    if room_id == 3:
                        print("Unlock the door?")
                        user_choice = input('? ')
                        if yes_no(user_choice):
                            print("You unlocked the door.")
                            player_inventory.remove('key')
                            room_state[room_id] = 0
                            input('Press ENTER to continue...')
                        else:
                            print("you put the key away.")
                            input('Press ENTER to continue...')
                    else:
                        print("It can't be used here.")
                        input('Press ENTER to continue...')
                else:
                    print("There's nothing there.")
                    input('Press ENTER to continue...')
            else:
                user_choice = verify_input(user_choice)
                if user_choice == 11:
                    break
            clear_console()
            print("Here's your inventory:")
            for index, item in enumerate(player_inventory):
                print(f"{index + 1}. {item}")
            show_info('inventory')
        clear_console()

# Controls the primary battle screen and it's imputs.
def battle_controller():
    global room_id
    enemy_name = ''
    print("You've entered a fight!\n")
    if room_id == 4:
        enemy_name = "Boss Beast"
    elif room_id == 2 or room_id == 5 or room_id == 8:
        enemy_name = "Lesser Beast"
    while enemy_hp[room_id] > 0:
        randominteger = randint(1, 10)
        print(enemy_name, ",", enemy_hp[room_id], "Health points.")
        show_info('battle')
        user_choice = input('? ')
        if verify_input(user_choice) == 8: # User selects 'Attack'
            calc_damage('attack')
            if enemy_hp[room_id] > 0:
                calc_damage('gethit')
            input('Press ENTER to continue...')
            clear_console()
        elif verify_input(user_choice) == 9: # User selects 'Flee'
            if randominteger < 8:
                print("You escape successfully..!")
                sleep(sleep_timer)
                if room_id == 4:
                    room_id = 3
                elif room_id == 2:
                    room_id = 1
                elif room_id == 5:
                    room_id = 2
                elif room_id == 8:
                    room_id = 2
                else:
                    room_id = 1
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
    if room_id == 2 or room_id == 4 or room_id == 5 or room_id == 8:
        if enemy_hp[room_id] > 0:
            battle_controller()

# Shows player statistics, health and damage primarily. Will show your custom name as well.
def check_self():
    clear_console()
    print(player_name)
    print('Current health:', player_hp, '/ 50 Health points.')
    print('Damage:', player_damage, 'Points')
    print('Mercenary on a job to slay the beast residing in this building.')
    input('Press ENTER to continue...')
    clear_console()

# Small settings changes, namely disabling the sleep timer for immediate feedback.
def set_settings():
    clear_console()
    global sleep_timer
    user_choice = 0
    while user_choice != 99:
        print('Available settings:')
        print('1: Sleep Timer (Delay for text display)')
        print('2: Other Valid Inputs (For all possible inputs)')
        print('0: Back')
        user_choice = input('? ')
        user_choice = user_choice.lower()
        if user_choice == '1' or user_choice == 'sleep': #Modify sleep timer settings for delayed text display.
            while user_choice != 99:
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
                        sleep_timer = int(user_choice)
                        print("Sleep timer set to ", sleep_timer)
                        input('Press ENTER to continue...')
                        clear_console()
                        break
                    else:
                        input("That's not a number.")
                        clear_console()
                elif user_choice == '0' or user_choice == 'back':
                    clear_console()
                    break
        elif user_choice == '2' or user_choice == 'other' or user_choice == 'inputs': # Shows all alternate inputs that're accepted.
            print("List of valid inputs based on suggested input:")
            print("North : n, up\nEast : e, right\nSouth : s, down\nWest : w, left")
            print("Examine : search, look")
            print("Inventory : items, backpack")
            print("Pickup : grab, yoink")
            print("Attack : fight, kill")
            print("Heal : healing, recover, potion")
            print("Back : exit, close")
            print("Settings : options, option")
            print("Check : self, inquire")
            print("Quit - Shuts the game down.")
            input('Press ENTER to continue...')
            clear_console()
        elif user_choice == '0' or user_choice == 'back':
            clear_console()
            break

# New search function, removes redundant room description and better hides the presence of items/levers.
def search_area():
    if room_state[room_id] == 1:
        if room_id == 2:
            print("\nThere's a potion here. You should take it.\n")
            sleep(sleep_timer)
        elif room_id == 5:
            print("\nThere's a lever under some debris. Maybe you should pull it.\n")
            sleep(sleep_timer)
        elif room_id == 7:
            print("\nThere's a bottle of oil on this adventurers corpse. Could be useful...\n")
            sleep(sleep_timer)
        elif room_id == 8:
            print("\nThere's a potion under the carcases. Could be useful.\n")
            sleep(sleep_timer)
        elif room_id == 3:
            print("\nThere's a large locked door here. The key must be nearby.\n")
            sleep(sleep_timer)
        else:
            print("\nThere's something here, but not really.\n")
            sleep(sleep_timer)
    else:
        print("\nThere's nothing useful in this room.\n")
        sleep(sleep_timer)

#####################################################################################################

# Core function for movement related tasks.
def central_loop():
    global room_id
    global room_state
    global game_state

    if not (0 < room_id < 10): # Just in case the player is not in a valid room.
        print("Error? Weird but okay. Moving you to entrance.")
        room_id = 1

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
        elif verify_input(user_choice) == 50: # If user quits the game.
            break
        else:
            print("That's not an option!")

#####################################################################################################

def main(): # Core of the project
    global player_name
    print('Welcome to my little game :)')
    print('')
    print('#######################################')
    print('# @@@@@ @   @  @@@  @@@@@ @@@@@ @@@@@ #')
    print('# @     @   @ @   @   @     @   @     #')
    print('# @  @@ @@@@@ @@@@@   @     @   @@@@  #')
    print('# @   @ @   @ @   @   @     @   @     #')
    print('# @@@@@ @   @ @   @   @     @   @@@@@ #')
    print('#######################################')
    print("{:^{}}".format('~ Beast Hunter ~', 39))
    print('')
    sleep(sleep_timer)
    loopcount = 1
    print('Input a name! Or leave blank for default.')
    user_choice = input('? ')
    if user_choice:
        player_name = user_choice
    clear_console()
    while game_state == 1:
        central_loop()
        loopcount += 1
        clear_console()
    if game_state == 2:
        print('Congratulations, you won!')
        if room_state[2] == 0 and room_state[3] == 0 and room_state[5] == 0 and room_state[6] == 0 and room_state[7] == 0 and room_state[8] == 0 and room_state[9] == 0:
            print('And you found everything on the map! Take a cookie :)')
    if user_choice:
        print('Thanks for playing,', player_name, '! :)')
    else:
        print('Thanks for playing :)')
    print('You played through', loopcount, 'loops.')
    input('Press ENTER to close the game.')

main()
