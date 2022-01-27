# constants.py
""" Defines constants for other modules to import. """

COLUMNS = ['question', 'answer', 'wrong_perc', 'wrong', 'total']
COLUMN_DTYPES = ['O','O','float64', 'int64', 'int64'] 

DISPLAY_COLUMNS = ['X/O', 'Question', 'Correct answer', 'User answer', 'Wrong/total']
STATS_COLUMNS = [
        'Total entries (#)',
        'Remaining unseen questions (#)',
        'Remaining unseen questions (%)',
        'Total practised questions (#)',
        'Wrongly answered questions (#)',
        'Wrongly answered questions (%)' ] 