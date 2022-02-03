# command_line.py

import sys

import pandas as pd

from src.GUI_interacting.RehearsifyGUI import RehearsifyGUI
from src.misc.compute_statistics import compute_statistics
from src.misc.find_duplicates import find_duplicates

from src.data_handling.file_handling import read_dictionary_txtfile, validate_score_df


def script_rehearsify():
    """ To use the command line to open the main Rehearsify GUI window. """

    if __name__ == "scripts.command_line":       
        
        app = RehearsifyGUI() 
        app.window.mainloop() 


def script_compute_statistics():
    """ To use the command line to give some statistics of a dictionary.
    INPUTS: 
            dictionary_fpath: str """

    if __name__ == "scripts.command_line":       
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
                validate_score_df(score_df)
            except (KeyError, TypeError, ValueError) as e: 
                print(f"error {e!r}")
                return
            
            stats_dict = compute_statistics(score_df)

            for stat_name, stat_val in stats_dict.items():
                print(f"{stat_name}: {stat_val}")


def script_find_duplicates():
    """ To use the command line to find duplicate questions within a given dictionary.
    INPUTS: 
            dictionary_fpath: str """

    if __name__ == "scripts.command_line":       
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

