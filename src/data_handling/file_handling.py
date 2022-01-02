# data_handling/file_handling.py

import pandas as pd

COLUMNS = ['question', 'answer', 'wrong_perc', 'wrong', 'total']



def read_dictionary_txtfile(filepath: str) -> pd.DataFrame:
    """ Read in the word list for the specified language combination into a df that is returned. """

    with open(filepath, 'r') as f:
        word_list = f.read().splitlines()       
    word_list = [ tuple( transl.split(' = ')[::-1] ) for transl in word_list if transl.strip() ]
    
    # check that every translation contained exactly one '=', i.e. has both a to and from side
    if not all( len(split_transl)==2 for split_transl in word_list ):
        raise ValueError("Some translations were incomplete!")
    
    zero_dict = dict.fromkeys( COLUMNS[2:], 0 )
    score_df = pd.DataFrame( word_list, columns=COLUMNS[:2] ).assign(**zero_dict)

    return score_df


def save_as_dictionary_txtfile(filepath: str, score_df: pd.DataFrame):
    """ Save the df as a dictionary txtfile. """

    n_translations = score_df.shape[0]
    question_array = score_df['question'].values
    answer_array = score_df['answer'].values
    eq_sign_list = [" = "]*n_translations

    with open(filepath, 'a+') as f:     
        f.writelines( zip(question_array, eq_sign_list, answer_array) )


