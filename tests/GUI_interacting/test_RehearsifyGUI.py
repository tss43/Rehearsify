# tests/GUI_interacting/RehearsifyGUI.py


import unittest

import pandas as pd
from itertools import product as cartprod

import tkinter as tk

from src.translation_handling.answer_handling import check_answer
from src.GUI_interacting.RehearsifyGUI import RehearsifyGUI, SortingPopUp


from src.constants import COLUMNS, DISPLAY_COLUMNS

class TestRehearsifyGUI(unittest.TestCase):
    """ Tests on RehearsifyGUI methods. """

    def assertHasAttr(self, obj, intendedAttr):
        """ Custom assert method to establish if instance has attribute. """
        testBool = hasattr(obj, intendedAttr)
        self.assertTrue(testBool, msg=f'obj lacking an attribute. {obj=}, {intendedAttr=}')

    def setUp(self):
        """ Hook method for setting up the test fixture before exercising it. """
        self.root = tk.Tk()
        self.app = RehearsifyGUI(window=self.root)

    def tearDown(self):
        """ Hook method for deconstructing the test fixture after testing it. """
        self.root.destroy()
        self.app = None
        

    def test_dynamic_attributes(self):
        """ Testing if app instance has appropriate dynamic attributes. """

        for dynamic_attr in ['window', 'question', 'user_answer']:
            self.assertHasAttr( self.app, dynamic_attr )

    def test_initialise_var_attributes(self):
        """ Testing if app instance has appropriate variable attributes. """

        for var_attr in [
            'score_df', 'sample', 'practise_count', 'practise_wrong_count', 'prev_practise_count', 'prev_practise_wrong_count']:
            self.assertHasAttr( self.app, var_attr )

    def test_initialise_GUI(self):
        """ Testing if the app instance has appropriate GUI elements. """

        for var_attr in [
            'button_frame', 'btn_open', 'btn_update', 'btn_save', 'btn_lookup_question', 'btn_lookup_answer', 'btn_dictionary_stats',
            'question_answer_frame', 'question_prompt', 'equal_sign', 'answer_entry', 'go_btn', 'log', 'lower_frame', 
            'mark_correct_btn', 'counter', 'stats' ]:
            self.assertHasAttr( self.app, var_attr )

    def test_methods(self):
        """ Testing if app instance has appropriate methods. """

        for method in [
            'initialise_var_attributes', 'initialise_GUI', 'initialise_log', 'open_file', 'update_file', 'save_file', 
            'get_sort_func_from_sorting_popup', 'process_answer', 'lookup_question', 'lookup_answer', 'display_dictionary_stats', 
            'mark_correct' ]:
            self.assertHasAttr( self.app, method )
            

class TestLogInsertionDict(unittest.TestCase):
    """ Tests on the dict used to insert new entries into RehearsifyGUI objects. """

    def test_keys_of_dict_to_insert_in_log(self):
        """ Test if the dict to insert has appropriate keys. """ 
        
        expected_keys = DISPLAY_COLUMNS

        user_answer_list = [ 'test_answer_0', 'wrong_test_answer' ]
        sample_list = [
            pd.Series(data=['test_question0', 'test_answer0', 50., 1, 2], index=COLUMNS),
            pd.Series(data=['test_question1', 'test_answer1', 25., 1, 4], index=COLUMNS) ]
        
        for user_answer, sample in cartprod(user_answer_list, sample_list):
            
            answer_is_correct = check_answer( user_answer, sample.answer ) 
            test_dict = RehearsifyGUI.dict_to_insert_in_log( sample, user_answer, answer_is_correct )
    
            with self.subTest(f"list( {test_dict}.keys() ) -> {expected_keys}"): 

                self.assertEqual( list( test_dict.keys() ), expected_keys )


class TestSortingPopUp(unittest.TestCase):
    """ Tests on SortingPopUp methods. """

    def assertHasAttr(self, obj, intendedAttr):
        """ Custom assert method to establish if instance has attribute. """
        testBool = hasattr(obj, intendedAttr)
        self.assertTrue(testBool, msg=f'obj lacking an attribute. {obj=}, {intendedAttr=}')

    def setUp(self):
        """ Hook method for setting up the test fixture before exercising it. """
        self.master = tk.Tk()
        self.popup = SortingPopUp(master=self.master)

    def tearDown(self):
        """ Hook method for deconstructing the test fixture after testing it. """
        self.master.destroy()
        self.popup = None

    def test_initialise_var_attributes(self):
        """ Testing if app instance has appropriate attributes. """

        for attr in [
            'top', 'sort_df_func', 'lbl', 'entry_question', 'entry_answer', 'radiobtns', 'btn_frame', 'btn_ok', 'btn_cancel']:
            self.assertHasAttr( self.popup, attr )

    def test_methods(self):
        """ Testing if app instance has appropriate methods. """

        for method in [
            'btn_parsing', 'get_ignore_str_from_entry', 'get_str_from_entry' ]:
            self.assertHasAttr( self.popup, method )

    

