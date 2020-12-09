#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Memory Stack Infomation Class
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/11/6 (Created: 2020/11/6)'

from utility import format_raw, get_value

class MemoryCell:
    """
    Memory Stack Infomation Class
    """

    def __init__(self):
        super().__init__()
        self._address = ''
        self._scope = ''
        self._name = ''
        self._data = ''
        self._raw = ''
        self._type = ''

    def __str__(self):
        return ('address: {}\n'.format(self._address)
                + 'scope: {}\n'.format(self._scope)
                + 'name: {}\n'.format(self._name)
                + 'data: {}\n'.format(self._data)
                + 'raw: {}\n'.format(self._raw)
                + 'type: {}\n'.format(self._type))

    def get_start_address(self):
        """Get the start address of this instance

        Returns:
            str: Start address
        """
        return self._address

    def get_end_address(self):
        """Get the end address of this instance

        Returns:
            str: End address
        """
        return '0x{:0=16x}'.format(int(self._address, 16) + len(self._raw)//2)

    def as_dict(self):
        """Return instance variables as dict

        Returns:
            dict: Variables as dict
        """
        return dict(
            address = self._address,
            scope = self._scope,
            name = self._name,
            data = self._data,
            raw = self._raw,
            type = self._type)

    def set_variable_info(self, scope, variable, read_memory):
        """Set the result analyzed by the debugger in the instance variable

        Args:
            scope (str): Scope in the script to debug
            variable (SBValue): Variable infomation by LLDB
            read_memory (function): Look into the memory of the current process
        """
        memory_raw = read_memory(int(str(variable.GetLocation()), 16), variable.GetByteSize())
        self._address = str(variable.GetLocation())
        self._scope = scope
        self._name = variable.GetName()
        self._data = get_value(str(variable))
        self._raw = format_raw(memory_raw)
        self._type = variable.GetTypeName()

    def set_padding_info(self, address, raw, name='padding', data='None'):
        """Set a padding for an instance variable

        Args:
            address (str): Memory address
            raw (str): Memory raw data
            name (str): Variable name in the script to debug. Defaults to 'padding'.
            data (str): Data by debugger format. Defaults to 'None'.
        """
        self._address = address
        self._scope = 'None'
        self._name = name
        self._data = data
        self._raw = raw
        self._type = 'None'
