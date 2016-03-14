from peewee import *

db = SqliteDatabase('cards.db')


class Card(Model):      #Database table parameters for cards
    name = CharField(unique=True)
    cost = IntegerField()
    set_name = CharField()
    card_text = TextField()
    types = CharField()
    flags = CharField(null=True)

    class Meta:
        database = db


def multiline(message):
    """Takes multiline user input for use in card text."""
    user_input = []
    print(message)
    entry = input("(Type 'done' when done.)\n> ")
    while entry != "done":
        user_input.append(entry)
        entry = input("> ")
    return '\n'.join(user_input)


def create_card(card_set=None): #Entering a set argument makes all created cards
                                #part of that set.
    """Creates a new card in the database."""
    db.connect()
    db.create_tables([Card], safe=True)
    cards = 0
    if not card_set:
        card_set = input("Set? > ") #Prompts user for card's set if no argument
    while True:
        try:
            Card.create(    #Creates card with user-input parameters
                name = input("Name? > ").capitalize(),
                cost = int(input("Cost? > ")),
                set_name = card_set,
                card_text = multiline("Text?"),
                types = input("Types? > ")
                )
            cards += 1
        except IntegrityError:  #Triggers when name exclusivity not met
            print('Card name already in use.')
        except TypeError:       #Triggers if non-number entered for Cost.
            print('Invalid number entered.')

        repeat = input('Create another card? Y/n > ')
        if repeat.lower() == 'n':
            break
    print(cards, ' cards created.') #Tells user how many cards were created


def select_card(card_name):
    """Selects a card from the database by name"""
    db.connect()
    db.create_tables([Card], safe=True)
    return Card.select().where(Card.name == card_name).get()


def examine_card(card_name):
    """Gives the details of the named card."""
    card = select_card(card_name.capitalize())
    return print('''
Name: {}
Cost: {}
Set: {}
Text:

{}

Type: {}
'''.format(card.name,
                   card.cost,
                   card.set_name,
                   card.card_text,
                   card.types
                   ))


def edit_card(card_name):
    """Rewrites the values of a card."""
    card = select_card(card_name.capitalize())
    print("What value would you like to change?\n"
          "Choices are Name, Cost, Set, Text, Type, or Flags.")
    choice = input("> ")

    if choice.lower() == 'quit':    #Quits python
        exit()
    elif choice.lower() == 'name':  #Changes card's name
        card.name = (input("What would you like to change it to?\n> ")
                     .capitalize())
    elif choice.lower() == 'cost':  #Changes card's cost
        change = input("What would you like to change it to?\n> ")
        try:
            change = int(change)
            card.cost = change
        except:
            print("That's not a valid number.")
            exit()
    elif choice.lower() == 'set':   #Changes card's set
        card.set_name = input("What would you like to change it to?\n> ")
    elif choice.lower() == 'text':  #Changes card text
        card.card_text = multiline("What would you like to change it to?")
    elif choice.lower() == 'type':  #Changes card's type(s)
        card.types = input("What would you like to change it to?\n> ")
    elif choice.lower() == 'flags': #Adds/changes card's flags
        card.flags = input("What would you like to change it to?\n> ")
    
    card.save()                     #Saves changes to database
    print("{}'s {} value has been changed.".format( #Tells user change worked
        card.name, choice.capitalize()))
