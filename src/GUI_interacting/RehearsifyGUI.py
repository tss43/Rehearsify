# GUI_interacting/RehearsifyGUI.py

import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring

import numpy as np
import pandas as pd

from src.data_handling.file_handling import read_dictionary_txtfile, update_with_df, save_as_dictionary_txtfile
from src.translation_handling.question_selecting import select_randomly_weighed_question
from src.translation_handling.answer_handling import check_answer, update_sample
from src.translation_handling.update_dataframe import add_correct_answer, decrement_wrong_score

from src.misc.df_sorting import sort_df
from src.misc.find_sample import find_sample_from_question, find_sample_from_answer

from src.constants import COLUMNS


class RehearsifyGUI:
    """ Class defining the RehearsifyGUI. """

    def __init__(self, window):
        """ Initialise object with the following attributes. """

        #instance attributes
        self.window = window
        self.practise_count = 0
        self.practise_wrong_count = 0
        self.counter_text = tk.StringVar( 
            window, value='session wrong/total: ' + str(self.practise_wrong_count) + '/' + str(self.practise_count) )

        self.score_df = pd.DataFrame()
        self.sample = pd.Series(['(questions)','(user input answers)', np.NaN,0,0], index=COLUMNS ) 
        self.question = tk.StringVar( window, value=self.sample.question )
        self.user_answer = tk.StringVar( window, value=self.sample.answer )

        # initialise the GUI
        self.initialise_GUI()
 

    #instance methods
    def initialise_GUI( self ):
        """ Initialise the GUI. """
               
        def define_widgets( self ):
            """ Define the widgets. """

            def initialise_log( self ):
                """ Initialise the log in the GUI. """
                self.log.heading('#0', text='', anchor=tk.CENTER)
                self.log.heading('#1', text='X/O', anchor=tk.CENTER)
                self.log.heading('#2', text='Question', anchor=tk.CENTER)
                self.log.heading('#3', text='Correct answer', anchor=tk.CENTER)
                self.log.heading('#4', text='User answer', anchor=tk.CENTER)
                self.log.heading('#5', text='Wrong/total', anchor=tk.CENTER)

                self.log.column('#0', width=0,  stretch=tk.NO)
                self.log.column('#1', width=35, minwidth=35, stretch=tk.NO, anchor=tk.CENTER)
                self.log.column('#2', width=150, minwidth=150, stretch=tk.YES)
                self.log.column('#3', width=280, minwidth=280, stretch=tk.YES)
                self.log.column('#4', width=280, minwidth=280, stretch=tk.YES)
                self.log.column('#5', width=75, minwidth=75, stretch=tk.NO, anchor=tk.CENTER)

            self.button_frame = tk.Frame(self.window, relief=tk.RAISED, bd=2)
            self.btn_open = tk.Button( self.button_frame, text="Open", command=self.open_file )
            self.btn_update = tk.Button( self.button_frame, text="Update with...", command=self.update_file )
            self.btn_save = tk.Button( self.button_frame, text="Save as...", command=self.save_file )
            self.btn_lookup_question = tk.Button( self.button_frame, text="Lookup question", command=self.lookup_question )
            self.btn_lookup_answer = tk.Button( self.button_frame, text="Lookup answer", command=self.lookup_answer )

            self.question_answer_frame = tk.Frame( self.window, relief=tk.RAISED, bd=2 )
            self.question_prompt = tk.Label( self.question_answer_frame, textvariable=self.question )
            self.equal_sign = tk.Label( self.question_answer_frame, text=" = " )
            self.answer_entry = tk.Entry( self.question_answer_frame, textvariable=self.user_answer  )
            self.answer_entry.bind( '<Return>', self.process_answer )    
            self.go_btn = tk.Button( self.question_answer_frame, text="Go", command = self.process_answer )

            self.log = ttk.Treeview( 
                self.window, columns=('X/O', 'Question', 'Correct answer', 'User answer', 'Wrong/total') )
            initialise_log( self ) 

            self.lower_frame = tk.Frame( self.window )
            self.mark_correct_btn = tk.Button( self.lower_frame, text="Mark previous correct", command=self.mark_correct )
            self.counter = tk.Label( self.lower_frame, textvariable=self.counter_text )
            

        def place_widgets_on_grid( self ):
            """ Place the widgets on the GUI grid. """
            self.button_frame.grid(row=0, column=0, rowspan=3, sticky='NSEW')
            self.button_frame.rowconfigure([0,1,3,4], weight=0)
            self.button_frame.rowconfigure(2, minsize=25, weight=1)
            self.btn_open.grid(row=0, column=0, padx=5)
            self.btn_save.grid(row=1, column=0, padx=5)
            self.btn_lookup_question.grid(row=3, column=0, padx=5)
            self.btn_lookup_answer.grid(row=4, column=0, padx=5)
    
            self.question_answer_frame.grid(row=0, column=1, sticky='NSEW' )
            self.question_answer_frame.columnconfigure([0,1,3], weight=0)
            self.question_answer_frame.columnconfigure(2, weight=1)
            self.question_prompt.grid(row=0, column=0, sticky='NSEW', padx=1, pady=15)
            self.equal_sign.grid(row=0, column=1, sticky='NSEW', padx=1, pady=15)
            self.answer_entry.grid(row=0, column=2, sticky='NSEW', padx=1, pady=15)
            self.go_btn.grid(row=0, column=3, sticky='NSEW', padx=1, pady=15)
    
            self.log.grid(row=1,column=1, sticky='NSEW', padx=5, pady=1 )
        
            self.lower_frame.grid(row=2,column=1, sticky='NSEW')
            self.lower_frame.columnconfigure([0,2], weight=0)
            self.lower_frame.columnconfigure(1, weight=1)
            self.mark_correct_btn.grid(row=0, column=0, sticky='W', padx=5)
            self.counter.grid(row=0, column=2, sticky='E', padx=5)
            
 
        # specify adaptive scaling behaviour of rows/columns in main window
        self.window.title("Rehearsify - a language practising app")
        self.window.geometry("600x200")
        self.window.columnconfigure(0, weight=0)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure(0, weight=0)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=0)

        # define widgets
        define_widgets( self )

        # place widgets on grid
        place_widgets_on_grid( self )

        
    def open_file( self ):
        """Open a dictionary file for practising."""
        
        filepath = askopenfilename( 
            filetypes=[("Pickle files", "*.pkl"), ("CSV files", "*.csv"), ("XLS files", "*.xls"), ("XLSX files", "*.xlsx"), 
            ("Text files", "*.txt")] )
        if not filepath:
            return
        elif filepath.endswith(".txt"):
            self.score_df = read_dictionary_txtfile( filepath )
        elif filepath.endswith("csv"):
            self.score_df = pd.read_csv( filepath )
        elif filepath.endswith(".xls") | filepath.endswith(".xlsx"):
            self.score_df = pd.read_excel( filepath )
        elif filepath.endswith(".pkl"):
            self.score_df = pd.read_pickle( filepath )

        try:
            self.score_df = self.score_df[COLUMNS]
        except KeyError("Attempted to open a corrupted DataFrame."):
            print(f"Table should contain columns {COLUMNS}.")

        # update prompt with first selected question
        self.sample = select_randomly_weighed_question( self.score_df )
        self.question.set(self.sample.question)
        
        # remove pre-initialisation default answer
        self.answer_entry.delete(0, tk.END)

        # replace 'open' button with 'update...' button in GUI window
        self.btn_open.grid_remove() 
        self.btn_update.grid(row=0, column=0, padx=5)

        self.window.title(f"Rehearsify - {os.path.basename(filepath)}")
        

    def update_file( self ):
        """Update the file by adding new words from a .txt and removing words that are not in this .txt """

        filepath = askopenfilename( filetypes=[("Text files", "*.txt")] )
        if not filepath:
            return
        elif filepath.endswith(".txt"):
            _temp_df = read_dictionary_txtfile( filepath )
            self.score_df = update_with_df( self.score_df, _temp_df )  


    def save_file( self ):
        """Save the current file as a new file."""

        # ask user for filepath
        filepath = asksaveasfilename( 
            defaultextension="pkl", 
            filetypes=[("Pickle files", "*.pkl"), ("CSV files", "*.csv"), ("XLS files", "*.xls"), ("XLSX files", "*.xlsx"),
             ("Text files", "*.txt")] )
        if not filepath:
            return
        else:
             # sort score_df by answer, ignoring the regex obtained from the user
            ignore_str = askstring( 
                "Translation ordering for saving", "Strings to ignore in sorting translations (separated by ' | '):" )
            _score_df = sort_df( self.score_df, ignore_str )
            
            if filepath.endswith(".txt"):
                save_as_dictionary_txtfile( filepath, _score_df )
            elif filepath.endswith(".csv"):
                _score_df.to_csv(filepath)
            elif filepath.endswith(".xls") | filepath.endswith(".xlsx"):
                _score_df.to_excel(filepath)
            elif filepath.endswith(".pkl"):
                _score_df.to_pickle(filepath)
            
        self.window.title(f"Rehearsify - {os.path.basename(filepath)}")


    def process_answer( self, event=None ):
        """Accept user input and process the answer, updating the score_df accordingly. Finally update the 
        prompt with a newly selected answer question. """

        # get user answer
        self.user_answer = self.answer_entry.get()
        self.answer_entry.delete(0, tk.END)

        # check answer and update score_df
        answer_is_correct = check_answer( self.user_answer, self.sample.answer ) 
        self.sample = update_sample( self.sample, answer_is_correct )
        
        # update counter
        self.practise_count += 1 
        self.practise_wrong_count += not answer_is_correct 
        self.counter_text.set( 
            'session wrong/total: ' + str(self.practise_wrong_count) + '/' + str(self.practise_count) )

        # update score_df with new sample statistics
        self.score_df[ self.score_df['question']==self.sample.question ] = self.sample

        # update log treeview widget
        update_dict = {
            'X/0':              f"{'ooo' if answer_is_correct else 'xxx'}",
            'Question':         f"{self.sample.question}",
            'Correct answer':   f"{self.sample.answer}",
            'User answer':      f"{self.user_answer}",
            'Wrong/total':      f"{self.sample.wrong}/{self.sample.total}" }
        self.log.insert('', index=0, iid=self.practise_count, values=list(update_dict.values()) )

        # update prompt with newly selected question
        self.sample = select_randomly_weighed_question( self.score_df )
        self.question.set(self.sample.question)


    def lookup_question( self ):
        """Open new window with prompt for question for which the corresponding sample is then looked up."""

        question = askstring( "Question lookup", "Question for which to find the sample:" )
        self.sample = find_sample_from_question( self.score_df, question )

        self.practise_count += 1

        # update log treeview widget
        update_dict = {
            'X/0':              "---",
            'Question':         f"{self.sample.question}",
            'Correct answer':   f"{self.sample.answer}",
            'User answer':      "---",
            'Wrong/total':      f"{self.sample.wrong}/{self.sample.total}" }
        self.log.insert('', index=0, iid=str(self.practise_count), values=list(update_dict.values()) )


    def lookup_answer( self ):
        """Open new window with prompt for answer for which the corresponding sample is then looked up."""

        answer = askstring( "Answer lookup", "Answer for which to find the sample:" )
        self.sample = find_sample_from_answer( self.score_df, answer )

        self.practise_count += 1

        # update log treeview widget
        update_dict = {
            'X/0':              "---",
            'Question':         f"{self.sample.question}",
            'Correct answer':   f"{self.sample.answer}",
            'User answer':      "---",
            'Wrong/total':      f"{self.sample.wrong}/{self.sample.total}" }
        self.log.insert('', index=0, iid=str(self.practise_count), values=list(update_dict.values()) )


    def mark_correct( self ):
        """Retroactively mark the previous answer as correct if it was false, and add it as a correct option."""
        
        previous_question = self.log.set( item=str(self.practise_count), column='Question' )
        previous_correct_answer = self.log.set( item=str(self.practise_count), column='Correct answer' )
        previous_user_answer = self.log.set( item=str(self.practise_count), column='User answer' )
        
        previous_answer_is_correct = check_answer( previous_user_answer, previous_correct_answer ) 
        if not previous_answer_is_correct:
            
            # update score_df
            self.score_df = add_correct_answer( self.score_df, previous_question, previous_user_answer )
            self.score_df = decrement_wrong_score( self.score_df, previous_question )
            
            # update counter
            self.practise_wrong_count -= not previous_answer_is_correct
            self.counter_text.set( 
                'session wrong/total: ' + str(self.practise_wrong_count) + '/' + str(self.practise_count) )
            
             # update log treeview widget
            _sample = self.score_df[ self.score_df['question'].str.match(previous_question) ].squeeze()
            update_dict = {
                'X/0':              "ooo",
                'Question':         f"{_sample.question}",
                'Correct answer':   f"{_sample.answer}",
                'User answer':      f"{previous_user_answer}",
                'Wrong/total':      f"{_sample.wrong}/{_sample.total}" }
            self.log.delete( str(self.practise_count) )
            self.log.insert('', index=0, iid=str(self.practise_count), values=list(update_dict.values()) )


        
        




    


