# tests/data_handling/test_file_handling.py

import unittest
from pandas.testing import assert_frame_equal      # for testing dataframes

import os
import pandas as pd
import numpy as np

from src.data_handling.file_handling import read_dictionary_txtfile, save_as_dictionary_txtfile, update_with_df

from constants import COLUMNS

class FileHandling(unittest.TestCase):
    """ Tests of handling files. """
    
    def setUp(self):
        """ Initialise attributes available for tests in class. """
        self.score_df = pd.DataFrame(
            data=[
                ['question0', 'answer0', 100.*(1/1), 1, 1],
                ['question1', 'answer1', 0, 0, 0] ], 
            columns=COLUMNS ) 
        self.fpath_dictionary_txt = os.path.join( os.path.dirname(__file__), 'mock_dictionary.txt' )
        
        save_as_dictionary_txtfile( self.fpath_dictionary_txt, self.score_df )


    def tearDown(self):
        """ Deinitialise attributes available for tests in class. """
        self.score_df = None
        os.remove( self.fpath_dictionary_txt )


    def test_read_dictionary_txtfile(self):
        """ Testing reading in a score_df from a .txt. Note that the .txt only contains the translations, 
        not the corresponding statistics. """

        read_score_df = read_dictionary_txtfile( self.fpath_dictionary_txt )
        zero_dict = {COLUMNS[2]: np.NaN, COLUMNS[3]: 0, COLUMNS[4]: 0}
        expected_read_score_df = self.score_df[COLUMNS[:2]].assign(**zero_dict)

        assert_frame_equal( read_score_df, expected_read_score_df )


    def test_save_as_dictionary_txtfile(self):
        """ Testing saving a score_df to a .txt. """
        
        save_as_dictionary_txtfile( self.fpath_dictionary_txt, self.score_df )
        saved_score_df = read_dictionary_txtfile( self.fpath_dictionary_txt )

        expected_saved_score_df = read_dictionary_txtfile( self.fpath_dictionary_txt )

        assert_frame_equal( saved_score_df, expected_saved_score_df )


    def test_update_with_df(self):
        """ Testing the updating of a score df with another. """

        add_df = pd.DataFrame( 
            data=[
                ['question0', 'answer0', 0, 0, 0],
                ['question_new', 'answer_new', 0, 0, 0] ], 
            columns=COLUMNS ) 

        expected_updated_score_df = pd.DataFrame( 
            data=[
                ['question0', 'answer0', 100.*(1/1), 1, 1],
                ['question_new', 'answer_new', 0, 0, 0] ], 
            columns=COLUMNS ) 

        updated_score_df = update_with_df( self.score_df, add_df )

        assert_frame_equal( updated_score_df, expected_updated_score_df )
