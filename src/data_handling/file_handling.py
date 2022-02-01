# data_handling/file_handling.py


import numpy as np
import pandas as pd

from src.misc.find_duplicates import find_duplicates

from src.constants import COLUMNS, COLUMN_DTYPES


def read_dictionary_txtfile(filepath: str) -> pd.DataFrame:
    """ Read in the word list for the specified language combination into a df that is returned, ignoring blank lines. """

    with open(filepath, 'r') as f:
        translation_list = f.read().splitlines()       
    translation_list = [ tuple( transl.split(' = ')[::-1] ) for transl in translation_list if len( transl.strip() ) > 0 ]
    
    # check that every translation contained exactly one '=', i.e. has both a to and from side
    incomplete_translations = [split_transl for split_transl in translation_list if len(split_transl)!=2 ]
    if incomplete_translations:
        raise ValueError(f"Some translations were incomplete:\n {incomplete_translations}")

    zero_dict = {COLUMNS[2]: np.NaN, COLUMNS[3]: 0, COLUMNS[4]: 0}
    score_df = pd.DataFrame( translation_list, columns=COLUMNS[:2] ).assign(**zero_dict)

    return score_df


def update_with_df(score_df: pd.DataFrame, _temp_df: pd.DataFrame) -> pd.DataFrame:
    """ Update the score df with the words from temp df. """

    # keeping only words from score_df that are in _temp_df
    mask_intersection = np.all( np.isin( score_df[COLUMNS[:2]].to_numpy(), _temp_df[COLUMNS[:2]].to_numpy() ), axis=1 )
    _intersection_df = score_df[mask_intersection]
    
    # adding words only in ._temp_df to score_df
    mask_ldiff = np.all( np.isin( _temp_df[COLUMNS[:2]].to_numpy(), score_df[COLUMNS[:2]].to_numpy(), invert=True ), axis=1 )
    _ldiff_df = _temp_df[mask_ldiff]
    
    _score_df = _intersection_df.append( _ldiff_df )

    return _score_df 


def save_as_dictionary_txtfile(filepath: str, score_df: pd.DataFrame):
    """ Save the df as a dictionary txtfile. """

    n_translations = score_df.shape[0]
    question_array = score_df['question'].to_numpy()
    answer_array = score_df['answer'].to_numpy()
    eq_sign_list = [" = "]*n_translations

    with open(filepath, 'w+') as dict_txtfile:     
        dict_txtfile.writelines( [ ''.join(transl) + '\n' for transl in zip(answer_array, eq_sign_list, question_array) ] )


def validate_translation_dictionary(score_df: pd.DataFrame):
    """Validate a score_df on opening."""

    # check if required columns are present
    if not all( [col in COLUMNS for col in score_df.columns]  ):
        raise  KeyError(f"Attempted to open a corrupted DataFrame: should contain columns {COLUMNS}.")


    # check column types
    if any( score_df.dtypes != COLUMN_DTYPES ):
        raise TypeError("DataFrame has inappropriate column types.")

    # check if df contains empty question and answer columns
    mask_empty_question_answer = (score_df['question']=='') | (score_df['answer']=='')
    if any( mask_empty_question_answer ):
        raise ValueError(f"DataFrame contains empty rows:\n {score_df[mask_empty_question_answer]}.")

    mask_invalid_score = (score_df['wrong'] < 0) | (score_df['total'] < 0)
    mask_invalid_perc_score = (score_df['wrong_perc'] < 0) | (score_df['wrong_perc'] > 100)
    if any( mask_invalid_score ) | any( mask_invalid_perc_score ):
        raise ValueError(f"DataFrame contains corrupted rows:\n {score_df[mask_invalid_score | mask_invalid_perc_score]}.")

    # check if df contains duplicate questions
    duplicates_set = find_duplicates(score_df)
    if duplicates_set:
        raise ValueError(f"Duplicate question entries are:\n {duplicates_set}.")


def validate_ignore_str(ignore_str: str):
    """Validate an ignore_str string given by the user for proper regex purposes."""

    if '\\' in ignore_str:
        raise ValueError("Ignore string cannot contain '\\'.")
