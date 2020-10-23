#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Memory Table Class
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/10/23 (Created: 2020/10/23)'

from pprint import pprint
import re

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
        super().__new__(self)
        self._table = []

    def get_table(self):
        return self._table

    def set_variables(self, vars, read_memory):
        """
        Parameters
        ----------
        vars: SBValueList
            this type is LLDB. the object has variables infomation
        read_memory: lambda (addr, size) -> str
            get memory in binary
        """
        for var in vars:
            table = dict(
                address = str(var.GetAddress()),
                data = str(var),
                raw = self.format_raw(read_memory(int(str(var.GetAddress()), 16), var.GetByteSize()).hex()),
            )
            table_index = self.index_of_table_by_address(table['address'])
            if table_index:
                self._table[table_index] = table
            else:
                self._table.append(table)

    def index_of_table_by_address(self, addr):
        index = 0
        for var in self._table:
            if var['address'] == addr:
                return index
            index = index + 1
        return None


    def format_raw(self, raw):
        """
        format memory raw string
        ex)
        c8010000 -> 000001c8
        """
        output = ''
        for byte in range(0, len(raw), 2):
            output = raw[byte:byte+2] + output
        return output
