# command_line.py
""" provides supporting functionality callable from command line """

import os
import sys

from data_handling.file_handling import scan_available_language_pairs, read_score_df, update_score_df
from translation_handling import find_sample_to_question

rehearsify_dir = os.path.join( os.path.dirname(__file__), os.pardir )
dictionary_dir = os.path.join( rehearsify_dir, "support", "Translation dictionaries" )
pickle_dir = os.path.join( rehearsify_dir, "support", ".metadata", "Pickled dictionaries" )


def script_translate():
    """ Find the translation for a question in a given from language to language dictionary.
    INPUTS: 
            to_language: str 
            from_language: str 
            question: str """
    
    if __name__ == "__main__":
        args=sys.argv[1:]
        argc=len(args) 
        if argc!=3: 
            raise IndexError("can only give exactly three arguments from command line")
        else: 
            to_language, from_language, question = list( *args )

            if not isinstance(to_language, str) or not isinstance(from_language, str):
                raise TypeError("to-from languages should be strings")
            if not isinstance(question, str):
                raise TypeError("question should be string")

            # scan for available .txt dictionary files
            available_language_pairs = scan_available_language_pairs(dictionary_dir)
            if (to_language, from_language) not in available_language_pairs:
                raise ValueError(f"to-from language combination should be any of {available_language_pairs}")

            # read in pre-exiting score_df of specified languages
            score_df = read_score_df(pickle_dir, to_language, from_language) 

            answer_sample = find_sample_to_question( score_df, question )
            print(f"Question:{question} in {from_language}-{to_language} dictionary")
            print(f"\t\t Sample: {answer_sample}")
        

    

    


