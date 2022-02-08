# tests/translation_handling/test_update_sample.py


import unittest
from pandas.testing import assert_series_equal      # for testing pandas series

import pandas as pd
import numpy as np

from src.translation_handling.update_sample import add_correct_answer, update_sample_score, decrement_sample_wrong_score

from src.constants import COLUMNS

class TestUpdateDataFrame(unittest.TestCase):
    """ Tests of updating the score dataframe. """

    def setUp(self):
        """ Hook method for setting up the test fixture before exercising it. """
        self.sample_list = [
            pd.Series( data=['test_answer0', 'test_question0', np.NaN, 0, 0], index = COLUMNS ),
            pd.Series( data=['test_answer1', 'test_question1', 100.*(2/10), 2, 10], index = COLUMNS) ]

    def tearDown(self):
        """ Hook method for deconstructing the test fixture after testing it. """
        self.sample_list =  None


    def test_add_correct_answer(self):
        """ Testing the adding of a correct answer to a sample. """

        further_correct_answer = 'further_correct_test_answer'

        expected_updated_sample_list = [
            pd.Series( data=['test_answer0' + '; ' + further_correct_answer, 'test_question0', np.NaN, 0, 0], index = COLUMNS ),
            pd.Series( data=['test_answer1' + '; ' + further_correct_answer, 'test_question1', 100.*(2/10), 2, 10], index = COLUMNS) ]

        for sample, expected_updated_sample in zip(self.sample_list, expected_updated_sample_list ):
           
            updated_sample = add_correct_answer(sample, further_correct_answer)
            assert_series_equal( updated_sample, expected_updated_sample )

    def test_update_sample_score(self):
        """ Testing the updating of a sample score if the answer was found wrong or correct. """

        answer_is_correct_list = [ True, False ]

        expected_updated_sample_list = [
            pd.Series( data=['test_answer0', 'test_question0', 0, 0, 1], index = COLUMNS ),
            pd.Series( data=['test_answer1', 'test_question1', 100.*(3/11), 3, 11], index = COLUMNS) ]

        for sample, answer_is_correct, expected_updated_sample in zip( 
            self.sample_list, answer_is_correct_list, expected_updated_sample_list ):
        
            updated_sample = update_sample_score( sample, answer_is_correct )
            assert_series_equal( updated_sample, expected_updated_sample )


    def test_decrement_sample_wrong_score(self):
        """ Testing the decrementing of the wrong score of a sample. """

        expected_updated_sample_list = [
            ValueError("Cannot decrement an unexisting or perfect score."),
            pd.Series( data=['test_answer1', 'test_question1', 100.*(1/10), 1, 10], index = COLUMNS) ]

        for sample, expected_updated_sample in zip(self.sample_list, expected_updated_sample_list ):
            
            try: 
                updated_sample = decrement_sample_wrong_score( sample )  
                assert_series_equal( updated_sample, expected_updated_sample )
            
            except ValueError: 
                with self.assertRaises( ValueError ) as context:
                    updated_sample = decrement_sample_wrong_score( sample )    
                self.assertTrue( str(expected_updated_sample) in str(context.exception) )
