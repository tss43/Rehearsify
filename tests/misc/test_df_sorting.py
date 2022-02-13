# tests/misc/test_df_sorting.py

import unittest
from pandas.testing import assert_frame_equal      # for testing dataframes

import numpy as np
import pandas as pd
from itertools import product as cartprod

from src.misc.df_sorting import no_sort_df, random_sort_df, sortby_num_df, sortby_str_df

from src.constants import COLUMNS

class TestDfSorting(unittest.TestCase):
    """ Tests of the sorting of the score df. """
    
    def setUp(self):
        """ Hook method for setting up the test fixture before exercising it. """
        self.score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['b', 'q0', np.NaN, 0, 0],
                    ['a', 'q1', 100., 1, 1],
                    ['c', 'q2', 50., 2, 4] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['the (non)sense', 'q0', 10., 1, 10],
                    ['an ant', 'q1', 20., 1, 5],
                    ['the aardvark', 'q2', 30., 3, 10],
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 40., 4, 10] ],
                columns=COLUMNS ) ]


    def tearDown(self):
        """ Hook method for deconstructing the test fixture after testing it. """
        self.score_df_list = None

    def test_no_sort_df(self):
        """ Testing not sorting a dataframe at all. """

        expected_not_sorted_score_df_list = self.score_df_list

        for score_df, expected_not_sorted_score_df in zip(self.score_df_list, expected_not_sorted_score_df_list):
            not_sorted_score_df = no_sort_df(score_df)
            assert_frame_equal( not_sorted_score_df, expected_not_sorted_score_df )   


    def test_random_sort_df(self):
        """ Testing the random sorting of a dataframe. """

        seed = 1

        expected_sorted_score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['b', 'q0', np.NaN, 0, 0],
                    ['c', 'q2', 50., 2, 4],
                    ['a', 'q1', 100., 1, 1] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 40., 4, 10],
                    ['the aardvark', 'q2', 30., 3, 10],
                    ['the (non)sense', 'q0', 10., 1, 10],
                    ['an ant', 'q1', 20., 1, 5] ],
                columns=COLUMNS ) ]

        for score_df, expected_sorted_score_df in zip(self.score_df_list, expected_sorted_score_df_list):

            sorted_score_df = random_sort_df(df=score_df, seed=seed)
            
            with self.subTest(f"{sorted_score_df} -> {expected_sorted_score_df}"): 
                assert_frame_equal( sorted_score_df.reset_index(drop=True), expected_sorted_score_df )


    def test_sortby_num_df(self):
        """ Testing the sorting of a dataframe on a numerical column. """

        sortby_list = ['wrong_perc', 'total']

        expected_sorted_score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['c', 'q2', 50., 2, 4],
                    ['a', 'q1', 100., 1, 1],
                    ['b', 'q0', np.NaN, 0, 0] ],
                columns=COLUMNS ),
            pd.DataFrame(
                data=[ 
                    ['b', 'q0', np.NaN, 0, 0],
                    ['a', 'q1', 100., 1, 1],
                    ['c', 'q2', 50., 2, 4] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['the (non)sense', 'q0', 10., 1, 10],
                    ['an ant', 'q1', 20., 1, 5],
                    ['the aardvark', 'q2', 30., 3, 10],
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 40., 4, 10] ],
                columns=COLUMNS ),
                pd.DataFrame( 
                data=[
                    ['an ant', 'q1', 20., 1, 5],
                    ['the (non)sense', 'q0', 10., 1, 10],
                    ['the aardvark', 'q2', 30., 3, 10],
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 40., 4, 10] ],
                columns=COLUMNS ) ]

        for (score_df, sortby), expected_sorted_score_df in zip(
            cartprod(self.score_df_list, sortby_list), expected_sorted_score_df_list):

            sorted_score_df = sortby_num_df(df=score_df, sortby=sortby)
            
            with self.subTest(f"{sorted_score_df} -> {expected_sorted_score_df}"): 
                assert_frame_equal( sorted_score_df.reset_index(drop=True), expected_sorted_score_df )


    def test_sortby_str_df(self):
        """ Testing the sorting of a dataframe on a string column. """

        answer_ignore_str_list = [ '', 'a |the | an' ]

        expected_sorted_score_df_list = [
            pd.DataFrame(
                data=[ 
                    ['a', 'q1', 100., 1, 1],
                    ['b', 'q0', np.NaN, 0, 0],
                    ['c', 'q2', 50., 2, 4] ],
                columns=COLUMNS ),
            pd.DataFrame(
                data=[ 
                    ['a', 'q1', 100., 1, 1],
                    ['b', 'q0', np.NaN, 0, 0],
                    ['c', 'q2', 50., 2, 4] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 40., 4, 10],
                    ['an ant', 'q1', 20., 1, 5],
                    ['the (non)sense', 'q0', 10., 1, 10],
                    ['the aardvark', 'q2', 30., 3, 10] ],
                columns=COLUMNS ),
            pd.DataFrame( 
                data=[
                    ['\'a zebra\' doesn\'t lose its stripes', 'q3', 40., 4, 10],
                    ['the (non)sense', 'q0', 10., 1, 10],
                    ['the aardvark', 'q2', 30., 3, 10],
                    ['an ant', 'q1', 20., 1, 5] ],
                columns=COLUMNS ) ]

        for (score_df, answer_ignore_str), expected_sorted_score_df in zip(
            cartprod(self.score_df_list, answer_ignore_str_list), expected_sorted_score_df_list):

            sorted_score_df = sortby_str_df(df=score_df, sortby='answer', ignore_str=answer_ignore_str)
            
            with self.subTest(f"{sorted_score_df} with ignore_str {answer_ignore_str} -> {expected_sorted_score_df}"): 
                assert_frame_equal( sorted_score_df.reset_index(drop=True), expected_sorted_score_df )

            

        
