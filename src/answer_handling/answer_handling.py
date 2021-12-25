# answer_handling/answer_handling.py

import string
import re
import pandas as pd


def check_answer(user_answer: str, correct_answer: str) -> bool:
    """ check if the answer given by the user is correct """

    user_answer_exploded = explode_answer( user_answer )
    correct_answer_exploded = explode_answer( correct_answer )
        
    if any( u_ans in correct_answer_exploded for u_ans in user_answer_exploded ):
        return True
    else:
        return False


def update_sample( sample: pd.Series, answer_is_correct: bool ) -> pd.DataFrame:
    """ update the sampling series after a receiving a True/False answer on the question from the user"""
    
    if not answer_is_correct:
        sample.wrong += 1
    sample.total += 1
    sample.wrong_perc = sample.wrong / sample.total

    return sample



### supportive functions

def explode_answer( answer: str ) -> list:
    """ Explode the given answer out to a list of possible constituent answers """
    
    # split the correct answer if it consists of multiple allowed options
    answer_explosion = answer.split('; ')
    # also count as an answer ommitting any text in brackets and ignore punctuation/case in the user answer
    answer_explosion = answer_explosion + [ re.sub(r'\(.*?\)', '', ans) for ans \
        in answer_explosion if re.sub(r'\(.*?\)', '', ans) not in answer_explosion ] 
    answer_explosion = [ ans.translate(str.maketrans('', '', string.punctuation)) for ans in answer_explosion ]
    answer_explosion = [ ans.lower() for ans in answer_explosion ]
    
    return answer_explosion
