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
from utility import format_raw, list_to_pattern, symbol_type_to_str

class LLDBObject:
    """
    Class that manages LLDB information
    LLDB structure:
        process > thread > frame > function, variables
    """

    def __init__(self):
        """ Instance initialization method """
        super().__init__()
        # Create a new debugger instance
        self._debugger = lldb.SBDebugger.Create()
        # When we step or continue, don't return from the function until the process
        # stops. We do this by setting the async mode to false.
        self._debugger.SetAsync (False)
        self._target = self._debugger.CreateTarget(constants.EXE)
        self._process = None
        self._thread = None
        self._frame = None
        
    def is_active(self):
        return self._process is not None

    def get_thread(self):
        """ return instance thread """
        return self._thread

    def get_process(self):
        """ return instance process """
        return self._process

    def get_target(self):
        """ return a.out module """
        return self._target

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
        self.update()
        return self

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
    
    def update(self):
        if self._process is None:
            return # Todo: error処理に変更
        self._thread = self._process.GetSelectedThread()
        self._frame = self._thread.GetSelectedFrame()
    
    def debug_process(self, process):
        """ debugger step into """
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
        self.update()

