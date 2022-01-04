# command_line.py
""" provides supporting functionality callable from command line, beyond the main function """

import sys

import pandas as pd

from translation_handling.compute_statistics import compute_statitics
from translation_handling.find_duplicates import find_duplicates
from data_handling.file_handling import read_dictionary_txtfile


def script_compute_statistics():
    """ Give some statistics of a dictionary.
    INPUTS: 
            dictionary_fpath: str """

    if __name__ == "command_line":       
        args=sys.argv[1:]
        argc=len(args) 

        if argc!=1: 
            raise IndexError("Usage: print_statistics(dictionary_fpath: str) -> set[str]")
        else:
            dictionary_fpath = args[0]
            if not isinstance(dictionary_fpath, str):
                raise TypeError("Usage: fprint_statistics(dictionary_fpath: str) -> list[str]")
            elif dictionary_fpath.endswith(".txt"):
                score_df = read_dictionary_txtfile( dictionary_fpath )
            elif dictionary_fpath.endswith(".pkl"):
                score_df = pd.read_pickle( dictionary_fpath )
            else:
                raise ValueError("Usage: print_statistics('dictionary.txt') or print_statistics('dictionary.pkl')")
            
            stats_dict = compute_statitics(score_df)

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