# misc/df_sorting.py

import pandas as pd
import re

def sort_df( score_df: pd.DataFrame, omit_str_list: list ) -> pd.DataFrame:
    """ Sort a score dataframe alphabetically, excluding the supplied chars. """   

    omit_strs = '|'.join( omit_str_list )

    score_df = score_df.sort_values(
        by='question', 
        key= lambda question: re.sub(f"\s+({omit_strs})(\s+)", '', question).strip() )

    return score_df