# question_posing/question_selecting.py

import math

def select_randomly_weighed_word( score_df ) -> tuple:
    """ select a randomly selected word from the score df, weighted by percentage wrong if possible """

    if not score_df['total'].any():
        # take a uniformly random sample out of all rows that have never been practised
        sampling = score_df[[ score_df['total']==0 ]].sample( n=1 ).squeeze()
    else:
        # take a random sample out of all rows, weighed by the percentage wrong (clipped to minimally 10%)
        weights = score_df['wrong_perc'].clip(lower=0.1)
        sampling = score_df.sample( n=1, weights=weights ).squeeze() 

    return ( sampling[['answer', 'question', 'wrong', 'total']].tolist() )

def select_ML_word() -> tuple:
    """ FUNCTION DESCRIPTION """
    pass