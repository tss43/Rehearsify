
import string
import re
import pandas as pd


def check_answer(user_answer: str, correct_answer) -> bool:
    """ check if the answer given by the user is correct """

    # ignore punctuaction
    user_answer = user_answer.translate(str.maketrans('', '', string.punctuation))

    # ignore capitalisation and case
    user_answer = user_answer.lower()

    # split the correct answer if it consists of multiple allowed options
    correct_answer_list = correct_answer.split('; ')

    # ignore any text in brackets in the correct answer
    correct_answer_list = correct_answer_list + [ re.sub(r'\(.*?\)', '', c_ans) for c_ans \
        in correct_answer_list if re.sub(r'\(.*?\)', '', c_ans) not in correct_answer_list ]

    if any( u_ans in correct_answer_list for u_ans in list([user_answer]) ):
        return True
    else:
        return False


def update_score_df( score_df, question, Q_check ) -> pd.DataFrame:
    """ update the score dataframe after a receiving a right/wrong answer on the question from the user"""
    
    score_df.loc[ score_df['question']==question, 'total' ] = score_df.loc[ score_df['question']==question, 'total' ]+1
    if not Q_check: # in case the user answer was wrong, also add 1 to the 'wrong' column
        score_df.loc[ score_df['question']==question, 'wrong' ] = score_df.loc[ score_df['question']==question, 'wrong' ]+1
    score_df.loc[ score_df['question']==question, 'wrong_perc' ] = 100*score_df.loc[ score_df['question']==question, 'wrong' ] \
            / score_df.loc[ score_df['question']==question, 'total' ]

    return score_df