# misc/df_sorting.py

import pandas as pd

import unidecode 

def sort_df(score_df: pd.DataFrame, ignore_str: str) -> pd.DataFrame:
    """ Sort the score df alphabetically by answer, ignoring the supplied characters. Do not reset index. """   

    def reduce_series(ans: pd.Series) -> pd.Series:
        """ Reduce a Series by ignoring the supplied characters and special characters and case. """
        
        ans = ans.str.replace( pat=fr'{ignore_str}', repl='', regex=True )
        ans = ans.apply( unidecode.unidecode )
        ans = ans.str.lower()

        return ans

    score_df = score_df.sort_values( by='answer', key=reduce_series )

    return score_df
