# command_line.py
# provides supporting functionality callable from command line

import sys

from main import rehearse


def script_rehearse():
    """ From the command line, one can call Rehearse with none or two string arguments indicating the to and from languages 
    to rehearse. """
    args = sys.argv[1:] 
    argc=len(args) 
    if argc==1:
        rehearse(*args)
    else:
        raise IndexError("can only give none or exactly two arguments from command line")


def script_remove_duplicates():
    """ DESCRIPTION """
    pass
