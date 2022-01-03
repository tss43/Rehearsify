# translation_handling/find_duplicates.py

import pandas as pd

def find_duplicates(score_df: pd.DataFrame) -> set[str]:
    """ Find duplicate questions within a given score_df. """

    # extract questions 
    question_list = score_df['question'].to_numpy().tolist()
    
    # find list of duplicate questions
    duplicates_set = { unique_question for unique_question in set(question_list) if question_list.count(unique_question)>1 }

    return duplicates_set