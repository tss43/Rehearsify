# translation_handling/find_sample_to_question.py

import pandas as pd

def find_sample_to_question( score_df: pd.DataFrame, question: str ) -> pd.Series:
    """ Find the sample in score df corresponding to the given question """

    answer_sample = score_df[ score_df['question'].str.contains(question) ].sample( n=1 ).squeeze()

    return answer_sample