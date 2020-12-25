#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
memory structure
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/12/9 (Created: 2020/12/9)'

import os
import re
from memory_cell import MemoryCell
import constants
from utility import format_raw, list_to_pattern, symbol_type_to_str, dictionaries_to_list_by_prop


class MemoryStructure:
    """
    memory structure
    """

    def __init__(self, lldb):
        """ Instance initialization method """
        super().__init__()
        # Data and code area are defined as static
        self.lldb = lldb
        self._static = []
        self._stack = []
        self._register = []
        
    def as_dict(self):
        return dict(
            register = self._register,
            static = self._static,
            stack = self._stack
        )

    def update(self):
        self.update_register()
        self.update_static_memory()
        self.update_stack_memory()

    def update_register(self):
        """ get register """
        thread = self.lldb.get_thread()
        a_list = []
        for frame in thread.get_thread_frames():
            values = dict(
                pc = '0x{:0=16x}'.format(frame.GetPC()),
                sp = '0x{:0=16x}'.format(frame.GetSP()),
                fp = '0x{:0=16x}'.format(frame.GetFP())
            )
            a_list.append(values)
        self._register = a_list

    def update_static_memory(self):
        """ get static memory """
        type_to_collect = ['Code', 'Trampoline', 'Data'] # Will be variable later
        a_list = []
        sb_target = self.lldb.get_target()
        # parse a.out module
        for symbol in sb_target.GetModuleAtIndex(0).get_symbols_array():
            symbol_type = symbol_type_to_str(symbol.GetType())
            if symbol_type in type_to_collect:
                start_addr = symbol.GetStartAddress().GetLoadAddress(sb_target)
                end_addr = symbol.GetEndAddress().GetLoadAddress(sb_target)
                extent = end_addr - start_addr
                static = dict(
                    address = '0x' + format(start_addr, '016x'),
                    name = symbol.GetName(),
                    raw = format_raw(self.read_memory()(start_addr, extent)),
                    type = symbol_type
                )
                a_list.append(static)
        sorted_by_address = (lambda stack: sorted(stack, key=lambda x:x['address']))
        self._static = fill_with_unanalyzed(sorted_by_address(a_list))

    def update_stack_memory(self):
        " Get current stack memory"
        a_list = []
        for frame in self.lldb.get_thread().get_thread_frames():
            function_name = frame.GetFunctionName()
            for variable in frame.GetVariables(True, True, False, False):
                memory_cell = MemoryCell()
                memory_cell.set_variable_info(function_name, variable, self.read_memory())
                a_list.append(memory_cell.as_dict())
        sorted_by_address = (lambda stack: sorted(stack, key=lambda x:x['address']))
        self._stack = self._fill_with_padding(sorted_by_address(a_list))

    def _fill_with_padding(self, a_list):
        """ stack infomation fill with padding """
        next_address = ''
        all_stack = []
        for data in a_list:
            current_address = data.get('address')
            if next_address and current_address != next_address:
                padding = MemoryCell()
                return_information = self._search_return_information(current_address, next_address)
                if return_information['value']:
                    padding.set_padding_info(next_address, return_information['raw'], 'Return Address', return_information['value'])
                else:
                    padding.set_padding_info(next_address, return_information['raw'])
                all_stack.append(padding.as_dict())
            all_stack.append(data)
            next_address = '0x{:0=16x}'.format(int(current_address, 16) + len(data.get('raw'))//2)
        return all_stack
    
    def _search_return_information(self, current_address, next_address):
        return_information = { 'value': None, 'raw': '' }
        pc_list = list(map((lambda a: '%x' % int(a, 16)), dictionaries_to_list_by_prop(self._register, 'pc')))
        fp_list = list(map((lambda a: '%x' % int(a, 16)), dictionaries_to_list_by_prop(self._register, 'fp')))
        length = int(current_address, 16) - int(next_address, 16)
        return_information['raw'] = format_raw(self.read_memory()(int(next_address, 16), length))
        a_pc = re.search(list_to_pattern(pc_list), return_information['raw'])
        a_fp = re.search(list_to_pattern(fp_list), return_information['raw'])
        if a_pc and a_fp:
            return_information['value'] = {
                'pc': '0x{:0=16x}'.format(int(a_pc.group(), 16)),
                'fp': '0x{:0=16x}'.format(int(a_fp.group(), 16))
            }
        return return_information

    def read_memory(self):
        """ return rambda read memory """
        return (lambda addr, size: self.lldb.get_process().ReadMemory(addr, size, constants.ERROR).hex())

def fill_with_unanalyzed(a_list):
    """ static infomation fill with Unanalyzed """
    next_address = ''
    all_stack = []
    for a_data in a_list:
        current_address = a_data.get('address')
        if next_address and current_address != next_address:
            padding = MemoryCell()
            padding.set_padding_info(next_address, '', 'Unanalyzed')
            all_stack.append(padding.as_dict())
        all_stack.append(a_data)
        next_address = '0x{:0=16x}'.format(int(current_address, 16) + len(a_data.get('raw'))//2)
    return all_stack
