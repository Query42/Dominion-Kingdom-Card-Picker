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
            return card_sets.choose_sets(
                "\nWhich sets would you like to use?\n",
                user_sets
                )
        elif mode.lower() == 'random':
            return random_sets
        elif mode.lower() == 'change':
            user_sets = change_user_sets()
        else:
            print("That's not a valid choice.")

def pick_cards():
    pass
                

#randomly select 10 cards from selected sets, add them to kingdom

#inform user of the current kingdom set

#give user option to examine specific cards, veto certain cards,
#or generate an entirely new set

def run_now():
    print("Welcome to the Dominion Kingdom Card Selector.\n"
      "Type 'Quit' anytime to quit.")
    card_sets.load_sets()
    mode = mode_select()
    

if __name__ == '__main__':
    run_now()
