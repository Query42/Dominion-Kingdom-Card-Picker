import os
import random

import card_sets
import card_functions


def select_sets():
    """Lets user choose a mode of set selection and determine sets."""
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

def build_card_list(set_list):
    """Compiles a list of all cards in all specified sets."""
    card_list = []
    for set_name in set_list:
        set_cards = card_functions.retrieve_set_cards(set_name)
            #Grabs cards from named set
        for card in set_cards:         #Adds cards to total list
            card_list.append(card)
    return card_list

def pick_cards(card_catalog):
    """Chooses 10 random cards from user-determined sets."""
    working_list = card_catalog
    cards = []
    count = 0
    event_count = 0

    while count <10:
        count +=1
        card = (working_list.pop(random.randint(0, (len(working_list)-1))))
        #Removes random card from list and sets it to this variable
        if card.types == "Event":
            count -= 1              #Does not count Events in 10 count
            if event_count == 3:    #Allows up to 3 Events to be added
                continue
            event_count +=1
        cards.append(card) #Adds card to cards list

    return cards
    
def list_tuple_seconds(tuple_list):
    """Takes list of tuples. Makes new list of second item in each tuple."""
    new_list = []
    for item in tuple_list:
        new_list.append(item[1])
    return new_list

def run_now():
    os.system('cls' if os.name == 'nt' else 'clear') #Clears terminal
    print("Welcome to the Dominion Kingdom Card Selector.\n"
      "Type 'Quit' anytime to quit.\n")
    set_tuples = select_sets()                  #Gathers list of sets to use
    set_list = list_tuple_seconds(set_tuples)   #Turns set_list into names list
    card_catalog = build_card_list(set_list)    #Builds list of all cards in sets
    cards = pick_cards(card_catalog)            #Picks 10 cards from card list
    for card in cards:
        print("{} ({})".format(card.name, card.set_name))
    print("{} cards selected.".format(len(cards)))
    input("Press ENTER to exit.")
    return

if __name__ == '__main__':
    run_now()
