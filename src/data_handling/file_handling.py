import os
import pandas as pd

# define word files directory

def scan_available_language_pairs(dictionary_dir: str) -> list:
    """ Return a list of available language combination tuples """

    transl_list = []
    for language_dictionary in os.listdir( dictionary_dir ):
        if language_dictionary.endswith("_dictionary.txt"):
            transl_list.append( tuple(language_dictionary.split('_')[0:2]) )

    return transl_list


def read_score_df(pickle_dir: str, to_language: str, from_language: str) -> pd.DataFrame | None:
    """ Read in and return the score dataframe, or none if not available """
    
    pickle_file = "_".join( [to_language, from_language, "dictionary.pkl"] )
    
    if pickle_file in os.listdir( pickle_dir ):
        pickle_path = os.path.join( pickle_dir, pickle_file )
        score_df = pd.read_pickle( pickle_path ) 
        return score_df
    else:
        return None
    

def create_score_df(dictionary_dir: str, to_language: str, from_language: str) -> pd.DataFrame:
    """ Create and return a score dataframe from the indicated .txt dictionary file """
      
    # build up word df of questions and answers from word list
    word_list = read_dictionary_txtfile(dictionary_dir, to_language, from_language )
    score_df = pd.DataFrame( word_list, columns=['question', 'answer'] )

    zero_dict = dict.fromkeys( keys=['correct_perc', 'correct', 'total'], value=0 )
    score_df.assign(**zero_dict)

    return score_df
    


def save_score_df(score_df: pd.DataFrame, to_language: str, from_language: str, pickle_dir: str):
    """ save the score dataframe to pickle """
    
    pickle_file = "_".join([to_language, from_language, "dictionary.pkl"])
    pickle_path = os.path.join( pickle_dir, pickle_file )
    score_df.to_pickle(pickle_path)


def read_dictionary_txtfile(dictionary_dir: str, lang1: str, lang2: str) -> list:
    """ read in the word list for the specified language combination, returning a list of translation tuples """

    dictionary_txtfile = "_".join( [lang1, lang2, "dictionary.txt"] )
    if dictionary_txtfile in os.listdir( dictionary_dir ):
        with open (os.path.join(dictionary_dir, dictionary_txtfile), 'r') as f:    
            word_list = f.read().splitlines()       
    
        word_list = [ transl.split(' = ')[::-1] for transl in word_list if transl.strip() ]

        # check that every translation contained exactly one '=', i.e. has both a to and from side
        if not all( len(split_transl)==2 for split_transl in word_list ):
            raise ValueError("Some translations were incomplete!")

    else: 
        raise OSError("file for specified dictionary not found")

    return word_list

