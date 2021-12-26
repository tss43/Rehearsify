# command_line.py
""" provides supporting functionality callable from command line """

import sys

from translation_handling import find_answer_to_question

def script_translate():
    """ Find the translation for a question in a given from langauge to language dictionary """
    if __name__ == "__main__":
        args=sys.argv[1:]
        argc=len(args) 
        if argc not in [0,3]: 
            raise IndexError("can only give one or exactly three arguments from command line")
        else: 
            pass    # implement functionality here find_answer_to_question

    


