# command_line.py
""" provides supporting functionality callable from command line, beyond the main function """

import sys

import pandas as pd

from src.translation_handling.find_duplicates import find_duplicates
from src.data_handling.file_handling import read_dictionary_txtfile


def script_find_duplicates():
    """ Find duplicate questions within a given dictionary.
    INPUTS: 
            dictionary_fpath: str """

    if __name__ == "__main__":
        args=sys.argv[1:]
        argc=len(args) 
        if argc!=1: 
            raise IndexError("Usage: find_duplicates(dictionary_fpath: str) -> list[str]")
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

            print(f"Duplicate entries are\n: {duplicates_set}")