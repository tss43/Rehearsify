 # translation_handling/update_dataframe.py

import pandas as pd

def add_correct_answer(sample: pd.Series, further_correct_answer: str) -> pd.Series:
    """ Add a further correct answer possibility to the translation(s) belonging to the question in the score_df. """

    sample.answer += '; ' + further_correct_answer

    return sample


def update_sample_score( sample: pd.Series, answer_is_correct: bool ) -> pd.Series:
    """ Update the translation sample after a receiving a True/False answer on the question from the user. """
    
    if not answer_is_correct:
        sample.wrong += 1
    sample.total += 1
    sample.wrong_perc = 100 * sample.wrong / sample.total

    return sample


def decrement_sample_wrong_score(sample: pd.Series) -> pd.Series:
    """ Decrement the wrong score of the translation sample. """

    sample.wrong -= 1
    sample.wrong_perc = 100 * sample.wrong / sample.total

    return sample