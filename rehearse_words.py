import sys
import pandas as pd

from file_handling import scan_dictionaries, read_words, read_score_df, save_score_df
from select_word import select_random_weighted_word
from answer_handling import check_answer, update_score_df

def rehearse(to_language='Spanish', from_language='English'):
    """ rehearse words from the dictionary specified by the user """
    
    # scan for available dictionary files
    available_dictionaries = scan_dictionaries()
    # available_to_languages, available_from_languages = list( zip(*available_transl) ) 

    if not isinstance(to_language, str) or not isinstance(from_language, str):
        raise TypeError("to-from languages should be strings")
    if (to_language, from_language) not in available_dictionaries:
        raise ValueError(f"to-from language combination should be any of {available_dictionaries}")
    print("Welcome to Rehearsify, a script for practising foreign language words!\n")

    # read in score df for dictionary of specified languages
    score_df = read_score_df( to_language, from_language )

    # test words from specified dictionary 
    while True:

        correct_answer, question = select_random_weighted_word( score_df )
        user_answer = input( f"{question} = " )

        # if the user types 'q' or 'exit', break loop
        if user_answer.upper() == 'Q' or user_answer.lower() == 'exit': break

        # check answer and update score_df, and if found wrong (Q_answer=False) display correct answer
        Q_answer = check_answer( user_answer, correct_answer )
        if not Q_answer: print( f"\t xxx \t {correct_answer}" )
        score_df = update_score_df( score_df, question, Q_answer )
    
    # once the user has chosen to exit, save the dataframe
    save_score_df( score_df, to_language, from_language ) 

if __name__ == "__main__":
    argc=len(sys.argv) 
    if argc not in [1,3]: raise IndexError( "can only give none or exactly two arguments from command line" )
    else: rehearse( *sys.argv[1:] )