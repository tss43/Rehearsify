# main.py
# to treat directory as executable 

import os
import sys
import pandas as pd

from src.data_handling.file_handling import scan_available_language_pairs, read_score_df, create_score_df, save_score_df
from src.question_posing.question_selecting import select_randomly_weighed_question
from src.answer_handling.answer_handling import check_answer, update_score_df


rehearsify_dir = os.path.dirname(__file__)
dictionary_dir = os.path.join(rehearsify_dir, "Translation dictionaries")
pickle_dir = os.path.join(rehearsify_dir, "Translation dictionaries", ".metadata", "Pickled dictionaries")


def rehearse(to_language='Spanish', from_language='English'):
    """ Rehearse words from the dictionary specified by the user """
    
    # scan for available .txt dictionary files
    available_language_pairs = scan_available_language_pairs(rehearsify_dir)
    # available_to_languages, available_from_languages = list( zip(*available_transl) ) 

    if not isinstance(to_language, str) or not isinstance(from_language, str):
        raise TypeError("to-from languages should be strings")
    if (to_language, from_language) not in available_language_pairs:
        raise ValueError(f"to-from language combination should be any of {available_language_pairs}")
    print("Welcome to Rehearsify, a programme for practising foreign language words!\n")

    # read in pre-exiting score_df of specified languages, or create it from .txt dictionary file if not available
    score_df = read_score_df(pickle_dir, to_language, from_language) or create_score_df(dictionary_dir, to_language, from_language)

    # test words from specified dictionary. Exit upon 'q' or 'exit' user input
    user_answer = ''
    while user_answer.lower() != 'q' or user_answer.lower() != 'exit':

        correct_answer, question, n_wrong, n_total = select_randomly_weighed_question( score_df )
        user_answer = input( f"{question} = " )

        # check answer and update score_df, and if found wrong display correct answer
        answer_is_correct = check_answer( user_answer, correct_answer )
        if not answer_is_correct: 
            print( f"\t xxx \t {correct_answer} \t\t score={n_wrong+1}/{n_total+1}" )
        else:
            print( f"\t ooo \t {correct_answer} \t\t score={n_wrong}/{n_total+1}" )
        score_df = update_score_df( score_df, question, answer_is_correct )
    
    # once the user has chosen to exit, save the dataframe
    save_score_df( score_df, to_language, from_language ) 

# to enable executing module as script 
if __name__ == "__main__":
    args=sys.argv[1:]
    argc=len(args) 
    if argc not in [0,2]: 
        raise IndexError("can only give none or exactly two arguments from command line")
    else: 
        rehearse( *args )