# GUI_interacting/RehearsifyGUI.py

import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring

import pandas as pd

from src.data_handling.file_handling import read_dictionary_txtfile, update_with_df, save_as_dictionary_txtfile
from src.question_posing.question_selecting import select_randomly_weighed_question
from src.answer_handling.answer_handling import check_answer, update_sample
from src.translation_handling.find_sample import find_sample_from_question, find_sample_from_answer


MAX_LINES_DISPLAY = 5
COLUMNS = ['question', 'answer', 'wrong_perc', 'wrong', 'total']


class RehearsifyGUI:
    """ Class defining the RehearsifyGUI. """

    def __init__(self, window):
        """ Initialise object with the following attributes. """

        #instance attributes
        self.window = window
        self.practise_count = 0
        self.practise_wrong_count = 0
        self.counter_text = tk.StringVar( 
            window, value='session wrong/total: ' + str(self.practise_wrong_count) + '/' +str(self.practise_count) )

        self.score_df = pd.DataFrame()
        self.sample = pd.Series(['(questions)','(user input answers)',0,0,0], index=COLUMNS ) 
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
                self.log.heading('#1', text='XO', anchor=tk.CENTER)
                self.log.heading('#2', text='Question', anchor=tk.CENTER)
                self.log.heading('#3', text='User Answer', anchor=tk.CENTER)
                self.log.heading('#4', text='Correct Answer', anchor=tk.CENTER)
                self.log.heading('#5', text='Wrong/Total', anchor=tk.CENTER)

                self.log.column('#0', width=0,  stretch=tk.NO)
                self.log.column('#1', width=35, minwidth=35, stretch=tk.NO, anchor=tk.CENTER)
                self.log.column('#2', width=110, minwidth=110, stretch=tk.YES)
                self.log.column('#3', width=100, minwidth=100, stretch=tk.YES)
                self.log.column('#4', width=120, minwidth=120, stretch=tk.YES)
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

            self.log = ttk.Treeview( self.window, columns=('XO', 'Question', 'User answer', 'Correct answer', 'Wrong/Total') )
            initialise_log( self ) 

            self.counter = tk.Label( self.window, textvariable=self.counter_text )

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
        
            self.counter.grid(row=2, column=1, sticky='E', padx=5)
 
        # specify adaptive scaling behaviour of rows/columns
        self.window.title("Rehearsify - a language practising app")
        self.window.geometry("600x150")
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
        
        filepath = askopenfilename( filetypes=[("Pickle files", "*.pkl"), ("Text files", "*.txt")] )
        if not filepath:
            return
        elif filepath.endswith(".txt"):
            self.score_df = read_dictionary_txtfile( filepath )
        elif filepath.endswith(".pkl"):
            self.score_df = pd.read_pickle( filepath )
                    
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
        
        filepath = asksaveasfilename( defaultextension="pkl", filetypes=[("Pickle files", "*.pkl"), ("Text files", "*.txt")] )
        if not filepath:
            return
        elif filepath.endswith(".txt"):
            save_as_dictionary_txtfile( filepath, self.score_df )
        elif filepath.endswith(".pkl"):
            self.score_df.to_pickle(filepath)

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
        self.counter_text.set( 'session wrong/total: ' + str(self.practise_wrong_count) + '/' +str(self.practise_count) )

        # update score_df with new sample statistics
        self.score_df[ self.score_df['question']==self.sample.question ] = self.sample

        # update text widgets 
        update_vals = (
            f"{'ooo' if answer_is_correct else 'xxx'}",
            f"{self.sample.question}",
            f"{self.user_answer}",
            f"{self.sample.answer}",
            f"{self.sample.total-self.sample.wrong}/{self.sample.total}" )
        self.log.insert('', 1, values=update_vals )
        
        #if self.practise_count > 0:
        #    self.just_rehearsed_xo.delete(1.0, tk.END)
        #    self.just_rehearsed.delete(1.0, tk.END)
        #self.just_rehearsed_xo.insert(1.0, f"{'ooo' if answer_is_correct else 'xxx'}")
        #self.just_rehearsed.insert(1.0, f"{self.sample.question} = {self.user_answer}")
        #self.previous_rehearsed.insert(1.0, f"score={self.sample.total-self.sample.wrong}/{self.sample.total}\
        #       {self.sample.question} = { self.sample.answer}\n")
#
        # update prompt with newly selected question
        self.sample = select_randomly_weighed_question( self.score_df )
        self.question.set(self.sample.question)


    def lookup_question( self ):
        """Open new window with prompt for question for which the corresponding sample is then looked up."""

        question = askstring( "Question lookup", "Question for which to find the sample:" )
        self.sample = find_sample_from_question( self.score_df, question )

         # update text widget of previously rehearsed questions
        self.previous_rehearsed.insert(1.0, f"score={self.sample.total-self.sample.wrong}/{self.sample.total}\
            \t{self.sample.question} = { self.sample.answer}\n")


    def lookup_answer( self ):
        """Open new window with prompt for answer for which the corresponding sample is then looked up."""

        answer = askstring( "Answer lookup", "Answer for which to find the sample:" )
        self.sample = find_sample_from_answer( self.score_df, answer )

         # update text widget of previously rehearsed questions
        self.previous_rehearsed.insert(1.0, f"score={self.sample.total-self.sample.wrong}/{self.sample.total}\
            \t{self.sample.question} = { self.sample.answer}\n")



    


