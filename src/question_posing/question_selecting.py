# question_posing/question_selecting.py

import pandas as pd

def select_randomly_weighed_question( score_df ) -> pd.Series:
    """ select a randomly selected word from the score df, weighted by percentage wrong if possible """

    if not score_df['total'].any():
        # take a uniformly random sample out of all rows that have never been practised
        sample = score_df[ score_df['total']==0 ].sample( n=1 ).squeeze()
    else:
        # take a random sample out of all rows, weighed by the percentage wrong (clipped to minimally 10%)
        weights = score_df['wrong_perc'].clip(lower=10.0)
        sample = score_df.sample( n=1, weights=weights ).squeeze() 

    return ( sample )

def select_ML_word() -> pd.Series:
    """ FUNCTION DESCRIPTION """
    pass