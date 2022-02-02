# command_line.py
""" provides supporting functionality callable from command line, beyond the main function """

import sys


import pandas as pd

from GUI_interacting.RehearsifyGUI import open_Rehearsify_GUI
from misc.compute_statistics import compute_statistics
from misc.find_duplicates import find_duplicates
from data_handling.file_handling import read_dictionary_txtfile

from constants import COLUMNS 

def script_rehearsify():
    """ Open the main Rehearsify GUI window. """

    if __name__ == "command_line":       
        open_Rehearsify_GUI() 


def script_compute_statistics():
    """ Give some statistics of a dictionary.
    INPUTS: 
            dictionary_fpath: str """

    if __name__ == "command_line":       
        args=sys.argv[1:]
        argc=len(args) 

        if argc!=1: 
            raise IndexError("Usage: print_statistics dictionary_fpath (=str) -> set[str]")
        else:
            dictionary_fpath = args[0]
            if not isinstance(dictionary_fpath, str):
                raise TypeError("Usage: fprint_statistics(dictionary_fpath: str) -> list[str]")
            elif dictionary_fpath.endswith(".txt"):
                score_df = read_dictionary_txtfile( dictionary_fpath )
            elif dictionary_fpath.endswith(".xls") | dictionary_fpath.endswith(".xlsx"):
                score_df = pd.read_excel( dictionary_fpath )
            elif dictionary_fpath.endswith(".pkl"):
                score_df = pd.read_pickle( dictionary_fpath )
            else:
                raise ValueError("Usage: print_statistics dictionary.txt/xls(x)/pkl")
            
            try:
                score_df = score_df[COLUMNS]
            except KeyError("Attempted to open a corrupted DataFrame."):
                print(f"Table should contain columns {COLUMNS}.")
            
            stats_dict = compute_statistics(score_df)

            for stat_name, stat_val in stats_dict.items():
                print(f"{stat_name}: {stat_val}")


def script_find_duplicates():
    """ Find duplicate questions within a given dictionary.
    INPUTS: 
            dictionary_fpath: str """

    if __name__ == "command_line":       
        args=sys.argv[1:]
        argc=len(args) 

        if argc!=1: 
            raise IndexError("Usage: find_duplicates(dictionary_fpath: str) -> set[str]")
        else:
            dictionary_fpath = args[0]
            if not isinstance(dictionary_fpath, str):
                raise TypeError("Usage: find_duplicates(dictionary_fpath: str) -> list[str]")
            elif dictionary_fpath.endswith(".txt"):
                score_df = read_dictionary_txtfile( dictionary_fpath )
            elif dictionary_fpath.endswith(".pkl"):
                score_df = pd.read_pickle( dictionary_fpath )
            else:
                raise ValueError("Usage: find_duplicates('dictionary.txt') or find_duplicates('dictionary.pkl')")
            
            duplicates_set = find_duplicates(score_df)

            if duplicates_set:
                print(f"Duplicate question entries are:\n {duplicates_set}")
            else:
                print("No duplicate questions found!")