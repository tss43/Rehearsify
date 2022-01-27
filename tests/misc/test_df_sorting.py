# tests/misc/test_df_sorting.py

import unittest
from pandas.testing import assert_frame_equal      # for testing dataframes

import pandas as pd
import itertools

from src.misc.df_sorting import sort_df

from constants import COLUMNS

class TestDfSorting(unittest.TestCase):
    """ Tests of the sorting of the score df. """
    
    def test_sorting(self):
        """ Testing the sorting of a dataframe. """

        score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['q0', 'b', 0, 0, 0],
                    ['q1', 'a', 0, 0, 0],
                    ['q2', 'c', 0, 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['q0', 'the (non)sense', 0., 0, 0],
                    ['q1', 'an ant', 0., 0, 0],
                    ['q2', 'the aardvark', 0., 0, 0],
                    ['q3', '\'a zebra\' doesn\'t lose its stripes', 0., 0, 0] ],
                columns=COLUMNS ) ]

        ignore_str_list = [ '', 'a |the | an' ]

        expected_sorted_score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['q1', 'a', 0, 0, 0],
                    ['q0', 'b', 0, 0, 0],
                    ['q2', 'c', 0, 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame(
                data=[ 
                    ['q1', 'a', 0, 0, 0],
                    ['q0', 'b', 0, 0, 0],
                    ['q2', 'c', 0, 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['q3', '\'a zebra\' doesn\'t lose its stripes', 0., 0, 0],
                    ['q1', 'an ant', 0., 0, 0],
                    ['q0', 'the (non)sense', 0., 0, 0],
                    ['q2', 'the aardvark',0., 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['q3', '\'a zebra\' doesn\'t lose its stripes', 0., 0, 0],
                    ['q0', 'the (non)sense', 0., 0, 0],
                    ['q2', 'the aardvark', 0., 0, 0],
                    ['q1', 'an ant', 0., 0, 0] ],
                columns=COLUMNS ) ]

        for (score_df, ignore_str), expected_sorted_score_df in zip(itertools.product(
            score_df_list, ignore_str_list), expected_sorted_score_df_list):
            
            sorted_score_df = sort_df(score_df, ignore_str)
            
            assert_frame_equal( sorted_score_df.reset_index(drop=True), expected_sorted_score_df )

            

        
