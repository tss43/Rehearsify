# misc/compute_statistics.py

import pandas as pd

def compute_statistics(score_df: pd.DataFrame) -> dict:
    """ Give some statistics of a given score_df. """

    n_translations = score_df.shape[0]
    n_unseen_questions = (score_df['total']==0).sum()
    perc_unseen_questions = 100 * n_unseen_questions / n_translations
    n_practised_questions = score_df['total'].sum()
    n_wrongly_answered_questions = score_df['wrong'].sum()
    perc_wrongly_answered_questions = 100 * n_wrongly_answered_questions / n_practised_questions 

    stats_dict = {
        'Total entries (#)':                n_translations, 
        'Remaining unseen questions (#)':   n_unseen_questions,
        'Remaining unseen questions (%)':   round(perc_unseen_questions, 2),
        'Total practised questions (#)':    n_practised_questions,
        'Wrongly answered questions (#)':   n_wrongly_answered_questions,
        'Wrongly answered questions (%)':   round(perc_wrongly_answered_questions, 2)
    }

    return stats_dict