#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Memory Table Class
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/10/23 (Created: 2020/10/23)'

import re

class MemoryTable:
    """
    Memory TableClass
    """

    def __init__(self):
        self._table = []

    def get_table(self):
        """ get a table """
        return self._table

    def set_variables(self, variables, read_memory):
        """
        Parameters
        ----------
        vars: SBValueList
            this type is LLDB. the object has variables infomation
        read_memory: lambda (addr, size) -> str
            get memory in binary
        """
        for a_variable in variables:
            a_list = str(a_variable).split(')')[1].split()
            table = dict(
                address = str(a_variable.GetAddress()),
                name = a_list[0],
                data = a_list[2],
                raw = format_raw(read_memory(int(str(a_variable.GetAddress()), 16), a_variable.GetByteSize()).hex()),
                type = get_type(str(a_variable)),
            )
            table_index = self.index_of_table_by_address(table.get('address'))
            if table_index is None:
                self._table.append(table)
            else:
                self._table[table_index] = table

    def index_of_table_by_address(self, addr):
        """
        get index of table by address
        """
        index = 0
        for var in self._table:
            if var.get('address') == addr:
                return index
            index = index + 1
        return None

""" Table Utilities """

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

def get_type(a_string):
    """
    get type by data string
    ex)
    (const char **) argv = 0x00007ffee6bb7510
        -> const char **
    """
    result = re.match(r'\((.+)\)', a_string)
    return result.group(1)

