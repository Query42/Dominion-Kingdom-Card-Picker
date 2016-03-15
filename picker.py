from peewee import *
import os

import card_sets
import card_functions


db = SqliteDatabase('cards.db')

class Card(Model):
    name = CharField(unique=True)
    cost = IntegerField()
    set_name = CharField()
    card_text = TextField()
    types = CharField()
    flags = CharField(null=True)

    class Meta:
        database = db

def select_mode():
    """Lets user choose a mode of set selection."""
    os.system('cls' if os.name == 'nt' else 'clear')
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
            return card_sets.user_sets
        elif mode.lower() == 'choice':
            return card_sets.choose_sets(
                "\nWhich sets would you like to use?\n",
                card_sets.user_sets
                )
        elif mode.lower() == 'random':
            return card_sets.random_sets(card_sets.user_sets)
        elif mode.lower() == 'change':
            card_sets.user_sets = card_sets.change_user_sets()
        else:
            print("That's not a valid choice.")

def compile_set_list(set_name):
    set_cards = Card.select().where(Card.set_name == set_name)
    available_cards.extend(list(set_cards))

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
    available_cards = []
    db.connect()
    db.create_tables([Card], safe=True)
    
    for set_name in mode:
        compile_set_list(set_name)
    

if __name__ == '__main__':
    run_now()
