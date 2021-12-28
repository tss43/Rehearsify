# main.py
""" to treat directory as executable """

import os
import sys

from src.data_handling.file_handling import scan_available_language_pairs, read_score_df, update_score_df, save_score_df
from src.question_posing.question_selecting import select_randomly_weighed_question
from src.answer_handling.answer_handling import check_answer, update_sample


rehearsify_dir = os.path.dirname(__file__)
dictionary_dir = os.path.join(rehearsify_dir, "support", "Translation dictionaries")
pickle_dir = os.path.join(rehearsify_dir, "support", ".metadata", "Pickled dictionaries")


def rehearse(to_language='Spanish', from_language='English'):
    """ Rehearse words from the dictionary specified by the user.
    INPUTS: 
        to_language: str (default: 'Spanish')
        from_language: str (default: 'English) """
    
    if not isinstance(to_language, str) or not isinstance(from_language, str):
        raise TypeError("to-from languages should be strings")

    # scan for available .txt dictionary files
    available_language_pairs = scan_available_language_pairs(dictionary_dir)

    if (to_language, from_language) not in available_language_pairs:
        raise ValueError(f"to-from language combination should be any of {available_language_pairs}")
    print("Welcome to Rehearsify, a programme for practising foreign language words!\n")

    # read in pre-exiting score_df of specified languages, or create it from .txt dictionary file if not available
    score_df = read_score_df(pickle_dir, to_language, from_language) 
    score_df = update_score_df(dictionary_dir, to_language, from_language, score_df)
    
    # test words from specified dictionary. Exit upon 'q' or 'exit' user input
    user_answer = ''
    while user_answer.lower() != 'q' or user_answer.lower() != 'exit':

        sample = select_randomly_weighed_question( score_df )
        user_answer = input( f"{sample.question} = " )

        # check answer and update score_df, and if found wrong display correct answer
        answer_is_correct = check_answer( user_answer, sample.answer )
        
        sample = update_sample( sample, answer_is_correct )
        
        print( f"\t {'ooo' if answer_is_correct else 'xxx'} \t {sample.question} = {sample.answer} \
            \t\t score={sample.wrong}/{sample.total}\n" )

        # update score_df with new sample statistics
        score_df[ score_df['question']==sample.question ] = sample
    
    # once the user has chosen to exit, save the dataframe
    save_score_df( score_df, to_language, from_language ) 

# to enable executing module as script 
if __name__ == "__main__":
    args=sys.argv[1:]
    argc=len(args) 
    if argc not in [0,2]: 
        raise IndexError("can only give none or exactly two arguments from command line")
    else: 
        rehearse(*args)