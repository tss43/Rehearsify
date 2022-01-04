# data_handling/file_handling.py

import numpy as np
import pandas as pd


COLUMNS = ['question', 'answer', 'wrong_perc', 'wrong', 'total']



def read_dictionary_txtfile(filepath: str) -> pd.DataFrame:
    """ Read in the word list for the specified language combination into a df that is returned. """

    with open(filepath, 'r') as f:
        translation_list = f.read().splitlines()       
    translation_list = [ tuple( transl.split(' = ')[::-1] ) for transl in translation_list if transl.strip() ]
    
    # check that every translation contained exactly one '=', i.e. has both a to and from side
    incomplete_translations = [split_transl for split_transl in translation_list if len(split_transl)!=2 ]
    if incomplete_translations:
        raise ValueError(f"Some translations were incomplete:\n {incomplete_translations}")
    
    zero_dict = dict.fromkeys( COLUMNS[2:], 0 )
    score_df = pd.DataFrame( translation_list, columns=COLUMNS[:2] ).assign(**zero_dict)

    return score_df


def update_with_df(score_df: pd.DataFrame, _temp_df: pd.DataFrame) -> pd.DataFrame:
    """ Update the score df with the words from the dictionary .txt in the given filepath. """

    # keeping only words from df that are in .txt
    mask_intersection = np.all( np.isin( score_df[COLUMNS[:2]].to_numpy(), _temp_df[COLUMNS[:2]].to_numpy() ), axis=1 )
    _intersection_df = score_df[mask_intersection]
    
    # adding words only in .txt to df
    mask_ldiff = np.all( np.isin( _temp_df[COLUMNS[:2]].to_numpy(), score_df[COLUMNS[:2]].to_numpy(), invert=True ), axis=1 )
    _ldiff_df = score_df[mask_ldiff]
    
    _score_df = _intersection_df.append( _ldiff_df )

    ## keeping only words from df that are in .txt
    #_intersection_df = pd.merge(score_df, _temp_df, how='left', on=COLUMNS[:2], indicator='Exist')
    #_intersection_df = score_df.loc[_intersection_df['Exist'] == 'both']

    ## adding words only in .txt to df
    #_rdiff_df = pd.merge(score_df, _temp_df, how='right', on=COLUMNS[:2], indicator='Exist')
    #_rdiff_df = _temp_df.loc[_rdiff_df['Exist'] == 'right_only']
    
    #_score__df = _intersection_df.append( _rdiff_df )

    return _score_df 




def save_as_dictionary_txtfile(filepath: str, score_df: pd.DataFrame):
    """ Save the df as a dictionary txtfile. """

    n_translations = score_df.shape[0]
    question_array = score_df['question'].to_numpy()
    answer_array = score_df['answer'].to_numpy()
    eq_sign_list = [" = "]*n_translations

    with open(filepath, 'a+') as dict_txtfile:     
        dict_txtfile.writelines( [ ''.join(transl) + '\n' for transl in zip(question_array, eq_sign_list, answer_array) ] )


