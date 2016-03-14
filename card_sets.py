import json
import random

SETS = [
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
        user_sets = json.load(open("user_sets.txt"))
    except:
        user_sets = SETS

load_sets()

def change_user_sets():
    """Changes the user's list of available sets and saves them."""
    new_sets = choose_sets("\nWhich sets do you have available?\n", SETS)
    json.dump(new_sets, open("user_sets.txt", "w"))
    return new_sets

def choose_sets(
    origin_set_list=user_sets,
    prompt="\nPlease choose your sets.\n"
    ):
    """Prompts user to choose sets for use by other functions."""
    print(prompt)
    for item in origin_set_list:
        print(item[0], ":", item[1])
    choice = input("\nChoose set numbers, separated by commas.\n"
                   "(Enter ALL to choose all sets.)\n>")
    if choice.lower() == 'quit':
            exit()
    elif choice.lower() == 'all':
            return origin_set_list
    else:
        sets = []
        choicelist = choice.replace(' ', '').split(',')
        for item in choicelist:
            try:
                itemnum = int(item)
                if SETS[itemnum] not in sets:
                    sets.append(SETS[itemnum])
            except:
                print('{} is not a valid set number.'.format(item))
        if len(sets) > 0:
            return print_sets(
                choose_sets,
                sets,
                "You chose:",
                origin_set_list,
                prompt
                )
        else:
            print("I'm sorry, your list is empty.")
            return choose_sets()


def random_sets(origin_set_list=user_sets):
    """Chooses random sets from those available"""
    sets = []
    for item in origin_set_list:
        if random.randint(0, 1):
            sets.append(item)

    if len(sets) == 0:
        return random_sets(origin_set_list)
    else:
        return print_sets(
            random_sets,
            sets,
            "Your random sets:",
            origin_set_list
            )

def print_sets(parent_func, sets, message, *args):
    """Displays sets selected through other functions"""
    print(message)
    for item in sets:
        print(item[1])
    correct = input("Use these sets? Y/n\n>")
    if correct.lower() == 'quit':
        exit()
    elif correct.lower() == 'n':
        return parent_func(*args)
    else:
        sets.sort()
        return sets    
