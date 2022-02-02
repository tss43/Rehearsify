# tests/misc/test_compute_statistics.py

import unittest
from numpy.testing import assert_array_equal      # for testing array equality, without raising NaN comparison exceptions

import pandas as pd
import numpy as np

from src.misc.compute_statistics import compute_statistics

from src.constants import COLUMNS, STATS_COLUMNS

class TestComputeStatistics(unittest.TestCase):
    """ Tests on the dict used to insert new entries into RehearsifyGUI objects. """

    def setUp(self):
        """ Hook method for setting up the test fixture before exercising it. """
        self.score_df_list = [
            pd.DataFrame( columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['test_question0', 'test_answer0', 0., 0, 0],
                    ['test_question1', 'test_answer1', 0., 0, 0] ],
                columns=COLUMNS ), 
            pd.DataFrame( 
                data=[
                    ['test_question0', 'test_answer0', 50., 1, 2],
                    ['test_question1', 'test_answer1', 25., 1, 4] ],  
                columns=COLUMNS ) ]

    def tearDown(self):
        """ Hook method for deconstructing the test fixture after testing it. """
        self.score_df_list =  None


    def test_keys_in_stats_dict(self):
        """ Test if the statistics dict has appropriate keys. """ 
        
        expected_keys = STATS_COLUMNS

        for score_df in self.score_df_list:
            stats_dict = compute_statistics( score_df )
    
            self.assertListEqual( list( stats_dict.keys() ), expected_keys )


    def test_values_in_stats_dict(self):
        """ Test if the statistics dict has appropriate values. """ 

        expected_vals_list = [
            [0, 0, np.NaN, 0, 0, np.NaN],
            [2, 2, round(100*2/2,2), 0, 0, np.NaN],
            [2, 0, round(100*0/2,2), 6, 2, round(100*2/6, 2) ] ]

        for expected_vals, score_df in zip(expected_vals_list, self.score_df_list):
            
            stats_dict = compute_statistics( score_df )

            assert_array_equal( list( stats_dict.values() ), expected_vals )
