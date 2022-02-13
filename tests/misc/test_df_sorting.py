# tests/misc/test_df_sorting.py

import unittest
from pandas.testing import assert_frame_equal      # for testing dataframes

import pandas as pd
from itertools import product as cartprod

from src.misc.df_sorting import sortby_str_df

from src.constants import COLUMNS

class TestDfSorting(unittest.TestCase):
    """ Tests of the sorting of the score df. """
    
    def setUp(self):
        """ Initialise attributes available for tests in class. """
        
        self.score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['b', 'q0', 0, 0, 0],
                    ['a', 'q1', 0, 0, 0],
                    ['c', 'q2', 0, 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['the (non)sense', 'q0', 0., 0, 0],
                    ['an ant', 'q1', 0., 0, 0],
                    ['the aardvark', 'q2', 0., 0, 0],
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 0., 0, 0] ],
                columns=COLUMNS ) ]

        self.ignore_str_list = [ '', 'a |the | an' ]


    def tearDown(self):
        """ Deinitialise attributes available for tests in class. """

        self.score_df_list = None
        self.ignore_str_list = None


    def sortby_str_df(self):
        """ Testing the sorting of a dataframe. """

        expected_sorted_score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['a', 'q1', 0, 0, 0],
                    ['b', 'q0', 0, 0, 0],
                    ['c', 'q2', 0, 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame(
                data=[ 
                    ['a', 'q1', 0, 0, 0],
                    ['b', 'q0', 0, 0, 0],
                    ['c', 'q2', 0, 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 0., 0, 0],
                    ['an ant', 'q1', 0., 0, 0],
                    ['the (non)sense', 'q0', 0., 0, 0],
                    ['the aardvark', 'q2', 0., 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 0., 0, 0],
                    ['the (non)sense', 'q0', 0., 0, 0],
                    ['the aardvark', 'q2', 0., 0, 0],
                    ['an ant', 'q1', 0., 0, 0] ],
                columns=COLUMNS ) ]

        for (score_df, ignore_str), expected_sorted_score_df in zip(cartprod(
            self.score_df_list, self.ignore_str_list), expected_sorted_score_df_list):
            
            sorted_score_df = sortby_str_df(score_df, ignore_str)
            
            with self.subTest(f"{sorted_score_df} with ignore_str {ignore_str} -> {expected_sorted_score_df}"): 
                assert_frame_equal( sorted_score_df.reset_index(drop=True), expected_sorted_score_df )

            

        
