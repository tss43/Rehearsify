 # translation_handling/update_dataframe.py

import pandas as pd

def add_correct_answer(score_df: pd.DataFrame, question: str, further_correct_answer: str) -> pd.DataFrame:
    """ Add a further correct answer possibility to the translation(s) belonging to the question in the score_df. """

    sample_mask = score_df['question']==question 
    score_df.loc[sample_mask, 'answer'] += '; ' + further_correct_answer

    return score_df


def decrement_wrong_score(score_df: pd.DataFrame, question: str) -> pd.DataFrame:
    """ Decrement the wrong score of the translation(s) belonging to the question in the score_df. """

    sample_mask = score_df['question']==question
    score_df.loc[sample_mask, 'wrong'] -= 1
    score_df.loc[sample_mask, 'wrong_perc'] = 100 * score_df.loc[sample_mask, 'wrong'] / score_df.loc[sample_mask, 'total']

    return score_df