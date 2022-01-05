# question_posing/question_selecting.py

import pandas as pd

def select_randomly_weighed_question( score_df: pd.DataFrame ) -> pd.Series:
    """ select a randomly selected word from the score df, weighted by percentage wrong if possible """

    # take a random sample out of all rows, weighed by the percentage wrong (clipped to minimally 1%)
    weights = score_df['wrong_perc'].clip(lower=1.0)
    sample = score_df.sample( n=1, weights=weights ).squeeze() 

    return ( sample )

def select_ML_question( score_df: pd.DataFrame ) -> pd.Series:
    """ DESCRIPTION """
    pass
