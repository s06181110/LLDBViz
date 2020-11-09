#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Class that manages LLDB information
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/10/12 (Created: 2020/10/12)'

import os
# pylint: disable=E0401
import lldb  # export PYTHONPATH=`lldb -P`
import constants
from stack_information import StackInformation
from utility import format_raw

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

    def update_addresses(self):
        """ Update some address """
        self.update_frame()
        if self._frame:
            self._pointer = {
                'fp': self._frame.GetFP(),
                'sp': self._frame.GetSP(),
            }

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
        start_addr = pc_addr.GetLoadAddress(self._target) - pc_addr.GetOffset()
        # start_addr2 = func.GetStartAddress().GetLoadAddress(self._target)
        end_addr = func.GetEndAddress().GetLoadAddress(self._target)
        extent = end_addr - start_addr

        return dict(
            address = '0x' + format(start_addr, '016x'),
            name = frame.GetFunctionName(),
            raw = format_raw(self.read_memory()(start_addr, extent))
        )

    def get_stack_memory(self):
        " Get current stack memory"
        from pprint import pprint
        if not self._process:
            return 'None'
        all_stack = []
        for index in range(self._thread.GetNumFrames() - 1): # Exclude before the main method
            frame = self._thread.GetFrameAtIndex(index)
            function = self.get_function(frame)
            print('PC: {}, FP: {}, SP: {}'.format(hex(frame.GetPC()), hex(frame.GetFP()), hex(frame.GetSP())))
            for variable in frame.GetVariables(True, True, True, False):
                stack_info = StackInformation()
                stack_info.set_variable_info(function.get('name'), variable, self.read_memory())
                all_stack.append(stack_info.as_dict())
        all_stack = self._fill_with_padding(all_stack)

    def _fill_with_padding(self, stack):
        sorted_stack = sorted(stack, key=lambda x:x['address'])
        next_address = ''
        all_stack = []
        for stack in sorted_stack:
            current_address = stack.get('address')
            if next_address and current_address != next_address:
                length = int(current_address, 16) - int(next_address, 16)
                raw = self.read_memory()(int(next_address, 16), length)
                padding = StackInformation()
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
