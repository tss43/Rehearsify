# translation_handling/question_selecting.py

import pandas as pd

def select_randomly_weighted_question( score_df: pd.DataFrame, seed=None ) -> pd.Series:
    """ select a randomly selected word from the score df, weighted by percentage wrong if possible """

    # take a random sample out of all rows, weighted by the percentage wrong. Replacing NaNs -> 10% for unpractised translations,
    # and clipping to to minimally 1% to give some non-zero probability to translations previously correctly answered. 
    clipped_weights = score_df['wrong_perc'].fillna( value=10.0, inplace=False ).clip(lower=1.0)
    sample = score_df.sample( n=1, weights=clipped_weights, random_state=seed ).squeeze() 

    return sample 

def select_ML_question( score_df: pd.DataFrame ) -> pd.Series:
    """ DESCRIPTION """
    pass
