import os
import pandas as pd

# define word files directory
rehearsify_dir = os.path.dirname(__file__)
pickle_dir = os.path.join(rehearsify_dir, "Translation dictionaries", ".metadata", "Pickled dictionary dfs")

def scan_dictionaries() -> list:
    """ returns a list of language combination tuples """

    transl_list = []
    for dictionary in os.listdir(os.path.join(rehearsify_dir,"Translation dictionaries")):
        if dictionary.endswith("_dictionary.txt"):
            transl_list.append( tuple(dictionary.split('_')[0:2]) )

    return transl_list


def read_words(lang1: str, lang2: str) -> list:
    """ read in the word list for the specified language combination, returning a list of translation tuples """

    words_txtfile = "_".join( [lang1, lang2, "dictionary.txt"] )
    if words_txtfile in os.listdir( os.path.join(rehearsify_dir, "Translation dictionaries") ):
        with open (os.path.join(rehearsify_dir, "Translation dictionaries", words_txtfile), 'r') as f:    
            word_list = f.read().splitlines()       
    
        word_list = [ transl.split(' = ')[::-1] for transl in word_list if transl.strip() ]

        # check that every translation contained exactly one '=', i.e. has both a to and from side
        if not all( len(split_transl)==2 for split_transl in word_list ):
            raise ValueError("Some translations were incomplete!")

    else: 
        raise OSError("file for specified dictionary not found")

    return word_list

def read_score_df( to_language: str, from_language: str) -> pd.DataFrame:
    """ read in (or create) the score dataframe """
    pickle_file = "_".join([to_language, from_language, "words.pkl"])
    if pickle_file in os.listdir( pickle_dir ):
        pickle_path = os.path.join( pickle_dir, pickle_file )
        score_df = pd.read_pickle( pickle_path ) 
    else:
        score_df = pd.DataFrame( columns=['question', 'answer', 'wrong_perc', 'wrong', 'total'] )
        
    # build up word df of questions and answers from word list
    word_list = read_words( to_language, from_language )
    word_df = pd.DataFrame( word_list, columns=['question', 'answer'] )

    # left join word df and score df to complete the preserved cols of the former with 
    # the extraneous cols of the latter (where row appears, if not fill with 0)
    score_df = word_df.merge( score_df, how='left' ).fillna( value=0 ) 

    return score_df


def save_score_df( score_df, to_language, from_language ):
    """ save the score dataframe to pickle """
    pickle_file = "_".join([to_language, from_language, "words.pkl"])
    pickle_path = os.path.join( pickle_dir, pickle_file )
    score_df.to_pickle(pickle_path)
