# answer_handling/answer_handling.py

import string
import re
import pandas as pd


def check_answer(user_answer: str, correct_answer: str) -> bool:
    """ check if the answer given by the user is correct """

    # split the correct answer if it consists of multiple allowed options
    user_answer_list = user_answer.split('; ')

    # ignore any text in brackets and punctuation/case in the correct answer
    user_answer_list = user_answer_list + [ re.sub(r'\(.*?\)', '', u_ans) for u_ans \
        in user_answer_list if re.sub(r'\(.*?\)', '', u_ans) not in user_answer_list ] 
    user_answer_list = [ u_ans.translate(str.maketrans('', '', string.punctuation)).lower() for u_ans in user_answer_list ]

    # split the correct answer if it consists of multiple allowed options
    correct_answer_list = correct_answer.split('; ')

    # ignore any text in brackets and punctuation/case in the correct answer 
    correct_answer_list = correct_answer_list + [ re.sub(r'\(.*?\)', '', c_ans) for c_ans \
        in correct_answer_list if re.sub(r'\(.*?\)', '', c_ans) not in correct_answer_list ]
    correct_answer_list = [ c_ans.translate(str.maketrans('', '', string.punctuation)).lower() for c_ans in correct_answer_list ]

    if any( u_ans in correct_answer_list for u_ans in user_answer_list ):
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