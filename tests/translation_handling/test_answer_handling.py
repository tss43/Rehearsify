# tests/translation_handling/test_answer_handling.py

import unittest

import itertools

from src.translation_handling.answer_handling import check_answer, explode_answer

class TestAnswerHandling(unittest.TestCase):
    """ Tests of answer handling. """

    def setUp(self):
        """ Initialise attributes available for tests in class. """
        self.correct_answer_list = [ 
            'a00 (b0) a01; á1,0(b1).á11', 
            'a0 (b0); á1,(b1)',
            '(b0) a0; (b1).á1' ]

    def tearDown(self):
        """ Deinitialise attributes available for tests in class. """
        self.answer_list = None


    def test_explode_answer(self):
        """ Testing exploding an answer out into a list of possible answers. """

        expected_exploded_answer_list = [
            {'a00 b0 a01', 'a00 a01', 'a10b1a11', 'a10a11'},
            {'a0 b0', 'a0', 'a1b1', 'a1'},
            {'b0 a0', 'a0', 'b1a1', 'a1'} ]

        for answer, expected_exploded_answer in zip( self.correct_answer_list, expected_exploded_answer_list):
            exploded_answer = explode_answer( answer)
            
            with self.subTest(f"{exploded_answer} -> {expected_exploded_answer}"): 
                self.assertEqual(exploded_answer, expected_exploded_answer)


    def test_check_answer(self):
        """ Testing checking an answer against the correct answer. """

        answer_list = [ 
            'a00 a01', 
            'a_wrong',
            '(b_wrong) a0' ]

        expected_answer_is_correct_list = [True, False, True]

        for answer, correct_answer, expected_answer_is_correct in zip(
            answer_list, self.correct_answer_list, expected_answer_is_correct_list ):
            
            answer_is_correct = check_answer(answer, correct_answer)

            with self.subTest(f"{answer} <> {correct_answer} = {answer_is_correct} -> {expected_answer_is_correct}"): 
                self.assertEqual(answer_is_correct, expected_answer_is_correct)