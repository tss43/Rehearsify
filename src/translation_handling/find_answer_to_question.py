# translation_handling/find_answer_to_question.py

import pandas as pd

def find_answer_to_question( score_df: pd.DataFrame, question: str ) -> tuple:
    """ FUNCTION DESCRIPTION """

    answer = ''
    translation = tuple( question, answer )

    return translation