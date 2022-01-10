# translation_handling/answer_handling.py

import string
import re
import unidecode 
import pandas as pd


def check_answer(user_answer: str, correct_answer: str) -> bool:
    """ check if the answer given by the user is correct """

    user_answer_exploded = explode_answer( user_answer )
    correct_answer_exploded = explode_answer( correct_answer )

    # count correct if intersection of exploded user answer set and exploded correct answer set is non-empty
    if user_answer_exploded & correct_answer_exploded:
        return True
    else:
        return False


def update_sample( sample: pd.Series, answer_is_correct: bool ) -> pd.DataFrame:
    """ update the sampling series after a receiving a True/False answer on the question from the user"""
    
    if not answer_is_correct:
        sample.wrong += 1
    sample.total += 1
    sample.wrong_perc = sample.wrong / sample.total * 100

    return sample



### supporting functions ###

def explode_answer( answer: str ) -> set[str]:
    """ Explode the given answer out to a list of possible constituent answers """
    
    # split the correct answer if it consists of multiple allowed options
    answer_explosion = answer.split('; ')
    # also count as an answer ommitting any text in brackets
    answer_explosion = set(answer_explosion) | { re.sub(r'\(.*?\)', '', ans).strip() for ans in answer_explosion }
    
    # ignore special characters/punctuation/case
    answer_explosion = { unidecode.unidecode(ans) for ans in answer_explosion }
    answer_explosion = { ans.translate(str.maketrans('', '', string.punctuation)) for ans in answer_explosion }
    answer_explosion = { ans.lower() for ans in answer_explosion }
    
    return answer_explosion
