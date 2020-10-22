#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Class that manages LLDB information
"""

__author__ = 'Enomoto Yoshiki'
__version__ = '1.0.0'
__date__ = '2020/10/12 (Created: 2020/10/12)'

import os
import constants
# pylint: disable=E0401
import lldb  # export PYTHONPATH=`lldb -P`

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
            self._process = None

    def get_stack_memory(self, extent=0x20):
        " Get current stack memory"
        if not self._process:
            return 'None'
        self.update_addresses()
        stack_pointer = self._pointer['sp']
        if self._pointer['sp'] == self._pointer['fp']:
            stack_pointer -= extent
        stack_memory = self._process.ReadMemory(stack_pointer, extent, self._error_ref)
        memory_string = stack_memory.hex()
        output = ''
        for four_byte in range(0, len(memory_string), 8):
            formatted_byte = ''
            for byte in range(four_byte, four_byte + 8, 2):
                formatted_byte = memory_string[byte:byte+2] + formatted_byte
            output += "{}: {}\n".format(hex(stack_pointer+int(four_byte/2)), formatted_byte)

        return output

    def get_variables(self):
        """ Get Valiables """
        self.update_frame()
        output = ''
        for var in self._frame.GetVariables(True, True, True, False):
            output += "{}: {}\n".format(var.GetAddress(), str(var))
        return output
