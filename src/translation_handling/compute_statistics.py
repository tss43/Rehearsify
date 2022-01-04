# translation_handling/compute_statistics.py

import pandas as pd

def compute_statitics(score_df: pd.DataFrame) -> dict:
    """ Give some statistics of a given score_df. """

    n_translations = score_df.shape[0]
    n_practised_questions = score_df['total'].sum()
    n_wrongly_answered_questions = score_df['wrong'].sum()
    perc_wrongly_answered_questions = n_wrongly_answered_questions / n_practised_questions

    stats_dict = {
        'Total number of translations':             n_translations, 
        'Number of practised questions':            n_practised_questions,
        'Number of wrongly answered questions':     n_wrongly_answered_questions,
        'Percentage of wrongly answered questions': perc_wrongly_answered_questions
    }

    return stats_dict