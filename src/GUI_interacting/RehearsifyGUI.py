# GUI_interacting/RehearsifyGUI.py

import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from typing import Callable

import pandas as pd

from functools import partial

from src.data_handling.file_handling import (
    read_dictionary_txtfile, update_with_df, save_as_dictionary_txtfile, 
    validate_score_df, validate_regex_str )
from src.translation_handling.sample_selecting import select_randomly_weighted_sample
from src.translation_handling.answer_handling import check_answer
from src.translation_handling.update_sample import add_correct_answer, update_sample_score, decrement_sample_wrong_score

from src.misc.df_sorting import no_sort_df, random_sort_df, sortby_num_df, sortby_str_df
from src.misc.find_sample import find_sample_from_question, find_sample_from_answer
from src.misc.compute_statistics import compute_statistics

from src.constants import COLUMNS, DISPLAY_COLUMNS


class RehearsifyGUI:
    """ Class defining the RehearsifyGUI. """

    def __init__( self, window ):
        """ Initialise object with the following attributes. """

        #instance attributes
        self.window = window
        self.initialise_var_attributes()       

        self.question = tk.StringVar( self.window, value='(questions)' )
        self.user_answer = tk.StringVar( self.window, value='(user input answers)' )

        # initialise the GUI
        self.initialise_GUI()
    
    #instance methods
    def initialise_var_attributes( self ):
        """Initialise the instance attributes."""

        self.score_df = pd.DataFrame( columns=COLUMNS )
        self.sample = pd.Series( index=COLUMNS ) 

        self.practise_count = 0
        self.practise_wrong_count = 0
        self.prev_practise_count = 0  
        self.prev_practise_wrong_count = 0
    
         
    def initialise_GUI( self ):
        """ Initialise the GUI. """
               
        def define_widgets( self ):
            """ Define the widgets. """
            
            self.button_frame = tk.Frame( self.window, relief='raised', bd=2 )
            self.btn_open = tk.Button( self.button_frame, text="Open", command=self.open_file )
            self.btn_update = tk.Button( self.button_frame, text="Update with...", command=self.update_file )
            self.btn_save = tk.Button( self.button_frame, text="Save as...", command=self.save_file )
            self.btn_lookup_question = tk.Button( self.button_frame, text="Lookup question", command=self.lookup_question )
            self.btn_lookup_answer = tk.Button( self.button_frame, text="Lookup answer", command=self.lookup_answer )
            self.btn_dictionary_stats = tk.Button( 
                self.button_frame, text="Dict statistics", command=self.display_dictionary_stats )
            
            self.question_answer_frame = tk.Frame( self.window, relief='raised', bd=2 )
            self.question_prompt = tk.Label( self.question_answer_frame, textvariable=self.question )
            self.equal_sign = tk.Label( self.question_answer_frame, text=" = " )
            self.answer_entry = tk.Entry( self.question_answer_frame, textvariable=self.user_answer  )
            self.answer_entry.bind( '<Return>', lambda event: self.process_answer() )    
            self.go_btn = tk.Button( self.question_answer_frame, text="Go", command = self.process_answer )

            self.log = ttk.Treeview( self.window, columns=DISPLAY_COLUMNS )
            self.initialise_log()

            self.lower_frame = tk.Frame( self.window )
            self.mark_correct_btn = tk.Button( self.lower_frame, text="Mark previous correct", command=self.mark_correct )
            self.counter = tk.Label( self.lower_frame, font=('', 10), text="session wrong/total practised: -/-" )
            self.stats = tk.Label( self.lower_frame, font=('', 10), text="overall wrong/total practised: -/-"  )
            

        def place_widgets_on_grid( self ):
            """ Place the widgets on the GUI grid. """
            self.button_frame.grid(row=0, column=0, rowspan=3, sticky='NSEW')
            self.button_frame.rowconfigure([0,1,2,4,5,6], weight=0)
            self.button_frame.rowconfigure(3, weight=1)
            self.button_frame.columnconfigure(0, minsize=150)
            self.btn_open.grid(row=0, column=0, padx=5)
    
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
            self.mark_correct_btn.grid(row=0, column=0, rowspan=2, sticky='W', padx=5)
            self.counter.grid(row=0, column=2, sticky='E', padx=5)
            self.stats.grid(row=1, column=2, sticky='E', padx=5)
            
 
        # specify adaptive scaling behaviour of rows/columns in main window
        self.window.title("Rehearsify - a language practising app")
        self.window.geometry("600x200")
        self.window.columnconfigure(0, weight=0)
        self.window.columnconfigure(1, weight=1)
        self.window.rowconfigure([0,2], weight=0)
        self.window.rowconfigure(1, weight=1)

        # define widgets
        define_widgets( self )

        # place widgets on grid
        place_widgets_on_grid( self )


    def initialise_log( self ):
        """ Initialise the log in the GUI. """
        
        self.log.heading('#0', text='', anchor=tk.CENTER)
        for col_idx, col in enumerate(DISPLAY_COLUMNS):
            self.log.heading(f'#{col_idx+1}', text=col, anchor=tk.CENTER)   
        
        self.log.column('#0', width=0,  stretch=tk.NO)
        self.log.column('#1', width=35, minwidth=35, stretch=tk.NO, anchor=tk.CENTER)
        self.log.column('#2', width=150, minwidth=150, stretch=tk.YES)
        self.log.column('#3', width=280, minwidth=280, stretch=tk.YES)
        self.log.column('#4', width=280, minwidth=280, stretch=tk.YES)
        self.log.column('#5', width=75, minwidth=75, stretch=tk.NO, anchor=tk.CENTER)


    def open_file( self ):
        """Open a dictionary file for practising."""
        
        filepath = askopenfilename( 
            filetypes=[("Pickle files", "*.pkl"), ("CSV files", "*.csv"), ("XLS files", ("*.xls")), 
            ("XLSX files", "*.xlsx"), ("Text files", "*.txt")] )
        if not filepath:
            return

        # reset attributes in case a file is opened on top of an old one. 
        if self.practise_count > 0:
            self.initialise_var_attributes()
            
            self.counter.config(text="session wrong/total practised: -/-")
            self.stats.config(text="overall wrong/total practised: -/-")

            # redefine and reinitialise the log to clear up the question/answers and their indices
            self.log = ttk.Treeview( self.window, columns=DISPLAY_COLUMNS )
            self.initialise_log()
            self.log.grid(row=1,column=1, sticky='NSEW', padx=5, pady=1 )
       
        try:
            if filepath.endswith(".txt"):
                self.score_df = read_dictionary_txtfile( filepath )
            elif filepath.endswith("csv"):
                self.score_df = pd.read_csv( filepath )
            elif filepath.endswith(".xls") | filepath.endswith(".xlsx"):
                self.score_df = pd.read_excel( filepath )
            elif filepath.endswith(".pkl"):
                self.score_df = pd.read_pickle( filepath )
            else:
                raise ValueError("This shouldn't happen.")    

            # validate opened score_df
            validate_score_df(self.score_df)
        except (KeyError, TypeError, ValueError) as e: 
            print(f"error {e!r}")
            return
        
        # keep only requisite columns
        self.score_df = self.score_df[COLUMNS]

        # update prompt with first selected question
        self.sample = select_randomly_weighted_sample( self.score_df )
        self.question.set(self.sample.question)
        
        # remove pre-initialisation default answer
        self.answer_entry.delete(0, tk.END)

        # set overall stats counter
        self.n_translations = self.score_df.shape[0] 
        self.prev_practise_wrong_count = self.score_df['wrong'].sum()
        self.prev_practise_count = self.score_df['total'].sum()
        self.stats.config( 
            text='overall wrong/total practised: ' \
            + str(self.prev_practise_wrong_count+self.practise_wrong_count) + '/' \
            + str(self.prev_practise_count+self.practise_count) )

        # update 'open' button text
        self.btn_open.config(text="Open new")  

        # add other buttons
        self.btn_update.grid(row=1, column=0, padx=5)
        self.btn_save.grid(row=2, column=0, padx=5)
        self.btn_lookup_question.grid(row=4, column=0, padx=5)
        self.btn_lookup_answer.grid(row=5, column=0, padx=5)
        self.btn_dictionary_stats.grid(row=6,column=0, padx=5)

        self.window.title(f"Rehearsify - {os.path.basename(filepath)}")
        

    def update_file( self ):
        """Update the file by adding new words from a .txt and removing words that are not in this .txt."""

        
        if ( filepath := askopenfilename( filetypes=[("Text files", "*.txt")] ) ):
            try:
                _update_df = read_dictionary_txtfile( filepath )
                # validate opened _update_df
                validate_score_df(_update_df)
            except (KeyError, TypeError, ValueError) as e: 
                print(f"error {e!r}")
                return
            self.score_df = update_with_df( self.score_df, _update_df )  


    def save_file( self ):
        """Save the current file as a new file."""

        # ask user for filepath
        if ( filepath := asksaveasfilename( 
            defaultextension="pkl", 
            filetypes=[("Pickle files", "*.pkl"), ("CSV files", "*.csv"), ("XLS files", "*.xls"), ("XLSX files", "*.xlsx"),
             ("Text files", "*.txt")] ) ): 
             
            sort_df_func = self.get_sort_func_from_sorting_popup()           
            _score_df = sort_df_func( self.score_df )
            
            if filepath.endswith(".txt"):
                save_as_dictionary_txtfile( filepath, _score_df )
            elif filepath.endswith(".csv"):
                _score_df.to_csv(filepath)
            elif filepath.endswith(".xls") | filepath.endswith(".xlsx"):
                _score_df.to_excel(filepath)
            elif filepath.endswith(".pkl"):
                _score_df.to_pickle(filepath)
            
            self.window.title(f"Rehearsify - {os.path.basename(filepath)}")


    def get_sort_func_from_sorting_popup( self ) -> Callable[[pd.DataFrame], pd.DataFrame]:
        """ Open the sorting pop up window. """
        
        self.sorting_popup = SortingPopUp( master=self.window )
        self.window.wait_window(self.sorting_popup.top)
        sort_df_func = self.sorting_popup.sort_df_func
        self.sorting_popup = None

        return sort_df_func


    def process_answer( self ):
        """Accept user input and process the answer, updating the score_df accordingly. Finally update the 
        prompt with a newly selected answer question. """

        # get user answer
        self.user_answer = self.answer_entry.get()
        self.answer_entry.delete(0, tk.END)

        # check answer and update sample
        answer_is_correct = check_answer( self.user_answer, self.sample.answer ) 
        self.sample = update_sample_score( self.sample, answer_is_correct )
        
        # update counter
        self.practise_count += 1 
        self.practise_wrong_count += not answer_is_correct 
        self.counter.config( 
            text='session wrong/total practised: ' + str(self.practise_wrong_count) + '/' + str(self.practise_count) )

        # update overall stats counter
        self.stats.config( 
            text='overall wrong/total practised: ' \
            + str(self.prev_practise_wrong_count+self.practise_wrong_count) + '/' \
            + str(self.prev_practise_count+self.practise_count) )
          
        # update score_df with new sample
        self.score_df[ self.score_df['question']==self.sample.question ] = self.sample

        # update log treeview widget
        update_dict = self.dict_to_insert_in_log(self.sample, self.user_answer, answer_is_correct) 
        self.log.insert('', index=0, iid=self.practise_count, values=list(update_dict.values()) )


        # select new question and update prompt
        self.sample = select_randomly_weighted_sample( self.score_df )
        self.question.set(self.sample.question)


    def lookup_question( self ):
        """Open new window with prompt for question for which the corresponding sample is then looked up."""
      
        if ( question := askstring( title="Question lookup", prompt="Question for which to find the sample:" ) ): 
            try:
                _sample = find_sample_from_question( self.score_df, question )        
                
                # update log treeview widget
                update_dict = self.dict_to_insert_in_log(_sample, "", None)  
                self.log.insert('', index=0, values=list(update_dict.values()) )

            except ValueError:
                print("Question not found.")


    def lookup_answer( self ):
        """Open new window with prompt for answer for which the corresponding sample is then looked up."""

        if ( answer := askstring( title="Answer lookup", prompt="Answer for which to find the sample:" ) ):
            try:
                _sample = find_sample_from_answer( self.score_df, answer )

                # update log treeview widget
                update_dict = update_dict = self.dict_to_insert_in_log(_sample, "", None)  
                self.log.insert('', index=0, values=list(update_dict.values()) )

            except ValueError:
                print("Question not found.")


    def display_dictionary_stats( self ):
        """Open new window displaying some general statistics about the translation dictionary."""
        
        stats_dict = compute_statistics(self.score_df)
        msg = '\n'.join([ ': '.join( [key, str(val)] ) for key, val in stats_dict.items() ] )
        showinfo( title="Translation dictionary statistics", message=msg )


    def mark_correct( self ):
        """Retroactively mark the previous answer as correct if it was false, and add it as a correct option."""
        
        previous_question = self.log.set( item=str(self.practise_count), column='Question' )
        previous_correct_answer = self.log.set( item=str(self.practise_count), column='Correct answer' )
        previous_user_answer = self.log.set( item=str(self.practise_count), column='User answer' )

        previous_user_answer_is_correct = check_answer( previous_user_answer, previous_correct_answer ) 
        
        # correct only if previous user anwer was not empty indeed marked as wrong 
        if previous_user_answer and not previous_user_answer_is_correct:
            
            # find sample belonging to previous question in score_df 
            _sample = self.score_df[ self.score_df['question']==previous_question ].sample( n=1 ).squeeze()
            
            # update sample and score_df
            _sample = add_correct_answer( _sample, previous_user_answer )
            _sample = decrement_sample_wrong_score( _sample )
            self.score_df[ self.score_df['question']==_sample.question ] = _sample

            # update counter
            self.practise_wrong_count -= not previous_user_answer_is_correct
            self.counter.config( 
                text='session wrong/total practised: ' + str(self.practise_wrong_count) + '/' + str(self.practise_count) )
            
            # update overall stats counter
            self.stats.config( 
                text='overall wrong/total practised: ' \
                + str(self.prev_practise_wrong_count+self.practise_wrong_count) + '/' \
                + str(self.prev_practise_count+self.practise_count) )

             # update log treeview widget
            update_dict = self.dict_to_insert_in_log( _sample, previous_user_answer, True )
            self.log.delete( str(self.practise_count) )
            self.log.insert( '', index=0, iid=str(self.practise_count), values=list(update_dict.values()) )

            # update the sample belonging to the current question if it was immediately repeated
            if previous_question==self.sample.question:
                self.sample = _sample 
    

    @staticmethod
    def dict_to_insert_in_log( sample: pd.Series, user_answer: str, answer_is_correct: bool|None ):
        """Combine some metrics into a dict whose values can easily be inserted into the log."""
        
        update_dict = {
            'X/O':              f"{'---' if answer_is_correct is None else 'ooo' if answer_is_correct else 'xxx'}",
            'Question':         f"{sample.question}",
            'Correct answer':   f"{sample.answer}",
            'User answer':      f"{user_answer}",
            'Wrong/total':      f"{sample.wrong}/{sample.total}" }
        
        return update_dict     
    


class SortingPopUp:
    """ Class defining the sorting option pop up. """

    def __init__( self, master ):
        """ Initialise object with the following attributes. """
        
        self.top = tk.Toplevel(master)
        self.top.title("Translation order for saving")

        # set default sorting function
        self.sort_df_func = no_sort_df

        # defining widgets
        self.lbl = tk.Label(self.top, text="""Preferred sorting order:""", justify = 'left')
        self.entry_question=tk.Entry(self.top, state='disabled')
        self.entry_answer=tk.Entry(self.top, state='disabled')

        btn_var = tk.IntVar(value=0)
        btn_texts = [
            "Sort in orginal order",
            "Sort in random order",
            "Sort by wrong percentage",
            "Sort alphabetically on answer, ignoring patterns (separated by '|'):",
            "Sort alphabetically on question, ignoring patterns (separated by '|'):" ]
        n_btns = len(btn_texts)

        self.radiobtns = [0]*n_btns
        for val, button_text in enumerate(btn_texts):
            self.radiobtns[val]=tk.Radiobutton(
                self.top, 
                text=button_text,
                padx=20, 
                variable=btn_var, 
                value=val,
                command=lambda: self.btn_parsing(self.entry_answer, self.entry_question, btn_var) )

        self.btn_frame = tk.Frame( self.top, relief='raised', bd=2 )
        self.btn_ok = tk.Button( self.btn_frame, text="OK", state='disabled', command=self.top.destroy )
        self.btn_cancel = tk.Button( self.btn_frame, text="Cancel", command=self.top.destroy )

        # placing popup widgets on grid
        self.lbl.grid(row=1,column=1, sticky='W', padx=0, pady=1)
        self.radiobtns[0].grid(row=2, column=1, sticky='W', padx=0, pady=1)
        self.radiobtns[1].grid(row=3, column=1, sticky='W', padx=0, pady=1)
        self.radiobtns[2].grid(row=4, column=1, sticky='W', padx=0, pady=1)
        self.radiobtns[3].grid(row=5, column=1, sticky='W', padx=0, pady=1)
        self.entry_answer.grid(row=6, column=1, sticky='NSEW', padx=0, pady=1)
        self.radiobtns[4].grid(row=7, column=1, sticky='W', padx=0, pady=1)
        self.entry_question.grid(row=8, column=1, sticky='NSEW', padx=0, pady=1)
        
        self.btn_frame.grid(row=9, column=1, sticky='NSEW', padx=0, pady=1)
        self.btn_frame.columnconfigure([1,3], weight=0)
        self.btn_frame.columnconfigure([0,2,4], weight=1)
        self.btn_ok.grid(row=0, column=1, padx=5)
        self.btn_cancel.grid(row=0, column=3, padx=5)


    #instance methods
    def btn_parsing(self, e1, e2, v):
        """ Parse the value yielded to v to obtain the appropriate sorting function, possibly further requiring a ignore string 
        to be given. """

        match v.get():
            case 0:
                self.sort_df_func = no_sort_df
                self.btn_ok.configure(state='normal')
                self.top.bind( '<Return>', lambda event: self.top.destroy() )
            case 1:
                self.sort_df_func = random_sort_df
                self.btn_ok.configure(state='normal')
                self.top.bind( '<Return>', lambda event: self.top.destroy() )
            case 2:
                self.sort_df_func = partial( sortby_num_df, sortby='wrong_perc' )
                self.btn_ok.configure(state='normal')
                self.top.bind( '<Return>', lambda event: self.top.destroy() )
            case 3:
                e1.configure(state='normal')
                e2.configure(state='disabled')
                
                self.sort_df_func = partial( sortby_str_df, sortby='answer' )
                self.btn_ok.configure(state='normal')
                self.top.bind( '<Return>', lambda event: self.top.destroy() )
                
                ignore_str=self.get_ignore_str_from_entry(e1)
                self.sort_df_func = partial( sortby_str_df, sortby='answer', ignore_str=ignore_str )
                self.top.destroy()
            case 4:
                e1.configure(state='disabled')
                e2.configure(state='normal')
                
                self.sort_df_func = partial( sortby_str_df, sortby='question' )
                self.btn_ok.configure(state='normal')
                self.top.bind( '<Return>', lambda event: self.top.destroy() )

                ignore_str=self.get_ignore_str_from_entry(e2)
                self.sort_df_func = partial( sortby_str_df, sortby='question', ignore_str=ignore_str )
                self.top.destroy()
    


    def get_ignore_str_from_entry(self, entry) -> str:
        """ Obtain a valid ignore string, only moving on upon clicking 'enter'.  """
        
        self.str = None
        self.str_is_entered = tk.BooleanVar(value=False)
        while self.str is None:
            try:
                entry.bind( '<Return>', lambda event: self.get_str_from_entry(entry=entry) )    
                self.top.wait_variable(self.str_is_entered)
                validate_regex_str( self.str )
            except ValueError as err: 
                print(f"error {err!r}")
                self.str = None
        
        ignore_str = self.str
        self.str = None
        self.str_is_entered = None

        return ignore_str


    def get_str_from_entry(self, entry):
        """ Get the ignore string from the entry widget, and flag that it was entered. """
        
        self.ignore_str = entry.get()
        self.str_is_entered.set(True)


    


