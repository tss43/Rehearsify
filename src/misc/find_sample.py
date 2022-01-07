# misc/find_sample.py

import pandas as pd

def find_sample_from_question( score_df: pd.DataFrame, question: str ) -> pd.Series:
    """ Find the sample in score df corresponding to the given question """

    answer_sample = score_df[ score_df['question'].str.contains(question) ].sample( n=1 ).squeeze()
    return answer_sample

def find_sample_from_answer( score_df: pd.DataFrame, answer: str ) -> pd.Series:
    """ Find the sample in score df corresponding to the given answer """
    
    question_sample = score_df[ score_df['answer'].str.contains(answer) ] .sample( n=1 ).squeeze()
    return question_sample    