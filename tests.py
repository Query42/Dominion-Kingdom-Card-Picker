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
        
    def test_create_card_asks_for_set(self):
        def test_input(*args): return(return(True))
        card_functions.input = test_input
        assert card_functions.create_card() == True

    def test_examine_card(self):
        pass

if __name__ == '__main__':
    unittest.main()
