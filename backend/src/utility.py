#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Memory Infomation Utilities """

import constants

def format_raw(raw):
    """Format memory raw string

    Args:
        raw (str): raw memory

    Returns:
        str: formatted string
    >>> format_row(c8010000)
    000001c8
    """
    output = ''
    for byte in range(0, len(raw), 2):
        output = raw[byte:byte+2] + output
    return output

def get_value(a_string):
    """Format and get the character string obtained by SBValue.GetValue()

    >>> get_value("(int *) ap = 0x00007ffee4ded554")
    0x00007ffee4ded554
    """
    return a_string.split(' = ', 1)[1]

def list_to_pattern(a_list):
    """Returns a pattern object that connects the list with OR

    Args:
        a_list (list): Word list

    Returns:
        str: Regular expressions
    >>> a_list = ['hoge\n', 'foo']
    >>> print('|'.join(a_list))
    hoge
    |foo
    >>> print(list_to_pattern(a_list))
    'hoge\n|foo'
    """
    return repr('|'.join(a_list))

def symbol_type_to_str(type_num):
    """Parses LLDB symbols and converts them to strings

    Args:
        type_num (int): number of type (LLDB's token)

    Returns:
        str: Symbol name
    """
    return constants.TYPE_SYMBOLS[type_num]
