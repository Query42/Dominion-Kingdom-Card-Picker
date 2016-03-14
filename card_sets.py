import json
import random

SETS = [                #Default list, includes all sets
    (0, 'Dominion'),
    (1, 'Intrigue'),
    (2, 'Seaside'),
    (3, 'Alchemy'),
    (4, 'Prosperity'),
    (5, 'Cornucopia'),
    (6, 'Hinterlands'),
    (7, 'Dark Ages'),
    (8, 'Guilds'),
    (9, 'Adventures')
    ]


def load_sets():
    """Loads the user's available sets, if saved. Otherwise, loads default."""
    global user_sets
    try:
        user_sets = json.load(open("user_sets.txt")) #Grabs user-saved setlist
    except:
        user_sets = SETS    #Defaults to SETS if no saved setlist found

load_sets()     #Loads user sets when module is imported

def change_user_sets():
    """Changes the user's list of available sets and saves them."""
    new_sets = choose_sets("\nWhich sets do you have available?\n", SETS)
    json.dump(new_sets, open("user_sets.txt", "w"))d
    return new_sets

def choose_sets(
    origin_set_list=user_sets,
    prompt="\nPlease choose your sets.\n"
    ):
    """Prompts user to choose sets for use by other functions."""
    print(prompt)
    for item in origin_set_list:    #Shows user sets to choose from
        print(item[0], ":", item[1])
    choice = input("\nChoose set numbers, separated by commas.\n"
                   "(Enter ALL to choose all sets.)\n>") #Collects user's choice
    if choice.lower() == 'quit':    #Quits python
            exit()
    elif choice.lower() == 'all':   #Lets user choose all listed sets
            return origin_set_list
    else:
        sets = []
        choicelist = choice.replace(' ', '').split(',') #Turns user input into
        for item in choicelist:                         #list
            try:
                itemnum = int(item)
                if SETS[itemnum] not in sets:
                    sets.append(SETS[itemnum])
            except:                 #Triggers if list item is non-valid
                print('{} is not a valid set number.'.format(item))
        if len(sets) > 0:   #Checks to make sure user has specified valid set(s)
            return print_sets(  #Informs user of selected sets
                choose_sets,
                sets,
                "You chose:",
                origin_set_list,
                prompt
                )
        else:
            print("I'm sorry, your list is empty.") #Retries on empty list
            return choose_sets()


def random_sets(origin_set_list=user_sets):
    """Chooses random sets from those available"""
    sets = []
    for item in origin_set_list:    #For each set, 50% chance of inclusion
        if random.randint(0, 1):
            sets.append(item)

    if len(sets) == 0:  #Ensures non-empty list, or rerolls all
        return random_sets(origin_set_list)
    else:
        return print_sets(  #Informs user of selected sets
            random_sets,
            sets,
            "Your random sets:",
            origin_set_list
            )

def print_sets(parent_func, sets, message, *args):
    """Displays sets selected through other functions"""
    print(message)  #Prints message inherited from parent function
    for item in sets:   #Prints list of selected sets
        print(item[1])
    correct = input("Use these sets? Y/n\n>")   #Allows user to approve setlist
    if correct.lower() == 'quit':
        exit()
    elif correct.lower() == 'n':    #If user disapproves, reruns parent function
        return parent_func(*args)
    else:
        sets.sort()     #On user approval, sorts sets and returns them
        return sets    
