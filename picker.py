import os


import card_sets
import cards


def select_mode():
    """Lets user choose a mode of set selection."""
    os.system('cls' if os.name == 'nt' else 'clear') #Clears terminal
    while True:
        mode = input(   #Lets user select mode of set selection or change sets
            "Which mode would you like to use?\n"
            "Enter ALL for all available sets.\n"
            "Enter CHOICE for your choice of sets.\n"
            "Enter RANDOM for random available sets.\n"
            "Enter CHANGE to change which sets are available.\n"
            ">"
            )
        if mode.lower() == 'quit':  #Quits python
            exit()
        elif mode.lower() == 'all': #Uses all available sets
            return card_sets.user_sets
        elif mode.lower() == 'choice':  #Prompts user to choose from available
            return card_sets.choose_sets(
                card_sets.user_sets,
                "\nWhich sets would you like to use?\n"
                )
        elif mode.lower() == 'random':  #Randomly chooses from available sets
            return card_sets.random_sets(card_sets.user_sets)
        elif mode.lower() == 'change':  #Prompts user to specify available sets
            card_sets.user_sets = card_sets.change_user_sets()
        else:
            print("That's not a valid choice.") #Retries on non-valid input

def pick_cards():
    """Chooses 10 random cards from user-determined sets."""
    pass
                

#randomly select 10 cards from selected sets, add them to kingdom

#inform user of the current kingdom set

#give user option to examine specific cards, veto certain cards,
#or generate an entirely new set

def run_now():
    print("Welcome to the Dominion Kingdom Card Selector.\n"
      "Type 'Quit' anytime to quit.")
    card_sets.load_sets()
    mode = select_mode()
    print(mode)
    

if __name__ == '__main__':
    run_now()
