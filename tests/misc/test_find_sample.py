# tests/misc/test_find_sample.py

import unittest
from pandas.testing import assert_series_equal      # for testing pandas series

import pandas as pd

from src.misc.find_sample import find_sample_from_answer, find_sample_from_question

from src.constants import COLUMNS

class TestFindSample(unittest.TestCase):
    """ Tests of finding samples. """
    
    def setUp(self):
        """ Initialise attributes available for tests in class. """
        self.score_df = pd.DataFrame(
            data=[
                ['question0', 'answer0', 100.*(1/1), 1, 1],
                ['question1', 'answer1', 0, 0, 0] ], 
            columns=COLUMNS ) 

    def tearDown(self):
        """ Deinitialise attributes available for tests in class. """
        self.score_df = None


    def test_find_sample_from_question(self):
        """ Testing finding a sample in the score df from a provided question. """

        found_sample = find_sample_from_question( self.score_df, question='question0' )
        expected_found_sample = pd.Series( data=['question0', 'answer0', 100.*(1/1), 1, 1], index=COLUMNS, name=0 )

        assert_series_equal( found_sample, expected_found_sample )


    def test_find_sample_from_answer(self):
        """ Testing finding a sample in the score df from a provided answer. """

        found_sample = find_sample_from_answer( self.score_df, answer='answer0' )
        expected_found_sample = pd.Series( data=['question0', 'answer0', 100.*(1/1), 1, 1], index=COLUMNS, name=0 )

        assert_series_equal( found_sample, expected_found_sample )