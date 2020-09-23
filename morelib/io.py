#!python3
#-*- coding: utf-8 -*-
"""
    MoreLib IO Module

    This module includes features for handling standard and file-related input
    and output.

    Functions:
        lines() -> generator: Yields each line of a file, stripping them and
            ignoring empty lines.

    [FUTURE]
    Functions:
        ask() -> Any: Bulked `input()` for specific-type questions.

    Classes:
        AskHandler: Class for handling specific-type questions.
        MenuHandler: Easy class for handling menues.
        OneLineArgs: Easy class for handling input arguments.


    Created:        23 Sep 2020
    Last modified:  23 Sep 2020
        - Ready for version 0.1.0

"""

#
# Functions
#
def lines (file, splitchar='\n', jump_empties=False):
    """Given a reading-mode file, it yields each line of it, stripped.

    You can provide a different character or substring to split the file using
    the keyword `splitchar`.

    It yields None if a line is empty; although you can make it directly ignore
    them by setting `jump_empties` to True.

    """
    for ln in file.read().split(splitchar):
        ln = ln.strip()
        if not ln and jump_empties:
            continue
        else:
            yield ln or None

