# tests/GUI_interacting/RehearsifyGUI.py


import unittest

import pandas as pd
import itertools

from src.translation_handling.answer_handling import check_answer
from src.GUI_interacting.RehearsifyGUI import dict_to_insert_in_log

from src.constants import COLUMNS, DISPLAY_COLUMNS

class TestRehearsifyGUI(unittest.TestCase):
    """ Tests on RehearsifyGUI and its methods. """

    def setUp(self) -> None:
        """ Initialise attributes available for tests in class. """
        return super().setUp()

    def tearDown(self) -> None:
        """ Deinitialise attributes available for tests in class. """
        return super().tearDown()


class TestLogInsertionDict(unittest.TestCase):
    """ Tests on the dict used to insert new entries into RehearsifyGUI objects. """

    def test_keys_of_dict_to_insert_in_log(self):
        """ Test if the dict to insert has appropriate keys. """ 
        
        expected_keys = DISPLAY_COLUMNS

        user_answer_list = [ 'test_answer_0', 'wrong_test_answer1' ]
        sample_list = [
            pd.Series(data=['test_question0', 'test_answer0', 50., 1, 2], index=COLUMNS),
            pd.Series(data=['test_question1', 'test_answer1', 25., 1, 4], index=COLUMNS) ]
        
        for user_answer, sample in itertools.product(user_answer_list, sample_list):
            
            answer_is_correct = check_answer( user_answer, sample.answer ) 
            test_dict = dict_to_insert_in_log( sample, user_answer, answer_is_correct )
    
            with self.subTest(f"list( {test_dict}.keys() ) -> {expected_keys}"): 

                self.assertEqual( list( test_dict.keys() ), expected_keys )

