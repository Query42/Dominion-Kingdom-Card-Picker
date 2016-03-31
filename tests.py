import json
import random
import unittest

import card_functions
import card_sets
import picker

class TestCardFunctions(unittest.TestCase):  
    def test_multiline_returns_empty(self):
        def test_input(*args): return "DoNe"
        card_functions.input = test_input
        assert card_functions.multiline() == ''

    def test_multiline_returns_correct_lines(self):
        test_list = ["done", "test2", "test1"]
        def test_input(string): return test_list.pop()
        card_functions.input = test_input
        assert card_functions.multiline() == "test1\ntest2"
        
##    def test_create_card_asks_for_set(self):  #Not currently testing as
##        def test_input(*args): return(True)   #it alters the database
##        card_functions.input = test_input
##        assert card_functions.create_card() == True

    def test_select_card(self):
        card = card_functions.select_card("Cellar")
        assert card.name == "Cellar"


class TestSetFunctions(unittest.TestCase):
    def test_load_sets_changes_global(self):
        def load(*args):
            return True
        json.load = load
        card_sets.load_sets()
        assert card_sets.user_sets

    def test_load_sets_default(self):
        def load(*args):
            int('test')
        json.load = load
        card_sets.load_sets()
        assert card_sets.user_sets == card_sets.SETS


if __name__ == '__main__':
    unittest.main()
