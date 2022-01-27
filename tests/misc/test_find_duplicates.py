# tests/misc/find_duplicates.py

import unittest

import pandas as pd

from src.misc.find_duplicates import find_duplicates

from constants import COLUMNS

class TestFindDuplicates(unittest.TestCase):
    """ Tests of finding duplicates in the score dataframe. """
    
    def test_finding_duplicates(self):
        """ Testing the finding of duplicates in the score dataframe. """

        score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['question0', 'answer0', 0, 0, 0],
                    ['question1', 'answer1', 0, 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame(
                data=[ 
                    ['question', 'answer0', 0, 0, 0],
                    ['question', 'answer1', 0, 0, 0] ],
                columns=COLUMNS ) ]

        expected_duplicates_set_list = [set(), {'question'}]

        for score_df, expected_duplicates_set in zip(score_df_list, expected_duplicates_set_list):
            
            duplicates_set = find_duplicates(score_df)
            
            with self.subTest(f"{duplicates_set} -> {expected_duplicates_set}"): 
                self.assertEqual( duplicates_set, expected_duplicates_set )
            
            