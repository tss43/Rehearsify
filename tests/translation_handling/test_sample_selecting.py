# tests/translation_handling/test_sample_selecting.py

import unittest
from pandas.testing import assert_series_equal      # for testing pandas series

import pandas as pd
import numpy as np

from src.translation_handling.sample_selecting import select_randomly_weighted_sample

from constants import COLUMNS

class TestSampleSelecting(unittest.TestCase):
    """ Tests of sample selecting. """

    def test_select_randomly_weighted_sample(self):
        """ Testing randomly selecting a sample. """

        score_df = pd.DataFrame(
            data = [
                ['test_question0', 'test_answer0', 15., 3, 20],
                ['test_question1', 'test_answer1', 10., 1, 10],
                ['test_question2', 'test_answer2', np.NaN, 0, 0],
                ['test_question3', 'test_answer3', 12.5, 1, 8] ],
            columns = COLUMNS )

        expected_selected_sample_list = [
            pd.Series( data=['test_question2', 'test_answer2', np.NaN, 0, 0], index = COLUMNS, name=2 ),
            pd.Series( data=['test_question1', 'test_answer1', 10., 1, 10], index = COLUMNS, name=1 ),
            pd.Series( data=['test_question1', 'test_answer1', 10., 1, 10], index = COLUMNS, name=1 ),
            pd.Series( data=['test_question2', 'test_answer2', np.NaN, 0, 0], index = COLUMNS, name=2 ),
            pd.Series( data=['test_question3', 'test_answer3', 12.5, 1, 8], index = COLUMNS, name=3 ),
            pd.Series( data=['test_question0', 'test_answer0', 15., 3, 20], index = COLUMNS, name=0 ),
            pd.Series( data=['test_question3', 'test_answer3', 12.5, 1, 8], index = COLUMNS, name=3 ),
            pd.Series( data=['test_question0', 'test_answer0', 15., 3, 20], index = COLUMNS, name=0 ),
            pd.Series( data=['test_question3', 'test_answer3', 12.5, 1, 8], index = COLUMNS, name=3 ),
            pd.Series( data=['test_question0', 'test_answer0', 15., 3, 20], index = COLUMNS, name=0 ) ]

        for seed, expected_selected_sample in enumerate(expected_selected_sample_list):
            randomly_weighted_selected_sample = select_randomly_weighted_sample(score_df, seed)

            assert_series_equal( randomly_weighted_selected_sample, expected_selected_sample )
