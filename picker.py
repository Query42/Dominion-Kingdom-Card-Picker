import card_sets
import cards


def mode_select():
    """Lets user choose a mode of set selection."""
    clear
    while True:
        mode = input(
            "Which mode would you like to use?\n"
            "Enter ALL for all available sets.\n"
            "Enter CHOICE for your choice of sets.\n"
            "Enter RANDOM for random available sets.\n"
            "Enter CHANGE to change which sets are available.\n"
            ">"
            )
        if mode.lower() == 'quit':
            exit()
        elif mode.lower() == 'all':
            return all_sets
        elif mode.lower() == 'choice':
            return choice_sets
        elif mode.lower() == 'random':
            return random_sets
        elif mode.lower() == 'change':
            user_sets = change_user_sets()
        else:
            print("That's not a valid choice.")

def choice_sets(): #finish updating this
    """Lets user choose a selection of sets from those available."""
    print("\nWhich sets would you like to use?\n")
    for set in user_sets:
        print(set[0], ":", set[1])
    choice = input("\nChoose your set numbers, separated by commas.\n"
                   "(Enter ALL if you want to use all available sets.)\n>")
    if choice.lower() == 'quit':
            exit()
    elif choice.lower() == 'all':
            return user_sets
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
                sets.sort()
                return sets
        else:
            print("I'm sorry, your list is empty.")
            return available_sets()
    
def pick_cards():
    pass
                

#randomly select 10 cards from selected sets, add them to kingdom

#inform user of the current kingdom set

#give user option to examine specific cards, veto certain cards,
#or generate an entirely new set

def run_now():
    print("Welcome to the Dominion Kingdom Card Selector.\n"
      "Type 'Quit' anytime to quit.")
    card_sets.set_selection()
    mode = mode_select()
    

if __name__ == '__main__':
    run_now()
