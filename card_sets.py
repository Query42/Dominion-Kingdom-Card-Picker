import json


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

def change_user_sets():
    """Changes the user's list of available sets and saves them."""
    new_sets = choose_sets("\nWhich sets do you have available?\n")
    json.dump(new_sets, open("user_sets.txt", "w"))
    return new_sets

def choose_sets(
    prompt="\nPlease choose your sets.\n",
    origin_set_list=SETS
    ):
    """Prompts user to choose sets for use by other functions."""
    print(prompt)
    for set in origin_set_list:
        print(set[0], ":", set[1])
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
            print('You chose:')
            for item in sets:
                print(item[1])
            correct = input("Is this correct? Y/n\n>")
            if correct.lower() == 'quit':
                exit()
            elif correct.lower() == 'n':
                return choose_sets()
            else:
                sets.sort()
                return sets
        else:
            print("I'm sorry, your list is empty.")
            return choose_sets()
