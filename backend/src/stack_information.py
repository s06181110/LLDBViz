#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Memory Stack Infomation Class
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/11/6 (Created: 2020/11/6)'

from pprint import pprint
from utility import format_raw, get_value

class StackInformation:
    """
    Memory Stack Infomation Class
    """

    def __init__(self):
        """ Instance initialization method """
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

    def _set(self, address, scope, name, data, raw, a_type):
        """
        Setting self field variable
        """
        self._address = address
        self._scope = scope
        self._name = name
        self._data = data
        self._raw = raw
        self._type = a_type
    
    
    def get_start_address(self):
        return self._address
    
    def get_end_address(self):
        return '0x{:0=16x}'.format(
            int(self._address, 16) 
            + len(self._raw)//2)
    
    def as_dict(self):
        return dict(
            address = self._address,
            scope = self._scope,
            name = self._name,
            data = self._data,
            raw = self._raw,
            type = self._type)

    def set_variable_info(self, scope, variable, read_memory):
        """
        Parameters
        ----------
        variable: SBValue
            this type is LLDB. the object has variable infomation
        read_memory: lambda (addr, size) -> str
            get memory in binary
        """
        memory_raw = read_memory(int(str(variable.GetLocation()), 16), variable.GetByteSize())
        self._set(
            str(variable.GetLocation()),
            scope,
            variable.GetName(),
            get_value(str(variable)),
            format_raw(memory_raw),
            variable.GetTypeName())

    def set_padding_info(self, address, raw, pc=None, fp=None):
        self._set(address, '', 'padding', 'None', format_raw(raw), 'None')

