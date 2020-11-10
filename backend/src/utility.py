#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Memory Infomation Utilities """

def format_raw(raw):
    """
    format memory raw string
    ex)
    c8010000 -> 000001c8
    """
    output = ''
    for byte in range(0, len(raw), 2):
        output = raw[byte:byte+2] + output
    return output

def get_value(a_string):
    """
    get value
    ex)
    (int *) ap = 0x00007ffee4ded554
        -> 0x00007ffee4ded554
    """
    return a_string.split(' = ', 1)[1]