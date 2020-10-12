#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Class that manages LLDB information
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/10/12 (Created: 2020/10/12)'

# pylint: disable=E0401
import lldb  # export PYTHONPATH=`lldb -P`
import os

class LLDBObject:
    """
    Class that manages LLDB information
    LLDB structure:
        process > thread > frame > function, variables
    """

    EXE = os.path.join(os.getcwd(), 'target', 'a.out')

    @staticmethod
    def __new__(cls):
        """ Instance generation method """
        self = super().__new__(cls)
        return self

    def __init__(self):
        """ Instance initialization method """
        super().__init__()
        # Create a new debugger instance
        self._debugger = lldb.SBDebugger.Create()
        # When we step or continue, don't return from the function until the process
        # stops. We do this by setting the async mode to false.
        self._debugger.SetAsync (False)
        self._target = self._debugger.CreateTarget(self.EXE)
        self._error_ref = lldb.SBError()
        self._process = None
        self._thread = None
        self._frame = None
        self._function = None
        self._pointer = { 'fp': None, 'sp': None}

    def set_breakpoint(self, line):
        """ Set a breakpoint """
        self._target.BreakpointCreateByLocation("main.c", line)

    def show_breakpoints(self):
        """ print some breakpoints """
        for breakpoint in self._target.breakpoint_iter():
                print(breakpoint)

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

    def get_stack_memory(self, extent=0x20):
        " Get current stack memory"
        self.update_addresses()
        stack_pointer = self._pointer['sp']
        stack_memory = self._process.ReadMemory(stack_pointer, extent, self._error_ref)
        memory_string = stack_memory.hex()
        output = ''
        for four_byte in range(0, len(memory_string), 8):
            formatted_byte = ''
            for byte in range(four_byte, four_byte + 8, 2):
                formatted_byte = memory_string[byte:byte+2] + formatted_byte
            output += "{}: {}\n".format(hex(stack_pointer+int(four_byte/2)), formatted_byte)

        return output