# GUI_interacting/RehearsifyGUI.py

# TO DO: 
#   - remove duplicates
#   - adding new translations

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring

import pandas as pd

from src.data_handling.file_handling import read_dictionary_txtfile, save_as_dictionary_txtfile
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
        self.score_df = pd.DataFrame()
        self.sample = pd.Series(['...','...',0,0,0], index=COLUMNS ) 
        self.question_text = tk.StringVar()
        self.question_text.set(self.sample.question)
        self.user_answer = ''

        # specify adaptive scaling behaviour of rows/columns
        window.title("Rehearsify - a language practising app")
        window.columnconfigure(0, minsize=50, weight=0)
        window.columnconfigure(1, minsize=100, weight=1)
        window.rowconfigure(0, minsize=50, weight=0)
        window.rowconfigure(1, minsize=100, weight=1)

        # define widgets
        self.button_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.btn_open = tk.Button( self.button_frame, text="Open", command=self.open_file )
        self.btn_save = tk.Button( self.button_frame, text="Save As...", command=self.save_file )
        self.btn_lookup_question = tk.Button( self.button_frame, text="Lookup question", command=self.lookup_question )
        self.btn_lookup_answer = tk.Button( self.button_frame, text="Lookup answer", command=self.lookup_answer )

        self.question_answer_frame = tk.Frame(window, relief=tk.RAISED, bd=2)
        self.question_prompt = tk.Label(self.question_answer_frame, textvariable=self.question_text )
        self.equal_sign = tk.Label(self.question_answer_frame, text= " = ")
        self.answer_entry = tk.Entry(self.question_answer_frame )
        self.answer_entry.bind('<Return>', self.process_answer ) 

        self.previous_rehearsed = tk.Text(window, height=MAX_LINES_DISPLAY)

        # place widgets on grid
        self.button_frame.grid(row=0, column=0, rowspan=2, sticky='NSEW')
        self.button_frame.rowconfigure([0,1,3,4], weight=0)
        self.button_frame.rowconfigure(2, minsize=25, weight=1)
        self.btn_open.grid(row=0, column=0, padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, padx=5, pady=5)
        self.btn_lookup_question.grid(row=3, column=0, padx=5, pady=5)
        self.btn_lookup_answer.grid(row=4, column=0, padx=5, pady=5)

        self.question_answer_frame.grid(row=0, column=1, sticky='NSEW')
        self.question_prompt.grid(row=0, column=0, sticky='NSEW', padx=3, pady=25)
        self.equal_sign.grid(row=0, column=1, sticky='NSEW', padx=3, pady=25)
        self.answer_entry.grid(row=0, column=2, sticky='NSEW', padx=3, pady=25)

        self.previous_rehearsed.grid(row=1, column=1, sticky='NSEW', padx=5, pady=5)

    #instance methods
    def open_file( self ):
        """Open a dictionary file for practising."""
        
        filepath = askopenfilename( filetypes=[("Text Files", "*.txt"), ("Pickle Files", "*.pkl")] )
        if not filepath:
            return
        elif filepath.endswith(".txt"):
            self.score_df = read_dictionary_txtfile( filepath )
        elif filepath.endswith(".pkl"):
            self.score_df = pd.read_pickle( filepath )
                    
        # update prompt with first selected question
        self.sample = select_randomly_weighed_question( self.score_df )
        self.question_text.set(self.sample.question)
        
        self.window.title(f"Rehearsify - {filepath}")


    def save_file( self ):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension="pkl",
            filetypes=[("Pickle Files", "*.pkl")],
        )
        if not filepath:
            return
        elif filepath.endswith(".txt"):
            self.score_df = save_as_dictionary_txtfile( filepath )
        elif filepath.endswith(".pkl"):
            self.score_df.to_pickle(filepath)

        self.window.title(f"Rehearsify - {filepath}")


    def process_answer( self, event=None ):
        """Accept user input and process the answer, updating the score_df accordingly. Finally update the 
        prompt with a newly selected answer question. """

        # get user answer
        self.user_answer = self.answer_entry.get()
        self.answer_entry.delete(0, tk.END)

        # check answer and update score_df, and if found wrong display correct answer
        answer_is_correct = check_answer( self.user_answer, self.sample.answer ) 
        self.sample = update_sample( self.sample, answer_is_correct )

        # update score_df with new sample statistics
        self.score_df[ self.score_df['question']==self.sample.question ] = self.sample

        # update text widget of previously rehearsed questions
        self.previous_rehearsed.insert(1.0, f"score={self.sample.total-self.sample.wrong}/{self.sample.total}\
            \t{self.sample.question} = { self.sample.answer}\n")

        # update prompt with newly selected question
        self.sample = select_randomly_weighed_question( self.score_df )
        self.question_text.set(self.sample.question)


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



    

