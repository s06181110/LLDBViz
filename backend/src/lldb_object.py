#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Class that manages LLDB information
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/10/12 (Created: 2020/10/12)'

import os
import re
# pylint: disable=E0401
import lldb  # export PYTHONPATH=`lldb -P`
import constants
from stack_information import StackInformation
from utility import format_raw, list_to_pattern, symbol_type_to_str

class LLDBObject:
    """
    Class that manages LLDB information
    LLDB structure:
        process > thread > frame > function, variables
    """

    EXE = os.path.join(os.getcwd(), 'target', 'a.out')
    ERROR = lldb.SBError()

    def __init__(self):
        """ Instance initialization method """
        super().__init__()
        # Create a new debugger instance
        self._debugger = lldb.SBDebugger.Create()
        # When we step or continue, don't return from the function until the process
        # stops. We do this by setting the async mode to false.
        self._debugger.SetAsync (False)
        self._target = self._debugger.CreateTarget(self.EXE)
        self._process = None
        self._thread = None
        self._frame = None

    def set_breakpoint(self, lines):
        """ Set a breakpoint """
        for line in lines:
            self._target.BreakpointCreateByLocation("main.c", line)
        output = ''
        for a_breakpoint in self._target.breakpoint_iter():
            output += str(a_breakpoint) + '\n'
        return output if output else 'None'

    def launch(self, argv=None, envp=None):
        """ Launch LLDB """
        self._process = self._target.LaunchSimple(argv, envp, os.getcwd())

    def update_thread(self, index=0):
        """ Update a Thread """
        if self._process:
            state = self._process.GetState()
            if state == lldb.eStateStopped:
                self._thread = self._process.GetThreadAtIndex(index)

    def update_frame(self, index=0):
        """ Update a Frame """
        self.update_thread()
        if self._thread:
            self._frame = self._thread.GetFrameAtIndex(index)

    def debug_process(self, process):
        """ debugger step into """
        self.update_thread()
        if not self._thread:
            return
        if process == constants.STEP_INTO:
            self._thread.StepInto()
        elif process == constants.STEP_OVER:
            self._thread.StepOver()
        elif process == constants.STEP_OUT:
            self._thread.StepOut()
        elif process == constants.CONTINUE:
            self._process.Continue()
        elif process == constants.STOP:
            self._process.Destroy()
            self.__init__()

    def get_function(self, frame=None):
        if frame is None:
            self.update_frame()
            frame = self._frame
        func = frame.GetFunction()
        pc_addr = frame.GetPCAddress()
        # start_addr = pc_addr.GetLoadAddress(self._target) - pc_addr.GetOffset()
        start_addr = func.GetStartAddress().GetLoadAddress(self._target)
        end_addr = func.GetEndAddress().GetLoadAddress(self._target)
        extent = end_addr - start_addr
        
        return dict(
            address = '0x' + format(start_addr, '016x'),
            name = frame.GetFunctionName(),
            raw = format_raw(self.read_memory()(start_addr, extent)),
            type = str(func.GetType())
        )

    def get_register(self, frame=None):
        if frame is None:
            self.update_frame()
            frame = self._frame
        return dict(
            pc = hex(frame.GetPC()),
            sp = hex(frame.GetSP()),
            fp = hex(frame.GetFP())
        )
        
    def get_static_memory(self):
        if self._process is None:
            return 'None'
        type_to_collect = ['Code', 'Trampoline', 'Data']
        all_stack = []
        # parse a.out module
        for symbol in self._target.GetModuleAtIndex(0).get_symbols_array():
            symbol_type = symbol_type_to_str(symbol.GetType())
            if symbol_type in type_to_collect:
                start_addr = symbol.GetStartAddress().GetLoadAddress(self._target)
                end_addr = symbol.GetEndAddress().GetLoadAddress(self._target)
                extent = end_addr - start_addr
                static = dict(
                    address = '0x' + format(start_addr, '016x'),
                    name = symbol.GetName(),
                    raw = format_raw(self.read_memory()(start_addr, extent)),
                    type = symbol_type
                )
                all_stack.append(static)
        all_stack = self._fill_with_Unanalyzed(all_stack)
        return all_stack

    def _fill_with_Unanalyzed(self, stack):
        sorted_stack = sorted(stack, key=lambda x:x['address'])
        next_address = ''
        all_stack = []
        for a_data in sorted_stack:
            current_address = a_data.get('address')
            if next_address and current_address != next_address:
                padding = StackInformation()
                padding.set_padding_info(next_address, '', 'Unanalyzed')
                all_stack.append(padding.as_dict())
            all_stack.append(a_data)
            next_address = '0x{:0=16x}'.format(int(current_address, 16) + len(a_data.get('raw'))//2)
        return all_stack

    def get_stack_memory(self):
        " Get current stack memory"
        if self._process is None:
            return 'None'
        self.update_thread()
        all_stack = []
        pointers = []
        for index in range(self._thread.GetNumFrames() - 1): # Exclude before the main method
            frame = self._thread.GetFrameAtIndex(index)
            function_name = frame.GetFunctionName()
            pointers.append(self.get_register(frame))
            for variable in frame.GetVariables(True, True, False, False):
                stack_info = StackInformation()
                stack_info.set_variable_info(function_name, variable, self.read_memory())
                all_stack.append(stack_info.as_dict())
        all_stack = self._fill_with_padding(all_stack, pointers)
        return all_stack

    def _fill_with_padding(self, stack, pointers):
        sorted_stack = sorted(stack, key=lambda x:x['address'])
        pc_list = list_to_pattern([pointer.get('pc')[2:] for pointer in pointers])
        fp_list = list_to_pattern([pointer.get('fp')[2:] for pointer in pointers])
        next_address = ''
        all_stack = []
        for stack in sorted_stack:
            current_address = stack.get('address')
            if next_address and current_address != next_address:
                length = int(current_address, 16) - int(next_address, 16)
                raw = format_raw(self.read_memory()(int(next_address, 16), length))
                pc = re.search(pc_list, raw)
                fp = re.search(fp_list, raw)
                padding = StackInformation()
                if pc and fp:
                    pc_str = '0x{:0=16x}'.format(int(pc.group(), 16))
                    fp_str = '0x{:0=16x}'.format(int(fp.group(), 16))
                    padding.set_padding_info(next_address, raw, 'return infomation', dict(pc=pc_str, fp=fp_str))
                else:
                    padding.set_padding_info(next_address, raw)
                all_stack.append(padding.as_dict())
            all_stack.append(stack)
            next_address = '0x{:0=16x}'.format(int(current_address, 16) + len(stack.get('raw'))//2)
        return all_stack

    def read_memory(self):
        return (lambda addr, size: self._process.ReadMemory(addr, size, self.ERROR).hex())

    def get_variables(self):
        """ Get Valiables """
        self.update_frame()
        output = ''
        for var in self._frame.GetVariables(True, True, True, False):
            output += "{}: {}\n".format(var.GetAddress(), str(var))
        return output
