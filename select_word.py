import math

def select_random_weighted_word( score_df ) -> tuple:
    """ select a randomly selected word from the score df, weighted by the wrong perctange if possible """

    if not score_df['wrong_perc'].apply( math.ceil ).all():
        # if any els of the wrong percentage col are zero, take a random sample 
        sampling = score_df.sample( n=1 ).squeeze()
    else:
        # if all els of the wrong percentage col are nonzero, weigh the random sampling 
        # by (a normalised version of) that percentage
        sampling = score_df.sample( n=1, weights='wrong_perc' ).squeeze()

    return ( sampling[['answer', 'question']] )

def select_ML_word() -> tuple:
    """ FUNCTION DESCRIPTION """
    pass