# misc/df_sorting.py

import pandas as pd

def sort_df( score_df: pd.DataFrame, ignore_str: str ) -> pd.DataFrame:
    """ Sort the score df alphabetically by answer, ignoring the supplied chars. """   

    score_df = score_df.sort_values( by='answer', key=lambda ans: ans.str.replace(f'{ignore_str}', '') )

    return score_df