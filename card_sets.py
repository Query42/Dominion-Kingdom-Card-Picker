import pickle


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


def set_selection():
    """Loads the user's available sets, if saved. Otherwise, loads default."""
    global user_sets
    try:
        user_sets = pickle.load(open("user_sets.p", "rb"))
    except:
        user_sets = SETS


def available_sets():
    """Determine's the user's available sets."""
    print("\nWhich sets do you have available?\n")
    for set in SETS:
        print(set[0], ":", set[1])
    choice = input("\nChoose your set numbers, separated by commas.\n"
                   "(Enter ALL if you have all sets.)\n>")
    if choice.lower() == 'quit':
            exit()
    elif choice.lower() == 'all':
            return SETS
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
                return available_sets()
            else:
                return sets
        else:
            print("I'm sorry, your list is empty.")
            return available_sets()


def change_user_sets():
    """Changes the user's list of available sets and saves them."""
    new_sets = available_sets()
    pickle.dump(new_sets, open("user_sets.p", "wb"))
    return new_sets
