# misc/df_sorting.py

import pandas as pd

import unidecode 


def no_sort_df( df: pd.DataFrame ) -> pd.DataFrame:
    """ Do not sort the DataFrame. """
    
    return df


def random_sort_df( df: pd.DataFrame, seed=None ) -> pd.DataFrame:
    """ Randomly rearrange the DataFrame. """
    
    return df.sample(frac=1, random_state=seed)


def sortby_num_df( df: pd.DataFrame, sortby: str ) -> pd.DataFrame:
    """ Sort the DataFrame alphabetically by a numerical col named sortby. Do not reset index. """
    
    return df.sort_values( by=sortby )


def sortby_str_df(df: pd.DataFrame, sortby: str, ignore_str: str='') -> pd.DataFrame:
    """ Sort the DataFrame alphabetically by a string col named sortby, ignoring the supplied characters. Do not reset index. """   

    def reduce_series(ans: pd.Series, ignore_str: str) -> pd.Series:
        """ Reduce a string Series by ignoring the supplied characters and special characters and case. """
        
        ans = ans.str.replace( pat=fr'{ignore_str}', repl='', regex=True )
        ans = ans.apply( unidecode.unidecode )
        ans = ans.str.lower()

        return ans

    df = df.sort_values( by=sortby, key=lambda ans, str=ignore_str: reduce_series(ans=ans, ignore_str=str) )

    return df
