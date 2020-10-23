#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Memory Table Class
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/10/23 (Created: 2020/10/23)'

class MemoryTable:
    """
    Memory TableClass
    """
    @staticmethod
    def __new__(cls):
        """ Instance generation method """
        self = super().__new__(cls)
        return self

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
            table = dict(
                address = str(a_variable.GetAddress()),
                data = str(a_variable),
                raw = format_raw(read_memory(int(str(a_variable.GetAddress()), 16), a_variable.GetByteSize()).hex()),
            )
            table_index = self.index_of_table_by_address(table['address'])
            if table_index:
                self._table[table_index] = table
            else:
                self._table.append(table)

    def index_of_table_by_address(self, addr):
        """
        get index of table by address
        """
        index = 0
        for var in self._table:
            if var['address'] == addr:
                return index
            index = index + 1
        return None


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
